"""Service layer for business-profile creation and lookup."""

from app.database import SessionLocal
from app.business_profiles.repository import BusinessProfileRepository
from app.business_profiles.schemas import BusinessProfileCreate, BusinessProfileRead


class BusinessProfileService:
    """Coordinate profile operations using a new database session per call.

    Managing sessions here lets HTTP routes and background workers share this
    service without requiring a FastAPI request-scoped dependency.
    """

    def get_profile(self, profile_id: str) -> BusinessProfileRead | None:
        """Return one profile as an API schema, or ``None`` if it is not found."""
        db = SessionLocal()
        try:
            repository = BusinessProfileRepository(db)
            profile = repository.get_by_id(profile_id)
            if profile is None:
                return None
            return BusinessProfileRead.from_orm(profile)
        finally:
            db.close()

    def get_latest_profile(self) -> BusinessProfileRead | None:
        """Return the newest profile for internal image-generation use."""
        db = SessionLocal()
        try:
            profile = BusinessProfileRepository(db).get_latest()
            if profile is None:
                return None
            return BusinessProfileRead.from_orm(profile)
        finally:
            db.close()

    def create_profile(self, data: BusinessProfileCreate) -> BusinessProfileRead:
        """Save validated profile data and return the newly created profile."""
        db = SessionLocal()
        try:
            repository = BusinessProfileRepository(db)
            profile = repository.create(data)
            return BusinessProfileRead.from_orm(profile)
        finally:
            db.close()


business_profile_service = BusinessProfileService()
