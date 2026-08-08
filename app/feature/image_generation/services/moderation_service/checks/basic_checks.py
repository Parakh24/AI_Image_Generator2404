# services/moderation_service/checks/basic_checks.py
from ..schemas import ModerationResult, ModerationReason

MAX_PROMPT_LENGTH = 500  # tune as needed


def check_basic(prompt: str) -> ModerationResult:
    stripped = prompt.strip()

    if not stripped:
        return ModerationResult(
            is_allowed=False,
            reason=ModerationReason.EMPTY_PROMPT,
            detail="Prompt cannot be empty"
        )

    if len(stripped) > MAX_PROMPT_LENGTH:
        return ModerationResult(
            is_allowed=False,
            reason=ModerationReason.PROMPT_TOO_LONG,
            detail=f"Prompt exceeds {MAX_PROMPT_LENGTH} characters"
        )

    return ModerationResult(is_allowed=True)