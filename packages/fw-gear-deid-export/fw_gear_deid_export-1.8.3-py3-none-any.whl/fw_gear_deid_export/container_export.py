#!/usr/bin/env python3
import argparse
import logging
import os
import random
import tempfile
import typing as t

import flywheel
import pandas as pd
from flywheel.rest import ApiException
from flywheel_gear_toolkit.utils import sdk_post_retry_handler
from flywheel_migration import deidentify
from ruamel.yaml import YAML

from fw_gear_deid_export import deid_template
from fw_gear_deid_export.file_exporter import FileExporter
from fw_gear_deid_export.metadata_export import get_deid_fw_container_metadata
from fw_gear_deid_export.retry_utils import (
    create_container_with_retry,
    sanitize_label,
)

log = logging.getLogger(__name__)


def matches_file(
    deid_profile: deidentify.DeIdProfile,
    file_obj: flywheel.FileEntry | dict,
) -> bool:
    """

    Args:
        deid_profile(flywheel_migration.deidentify.DeIdProfile): the de-identification profile
        file_obj(flywheel.FileEntry or dict): the flywheel file object

    Returns:
        bool: whether the profile supports the file

    """
    return_bool = False
    file_type = file_obj.get("type")
    file_name = file_obj.get("name")
    if file_type == "dicom" and deid_profile.get_file_profile("dicom"):
        return_bool = True
    else:
        for profile in deid_profile.file_profiles:
            if profile.name != "dicom" and profile.matches_file(file_name):
                return_bool = True
                break

    return return_bool


def load_template_dict(template_file_path: str) -> dict:
    """
    Determines whether the file is YAML and returns the Python dictionary representation
    Args:
        template_file_path (str): path to the YAML file
    Raises:
        ValueError: when fails to load the template
    Returns:
        (dict): dictionary representation of the the template file

    """
    _, ext = os.path.splitext(template_file_path.lower())

    template = None
    try:
        if ext in [".yml", ".yaml"]:
            deid_template.update_deid_profile(
                template_file_path, updates=dict(), dest_path=template_file_path
            )
            with open(template_file_path, "r") as f:
                yaml = YAML(typ="safe", pure=True)
                template = yaml.load(f)
        return template
    except ValueError:
        log.exception(f"Unable to load template at: {template_file_path}")

    if not template:
        raise ValueError(f"Could not load template at: {template_file_path}")


def _update_fw_metadata_profile(cont_profile: dict) -> dict:
    """Add default datetime format to Flywheel container metadata if not specified."""

    # Check if "fields" key is present in the profile
    if "fields" not in cont_profile and cont_profile.get("all"):
        # If all is specified, we want to keep timestamp _and_ specify date-time format
        cont_profile["fields"] = [
            {
                "datetime-format": "%Y-%m-%d %H:%M:%S.%f",
                "name": "timestamp",
                "keep": True,
            }
        ]
        log.debug(
            f"Updated fw metadata profile {cont_profile} to specify timestamp datetime-format."
        )
    else:
        fields = cont_profile.get("fields", [])

        # Check if "fields" is a list of dictionaries
        if not isinstance(fields, list) or not all(
            isinstance(item, dict) for item in fields
        ):
            raise ValueError("'fields' should be a list of dictionaries")
        # If user has specified timestamp, keep user specified config, but also override timestamp
        # to be correct
        for field in fields:
            if "name" in field and field["name"] == "timestamp":
                if "datetime-format" not in field:
                    field["datetime-format"] = "%Y-%m-%d %H:%M:%S.%f"
                    log.debug(
                        f"Updated fw metadata profile {cont_profile} to specify timestamp datetime-format."
                    )
                break

    return cont_profile


def get_api_key_from_client(fw_client: flywheel.Client) -> str:
    """
    Parses the api key from an instance of the flywheel client
    Args:
        fw_client (flywheel.Client): an instance of the flywheel client

    Returns:
        (str): the api key
    """
    site_url = fw_client.get_config().site.get("api_url").rsplit(":", maxsplit=1)[0]
    site_url = site_url.rsplit("/", maxsplit=1)[1]
    key_string = fw_client.get_current_user().api_key.key
    api_key = ":".join([site_url, key_string])
    return api_key


def find_or_create_container(
    client: flywheel.Client,
    origin: flywheel.Subject | flywheel.Session | flywheel.Acquisition,
    dest_parent: flywheel.Project | flywheel.Subject | flywheel.Session,
    fw_metadata_profile: dict = None,
) -> flywheel.Subject | flywheel.Session | flywheel.Acquisition:
    """Find or create a destination container based on source container and parent destination.

        Searches is based on matching info.export.origin_id (or label for subject).
        Container metadata get de-id and populated accordingly to fw_metadata_profile and
        the metadata in the origin container.
    Args:
        client (flywheel.Client): the flywheel client.
        origin (flywheel.<Container>): the source container.
        dest_parent (flywheel.<Container>): the parent of the destination container to be created.
        fw_metadata_profile (dict): an optional dictionary matching a JSONFileProfile.

    Returns:
        (object): the found or created container in dest_parent
    """
    origin_type = origin.container_type
    if not fw_metadata_profile:
        fw_metadata_profile = {origin_type: {}}
    config = fw_metadata_profile.get(origin_type, {})
    if fw_metadata_profile.get("date-increment"):
        config.update({"date-increment": fw_metadata_profile["date-increment"]})
    if origin_type != "subject":
        _update_fw_metadata_profile(config)
    meta_dict = get_deid_fw_container_metadata(client, config, origin)
    new_label = meta_dict.pop("label", origin.label)
    if len(new_label) > 64:
        # Container label max length
        new_label = new_label[:64]
    query = f"label={sanitize_label(new_label)}"

    # Getting the find_first method for the children of dest_parent
    finder_first = getattr(getattr(dest_parent, f"{origin_type}s"), "find_first")
    dest_container = finder_first(query)
    if not dest_container:
        log.debug(f"Creating destination {origin_type} for ({origin.id})")

        # Add the container to the destination project
        # Tags cannot be added upon container creation
        tags = meta_dict.pop("tags", None)
        dest_container = create_container_with_retry(
            dest_parent=dest_parent,
            origin_type=origin_type,
            label=new_label,
            meta_dict=meta_dict,
            max_retry=3,
        )
        if tags:
            for t in tags:
                with sdk_post_retry_handler(client):
                    try:
                        # POST /container/cid/tags
                        dest_container.add_tag(t)
                    except ApiException as e:
                        if e.status == 409:
                            # If tag already exists, throws ApiException: (409) Reason: Tag already exists
                            log.debug(
                                f"API call to add tag returned a 409, tag should exist.\n{e}"
                            )
                        else:
                            raise e

        # Reload the newly-created container
        dest_container = dest_container.reload()
    else:
        log.debug(f"Found destination {origin_type} for ({origin.id})")
    return dest_container


def initialize_container_file_export(  # noqa: PLR0913
    fw_client: flywheel.Client,
    deid_profile: deidentify.DeIdProfile,
    origin_container: flywheel.Subject | flywheel.Session | flywheel.Acquisition,
    dest_container: flywheel.Subject | flywheel.Session | flywheel.Acquisition,
    overwrite: str = "Cleanup",
    config: t.Optional[dict] = None,
) -> list:
    """
    Initializes a list of FileExporter objects for the origin_container/dest_container combination

    Args:
        config: the export configuration dictionary
        deid_profile(flywheel_migration.deidentify.DeIdProfile): the de-identification profile
        fw_client (fw.Client): an instance of the flywheel client
        origin_container (flywheel.<Container>): the container with files to be exported
        dest_container (flywheel.<Container>): the container to which files are to be exported
        overwrite (str): Strategy on how to overwrite file if file exists at destination

    Returns:
        (list): list of FileExporter objects
    """
    file_exporter_list = list()
    for container_file in origin_container.files:
        tmp_file_exporter = FileExporter(
            fw_client=fw_client,
            origin_parent=origin_container,
            origin_filename=container_file.name,
            dest_parent=dest_container,
            overwrite=overwrite,
            config=config,
        )
        if matches_file(deid_profile, container_file):
            log.debug(
                f"Initializing {origin_container.container_type} {origin_container.id} file {container_file.name}"
            )

        else:
            tmp_file_exporter.error_handler(
                log_str=f"Skipping file {container_file.name}, as it does not have a matching template",
                state="skipped",
            )
        file_exporter_list.append(tmp_file_exporter)

    return file_exporter_list


class SessionExporter:
    def __init__(
        self,
        fw_client: flywheel.Client,
        template_dict: dict,
        origin_session: flywheel.Session,
        dest_proj_id: str,
        dest_container_id: str = None,
    ):
        self.client = fw_client
        self.deid_profile, self.fw_metadata_profile = deid_template.load_deid_profile(
            template_dict
        )

        self.origin_project = fw_client.get_project(origin_session.project)
        self.dest_proj = fw_client.get_project(dest_proj_id)
        self.origin = origin_session.reload()
        # self.log = logging.getLogger(f'{self.origin.id}_exporter')

        self.errors = list()
        self.files = list()
        self.dest_subject = None

        # use dest_container_id if it's been provided
        if dest_container_id:
            self.dest = fw_client.get_session(dest_container_id)
            self.dest_subject = self.dest.subject.reload()
        else:
            self.dest = None

    def find_or_create_dest_subject(self):
        if not self.dest_subject:
            self.dest_subject = find_or_create_container(
                self.client,
                origin=self.origin.subject,
                dest_parent=self.dest_proj,
                fw_metadata_profile=self.fw_metadata_profile,
            )
        return self.dest_subject

    def find_or_create_dest(self):
        if not self.dest:
            if not self.dest_subject:
                self.find_or_create_dest_subject()

            self.dest = find_or_create_container(
                self.client,
                origin=self.origin,
                dest_parent=self.dest_subject,
                fw_metadata_profile=self.fw_metadata_profile,
            )
        return self.dest

    def find_or_create_acquisitions(self):
        if not self.dest:
            self.find_or_create_dest()
        self.origin = self.origin.reload()
        for acquisition in self.origin.acquisitions():
            find_or_create_container(
                self.client,
                origin=acquisition,
                dest_parent=self.dest,
                fw_metadata_profile=self.fw_metadata_profile,
            )

        self.dest.reload()

    def initialize_files(
        self, subject_files=False, project_files=False, overwrite="Cleanup"
    ):
        log.debug(f"Initializing {self.origin.id} files")
        if not self.dest:
            self.dest = self.find_or_create_dest()

        # project files
        if project_files is True:
            proj_file_list = initialize_container_file_export(
                deid_profile=self.deid_profile,
                fw_client=self.client,
                origin_container=self.origin_project.reload(),
                dest_container=self.dest_proj.reload(),
                config=self.fw_metadata_profile,
                overwrite=overwrite,
            )
            self.files.extend(proj_file_list)

        # subject files
        if subject_files is True:
            subj_file_list = initialize_container_file_export(
                deid_profile=self.deid_profile,
                fw_client=self.client,
                origin_container=self.origin.subject.reload(),
                dest_container=self.dest.subject.reload(),
                config=self.fw_metadata_profile,
                overwrite=overwrite,
            )
            self.files.extend(subj_file_list)

        # session files
        sess_file_list = initialize_container_file_export(
            deid_profile=self.deid_profile,
            fw_client=self.client,
            origin_container=self.origin,
            dest_container=self.dest.reload(),
            config=self.fw_metadata_profile,
            overwrite=overwrite,
        )
        self.files.extend(sess_file_list)

        self.origin = self.origin.reload()
        # acquisition files
        for origin_acq in self.origin.acquisitions.iter():
            origin_acq = origin_acq.reload()
            dest_acq = find_or_create_container(
                self.client,
                origin=origin_acq,
                dest_parent=self.dest,
                fw_metadata_profile=self.fw_metadata_profile,
            )
            tmp_acq_file_list = initialize_container_file_export(
                deid_profile=self.deid_profile,
                fw_client=self.client,
                origin_container=origin_acq,
                dest_container=dest_acq,
                config=self.fw_metadata_profile,
                overwrite=overwrite,
            )
            self.files.extend(tmp_acq_file_list)

        return self.files

    def local_file_export(self):
        # De-identify
        for file_exporter in self.files:
            if file_exporter.state not in ["error", "skipped"]:
                file_exporter.deidentify(self.deid_profile)
        fname_dict = dict()
        for file_exporter in self.files:
            if file_exporter.filename:
                if file_exporter.dest_parent.id not in fname_dict.keys():
                    fname_dict[file_exporter.dest_parent.id] = [file_exporter.filename]
                elif file_exporter.filename not in fname_dict.get(
                    file_exporter.dest_parent.id
                ):
                    fname_dict[file_exporter.dest_parent.id].append(
                        file_exporter.filename
                    )

                else:
                    file_exporter.error_handler(
                        f"Cannot upload {file_exporter.origin_filename} "
                        f"({file_exporter.origin.id}) from "
                        f"{file_exporter.origin.parent_ref.get('type')}, id - "
                        f"({file_exporter.origin.parent_ref.get('id')}) to "
                        "destination container because another file has already been uploaded "
                        "with the same name. Please use filename output strings that will "
                        "create unique filenames in your de-identification template."
                    )

        for file_exporter in self.files:
            file_exporter.reload()
            if (
                file_exporter.state not in ["error", "skipped"]
                and file_exporter.filename
            ):
                file_exporter.upload()
        for file_exporter in self.files:
            file_exporter.reload()
            if file_exporter.state == "upload_attempted":
                file_exporter.update_metadata()

        dict_list = [file_exporter.get_status_dict() for file_exporter in self.files]
        export_df = pd.DataFrame(dict_list)

        del dict_list
        return export_df

    def get_status_df(self):
        if not self.files:
            return None
        else:
            status_df = pd.DataFrame(
                [file_exporter.get_status_dict() for file_exporter in self.files]
            )
            return status_df


# TODO: Allow files to be exported without template
def export_session(  # noqa: PLR0913
    fw_client: flywheel.Client,
    origin_session_id: str,
    dest_proj_id: str,
    template_path: str,
    subject_files: bool = False,
    project_files: bool = False,
    csv_output_path: str = None,
    overwrite: str = "Cleanup",
):
    template = load_template_dict(template_path)
    origin_session = fw_client.get_session(origin_session_id)

    session_exporter = SessionExporter(
        fw_client=fw_client,
        origin_session=origin_session,
        dest_proj_id=dest_proj_id,
        template_dict=template,
    )

    session_exporter.initialize_files(
        subject_files=subject_files, project_files=project_files, overwrite=overwrite
    )
    session_export_df = session_exporter.local_file_export()
    if len(session_export_df) >= 1:
        if csv_output_path:
            session_export_df.to_csv(csv_output_path, index=False)

        if session_export_df["state"].all() == "error":
            log.error(
                f"Failed to export all {origin_session_id} files."
                f" Please check template {os.path.basename(template_path)}"
            )
    return session_export_df
    # else:
    #     return None


def get_session_error_df(  # noqa: PLR0913
    fw_client: flywheel.Client,
    session_obj: flywheel.Session,
    error_msg: str,
    deid_profile: deidentify.DeIdProfile,
    project_files: bool = False,
    subject_files: bool = False,
) -> pd.DataFrame:
    session_obj = session_obj.reload()
    status_dict_list = list()

    def _append_file_status_dicts(parent_obj):
        for file_obj in parent_obj.files:
            if deid_profile.matches_file(file_obj.name):
                status_dict = {
                    "origin_filename": file_obj.name,
                    "origin_parent": parent_obj.id,
                    "origin_parent_type": parent_obj.container_type,
                    "export_filename": None,
                    "export_file_id": None,
                    "export_parent": None,
                    "state": "error",
                    "errors": error_msg,
                }
                status_dict_list.append(status_dict)

    # Handle project files
    if project_files:
        project_obj = fw_client.get_project(session_obj.project)
        _append_file_status_dicts(project_obj)
    # Handle subject files
    if subject_files:
        subject_obj = session_obj.subject.reload()
        _append_file_status_dicts(subject_obj)
    # Handle session files
    _append_file_status_dicts(session_obj)
    # Handle acquisition files
    for acquisition_obj in session_obj.acquisitions():
        acquisition_obj = acquisition_obj.reload()
        _append_file_status_dicts(acquisition_obj)

    session_df = pd.DataFrame(status_dict_list)
    return session_df


# TODO: incorporate filetype list
def export_container(  #   # noqa: PLR0913, PLR0915
    fw_client: flywheel.Client,
    container_id: str,
    dest_proj_id: str,
    template_path: str,
    jinja_var_df: t.Optional[pd.DataFrame],
    key_dict: dict,
    csv_output_path: t.Optional[str] = None,
    overwrite: str = "Cleanup",
    old_label_col: str = deid_template.DEFAULT_SUBJECT_CODE_COL,
):
    container = fw_client.get(container_id).reload()

    error_count = 0

    # If jinja variables exist, add keys to variable dataframe
    if isinstance(jinja_var_df, pd.DataFrame):
        for k, v in key_dict.items():
            jinja_var_df[k] = v

    elif key_dict:
        # If jinja_var_df = None, the only possible jinja variables should be keys
        deid_template.update_deid_profile(
            template_path, updates=key_dict, dest_path=template_path
        )

    def _export_session(
        session_id: str,
        session_template_path: t.Optional[str] = None,
        project_files: bool = False,
        subject_files: bool = False,
        sess_error_msg: t.Optional[str] = None,
    ) -> int:
        template_dict = load_template_dict(session_template_path)

        if sess_error_msg:
            sess_deid_profile, _ = deid_template.load_deid_profile(template_dict)
            session_obj = fw_client.get_session(session_id)
            session_df = get_session_error_df(
                fw_client=fw_client,
                session_obj=session_obj,
                error_msg=sess_error_msg,
                deid_profile=sess_deid_profile,
            )
        else:
            session_df = export_session(
                fw_client=fw_client,
                origin_session_id=session_id,
                dest_proj_id=dest_proj_id,
                template_path=session_template_path,
                subject_files=subject_files,
                project_files=project_files,
                csv_output_path=None,
                overwrite=overwrite,
            )
        df_count = 0

        if isinstance(session_df, pd.DataFrame):
            if "state" in session_df:
                df_count = session_df["state"].value_counts().get("error", 0)
            if (
                csv_output_path
                and not os.path.isfile(csv_output_path)
                and (len(session_df) >= 1)
            ):
                session_df.to_csv(csv_output_path, index=False)
            elif (
                csv_output_path
                and os.path.isfile(csv_output_path)
                and (len(session_df) >= 1)
            ):
                session_df.to_csv(csv_output_path, mode="a", header=False, index=False)

        return df_count

    def _get_subject_template(
        subject_obj: flywheel.Subject, directory_path: str
    ) -> tuple[str | None, str | None]:
        subj_template_path = os.path.join(
            directory_path, f"{subject_obj.id}_{os.path.basename(template_path)}"
        )
        try:
            subj_template_path = deid_template.get_updated_template(
                df=jinja_var_df,
                deid_template_path=template_path,
                subject_label=subject_obj.label,
                subject_label_col=old_label_col,
                dest_template_path=subj_template_path,
            )
            error_msg = None
        except ValueError as e:
            error_msg = f"Could not create subject template for {subject.label}: {e}"
            subj_template_path = None
            log.info(error_msg)
        except Exception as e:
            error_msg = f"An exception occurred when creating subject template for {subject.label}: {e}"
            subj_template_path = None
            log.error(error_msg, exc_info=True)
        return subj_template_path, error_msg

    def _export_subject(
        subject_obj: flywheel.Subject, project_files: bool = False
    ) -> int:
        subject_error_count = 0
        subj_error_msg = None
        with tempfile.TemporaryDirectory() as temp_dir:
            subj_template_path = template_path
            if isinstance(jinja_var_df, pd.DataFrame):
                subj_template_path, subj_error_msg = _get_subject_template(
                    subject_obj=subject_obj, directory_path=temp_dir
                )
            subject_files = True
            # Only process if subj_template_path is provided
            if subj_template_path:
                sessions = subject_obj.sessions()
                # deterministic shuffling to avoid creating sessions in same order
                # as source project
                random.seed(container_id)
                random.shuffle(sessions)
                for session in sessions:
                    sess_count = _export_session(
                        session_id=session.id,
                        session_template_path=subj_template_path,
                        project_files=project_files,
                        subject_files=subject_files,
                        sess_error_msg=subj_error_msg,
                    )
                    subject_error_count += sess_count
                    subject_files = False
                    project_files = False

        return subject_error_count

    if container.container_type not in ["subject", "project", "session"]:
        raise ValueError(
            f"Cannot load container type {container.container_type}. Must be session, subject, or project"
        )

    elif container.container_type == "project":
        project_files = True
        for subject in container.subjects():
            subj_error_count = _export_subject(
                subject_obj=subject, project_files=project_files
            )
            error_count += subj_error_count
            project_files = False

    elif container.container_type == "subject":
        project_files = False
        error_count = _export_subject(
            subject_obj=container, project_files=project_files
        )

    elif container.container_type == "session":
        session_export_error = None
        with tempfile.TemporaryDirectory() as temp_dir:
            sess_template_path = template_path
            if isinstance(jinja_var_df, pd.DataFrame):
                sess_template_path, session_export_error = _get_subject_template(
                    subject_obj=container.subject, directory_path=temp_dir
                )
            error_count = _export_session(
                session_id=container_id,
                session_template_path=sess_template_path,
                sess_error_msg=session_export_error,
            )

    return error_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "origin_container_path", help="Resolver path of the container to export"
    )
    parser.add_argument(
        "project_path", help="Resolver path of the project to which to export"
    )
    parser.add_argument(
        "template_path", help="Local path of the de-identification template"
    )
    parser.add_argument(
        "--csv_output_path", help="path to which to write the output csv"
    )
    parser.add_argument("--api_key", help="Use if not logged in via cli")
    parser.add_argument(
        "--overwrite_files",
        help="Overwrite existing files in the destination project where present",
        action="store_true",
    )
    parser.add_argument(
        "--subject_csv_path", help="path to the subject csv", default=None
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging when running as script",
    )
    args = parser.parse_args()
    if args.api_key:
        fw = flywheel.Client(args.api_key)
    else:
        fw = flywheel.Client()

    if args.debug:
        # Set root logger level to debug
        logging.getLogger().setLevel("DEBUG")

    dest_project = fw.lookup(args.project_path)
    origin_container = fw.lookup(args.origin_container_path)
    csv_output_path = os.path.join(
        os.getcwd(),
        f"{origin_container.container_type}_{origin_container.id}_export.csv",
    )
    if args.csv_output_path:
        csv_output_path = args.csv_output_path

    export_container(
        fw_client=fw,
        container_id=origin_container.id,
        dest_proj_id=dest_project.id,
        template_path=args.template_path,
        csv_output_path=csv_output_path,
        overwrite=args.overwrite_files,
        subject_csv_path=args.subject_csv_path,
    )
