"""Data schemas used while building a provider-ready image prompt."""

from enum import Enum 
from typing import Optional 
from pydantic import BaseModel 


class PromptPreset(str, Enum): 
    """List the supported visual-style presets for image requests."""
    SOCIAL_MEDIA_AD = "social_media_ad"
    PRODUCT_SHOWCASE = "product_showcase"
    PROMOTIONAL_BANNER = "promotional_banner"
    GENERIC = "generic" 


class BusinessProfile(BaseModel): 
    """Hold the brand details that may be added to an image prompt."""
    brand_name: str 
    primary_color: Optional[str] = None 
    secondary_color: Optional[str] = None 
    audience_demographics: Optional[str] = None 
    tone: Optional[str] = None 
    default_category: Optional[str] = None


class PromptRequest(BaseModel):
    """Bundle the user's text, brand details, and selected preset."""
    user_prompt: str
    business_profile: BusinessProfile
    preset: PromptPreset = PromptPreset.GENERIC
        


