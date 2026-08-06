# app/business_profiles/routes.py

from fastapi import APIRouter, HTTPException
from app.business_profiles.schemas import BusinessProfileCreate, BusinessProfileRead
from app.business_profiles.service import business_profile_service

router = APIRouter(prefix="/business-profiles", tags=["business-profiles"])


@router.post("/", response_model=BusinessProfileRead)
def create_business_profile(data: BusinessProfileCreate):
    return business_profile_service.create_profile(data)


@router.get("/{profile_id}", response_model=BusinessProfileRead)
def get_business_profile(profile_id: str):
    profile = business_profile_service.get_profile(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Business profile not found")
    return profile