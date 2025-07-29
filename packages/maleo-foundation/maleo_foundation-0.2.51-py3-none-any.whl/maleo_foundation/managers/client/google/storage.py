import os
from datetime import timedelta
from google.cloud.storage import Bucket, Client
from google.oauth2.service_account import Credentials
from pathlib import Path
from typing import Optional, Union
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.logging import SimpleConfig
from .base import GoogleClientManager

class GoogleCloudStorage(GoogleClientManager):
    def __init__(
        self,
        log_config:SimpleConfig,
        service_key:BaseTypes.OptionalString=None,
        credentials:Optional[Credentials]=None,
        credentials_path:Optional[Union[Path, str]]=None,
        bucket_name:BaseTypes.OptionalString = None
    ) -> None:
        key = "google-cloud-storage"
        name = "GoogleCloudStorage"
        super().__init__(key, name, log_config, service_key, credentials, credentials_path)
        self._client = Client(credentials=self._credentials)
        self._bucket_name = bucket_name or os.getenv("GCS_BUCKET_NAME")
        if self._bucket_name is None:
            self._client.close()
            raise ValueError("GCS_BUCKET_NAME environment variable must be set if 'bucket_name' is set to None")
        self._bucket = self._client.lookup_bucket(bucket_name=self._bucket_name)
        if self._bucket is None:
            self._client.close()
            raise ValueError(f"Bucket '{self._bucket_name}' does not exist.")
        self._logger.info("Client manager initialized successfully")

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @property
    def bucket(self) -> Bucket:
        return self._bucket

    def dispose(self) -> None:
        if self._client is not None:
            self._logger.info("Disposing client manager")
            self._client.close()
            self._client = None
            self._logger.info("Client manager disposed successfully")

    def generate_signed_url(self, location:str) -> str:
        """
        generate signed URL of a file in the bucket based on its location.

        Args:
            location: str
                Location of the file inside the bucket

        Returns:
            str: File's pre-signed download url

        Raises:
            ValueError: If the file does not exist
        """
        blob = self._bucket.blob(blob_name=location)
        if not blob.exists():
            raise ValueError(f"File '{location}' did not exists.")

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=15),
            method="GET"
        )
        return url