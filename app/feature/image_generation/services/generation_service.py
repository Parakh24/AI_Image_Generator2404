"""
generation_service.py

Coordinator between the API and the job queue.

RULE: this file NEVER calls the image provider directly. Its job
ends the moment a job_id is queued - actually generating the image
is the worker's responsibility, not the service's.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.feature.image_generation.models.generation_job import GenerationJob
from app.feature.image_generation.services.queue_client import enqueue_generation_job
from app.feature.image_generation.repositories.generation_jobs import GenerationJobRepository
from app.feature.image_generation.repositories.image_assets import ImageAssetRepository


class GenerationService:
    def __init__(self, db: Session):
        self.job_repo = GenerationJobRepository(db)
        self.asset_repo = ImageAssetRepository(db)

    def create_generation(
        self, user_id: str, prompt: str, aspect_ratio: str
    ) -> GenerationJob:
        """
        Basic flow:
          1. Create the job row in the database (status PENDING -
             this project's "queued" state)
          2. Send the job_id to the queue so a worker can pick it up
          3. Return the job immediately - the API responds to the
             client without waiting for the image to actually exist

        This function never imports or calls the image provider -
        it stops right after the job_id is queued.
        """
        job = self.job_repo.create_job(
            user_id=user_id, prompt=prompt, aspect_ratio=aspect_ratio
        )
        enqueue_generation_job(job.id)
        return job

    def get_job_for_user(self, job_id: str, user_id: str) -> Optional[GenerationJob]:
        """
        Fetches a job, but only returns it if it belongs to user_id -
        otherwise treats it exactly like the job doesn't exist.
        """
        job = self.job_repo.get_job_by_id(job_id)
        if job is None or job.user_id != user_id:
            return None
        return job

    def get_image_url_for_job(self, job_id: str) -> Optional[str]:
        """Returns the generated image's URL, if one exists yet."""
        asset = self.asset_repo.get_asset_by_job_id(job_id)
        return asset.image_url if asset else None