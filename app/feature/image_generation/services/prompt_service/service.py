"""
Provide a simple service interface for compiling image-generation prompts.

API routes can use this service without needing to know the individual prompt-
building rules.
"""

from app.feature.image_generation.services.prompt_service.builder import build_final_prompt
from app.feature.image_generation.services.prompt_service.schemas import PromptRequest


class PromptService: 
    """Expose prompt building through one reusable service method."""

    def compile(self, request: PromptRequest) -> str: 
        """Convert a validated prompt request into the final provider prompt."""
        return build_final_prompt(
                user_prompt=request.user_prompt,
                business_profile=request.business_profile,
                preset= request.preset,
        )


prompt_service = PromptService() 
