import re

from app.feature.image_generation.services.prompt_service.categories import (
    CATEGORY_KEYWORDS,
    CATEGORY_STYLE_BOOST,
)
from app.feature.image_generation.services.prompt_service.presets import PRESET_STYLE_WORDS
from app.feature.image_generation.services.prompt_service.schemas import PromptPreset , BusinessProfile
from app.feature.image_generation.services.prompt_service.categories import CATEGORY_STYLE_BOOST
from app.feature.image_generation.services.prompt_service.categorizer import detect_category



_LEADING_VERBS = ("create" , "generate" , "make" , "design" , "produce" , "build" , "develop" , "assemble")


def _detect_category(user_prompt: str, default_category: str | None = None) -> str | None:
    """Return the first category whose complete keyword occurs in the prompt."""
    normalized_prompt = user_prompt.casefold().replace("_", " ").replace("-", " ")
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(
            re.search(rf"(?<!\w){re.escape(keyword.casefold())}(?!\w)", normalized_prompt)
            for keyword in keywords
        ):
            return category

    if default_category:
        normalized_default = default_category.strip().casefold().replace("-", " ").replace("_", " ")
        for category in CATEGORY_KEYWORDS:
            if normalized_default == category.replace("_", " "):
                return category
    return None



def _normalize_user_prompt(user_prompt: str) -> str: 
    """
    User often types 'Create a' -- we remove these words from the prompt to 
    make it more concise and focused on the subject matter.
    """
    text = user_prompt.strip().lower() 
    lowered = text.lower() 
    for verb in _LEADING_VERBS:
        for article in ("a ", "an "):
            prefix = f"{verb} {article}"
            if lowered.startswith(prefix):
                return text[len(prefix):]
    return text


def build_final_prompt(
    user_prompt: str, 
    business_profile: BusinessProfile,
    preset: PromptPreset,
) -> str:  
    style_word = PRESET_STYLE_WORDS.get(preset, PRESET_STYLE_WORDS[PromptPreset.GENERIC])
    subject = _normalize_user_prompt(user_prompt)

    category = _detect_category(user_prompt, business_profile.default_category)
    category_boost = CATEGORY_STYLE_BOOST.get(category) if category else None
    if category_boost:
        style_word = f"{style_word}, {category_boost}"

    sentences = [f"Create a {style_word} {subject} for {business_profile.brand_name}."]

    if business_profile.primary_color:
        sentences.append(f"Use the primary color {business_profile.primary_color} as the primary color.")

    if business_profile.secondary_color:
        sentences.append(f"Use the secondary color {business_profile.secondary_color} as the accent color.")

    if business_profile.audience_demographics:
        sentences.append(f"Target the following audience: {business_profile.audience_demographics}.")

    if business_profile.tone:
        sentences.append(f"The overall tone should feel {business_profile.tone}.")

    # Category detection: layer 2 (prompt keywords) checked before
    # layer 1 (business default). See categorizer.py for the full logic.
    category = detect_category(user_prompt, business_profile)
    if category is not None:
        style_boost = CATEGORY_STYLE_BOOST.get(category)
        if style_boost:
            sentences.append(f"Include: {style_boost}.")

    return " ".join(sentences) 
                                         
    
