"""Database operations for creating, reading, and updating generation jobs."""

from datetime import datetime, timezone 
from typing import Optional 
from sqlalchemy.orm import Session 
from app.feature.image_generation.models.generation_job import GenerationJob, GenerationStatus 


class GenerationJobRepository: 
      """
      Wraps every database operation related to the generation_jobs table.

      A service calls 'job_repository.create_job(...)' - it never writes 
      INSERT into generation_jobs. That separation is the whole point of 
      this file existing.
      """

      def __init__(self, db: Session):
        """Store the database session used for all job operations."""
        # session just uses the repository, does not create the repository
        self.db = db 



      def create_job(
              self, user_id: str, profile_id: str, prompt: str, aspect_ratio:str = "1:1"
      ) -> GenerationJob: 
        """Insert and return a new job whose initial status is ``PENDING``."""
        job = GenerationJob(
            user_id=user_id,
            profile_id=profile_id,
            prompt=prompt,
            aspect_ratio=aspect_ratio,
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)  # DB-generated fields (id, created_at) wapas le aata hai
        return job 



      def get_job_by_id(self, job_id: str) -> Optional[GenerationJob]:
        """Return the job with the given ID, or ``None`` when it does not exist."""

        return self.db.query(GenerationJob).filter(GenerationJob.id == job_id).first() 



      def update_job_status(
            self, job_id: str, status: GenerationStatus
      ) -> Optional[GenerationJob]: 
         """Set a job to the supplied status and return the updated record."""
         job = self.get_job_bby_id(job_id) 

         if job is None: 
            return None 

         job.status = status 
         self.db.commit() 
         self.db.refresh(job) 
         return job 



      def mark_job_completed(self, job_id: str) -> Optional[GenerationJob]: 
         """Mark a job completed after its image-asset record has been saved."""
         job = self.get_job_by_id(job_id) 
         if job is None: 
            return None 

         job.status = GenerationStatus.COMPLETED 
         job.completed_at = datetime.now(timezone.utc) 
         self.db.commit() 
         self.db.refresh(job) 
         return job 



      def mark_job_failed(self, job_id: str, error_message: str) -> Optional[GenerationJob]:
         """Mark a job failed and store a message explaining the failure."""
         job = self.get_job_by_id(job_id) 

         if job is None: 
            return None 

         job.status = GenerationStatus.FAILED 
         job.error_message = error_message
         job.completed_at = datetime.now(timezone.utc) 
         self.db.commit() 
         self.db.refresh(job) 
         return job
