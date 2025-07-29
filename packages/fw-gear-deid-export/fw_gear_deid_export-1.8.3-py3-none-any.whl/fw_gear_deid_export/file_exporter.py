import datetime
import logging
import os
import re
import tempfile

import flywheel
from flywheel_gear_toolkit.utils import sdk_post_retry_handler
from flywheel_migration.util import sanitize_filename

from fw_gear_deid_export.deid_file import deidentify_file
from fw_gear_deid_export.metadata_export import get_deid_fw_container_metadata
from fw_gear_deid_export.uploader import Uploader

log = logging.getLogger(__name__)


def search_job_log_str(regex_string, job_log_str):
    if not job_log_str:
        return list()
    else:
        pattern = re.compile(regex_string)
        return pattern.findall(job_log_str)


def get_last_timestamp(job_log_str):
    JOB_LOG_TIME_STR_REGEX = (
        r"[\d]{4}\-[\d]{2}\-[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2}\.[\d]+"
    )
    time_str_list = search_job_log_str(JOB_LOG_TIME_STR_REGEX, job_log_str)
    dt_list = [
        datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        for time in time_str_list
    ]
    dt_list = [time_obj.replace(tzinfo=datetime.timezone.utc) for time_obj in dt_list]
    if not dt_list:
        return None
    else:
        return dt_list[-1]


def get_job_state_from_logs(
    job_log_obj,
    previous_state="pending",
    job_details=None,
    current_time=datetime.datetime.now(datetime.timezone.utc),
    max_seconds=500,
):
    """Parses job log to get information about state, leveraging log timestamps
    (configured to be UTC for grp-13-deid-file)
    """
    # If job details were provided, get the state from them
    if isinstance(job_details, flywheel.models.job_detail.JobDetail):
        detail_state = job_details.get("state")
    else:
        detail_state = None

    job_log_str = "".join(
        [log_line.get("msg") for log_line in job_log_obj.logs]
    ).replace("\n", " ")

    # We don't want to update state if the job is already done
    if detail_state in ["complete", "failed", "cancelled"]:
        state = detail_state
    elif previous_state in ["complete", "failed", "cancelled", "failed_or_cancelled"]:
        state = previous_state

    # If there are no logs, the job hasn't started yet
    elif not job_log_str:
        state = "pending"

    # Completed jobs contain "Job complete."
    elif search_job_log_str("Job complete.", job_log_str):
        state = "complete"

    # If contains 'Uploading results...' but is not complete, it is failed or cancelled.
    # (Can't tell which from log alone)
    elif search_job_log_str(r"Uploading results[\.]{3}", job_log_str):
        state = "failed_or_cancelled"

    # If the log contains timestamps, but is none of the above, it's running
    # If the log's last timestamp is more than max_seconds from current_time, we'll consider it
    # "hanging"
    elif get_last_timestamp(job_log_str):
        delta_time = current_time - get_last_timestamp(job_log_str)
        if delta_time.total_seconds() > max_seconds:
            state = "hanging"
        else:
            state = "running"

    # For this specific gear, if it doesn't meet any of the above, but has printed 'Gear Name:',
    # we probably caught it before it started logging.
    elif search_job_log_str("Gear Name:", job_log_str):
        state = "running"

    else:
        state = "unknown"

    return state


class DeidUtilityJob:
    def __init__(self, job_id=None):
        self.id = None
        self.detail = None
        self.job_logs = None
        self.state = None
        self.forbidden = False
        if job_id:
            self.id = job_id

    def submit_job(self, fw_client: flywheel.Client, gear_path: str, **kwargs):
        gear_obj = fw_client.lookup(gear_path)

        # Underlying API call is POST /api/{containertype}/{ContainertypeId}/analyses
        # It *is* possible for `gear_obj.run()` to spawn a job but fail to return an id
        # (see note on ZD-22926; it at least seems to be a rare issue...)
        # Possible check would be to check for job that matches all params, but if
        # bulk running, could get tricky.
        # Using sdk_post_retry_handler here still has a chance to duplicate jobs, I think.
        # NOTE: AFAIK this code is not utilized in current gear

        with sdk_post_retry_handler(fw_client):
            self.id = gear_obj.run(**kwargs)
        self.detail = fw_client.get_job_detail(self.id)
        self.job_logs = fw_client.get_job_logs(self.id)
        self.state = self.detail.state
        self.forbidden = False

    def reload(self, fw_client: flywheel.Client, force=False):
        self.job_logs = fw_client.get_job_logs(self.id)

        # It's possible for a non-admin to lose the ability to check detail if sessions are moved
        # or permissions are changed, don't update the detail if this happens
        if not self.forbidden or force:
            try:
                self.detail = fw_client.get_job_detail(self.id)
            except flywheel.ApiException as e:
                if e.status == "403":
                    self.forbidden = True
                else:
                    raise e
        self.state = get_job_state_from_logs(
            job_log_obj=self.job_logs,
            previous_state=self.state,
            job_details=self.detail,
            max_seconds=120,
        )

    def cancel(self, fw_client: flywheel.Client):
        if self.state in ["pending", "running", "hanging", "unknown"] or self.forbidden:
            try:
                fw_client.modify_job(self.id, {"state": "cancelled"})
                self.state = "cancelled"
                return self.state
            except flywheel.ApiException as e:
                # If the job is already cancelled, then the exception detail will be:
                #  "Cannot mutate a job that is <state>."
                done_job_str = "Cannot mutate a job that is "
                if done_job_str in e.detail:
                    job_state = e.detail.replace(done_job_str, "").replace(".", "")
                    self.state = job_state
                    return self.state
                else:
                    raise e
        else:
            return self.state


class FileExporter:
    """A class for representing the export status of a file"""

    def __init__(  # noqa: PLR0913
        self,
        fw_client: flywheel.Client,
        origin_parent: flywheel.Subject | flywheel.Session | flywheel.Acquisition,
        origin_filename: str,
        dest_parent: flywheel.Subject | flywheel.Session | flywheel.Acquisition,
        overwrite: str = "Cleanup",
        log_level: str = "INFO",
        config=None,
    ):
        self.fw_client = fw_client
        self.uploader = Uploader(fw_client)
        self.origin_parent = origin_parent
        self.dest_parent = dest_parent
        self.origin_filename = origin_filename
        self.config = dict()
        self.state = "initialized"
        self.overwrite = overwrite
        self.filename = ""
        self.deid_path = ""
        self.deid_job = DeidUtilityJob()
        self.errors = list()
        self.metadata_dict = None
        self.origin = origin_parent.get_file(origin_filename)
        if not self.origin:
            self.error_handler(
                f"{self.origin_filename} does not exist in {self.origin_parent.container_type} {self.origin_parent.id}"
            )
        self.dest = None
        self.initial_state = self.state
        if isinstance(config, dict):
            self.config = config

    def error_handler(self, log_str, state="error"):
        self.state = state
        if state == "skipped":
            log.warning(log_str)
        else:
            log.error(log_str)
        self.errors.append(log_str)

    def get_metadata_dict(self):
        fw_metadata_profile = dict()
        if isinstance(self.config, dict):
            fw_metadata_profile = self.config
        config = fw_metadata_profile.get("file", {})
        self.metadata_dict = get_deid_fw_container_metadata(
            self.fw_client, config, self.origin
        )

        return self.metadata_dict

    def update_metadata(self):  # noqa: PLR0912
        if not self.metadata_dict:
            self.get_metadata_dict()

        if self.dest:
            metadata_dict = self.metadata_dict.copy()
            type_ = metadata_dict.pop("type", None)
            modality = metadata_dict.pop("modality", None)
            if metadata_dict.get("info"):
                log.debug(
                    f"updating info for file {self.origin_filename} (origin = {self.origin.id})"
                )
                # POST /container/ContainerId/files/FileName/info
                with sdk_post_retry_handler(self.fw_client):
                    self.dest_parent.update_file_info(
                        self.filename, metadata_dict.pop("info")
                    )
                log.debug(
                    f"updated info for file {self.origin_filename} (origin = {self.origin.id})"
                )
            if modality:
                log.debug(
                    f"updating modality for file {self.origin_filename} (origin = {self.origin.id})"
                )
                if type_:
                    self.dest_parent.update_file(
                        self.filename, modality=modality, type=type_
                    )
                else:
                    self.dest_parent.update_file(self.filename, modality=modality)
                log.debug(
                    f"updated modality for file {self.origin_filename} (origin = {self.origin.id})"
                )
                # modality is required to set classification but for custom classif
                if metadata_dict.get("classification"):
                    log.debug(
                        f"updating classification for file {self.origin_filename} (origin = {self.origin.id})"
                    )
                    # replacing instead of updating to avoid 422 in case modality not set yet
                    # POST /acquisitions/cid/files/filename/classification
                    with sdk_post_retry_handler(self.fw_client):
                        self.dest_parent.replace_file_classification(
                            self.filename,
                            metadata_dict.get("classification"),
                            modality=modality,
                        )
                    log.debug(
                        f"updated classification for file {self.origin_filename} (origin = {self.origin.id})"
                    )
            else:  # if no modality, set custom classification if defined
                # setting type here to overcome https://flywheelio.atlassian.net/browse/FLYW-6472
                if type_ is not None:
                    self.dest_parent.update_file(self.filename, type=type_)

                if metadata_dict.get("classification", {}).get("Custom"):
                    log.debug(
                        f"updating custom classification for file {self.origin_filename} (origin = {self.origin.id})"
                    )
                    custom_classification = {
                        "Custom": metadata_dict.get("classification", {}).get("Custom")
                    }
                    # POST /acquisitions/cid/files/filename/classification
                    with sdk_post_retry_handler(self.fw_client):
                        self.dest_parent.replace_file_classification(
                            self.filename, custom_classification
                        )
                    log.debug(
                        f"updated custom classification for file {self.origin_filename} (origin = {self.origin.id})"
                    )

            if metadata_dict:
                metadata_dict.pop("info", None)
                metadata_dict.pop("classification", None)
                if metadata_dict:
                    self.dest_parent.update_file(self.filename, metadata_dict)
        else:
            self.error_handler(
                f"could not update metadata for file {self.origin_filename} in container {self.origin.id} - file was not found!"
            )

    def reload_fw_object(self, fw_object):
        fw_object = fw_object.reload()
        return fw_object

    def reload(self):  # noqa: PLR0912
        if self.state != "error":
            try:
                self.origin_parent = self.origin_parent.reload()
                self.dest_parent = self.dest_parent.reload()
                if self.filename:
                    self.dest = self.dest_parent.get_file(self.filename)

                if self.dest and self.state in [
                    "pending",
                    "running",
                    "upload_attempted",
                    "metadata_updated",
                ]:
                    dest_uid = (
                        self.dest.get("info", {})
                        .get("export", {})
                        .get("origin_id", None)
                    )
                    local_uid = (
                        self.get_metadata_dict()
                        .get("info", {})
                        .get("export", {})
                        .get("origin_id", None)
                    )
                    if dest_uid and dest_uid == local_uid:
                        self.state = "exported"
                        self.cleanup()
                    else:
                        self.update_metadata()
                        self.state = "metadata_updated"

                if self.deid_job.id:
                    self.deid_job = self.deid_job.reload(self.fw_client)
                    if self.state == "pending":
                        if self.deid_job.state == "cancelled":
                            self.state = "cancelled"
                        elif self.deid_job.state in ["failed", "failed_or_cancelled"]:
                            log_str = (
                                f"De-id job failed. Please refer to the logs for job {self.deid_job.id} for "
                                f"{self.dest_parent.container_type} {self.dest_parent.id} "
                                "for additional details"
                            )
                            self.error_handler(log_str)
                    elif self.deid_job.state == "complete" and self.dest:
                        self.state = "exported"
                    else:
                        pass
                log.debug(f"file state is {self.state}")

            except Exception as e:
                log_str = f"An exception occurred while reloading file in {self.origin.id}: {e}"
                self.error_handler(log_str)
            finally:
                return self

    def submit_deid_job(self, gear_path, template_file_obj):
        self.reload()

        if self.deid_job.id:
            log.warning(
                f"Job already exists for {self.filename} ({self.deid_job.id}). A new one will not be queued"
            )
            return self.deid_job.id

        if self.state != "error":
            job_dict = dict()
            job_dict["config"] = {
                "origin": self.origin.id,
                "output_filename": self.filename,
            }
            job_dict["inputs"] = {
                "input_file": self.origin,
                "deid_profile": template_file_obj,
            }
            job_dict["destination"] = self.dest_parent
            try:
                self.deid_job.submit_job(
                    fw_client=self.fw_client, gear_path=gear_path, **job_dict
                )
            except Exception as e:
                log_str = f"An exception was raised while attempting to submit a job for {self.origin_filename}: {e}"
                self.error_handler(log_str)
            self.state = "pending"
            return self.deid_job.id

    def cancel_deid_job(self):
        if not self.deid_job.id:
            log.debug("Cannot cancel a job that does not exist...")
            return None
        else:
            self.deid_job.cancel(self.fw_client)
            self.state = "cancelled"

    def deidentify(self, deid_profile):
        with tempfile.TemporaryDirectory() as temp_dir1:
            # Download the file

            local_file_path = os.path.join(
                temp_dir1, sanitize_filename(self.origin_filename)
            )
            log.debug(f"Downloading {self.origin_filename}")
            self.origin.download(local_file_path)

            # De-identify
            log.debug(f"Applying de-identfication template to {local_file_path}")
            temp_dir = tempfile.mkdtemp()
            try:
                deid_path = deidentify_file(
                    deid_profile=deid_profile,
                    file_path=local_file_path,
                    output_directory=temp_dir,
                )
            except Exception as e:
                exc = str(e).split("\n")[0]
                self.error_handler(
                    f"an exception was raised when de-identifying {self.origin_filename}: {exc}"
                )
                log.exception(e)
                return None
            if not os.path.exists(deid_path):
                self.error_handler(f"{self.origin_filename} de-identification failed.")
            else:
                self.filename = os.path.basename(deid_path)
                self.deid_path = deid_path
                self.get_metadata_dict()
                self.state = "processed"

    def upload(self):  # noqa: PLR0915, PLR0912
        """
        If self.deid_file exists and no file conflicts are found for the dest parent container,
            the file will be uploaded
        """

        def can_upload():
            """
            Checks whether a file of the same filename exists on the destination parent container. If not, it is safe to
            upload. If so, overwrite must be True and the export_id of the existing file must match the one for the file
            to be uploaded.

            Returns:
                bool: whether a file can be uploaded to the destination parent container

            """
            upload = False
            delete_strategy = None
            self.reload()
            if not self.dest:
                upload = True
            # when file exists at destination
            # verify overwrite configuration
            elif self.overwrite == "Skip":
                # Skip upload file if file exists at destination
                self.error_handler(
                    f"File {self.origin_filename} cannot be uploaded (origin = {self.origin.id}). "
                    f"File exists at destination and overwrite config is set to Skip",
                    state="skipped",
                )
            elif self.overwrite == "Cleanup":
                # Delete file and upload a new file if file exists at destination
                upload = True
                delete_strategy = "basic"  # shallow delete file
            elif self.overwrite == "Cleanup_force":
                # Force delete file and upload new file if file exists at destination
                upload = True
                delete_strategy = (
                    "force"  # force delete file (even it is smart copied file)
                )
            elif self.overwrite == "Replace":
                # Upload a new version of file if file exists at destination without deletion of file
                upload = True
            else:
                self.error_handler(f"Invalid overwrite config value: {self.overwrite}")

            return upload, delete_strategy

        if not os.path.exists(self.deid_path):
            self.error_handler(
                f"File {self.origin_filename} cannot be uploaded to destination (origin = {self.origin.id}) - local path does not exist"
            )
        if self.state == "processed":
            upload, delete_strategy = can_upload()
            if upload:
                failed = False
                if self.dest:
                    log.debug(
                        f"File {self.origin_filename} (origin = {self.origin.id}) already exists at destination. "
                    )
                    if delete_strategy and delete_strategy in ["basic", "force"]:
                        log.debug(
                            f"Delete strategy is set to {delete_strategy}. Deleting {self.filename} at destination"
                        )
                        self.dest_parent.update_file(
                            self.filename, {"type": "tmp-type"}
                        )

                        force = True if delete_strategy == "force" else False

                        try:
                            self.fw_client.delete_file(self.dest.file_id, force=force)
                        except flywheel.rest.ApiException as e:
                            err_msg = (
                                f"Error occurred when "
                                f"deleting file {self.filename}. Details: {str(e)} "
                            )
                            log.debug(err_msg)
                            if e.status == 409:
                                # Handle 409 Cannot delete file with copies error separately
                                self.error_handler(err_msg)
                                failed = True
                            else:
                                # raise exception for other error message
                                raise
                if failed:
                    self.state = "error"
                else:
                    # Export file's zip_member_count and file tags
                    metadata_dict = dict()
                    if self.origin.zip_member_count:
                        metadata_dict["zip_member_count"] = self.origin.zip_member_count
                    if self.origin.tags:
                        metadata_dict["tags"] = self.origin.tags
                    self.uploader.upload(
                        self.dest_parent, self.deid_path, metadata_dict
                    )
                    self.state = "upload_attempted"
        else:
            log.warning(
                "Cannot upload file %s for origin %s. State %s is not processed.",
                self.origin_filename,
                self.origin.id,
                self.state,
            )

    def cleanup(self):
        if os.path.exists(self.deid_path):
            os.remove(self.deid_path)

    def get_status_dict(self):
        self.reload()
        status_dict = {
            "origin_filename": self.origin.name,
            "origin_parent": self.origin_parent.id,
            "origin_parent_type": self.origin_parent.container_type,
            "state": self.state,
            "errors": "\t".join(self.errors),
        }
        return status_dict
