"""
generation_response.py

Response schema for a generation job - this shape is used to show
the client the job's status/result (in the poll endpoint).
"""

from typing import Optional

from pydantic import BaseModel

from app.feature.image_generation.models.generation_job import GenerationStatus


class GenerationResponse(BaseModel):
    """
    Sent back to the client to show a job's current state.

    image_url is only set once status is COMPLETED.
    error is only set once status is FAILED.
    In both cases the other field stays None - this lets the client
    tell what stage the job is in without any extra logic.
    """

    job_id: str
    status: GenerationStatus
    image_url: Optional[str] = None
    error: Optional[str] = None