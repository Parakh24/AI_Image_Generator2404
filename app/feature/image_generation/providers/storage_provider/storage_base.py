"""
base.py

Defines the contract every storage provider adapter must follow.

RULE: the worker depends ONLY on this file - never on a specific
storage backend (local disk, S3, etc). This is what lets us swap
local disk for cloud storage later without touching worker code.
"""


from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class StorageResult:
    """
    Standardized result shape returned by EVERY storage provider,
    no matter where the file actually ended up.

    storage_key: internal path/identifier (what gets saved in the
                 image_assets table)
    image_url:   public/servable URL given to the client
    """

    storage_key: str
    image_url: str


class StorageProviderError(Exception):
    """
    Base error type for all storage provider adapters. Worker code
    catches THIS type, never a backend-specific exception - same
    reasoning as ImageProviderError.
    """


class StorageProvider(ABC):
    """
    Interface every storage provider adapter must implement.

    The worker only ever calls save_image() on this interface - it
    never knows or cares whether the file ends up on local disk,
    S3, or anywhere else.
    """

    @abstractmethod
    def save_image(
        self, job_id: str, image_bytes: bytes, mime_type: str
    ) -> StorageResult:
        """Saves image bytes somewhere persistent, returns where to find it."""
        raise NotImplementedError