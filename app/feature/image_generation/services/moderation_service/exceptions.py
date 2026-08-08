# services/moderation_service/exceptions.py
from .schemas import ModerationResult


class PromptRejectedException(Exception):
    def __init__(self, result: ModerationResult):
        self.result = result
        super().__init__(result.detail or "Prompt rejected by moderation")