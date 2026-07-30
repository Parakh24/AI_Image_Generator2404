"""
database.py 

It defines two things: 

1. Database connection setup 
2. Defines 2 modules: GenerationJob and Image asset

design decisions: 

- GenerationJob= the "state tracker" for a request. It tracks whcih stage a job is in. 
- ImageAsset = the record of the actual generated output. the image binary is not stored 
  here - only the storage_key (path) and metadata are stored. Storing binary blobs in the 
  db slows down backups, replication and query performance. 
- Sequence - the image_asset row is created FIRST, and only then is the generation_job status
  set to be completed 
"""


import enum 
import uuid 
from datetime import datetime 
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

#-----------------------------------------------------------------------
# Connection setup 
#-----------------------------------------------------------------------

DATABASE_URL = ""
engine = create_engine(DATABASE_URL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 


def get_db():
    """
    FastAPI dependency - yields a DB session, closes it after the request
    """

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
    Base.metadata.create_all(bind=engine)