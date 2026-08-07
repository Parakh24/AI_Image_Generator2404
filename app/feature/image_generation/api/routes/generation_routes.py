"""
generation_routes.py

The two routes for image generation:
  POST /api/image-generations        -> create a job
  GET  /api/image-generations/{job_id} -> check a job's status
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.authentication.deps import get_current_user
from app.database import get_db
from app.business_profiles.service import business_profile_service
from app.feature.image_generation.models.generation_job import GenerationStatus
from app.feature.image_generation.api.schemas.generation_request import GenerationCreateRequest
from app.feature.image_generation.api.schemas.generation_response import GenerationResponse
from app.feature.image_generation.api.routes.generation_services import GenerationService
from app.feature.image_generation.services.prompt_service import (
    BusinessProfile,
    PromptRequest,
    prompt_service,
)


router = APIRouter(prefix="/api/image-generations", tags=["image-generations"])


@router.post("", status_code=status.HTTP_202_ACCEPTED, response_model=GenerationResponse)
def create_image_generation(
    request: GenerationCreateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GenerationResponse:
    
    user_id = current_user.get("user_id") or current_user.get("sub") or "default_user"
    
    # 👈 Check for multiple common claim names OR fallback to a test tenant ID
    tenant_id = (
        current_user.get("tenant_id") 
        or current_user.get("tenantId") 
        or current_user.get("org_id") 
        or "test_tenant_123"  # 👈 Temporary testing fallback
    )

    # Ab exception raise nahi hoga!
    service = GenerationService(db)
    created_profile = business_profile_service.create_profile(request.business_profile)
    
    prompt_request = PromptRequest(
        user_prompt=request.prompt,
        business_profile=BusinessProfile(brand_name="your brand"),
        preset=request.preset,
    )
    final_prompt = prompt_service.compile(prompt_request)

    job = service.start_generation(
        user_id=user_id,
        profile_id=created_profile.id,
        tenant_id=tenant_id,
        prompt=final_prompt,
        aspect_ratio=request.aspect_ratio,
    )
    return GenerationResponse(job_id=job.id, status=job.status)


@router.get("/{job_id}", response_model=GenerationResponse)
def get_image_generation_status(
    job_id: str,
    current_user: dict = Depends(get_current_user),  # Gets authenticated user details
    db: Session = Depends(get_db),
) -> GenerationResponse:
    """
    Checks the status of an existing job.

    Security rule: A job is only ever returned if it matches BOTH the 
    user_id AND the tenant_id of the requester.
    """
    user_id = current_user.get("id")
    tenant_id = current_user.get("tenant_id")

    service = GenerationService(db)
    
    # Check both user_id and tenant_id to enforce multi-tenant isolation
    job = service.get_job_for_user_and_tenant(
        job_id=job_id, 
        user_id=user_id, 
        tenant_id=tenant_id
    )

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    image_url = None
    if job.status == GenerationStatus.COMPLETED:
        image_url = service.get_image_url_for_job(job_id)

    return GenerationResponse(
        job_id=job.id,
        status=job.status,
        image_url=image_url,
        error=job.error_message,
    )
