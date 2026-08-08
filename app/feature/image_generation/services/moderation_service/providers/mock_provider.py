# services/moderation_service/providers/mock_provider.py
from .base import ModerationProvider
from ..schemas import ModerationResult


class MockModerationProvider(ModerationProvider):
    """Local dev stand-in. Always allows — replace with a real provider
    (embedding relevance check, Ollama LLM check, or third-party API)
    before going to production."""

    def check(self, prompt: str, business_context: str) -> ModerationResult:
        return ModerationResult(is_allowed=True)