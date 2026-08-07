"""Database model for metadata about generated image files."""

import uuid  
from datetime import datetime , timezone 
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey 
from app.database import Base 


def generate_asset_id(): 
    """
    Create a unique asset id like 'asset_<random_hex>'
    """
    return "asset" + uuid.uuid4().hex 


def get_current_time(): 
    """
    Return current time when the asset record is created
    """
    return datetime.now(timezone.utc) 


class ImageAsset(Base):
    """
    Database table that stores one generated image linked to a generation job. 
    A single job can produce multiple images, each stored as its own row here.
    """

    __tablename__ = "image_assets"

    id = Column(String(50), primary_key=True, default=generate_asset_id)
    job_id = Column(String(50), ForeignKey("generation_jobs.id"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    seed = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_current_time, nullable=False)
