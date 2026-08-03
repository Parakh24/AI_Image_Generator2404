class TemporaryGenerationError(Exception):
    """Network timeout, GPU busy, provider 5xx — retry karne layak"""

class PermanentGenerationError(Exception):
    """Invalid prompt, safety filter block, missing LoRA file — retry se fayda nahi"""