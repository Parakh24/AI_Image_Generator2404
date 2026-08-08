# services/moderation_service/moderation_service.py
from .checks.basic_checks import check_basic
from .checks.blocklist_check import check_blocklist
from .providers.base import ModerationProvider
from .schemas import ModerationResult


def moderate_prompt(
    prompt: str,
    business_context: str,
    provider: ModerationProvider
) -> ModerationResult:
    """Runs checks cheapest-first, short-circuits on first failure."""

    result = check_basic(prompt)
    if not result.is_allowed:
        return result

    result = check_blocklist(prompt)
    if not result.is_allowed:
        return result

    result = provider.check(prompt, business_context)
    if not result.is_allowed:
        return result

    return ModerationResult(is_allowed=True)