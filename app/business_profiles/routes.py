# app/business_profiles/routes.py

from fastapi import APIRouter
from app.business_profiles.schemas import BusinessProfileCreate, BusinessProfileRead
from app.business_profiles.service import business_profile_service

router = APIRouter(prefix="/business-profiles", tags=["business-profiles"])


@router.post("/", response_model=BusinessProfileRead)
def create_business_profile(data: BusinessProfileCreate):
    return business_profile_service.create_profile(data)
