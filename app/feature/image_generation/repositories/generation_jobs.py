"""
Repository layer for GenerationJob. 

this file only talks to the database - insert , fetch , update.
It never decides "whether" something should happen - it just does what 
its told and reports back what's actually in the database. 
"""

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
        # session just uses the repository, does not create the repository
        self.db = db 



      def create_job(
              self, user_id: str, profile_id: str, prompt: str, aspect_ratio:str = "1:1"
      ) -> GenerationJob: 
        """
          Inserts new row with "PENDING" status. When the user submits the prompt, 
          this function gets called before the image generation starts.
        """
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
        """
         This function fetches one of the job ids to check whether the tables
         exist on the database server or not. If not, then service decides whether 
         to send an error or to retry it.
        """

        return self.db.query(GenerationJob).filter(GenerationJob.id == job_id).first() 



      def update_job_status(
            self, job_id: str, status: GenerationStatus
      ) -> Optional[GenerationJob]: 
         """
         Generic status change -> like "PENDING" -> "PROCESSING" only when worker picks up the job 
         """
         job = self.get_job_bby_id(job_id) 

         if job is None: 
            return None 

         job.status = status 
         self.db.commit() 
         self.db.refresh(job) 
         return job 



      def mark_job_completed(self, job_id: str) -> Optional[GenerationJob]: 
         """
         It sets the job as completed. Call this only when the image asset row is created. 
         """
         job = self.get_job_by_id(job_id) 
         if job is None: 
            return None 

         job.status = GenerationStatus.COMPLETED 
         job.completed_at = datetime.now(timezone.utc) 
         self.db.commit() 
         self.db.refresh(job) 
         return job 



      def mark_job_failed(self, job_id: str, error_message: str) -> Optional[GenerationJob]:
         """
         It sets the job as FAILED and records the reason behind this
         """
         job = self.get_job_by_id(job_id) 

         if job is None: 
            return None 

         job.status = GenerationStatus.FAILED 
         job.error_message = error_message
         job.completed_at = datetime.now(timezone.utc) 
         self.db.commit() 
         self.db.refresh(job) 
         return job
