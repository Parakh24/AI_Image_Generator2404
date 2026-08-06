# app/business_profiles/models/business_profile.py

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from app.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(String, primary_key=True, default=generate_uuid)

    brand_name = Column(String, nullable=False)
    brand_colours = Column(JSON, nullable=False)
    target_audience = Column(String, nullable=False)
    tone = Column(String, nullable=False)
    industry = Column(String, nullable=False)

    address = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    owner_name = Column(String, nullable=True)
    gst_number = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)