"""
Defines the contract every image provider adapter must follow.

RULE: generation_service and the worker depend only on this interface, never on a specific provider's SDK, request format, 
      or response format. This is what lets us swap out providers without changing the service or worker code.
"""

from abc import ABC, abstractmethod 
from dataclasses import dataclass 



@dataclass 
class ImageGenerationResult: 
    """
    Standardized result shape returned by EVERY provider adapter, 
    no matter which actual service generated the image underneath.
    """

    image_bytes: bytes
    mime_type: str
    width: int
    height: int
    provider_request_id: str


class ImageProviderError(Exception):
    """Base error raised by image provider adapters."""


class ImageProvider(ABC): 
    """
    Interface every image provider adapter must implement. 
    generation_service and the worker onle ever call generate_image() on this interface, they never know or they care 
    whether the actual call goes to Forge, Replicate, or anything else. 
    """

    @abstractmethod
    def generate_image(
        self, prompt: str, negative_prompt: str, aspect_ratio: str
    ) -> ImageGenerationResult:
        """
        Generates one image and returns it in the standardized shape
        """
        raise NotImplementedError
