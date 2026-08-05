"""
forge-image-provider.py 

Concrete adapter for Stable Diffusion Forge's API. 
RULE: everything specific to FORGE's API lives here - request format, base URL, timeouts, response parsing, error handling. Nothing outside 
      this file should know or care about Forge's API. If forge changes its API tomorrow, we only change this file. 
""" 

import base64 
import os
import uuid 
import requests
from app.feature.image_generation.providers.image_provider.image_base import (
     ImageGenerationResult, 
     ImageProvider, 
     ImageProviderError, 
)


# Forge does not take aaspect ratios directly - it needs actual pixel 
# dimensions, so this adapter maps between the two. This mapping is 
# Forge-specific and stays in this file. If we switch to a different provider, we will need a different mapping.

ASPECT_RATIO_TO_DIMENSIONS = {
    "1:1" : (512, 512),
    "16:9" : (1024, 576),
    "9:16" : (576, 1024),
}


class ForgeImageProviderError(ImageProviderError):
    """Raised when Forge's API returns an error response or when the request fails due to network issues."""


class ForgeImageProvider(ImageProvider):

    def __init__(self):
        self.base_url = os.getenv("FORGE_API_BASE_URL", "http://127.0.0.1:7860")
        self.timeout_seconds = int(os.getenv("FORGE_TIMEOUT_SECONDS", "120"))

    def generate_image(
        self, prompt: str, negative_prompt: str, aspect_ratio: str
    ) -> ImageGenerationResult:
        width, height = ASPECT_RATIO_TO_DIMENSIONS.get(aspect_ratio, (512, 512)) 
        request_id = f"forge_{uuid.uuid4().hex[:10]}"


        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width, 
            "height": height,
            "steps": 25,
            "sampler_name": "DPM++ 2M Karras",
        }

        try:
            response = requests.post(
                f"{self.base_url}/sdapi/v1/txt2img",
                json=payload,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise ForgeImageProviderError(
                f"Forge timed out after {self.timeout_seconds}s"
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise ForgeImageProviderError(f"Forge request failed: {exc}") from exc
 
        data = response.json()
        images = data.get("images")
        if not images:
            raise ForgeImageProviderError("Forge returned no image data")
 
        # Forge returns images as base64 strings - decode to raw bytes
        # so the rest of the app always works with plain bytes,
        # regardless of what encoding a given provider happens to use.
        image_bytes = base64.b64decode(images[0])
 
        return ImageGenerationResult(
            image_bytes=image_bytes,
            mime_type="image/png",
            width=width,
            height=height,
            provider_request_id=request_id,
        )

