"""
generation_routes.py

The two routes for image generation:
  POST /api/image-generations          -> create a job
  GET  /api/image-generations/{job_id} -> check a job's status
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.feature.image_generation.api.routes.dependencies import get_current_user_id
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
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> GenerationResponse:
    """
    Creates a new image generation job. Does NOT generate the image
    itself - that happens later, in a background worker.

    Steps:
    1. get_current_user_id identifies who is making the request
    2. GenerationCreateRequest schema has already validated the body
       (prompt not blank, aspect_ratio is one of the allowed values)
       before this function even runs
    3. GenerationService.start_generation() creates and queues the job
    4. The job id and status are returned immediately

    202 Accepted (not 200 OK) means "request accepted, processing
    not finished yet" - which is exactly what's true here.
    """
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
        prompt=final_prompt,
        aspect_ratio=request.aspect_ratio,
    )
    return GenerationResponse(job_id=job.id, status=job.status)


@router.get("/{job_id}", response_model=GenerationResponse)
def get_image_generation_status(
    job_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> GenerationResponse:
    """
    Checks the status of an existing job.

    Security rule: a job is only ever returned to the user who
    created it. If the job doesn't exist, or it belongs to a
    different user, this returns the exact same 404 - never 403.
    """
    service = GenerationService(db)
    job = service.get_job_for_user(job_id=job_id, user_id=user_id)

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
