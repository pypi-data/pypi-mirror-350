"""
Voice request models for the Naxai SDK.

This module provides data structures for voice-related API requests,
including broadcast creation and individual call initiation.
"""

from .broadcasts_requests import CreateBroadcastRequest
from .call_requests import CreateCallRequest

__all__ = [
    "CreateBroadcastRequest",
    "CreateCallRequest"
]
