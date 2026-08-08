# services/moderation_service/providers/base.py
from abc import ABC, abstractmethod
from ..schemas import ModerationResult


class ModerationProvider(ABC):
    @abstractmethod
    def check(self, prompt: str, business_context: str) -> ModerationResult:
        """Evaluate prompt for relevance + safety against business context."""
        ...