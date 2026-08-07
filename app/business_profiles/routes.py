"""HTTP endpoint for submitting and saving a business-profile form."""

from fastapi import APIRouter
from app.business_profiles.schemas import BusinessProfileCreate, BusinessProfileRead
from app.business_profiles.service import business_profile_service

router = APIRouter(prefix="/business-profiles", tags=["business-profiles"])


@router.post("/", response_model=BusinessProfileRead)
def create_business_profile(data: BusinessProfileCreate):
    """Validate the submitted form, save it, and return the new profile."""
    return business_profile_service.create_profile(data)
