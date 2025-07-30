import logging
import time
from dataclasses import dataclass
from os import path

import requests

from edge_addons_api.exceptions import UploadException

logger = logging.getLogger(__name__)


class ResponseStatus:
    SUCCEEDED = "Succeeded"
    IN_PROGRESS = "InProgress"
    FAILED = "Failed"


@dataclass
class Options:
    product_id: str
    client_id: str
    api_key: str
    retry_count: int = 10
    sleep_seconds: int = 3


class Client:
    BASE_URL = "https://api.addons.microsoftedge.microsoft.com"

    def __init__(self, options: Options):
        self.options = options

    def submit(self, file_path: str, notes: str) -> str:
        if not path.exists(file_path):
            raise FileNotFoundError(f"Unable to locate file at {file_path}")

        operation_id = self._upload(file_path)
        self._check_upload(operation_id)
        return self._publish(notes)

    def fetch_publish_status(self, operation_id: str) -> dict:
        logger.debug(f"Fetching publish status for {operation_id}")
        response = requests.get(
            self._publish_status_endpoint(operation_id),
            headers=self._publish_default_headers(),
        )

        response.raise_for_status()

        logger.debug(f"Publish status response: {response.content.decode()}")
        return response.json()

    def _publish(self, notes: str) -> str:
        logger.debug("Publishing")
        response = requests.post(
            self._publish_endpoint(),
            data={"notes": notes},
            headers=self._publish_default_headers(),
        )

        response.raise_for_status()

        logger.debug(f"Publish response: {response.content.decode()}")

        return response.headers["Location"]

    def _upload(self, file_path: str) -> str:
        logger.debug(f"Uploading {file_path}")
        with open(file_path, "rb") as f:
            response = requests.post(
                self._upload_endpoint(),
                data=f,
                headers={
                    "Content-Type": "application/zip",
                    **self._publish_default_headers(),
                },
            )

        response.raise_for_status()

        logger.debug("Finished upload")

        return response.headers["Location"]

    def _check_upload(
        self,
        operation_id,
    ) -> str:
        logger.debug("Checking upload")

        upload_status = ""
        attempts = 0

        while (
            upload_status != ResponseStatus.SUCCEEDED
            and attempts < self.options.retry_count
        ):
            response = requests.get(
                self._status_endpoint(operation_id),
                headers=self._publish_default_headers(),
            )

            response.raise_for_status()
            response_json = response.json()

            logger.debug(f"Status response: {response_json}")
            upload_status = response_json["status"]
            if upload_status == ResponseStatus.FAILED:
                raise UploadException(
                    response_json["status"],
                    response_json["message"],
                    response_json["errorCode"],
                    response_json["errors"],
                )
            elif upload_status == ResponseStatus.IN_PROGRESS:
                time.sleep(self.options.sleep_seconds)
                attempts += 1

        return upload_status

    def _product_endpoint(self) -> str:
        return f"{self.BASE_URL}/v1/products/{self.options.product_id}"

    def _publish_endpoint(self) -> str:
        return f"{self._product_endpoint()}/submissions"

    def _upload_endpoint(self) -> str:
        return f"{self._publish_endpoint()}/draft/package"

    def _status_endpoint(self, operation_id: str) -> str:
        return f"{self._upload_endpoint()}/operations/{operation_id}"

    def _publish_status_endpoint(self, operation_id: str) -> str:
        return f"{self._publish_endpoint()}/operations/{operation_id}"

    def _publish_default_headers(self):
        return {
            "Authorization": f"ApiKey {self.options.api_key}",
            "X-ClientID": self.options.client_id,
        }
