"""Database operations for creating and finding business profiles."""

from sqlalchemy.orm import Session
from app.business_profiles.models import BusinessProfile
from app.business_profiles.schemas import BusinessProfileCreate


class BusinessProfileRepository:
    """Provide a small database-access layer for business profiles."""

    def __init__(self, db: Session):
        """Store the SQLAlchemy session used by repository operations."""
        self.db = db

    def create(self, data: BusinessProfileCreate) -> BusinessProfile:
        """Insert a business profile and return the saved database model."""
        profile = BusinessProfile(**data.dict())
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_by_id(self, profile_id: str) -> BusinessProfile | None:
        """Return the profile with the given ID, or ``None`` if it is absent."""
        return self.db.query(BusinessProfile).filter(BusinessProfile.id == profile_id).first()

    def get_latest(self) -> BusinessProfile | None:
        """Return the most recently created business profile, if one exists."""
        return (
            self.db.query(BusinessProfile)
            .order_by(BusinessProfile.created_at.desc(), BusinessProfile.id.desc())
            .first()
        )
