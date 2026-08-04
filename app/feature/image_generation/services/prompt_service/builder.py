"""Build the final image-generation prompt from request and business data."""

from app.feature.image_generation.services.prompt_service.categorizer import detect_category
from app.feature.image_generation.services.prompt_service.categories import CATEGORY_STYLE_BOOST
from app.feature.image_generation.services.prompt_service.presets import PRESET_STYLE_WORDS
from app.feature.image_generation.services.prompt_service.schemas import (
    BusinessProfile,
    PromptPreset,
)


_LEADING_VERBS = (
    "create",
    "generate",
    "make",
    "design",
    "produce",
    "build",
    "develop",
    "assemble",
)


def _normalize_user_prompt(user_prompt: str) -> str:
    """Trim the prompt and remove a redundant leading creation instruction."""
    text = user_prompt.strip()
    lowered = text.casefold()

    for verb in _LEADING_VERBS:
        for suffix in (" an ", " a ", " "):
            prefix = f"{verb}{suffix}"
            if lowered.startswith(prefix):
                return text[len(prefix):].strip()

    return text


def _indefinite_article(phrase: str) -> str:
    """Choose the appropriate article for the configured style phrase."""
    return "an" if phrase.lstrip().casefold().startswith(("a", "e", "i", "o", "u")) else "a"


def build_final_prompt(
    user_prompt: str,
    business_profile: BusinessProfile,
    preset: PromptPreset,
) -> str:
    """Compile a user prompt, preset, and business profile into one prompt."""
    style = PRESET_STYLE_WORDS.get(
        preset,
        PRESET_STYLE_WORDS[PromptPreset.GENERIC],
    )
    subject = _normalize_user_prompt(user_prompt)
    article = _indefinite_article(style)

    sentences = [
        f"Create {article} {style} {subject} for {business_profile.brand_name}."
    ]

    if business_profile.primary_color:
        sentences.append(
            f"Use {business_profile.primary_color} as the primary color."
        )

    if business_profile.secondary_color:
        sentences.append(
            f"Use {business_profile.secondary_color} as the accent color."
        )

    if business_profile.audience_demographics:
        sentences.append(
            f"Target the following audience: {business_profile.audience_demographics}."
        )

    if business_profile.tone:
        sentences.append(f"The overall tone should feel {business_profile.tone}.")

    category = detect_category(user_prompt, business_profile)
    style_boost = CATEGORY_STYLE_BOOST.get(category) if category else None
    if style_boost:
        sentences.append(f"Include: {style_boost}.")

    return " ".join(sentences)
