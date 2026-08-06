# app/business_profiles/repository.py

from sqlalchemy.orm import Session
from app.business_profiles.models import BusinessProfile
from app.business_profiles.schemas import BusinessProfileCreate


class BusinessProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: BusinessProfileCreate) -> BusinessProfile:
        profile = BusinessProfile(**data.dict())
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_by_id(self, profile_id: str) -> BusinessProfile | None:
        return self.db.query(BusinessProfile).filter(BusinessProfile.id == profile_id).first()