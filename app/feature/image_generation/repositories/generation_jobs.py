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
              self, user_id: str, prompt: str, aspect_ratio:str = "1:1"
      ) -> GenerationJob: 
        """
          Inserts new row with "PENDING" status. When the user submits the prompt, 
          this function gets called before the image generation starts.
        """
        job = GenerationJob(user_id=user_id, prompt=prompt, aspect_ratio=aspect_ratio)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)  # DB-generated fields (id, created_at) wapas le aata hai
        return job 


      
