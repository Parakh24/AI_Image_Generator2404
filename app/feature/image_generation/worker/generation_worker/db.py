"""Database-session helper used by the background worker."""

from app.database import SessionLocal 

def get_worker_session(): 
    """
    Returns a new SQLAlchemy session for the worker process. 
    This function creates a new session because the worker process runs in 
    a separate thread from the main FASTAPI app, and we want to avoid sharing sessions 
    across threads. """

    return SessionLocal()
