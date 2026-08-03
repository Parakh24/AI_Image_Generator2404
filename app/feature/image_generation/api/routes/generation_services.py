"""Compatibility import for the canonical generation service."""

from app.feature.image_generation.services.generation_service import GenerationService
"""
generation_service.py

Service layer for image generation. Creates a job record, enqueues it
for background processing, and fetches job status while enforcing
that a job belongs to the requesting user.
"""

from typing import Optional
from sqlalchemy.orm import Session
from rq import Retry
from app.feature.image_generation.models.generation_job import GenerationJob
from app.feature.image_generation.repositories.generation_jobs import GenerationJobRepository
from app.feature.image_generation.repositories.image_assets import ImageAssetRepository
from app.feature.image_generation.services.queue_client import generation_queue  # <- apna actual path confirm kar lena, jahan Queue() bana hai


class GenerationService:
    def __init__(self, db: Session):
        self.db = db
        self.job_repo = GenerationJobRepository(db)
        self.asset_repo = ImageAssetRepository(db)

    def start_generation(
        self, user_id: str, prompt: str, aspect_ratio: str
    ) -> GenerationJob:
        """
        Creates a new job record with status PENDING, saves it,
        and enqueues it for the background worker to pick up.
        """
        job = self.job_repo.create_job(
            user_id=user_id, prompt=prompt, aspect_ratio=aspect_ratio
        )
        self.db.commit()

        generation_queue.enqueue(
            "generation_worker.tasks.process_generation_job",
            job.id,
            retry=Retry(max=3, interval=[10, 30, 90]),
        )

        return job

    def get_job_for_user(self, job_id: str, user_id: str) -> Optional[GenerationJob]:
        """
        Fetches a job, but ONLY returns it if it belongs to user_id.
        """
        job = self.job_repo.get_job_by_id(job_id)
        if job is None or job.user_id != user_id:
            return None
        return job

    def get_image_url_for_job(self, job_id: str) -> Optional[str]:
        """Returns the generated image's URL, if one exists yet."""
        asset = self.asset_repo.get_asset_by_job_id(job_id)
        return asset.image_url if asset else None



__all__ = ["GenerationService"]
