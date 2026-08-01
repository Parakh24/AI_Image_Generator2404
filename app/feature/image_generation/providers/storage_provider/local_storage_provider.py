"""
local_storage_provider.py

Concrete adapter that saves images to the local file system.

RULE: everything specific to "how local disk storage works" lives
here - folder structure, file naming, how the URL is built. If we
switch to S3 later, only this file gets replaced - a new
s3_storage_provider.py implementing the same StorageProvider
interface, nothing else in the project changes.
"""

import os

from app.feature.image_generation.providers.storage_provider.storage_base import (
    StorageProvider,
    StorageProviderError,
    StorageResult,
)

MIME_TYPE_TO_EXTENSION = {
    "image/png": "png",
    "image/jpeg": "jpg",
}


class LocalStorageProviderError(StorageProviderError):
    """Raised when saving to local disk fails."""


class LocalStorageProvider(StorageProvider):
    def __init__(self):
        # Where files physically live on disk
        self.base_dir = os.getenv("STORAGE_BASE_DIR", "./generated-images")
        # How that same folder is exposed as a URL clients can hit -
        # e.g. FastAPI serving this folder as static files
        self.base_url = os.getenv(
            "STORAGE_BASE_URL", "http://localhost:8000/static/generated-images"
        )

    def save_image(
        self, job_id: str, image_bytes: bytes, mime_type: str
    ) -> StorageResult:
        extension = MIME_TYPE_TO_EXTENSION.get(mime_type, "png")

        # Matches the folder pattern decided all the way back in
        # Step 2: generated-images/job_123/image.png
        job_folder = os.path.join(self.base_dir, job_id)

        try:
            os.makedirs(job_folder, exist_ok=True)
            file_path = os.path.join(job_folder, f"image.{extension}")
            with open(file_path, "wb") as f:
                f.write(image_bytes)
        except OSError as exc:
            raise LocalStorageProviderError(f"Failed to save image: {exc}") from exc

        storage_key = f"{job_id}/image.{extension}"
        image_url = f"{self.base_url}/{storage_key}"

        return StorageResult(storage_key=storage_key, image_url=image_url)