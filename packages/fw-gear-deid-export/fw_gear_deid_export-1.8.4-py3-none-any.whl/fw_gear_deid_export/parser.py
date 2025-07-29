import logging
import os

import flywheel
from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_deid_export.var_utils import create_jinja_var_df

log = logging.getLogger(__name__)


def parse_args_from_context(gear_context: GearToolkitContext):
    # Confirm existence of destination project
    project_path = gear_context.config.get("project_path")
    project = lookup_project(gear_context.client, project_path)
    if not project:
        log.error(f"Project {project_path} not found. Exiting")
        os.sys.exit(1)

    destination_id = gear_context.destination.get("id")

    origin = get_analysis_parent(gear_context.client, destination_id)
    has_proj_perm = user_has_project_permissions(gear_context.client, project)
    if not has_proj_perm:
        log_str = (
            f"User {gear_context.client.get_current_user().id} does not have "
            f"permission on destination project {project.id}"
        )

        log.error(log_str)
        log_str = (
            " Please add permission for this user on the project before"
            " running this gear."
        )
        log.error(log_str)

    # Return None if we failed to get the origin or destination project
    if not project or not origin or not has_proj_perm:
        return None

    template_path = gear_context.get_input_path("deid_profile")
    csv_path = gear_context.get_input_path("subject_csv")

    export_container_args = {
        "fw_client": gear_context.client,
        "container_id": origin.id,
        "dest_proj_id": project.id,
        "template_path": template_path,
        "jinja_var_df": create_jinja_var_df(
            template_path=template_path, origin=origin, csv_path=csv_path
        ),
        "key_dict": create_key_dict(gear_context),
        "csv_output_path": os.path.join(
            gear_context.output_dir, f"{origin.id}_export.csv"
        ),
        "overwrite": gear_context.config.get("overwrite_files"),
    }

    return export_container_args


def lookup_project(fw_client, project_resolver_path):
    """Attempts to lookup and return the project at the resolver path.

    If the path is not for a project or an exception is raised, will return None

    Args:
        fw_client (flywheel.Client): An instance of the Flywheel client
        project_resolver_path (str): Path to project

    Returns:
        object: The project at the resolver path

    """
    try:
        project = fw_client.lookup(project_resolver_path)
        if project.container_type != "project":
            log.error(f"{project.container_type} {project.id} is not a project!")
            return None
        else:
            return project
    except flywheel.ApiException as e:
        log.error(e, exc_info=True)
        log.error(f"could not retrieve a project at {project_resolver_path}")
        return None


def get_analysis_parent(fw_client, container_id):
    """Return parent container id of the analysis container provided
    Args:
        fw_client (flywheel.Client): An instance of the Flywheel client
        container_id (str): A flywheel analysis container id

    Returns:
        (object or None): The container object or None if an exception is raised retrieving the container
    """
    try:
        container = fw_client.get(container_id)
        container_parent = fw_client.get(container.parent.id)
        log.info(
            f"Destination analysis {container.id} parent is a {container_parent.container_type} with "
            f"id {container_parent.id}"
        )
        return container_parent
    except Exception as e:
        log.error(e, exc_info=True)
        return None


def user_has_project_permissions(fw_client, project_obj):
    """
    Returns True if user has explicit permissions on the project, otherwise
        returns False
    Args:
        fw_client (flywheel.Client): An instance of the Flywheel client
        project_obj (flywheel.Project): a Flywheel project

    Returns:
        bool: whether the user has explicit permissions on the project
    """
    project_obj = project_obj.reload()
    user_id = fw_client.get_current_user().id
    has_permissions = any([perm.id == user_id for perm in project_obj.permissions])
    return has_permissions


def create_key_dict(gear_context: GearToolkitContext) -> dict:
    """Creates dictionary of keys to be inserted into the deid profile."""
    key_dict = dict()
    public_key_input = gear_context.config.get("public_key")
    if public_key_input:
        public_key_path = get_keys_from_path(
            gear_context.client,
            public_key_input,
            "public",
            gear_context.work_dir,
        )
        key_dict["PUBLIC_KEY"] = public_key_path
    private_key_input = gear_context.config.get("private_key")
    if private_key_input:
        private_key_path = get_keys_from_path(
            gear_context.client,
            private_key_input,
            "private",
            gear_context.work_dir,
        )
        key_dict["PRIVATE_KEY"] = private_key_path
    secret_key_input = gear_context.config.get("secret_key")
    if secret_key_input:
        secret_key_path = get_keys_from_path(
            gear_context.client,
            secret_key_input,
            "secret",
            gear_context.work_dir,
        )
        with open(secret_key_path) as f:
            secret_key = f.read()
        key_dict["SECRET_KEY"] = secret_key

    return key_dict


def get_keys_from_path(
    fw_client: flywheel.Client, key_input: str, key_type: str, workdir: str
) -> str:
    """Retrieves key file(s) from given path, saves to workdir, returns path(s)

    Args:
        fw_client: An instance of the Flywheel client
        key_input: Path to key(s), formatted as `group/project:filename`, multiple values separated by `, `
        key_type: "public" or "private"
        workdir: Path to work directory

    Returns:
        str: String representation of path(s) to downloaded key(s)
    """
    try:
        keys = key_input.split(", ")
        downloaded_keys = []
        for key in keys:
            result = fw_client.lookup(key)
            downloaded_key = f"{workdir}/{result.name}"
            file = fw_client.get_file(result.file_id)
            file.download(downloaded_key)
            downloaded_keys.append(downloaded_key)
        if key_type == "public":
            return repr(downloaded_keys)
        else:  # key_type in "private", "secret"
            return downloaded_keys[0]
    except flywheel.rest.ApiException as e:
        log.error(e, exc_info=True)
        log.error(f"Unable to download {key_type} key from {key_input}. Exiting.")
        os.sys.exit(1)
