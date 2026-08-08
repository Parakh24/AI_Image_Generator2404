"""
main.py

Entry point for the FastAPI application.

This is the file uvicorn points to when starting the server:
    uvicorn app.main:app --reload

Its only responsibility is to create the FastAPI app instance and
register (include) each feature's router. No business logic belongs
in this file -- that lives inside each feature's own routes/services.
"""

if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from app.feature.image_generation.api.routes.generation_routes import router as generation_router
from app.business_profiles.routes import router as business_profiles_router


app = FastAPI(title="CRMJIO Image Generation Service")

app.include_router(generation_router)
app.include_router(business_profiles_router)
