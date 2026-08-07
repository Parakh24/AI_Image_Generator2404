"""Build the provider prompt and negative prompt for a queued job."""

DEFAULT_NEGATIVE_PROMPT = "blurry, low quality, bad anatomy, disfigured, poorly drawn, deformed," \
                          "extra limbs, cloned face, skinny, glitchy, double torso, extra arms, " \
                          "extra hands, mangled fingers, missing lips, ugly face, distorted face, " \
                          "text, error, extra digit, cropped"


def build_prompt(job):
    """Return the positive and negative prompts used to process a job."""
    parts = []

    lora_trigger = getattr(job, "lora_trigger_word", None)
    if lora_trigger:
        parts.append(lora_trigger)

    parts.append(job.prompt)   

    style_tags = getattr(job, "style_tags", None)
    if style_tags:
        parts.append(style_tags)

    final_prompt = ", ".join(parts)

    negative_prompt = getattr(job, "negative_prompt", None) or DEFAULT_NEGATIVE_PROMPT

    return final_prompt, negative_prompt
