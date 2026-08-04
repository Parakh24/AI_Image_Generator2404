from app.feature.image_generation.services.prompt_service.presets import PRESET_STYLE_WORDS
from app.feature.image_generation.services.prompt_service.schemas import PromptPreset , BusinessProfile

_LEADING_VERBS = ("create" , "generate" , "make" , "design" , "produce" , "build" , "develop" , "assemble")



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

    sentences = [f"Create a {style_word} {subject} for {business_profile.brand_name}."]

    if business_profile.primary_color: 
        sentences.append(f"Use the primary color {business_profile.primary_colour} as the primary colour")

    if business_profile.secondary_colour:
        sentences.append(f"Use the secondary colour {business_profile.secondary_colour} as the accent colour")

    if business_profile.audience:
        sentences.append(f"Target the following audience: {business_profile.audience}")

    if business_profile.tone:
        sentences.append(f"The overall tone should feel {business_profile.tone}.")

    return " ".join(sentences) 
                                         
    