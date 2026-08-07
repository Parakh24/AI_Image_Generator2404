"""Request and response schemas used by the business-profile API."""

from typing import List, Optional
from pydantic import BaseModel


class BusinessProfileCreate(BaseModel):
    """Describe the fields accepted when a business profile is created."""
    brand_name: str
    brand_colours: List[str]
    target_audience: str
    tone: str
    industry: str
    address: Optional[str] = None
    contact_email: Optional[str] = None
    owner_name: Optional[str] = None
    gst_number: Optional[str] = None


class BusinessProfileRead(BusinessProfileCreate):
    """Describe a saved business profile, including its generated ID."""
    id: str

    class Config:
        """Allow Pydantic to build this schema from SQLAlchemy models."""
        from_attributes = True
