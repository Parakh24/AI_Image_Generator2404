

DEFAULT_NEGATIVE_PROMPT = "blurry, low quality, bad anatomy, disfigured, poorly drawn, deformed," \
                          "extra limbs, cloned face, skinny, glitchy, double torso, extra arms, " \
                          "extra hands, mangled fingers, missing lips, ugly face, distorted face, " \
                          "text, error, extra digit, cropped" 


def build_prompt(job):
    """
    Builds the final prompt and negative prompt for the image generation job. 
    """
    parts = []

    if job.lora_trigger_word:
        parts.append(job.lora_trigger_word)

    parts.append(job.user_prompt)

    if job.style_tags:
        parts.append(job.style_tags)

    final_prompt = ", ".join(parts)
    negative_prompt = job.negative_prompt or DEFAULT_NEGATIVE_PROMPT

    return final_prompt, negative_prompt