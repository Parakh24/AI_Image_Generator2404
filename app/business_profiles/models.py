# app/business_profiles/models/business_profile.py

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from app.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(String(50), primary_key=True, default=generate_uuid)

    brand_name = Column(String(255), nullable=False)
    brand_colours = Column(JSON, nullable=False)
    target_audience = Column(String(500), nullable=False)
    tone = Column(String(255), nullable=False)
    industry = Column(String(255), nullable=False)

    address = Column(String(500), nullable=True)
    contact_email = Column(String(255), nullable=True)
    owner_name = Column(String(255), nullable=True)
    gst_number = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)