"""
generation_service.py

Coordinator between the API and the job queue.

RULE: this file NEVER calls the image provider directly. Its job
ends the moment a job_id is queued - actually generating the image
is the worker's responsibility, not the service's.
"""
from typing import Optional
from sqlalchemy.orm import Session
from rq import Retry
from app.feature.image_generation.models.generation_job import GenerationJob
from app.feature.image_generation.repositories.generation_jobs import GenerationJobRepository
from app.feature.image_generation.repositories.image_assets import ImageAssetRepository
from app.feature.image_generation.services.generation_service.queue_client import generation_queue  # <- apna actual path confirm kar lena, jahan Queue() bana hai


class GenerationService:
    """Coordinate job records, queue submission, and generation-result lookup."""

    def __init__(self, db: Session):
        """Create repositories that share the request's database session."""
        self.db = db
        self.job_repo = GenerationJobRepository(db)
        self.asset_repo = ImageAssetRepository(db)

    def start_generation(
        self,
        user_id: str,
        profile_id: str,
        tenant_id: str,
        prompt: str,
        aspect_ratio: str,
    ) -> GenerationJob:
        """
        Creates a new job record with status PENDING, saves it,
        and enqueues it for the background worker to pick up.
        """
        job = self.job_repo.create_job(
            user_id=user_id,
            profile_id=profile_id,
            tenant_id=tenant_id,
            prompt=prompt,
            aspect_ratio=aspect_ratio,
        )
        self.db.commit()

        generation_queue.enqueue(
            "app.feature.image_generation.worker.generation_worker.tasks.process_generation_job",
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

    def get_job_for_user_and_tenant(
        self, job_id: str, user_id: str, tenant_id: str
    ) -> Optional[GenerationJob]:
        """Return a job only when it belongs to both the user and the tenant."""
        job = self.job_repo.get_job_by_id_and_tenant(job_id, tenant_id)
        if job is None or job.user_id != user_id:
            return None
        return job

    def get_image_url_for_job(self, job_id: str) -> Optional[str]:
        """Returns the generated image's URL, if one exists yet."""
        asset = self.asset_repo.get_asset_by_job_id(job_id)
        return asset.image_url if asset else None
