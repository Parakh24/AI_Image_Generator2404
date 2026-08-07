"""Map each prompt preset to descriptive style words for the final prompt."""

from app.feature.image_generation.services.prompt_service.schemas import PromptPreset 


PRESET_STYLE_WORDS: dict[PromptPreset, str] = {
    PromptPreset.SOCIAL_MEDIA_AD: "modern",
    PromptPreset.PRODUCT_SHOWCASE: "clean, professional",
    PromptPreset.PROMOTIONAL_BANNER: "eye-catching, bold",
    PromptPreset.GENERIC: "high quality, visually appealing",
}

