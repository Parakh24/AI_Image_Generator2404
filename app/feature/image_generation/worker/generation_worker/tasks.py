"""RQ task entry points for image generation."""

from importlib import import_module

from app.feature.image_generation.providers.storage_provider.local_storage_provider import (
    LocalStorageProvider,
)

from .pipeline import GenerationPipeline


def process_generation_job(job_id: str) -> None:
    """Build the configured providers and process one queued job."""
    # The existing Forge adapter has a legacy hyphenated filename, so it cannot
    # be referenced by a normal ``from ... import`` statement.
    forge_module = import_module(
        "app.feature.image_generation.providers.image_provider.Forge-Image-Provider"
    )
    pipeline = GenerationPipeline(
        job_id=job_id,
        image_provider=forge_module.ForgeImageProvider(),
        storage_provider=LocalStorageProvider(),
    )
    pipeline.run()
