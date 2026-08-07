"""Configure SQLAlchemy and provide database sessions for the application.

The database stores job status and image metadata. Generated image bytes are
saved by a storage provider instead of being placed directly in the database.
"""


import enum 
import uuid 
from datetime import datetime 
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

#-----------------------------------------------------------------------
# Connection setup 
#-----------------------------------------------------------------------

DATABASE_URL = "sqlite:///./crmjio_image_gen.db"
engine = create_engine(DATABASE_URL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 


def get_db():
    """Provide a database session for one request and close it afterward."""

    db = SessionLocal() 
    try: 
        yield db 

    finally: 
        db.close() 


def init_db():
    """
    Creates all registered tables in the database.
 
    Models are imported here, inside the function, so Base.metadata knows
    about them before create_all runs - importing at the top of this file
    would cause a circular import, since the model files import Base
    from this same file.
 
    Adjust these paths if your model files live somewhere else.
    """
    from app.feature.image_generation.models.generation_job import GenerationJob  # noqa: F401
    from app.feature.image_generation.models.image_asset import ImageAsset  # noqa: F401
    from app.business_profiles.models import BusinessProfile
    Base.metadata.create_all(bind=engine)
