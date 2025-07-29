"""
Resource classes for the Naxai SDK.

This package provides access to various API resources including voice, calendars,
email, and people management functionality.
"""

from .voice import VoiceResource
from .calendars import CalendarsResource
from .email import EmailResource
from .people import PeopleResource
from .webhooks import WebhooksResource

__all__ = [
    "VoiceResource",
    "CalendarsResource",
    "EmailResource",
    "PeopleResource",
    "WebhooksResource"
]
