"""
Generation Pipeline 

This module defines the end-to-end workflow executed by the background worker for 
processing an image generation job. It orchestrates the following steps: 



Responsibilities: 

1. Retrieve the generation job details from the database. 
2. Prevent duplicate processing of the same job by checking if it has already been completed. 
3. Mark the job as Processing. 
4. Build the final prompt and negative prompt. 
5. Invoke the configured image to object storage. 
6. Mark the job as COMPLETED on success.

Error Handling: 
  - TemporaryGenerationError: Raised for transient issues. The job will be retried later.


  - PermanentGenerationError: Raised for unrecoverable issues. The job will be marked as failed and will not be retried. 

Designed Notes: 

  - The pipeline is executed by the background worker and is intentionally independent 
    of the HTTP request/response cycle. 

  - Database operations are performed within a worker session and are cleaned up regardless 
    of success or failure. 

  - An idempotency guard prevents duplicate image generation if the same job is delivered more than 
    once by the queue.
"""


from app.feature.image_generation.models.generation_job import GenerationStatus
from app.feature.image_generation.providers.image_provider.image_base import ImageProvider
from app.feature.image_generation.providers.storage_provider.storage_base import StorageProvider
from app.feature.image_generation.repositories.generation_jobs import GenerationJobRepository
from app.feature.image_generation.repositories.image_assets import ImageAssetRepository
from generation_worker.db import get_worker_session
from generation_worker.errors import PermanentGenerationError, TemporaryGenerationError

class GenerationPipeline:
    def __init__(
        self,
        job_id: str,
        image_provider: ImageProvider,
        storage_provider: StorageProvider,
    ):
        self.job_id = job_id
        self.image_provider = image_provider
        self.storage_provider = storage_provider

    def run(self):
        db = get_worker_session()
        job_repository = GenerationJobRepository(db)
        image_asset_repository = ImageAssetRepository(db)
        job = None

        try:
            job = job_repository.get_job_by_id(self.job_id)

            if job is None:
                raise PermanentGenerationError(
                    f"Generation job {self.job_id} was not found"
                )

            if job.status == GenerationStatus.COMPLETED:
                return  # idempotency guard

            job.status = GenerationStatus.PROCESSING
            db.commit()

            result = self.image_provider.generate_image(job.prompt, job.aspect_ratio)
            stored = self.storage_provider.save_image(
                job.id, result.image_bytes, result.mime_type
            )

            image_asset_repository.create_asset(
                job_id=job.id,
                image_url=stored.image_url,
                width=result.width,
                height=result.height,
            )
            job_repository.mark_job_completed(job.id)

        except TemporaryGenerationError as e:
            if job is not None:
                job.error_message = str(e)
                db.commit()
            raise  # RQ ko dobara try karne do

        except PermanentGenerationError as e:
            if job is not None:
                job_repository.mark_job_failed(job.id, str(e))
            # yahan raise NAHI karenge — RQ ko retry nahi karna

        finally:
            db.close()
