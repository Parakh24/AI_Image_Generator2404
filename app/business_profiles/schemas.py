# app/business_profiles/schemas.py

from typing import List, Optional
from pydantic import BaseModel


class BusinessProfileCreate(BaseModel):
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
    id: str

    class Config:
        from_attributes = True