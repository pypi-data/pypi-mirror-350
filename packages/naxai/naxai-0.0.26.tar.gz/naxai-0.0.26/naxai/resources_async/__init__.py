"""
Asynchronous resources package for the Naxai SDK.

This package provides access to all asynchronous API resources for the Naxai platform including:
- Voice: For managing voice calls, broadcasts, and related analytics
- Calendars: For defining business hours, holidays, and time-based constraints
- Email: For sending and tracking emails, managing templates, and analyzing performance
- People: For managing customer data, contacts, segments, and attributes
- SMS: For sending text messages and analyzing messaging performance

These resources enable non-blocking access to Naxai platform functionality, allowing for
efficient operations in high-performance asynchronous applications built with asyncio.
"""

from .voice import VoiceResource
from .calendars import CalendarsResource
from .email import EmailResource
from .people import PeopleResource
from .sms import SMSResource
from .webhooks import WebhooksResource

__all__ = [
    "VoiceResource",
    "CalendarsResource",
    "EmailResource",
    "PeopleResource",
    "SMSResource",
    "WebhooksResource"
]
