"""Database model and status values for image-generation jobs."""

import enum 
import uuid 
import sqlalchemy 
from datetime import datetime, timezone 
from sqlalchemy import Column, String, Text, DateTime, Enum 
from app.database import Base 


class GenerationStatus(str , enum.Enum):
    """
    Possible states of a generation job.
    """

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED" 
    FAILED = "FAILED" 

def generate_job_id():
    """
    Create a unique job id like 'job_<random_hex>'.
    """
    return "job_" + uuid.uuid4().hex
    

def get_current_time(): 
    """Return the current UTC time for job timestamps."""
    return datetime.now(timezone.utc) 


class GenerationJob(Base): 
    """Represent one image request and track its processing state."""

    __tablename__ = "generation_jobs" 

    id = Column(String(50), primary_key=True, default=generate_job_id)
    user_id = Column(String(50), nullable=False, index=True)
    profile_id = Column(String(50), nullable=False)
    prompt = Column(Text, nullable=False)
    aspect_ratio = Column(String(10), nullable=False, default="1:1")
    status = Column(Enum(GenerationStatus), nullable=False, default=GenerationStatus.PENDING, index=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_current_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=get_current_time, onupdate=get_current_time, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
