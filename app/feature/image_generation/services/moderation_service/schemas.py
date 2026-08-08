from enum import Enum 
from pydantic import BaseModel 


class ModerationReason(str, Enum): 
    EMPTY_PROMPT = "empty_prompt" 
    PROMPT_TOO_LONG = "prompt_too_long"
    BLOCKED_CATEGORY = "blocked_category"
    PROVIDER_REJECTED = "provider_rejected"


class ModerationResult(BaseModel):
    is_allowed: bool
    reason: ModerationReason | None = None 
    detail: str | None = None
