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
    """
    Return current time when the image is generated
    """
    return datetime.now(timezone.utc) 


class GenerationJob(Base): 
    """
    database table that tracks one image generation request. 
    this receives the request from the frontend and creates a 
    table like structure which stores the properties of an image. 
    """

    __tablename__ = "generation_jobs" 

    id = Column(String(50), primary_key=True, default=generate_job_id)
    user_id=Column(String(50), nullable=False, index=True) 
    prompt=Column(Text, nullable=False)