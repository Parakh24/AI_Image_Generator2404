"""Worker exceptions that distinguish retryable and permanent failures."""

class TemporaryGenerationError(Exception):
    """Report a temporary failure for which retrying the job may succeed."""

class PermanentGenerationError(Exception):
    """Report a permanent failure that should not be retried."""
