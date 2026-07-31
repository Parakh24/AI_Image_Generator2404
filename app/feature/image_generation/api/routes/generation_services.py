"""
generation_service.py

Minimal service layer for image generation. This will grow once the
worker and providers exist (later steps) - right now it only does
two things: create a job record, and fetch a job while enforcing
that it belongs to the requesting user.
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.feature.image_generation.models.generation_job import GenerationJob 
from app.feature.image_generation.repositories.generation_jobs import GenerationJobRepository 
from app.feature.image_generation.repositories.image_assets import ImageAssetRepository


class GenerationService:
    def __init__(self, db: Session):
        self.job_repo = GenerationJobRepository(db)
        self.asset_repo = ImageAssetRepository(db)

    def start_generation(
        self, user_id: str, prompt: str, aspect_ratio: str
    ) -> GenerationJob:
        """
        Creates a new job record with status PENDING. This does NOT
        generate the image - it only creates the row that a background
        worker will later pick up and process.
        """
        return self.job_repo.create_job(
            user_id=user_id, prompt=prompt, aspect_ratio=aspect_ratio
        )

    def get_job_for_user(self, job_id: str, user_id: str) -> Optional[GenerationJob]:
        """
        Fetches a job, but ONLY returns it if it belongs to user_id.

        If the job exists but belongs to someone else, this returns
        None - exactly the same as if the job didn't exist at all.
        The route layer turns None into a 404, so User A can never
        tell the difference between "no such job" and "that's not
        your job".
        """
        job = self.job_repo.get_job_by_id(job_id)
        if job is None or job.user_id != user_id:
            return None
        return job

    def get_image_url_for_job(self, job_id: str) -> Optional[str]:
        """Returns the generated image's URL, if one exists yet."""
        asset = self.asset_repo.get_asset_by_job_id(job_id)
        return asset.image_url if asset else None