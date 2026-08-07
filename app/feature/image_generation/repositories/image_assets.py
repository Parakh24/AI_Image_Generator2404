"""
image_asset_repository.py

Repository layer for ImageAsset. Same rule as generation_job_repository -
only database reads/writes here, nothing else.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.feature.image_generation.models.image_asset import ImageAsset


class ImageAssetRepository:
    """Wraps every database operation related to the image_assets table."""

    def __init__(self, db: Session):
        """Store the database session used for all image-asset operations."""
        self.db = db

    def create_asset(
        self,
        job_id: str,
        image_url: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> ImageAsset:
        """
        Inserts a new row, linking a generated image to its job.
        Called once Forge has returned the image and it has been
        saved to storage - only after this step should the
        generation_job be marked COMPLETED.
        """
        asset = ImageAsset(
            job_id=job_id, image_url=image_url, width=width, height=height, seed=seed
        )
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def get_asset_by_job_id(self, job_id: str) -> Optional[ImageAsset]:
        """
        Fetches the generated image for a given job. Used when the
        client polls the job and its status is COMPLETED - this is
        how the client gets the image_url back.
        """
        return (
            self.db.query(ImageAsset)
            .filter(ImageAsset.job_id == job_id)
            .first()
        )
