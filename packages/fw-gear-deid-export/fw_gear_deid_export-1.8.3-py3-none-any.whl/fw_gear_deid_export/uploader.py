import logging
import os
import typing as t

import flywheel

from fw_gear_deid_export.retry_utils import upload_file_with_retry

TICKETED_UPLOAD_PATH = "/{ContainerType}/{ContainerId}/files"
log = logging.getLogger(__name__)


class Uploader:
    def __init__(self, fw_client: flywheel.Client):
        self.fw_client = fw_client
        self.supports_signed_url: bool = self._supports_signed_url()

    def _supports_signed_url(self) -> bool:
        """Get signed url feature.

        This method checks if the signed URL feature is supported by the Flywheel
        client.

        It's supposed to be called at initialization time.

        Returns:
            bool: True if the signed URL feature is supported, False otherwise.
        """
        config = self.fw_client.get_config()

        # Support the new and legacy method of feature advertisement, respectively
        features = config.get("features")
        f1 = features.get("signed_url", False) if features else False
        f2 = config.get("signed_url", False)

        return f1 or f2

    def upload(
        self,
        container: flywheel.Subject | flywheel.Session | flywheel.Acquisition,
        filepath: str,
        metadata: t.Optional[t.Dict] = None,
    ):
        """Upload a file to a Flywheel container.

        This method uploads a file to a specified Flywheel container (Subject, Session,
        or Acquisition) using the Flywheel client. It supports both signed and unsigned
        URL uploads, depending on the Flywheel server configuration.

        Args:
            container (flywheel.Subject | flywheel.Session | flywheel.Acquisition):
                The Flywheel container to which the file will be uploaded.
            filepath (str): The path to the file to be uploaded.
            metadata (dict, optional): Metadata to attach to the uploaded file. Defaults to None.
        """
        log.debug(
            "Uploading file %s to %s=%s",
            os.path.basename(filepath),
            container.container_type,
            container.id,
        )

        upload_file_with_retry(
            container=container,
            upload_fn=self.fw_client.upload_file_to_container,
            file=filepath,
            signed=self.supports_signed_url,
            metadata=metadata,
            max_retry=3,
        )
