"""
generation_request.py

Request schema for creating a new image generation job.

RULE: if validation fails here, the request never reaches the service
layer - FastAPI automatically sends back a 422 error to the client.
"""

from pydantic import BaseModel, Field, field_validator

class GenerationCreateRequest(BaseModel):
    """
    Shape the request body must have when a client submits a new
    image generation job.
    """

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="User's image generation prompt. Cannot be blank.",
    )
    @field_validator("prompt")
    @classmethod
    def prompt_must_not_be_blank(cls, value: str) -> str:
        """
        min_length=1 only checks "string isn't empty" - but "   "
        (just spaces) would pass that check since it technically has
        3 characters. This validator strips whitespace and checks
        the actual content instead.
        """
        stripped = value.strip()
        if not stripped:
            raise ValueError("prompt cannot be blank or only whitespace")
        return stripped
