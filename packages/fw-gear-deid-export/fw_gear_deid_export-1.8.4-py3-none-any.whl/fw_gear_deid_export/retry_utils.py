"""Module for situation-specific retry utils."""

import logging
import os
import time
import typing as t

from flywheel import Acquisition, Project, Session, Subject

log = logging.getLogger(__name__)


def upload_file_with_retry(  # noqa: PLR0913   (Too many arguments)
    container: Project | Subject | Session | Acquisition,
    upload_fn: t.Callable,
    file: str,
    signed: bool = False,
    metadata: t.Optional[t.Dict[str, str]] = None,
    max_retry: int = 3,
):
    """Calls the upload_fn with smart retry.

    Args:
        container: Flywheel Project/Subject/Session/Acquisition object
        upload_fn: fw_client.upload_file_to_{container_type}
        file: path to file to upload
        signed: Whether to use signed URL upload methods
        metadata: Metadata dict to attach to the uploaded file, if any
        max_retry: Max times to retry after initial POST, default 3
    """
    file_name = os.path.basename(file)
    # If a version of the file already exists in destination container,
    # will need to make sure overwrite happens, not just that file exists,
    # to confirm upload.
    version = 0
    for f in container.files:
        if f.name == file_name:
            # Overwriting, store current version
            version = f.version

    retry_num = 0
    while retry_num <= max_retry:
        try:
            return upload_fn(container.id, file, signed=signed, metadata=metadata)
            # API: POST /api/container/cid/files
        except Exception as e:
            log.warning(
                f"Encountered error uploading file {file_name}\n{e}\n"
                f"Retries remaining: {max_retry - retry_num}"
            )
            time.sleep(2**retry_num)
            container = container.reload()
            for f in container.files:
                if f.name == file_name and f.version > version:
                    # File uploaded, log, don't retry
                    log.info(
                        f"{file_name} version {f.version} exists in {container.type} {container.label}. "
                        "Upload completed with above error, continuing..."
                    )
                    return f
            retry_num += 1
    raise Exception(f"Max retries attempted for uploading {file_name}.")


def create_container_with_retry(
    dest_parent: Project | Subject | Session,
    origin_type: str,
    label: str,
    meta_dict: dict,
    max_retry: int = 3,
):
    """Calls POST /api/container with smart retry.

    Args:
        dest_parent: Parent of container to be created
        origin_type: Type of container to create
        label: Label of new container
        meta_dict: Dictionary of container meta information
        max_retry: Max times to retry after initial POST, default 3
    """
    adder = getattr(dest_parent, f"add_{origin_type}")
    finder_first = getattr(getattr(dest_parent, f"{origin_type}s"), "find_first")
    query = f"label={sanitize_label(label)}"

    retry_num = 0
    while retry_num <= max_retry:
        try:
            # API: POST /container
            return adder(label=label, **meta_dict)
        except Exception as e:
            log.warning(
                f"Encountered error creating {origin_type} {label}\n{e}\n"
                f"Retries remaining: {max_retry - retry_num}"
            )
            time.sleep(2**retry_num)
            # Check to see if container exists
            dest_container = finder_first(query)
            if dest_container:
                log.info(
                    f"{origin_type} {label} exists in {dest_parent.label}. "
                    "Container creation completed with above error, continuing..."
                )
                return dest_container
            retry_num += 1
    raise Exception(f"Max retries attempted for creating {origin_type} {label}.")


def sanitize_label(label: str) -> str:
    """Perform preprocessing on a label to make it safe for finder."""

    # Escape commas
    label = label.replace(",", "\\,")
    # Quote the string
    label = f'"{label}"'
    return label
