# app/business_profiles/service.py

from app.database import SessionLocal
from app.business_profiles.repository import BusinessProfileRepository
from app.business_profiles.schemas import BusinessProfileCreate, BusinessProfileRead


class BusinessProfileService:
    """
    Public interface — routes aur worker dono isi ko call karenge.
    Har call apna khud ka DB session kholta aur band karta hai (Depends(get_db)
    use nahi kiya), kyunki worker ke paas FastAPI ka request-scoped session
    available nahi hota.
    """

    def get_profile(self, profile_id: str) -> BusinessProfileRead | None:
        db = SessionLocal()
        try:
            repository = BusinessProfileRepository(db)
            profile = repository.get_by_id(profile_id)
            if profile is None:
                return None
            return BusinessProfileRead.from_orm(profile)
        finally:
            db.close()

    def create_profile(self, data: BusinessProfileCreate) -> BusinessProfileRead:
        db = SessionLocal()
        try:
            repository = BusinessProfileRepository(db)
            profile = repository.create(data)
            return BusinessProfileRead.from_orm(profile)
        finally:
            db.close()


business_profile_service = BusinessProfileService()