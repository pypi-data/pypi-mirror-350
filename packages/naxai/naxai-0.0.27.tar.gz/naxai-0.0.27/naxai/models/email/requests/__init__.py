"""
Email request models for the Naxai SDK.

This module provides data structures for email-related API requests,
including transactional emails, newsletters, and email templates.
"""

from .transactional_requests import (SenderObject,
                                     DestinationObject,
                                     CCObject,
                                     BCCObject,
                                     Attachment,
                                     SendTransactionalEmailRequest)

__all__ = [
    "SenderObject",
    "DestinationObject",
    "CCObject",
    "BCCObject",
    "Attachment",
    "SendTransactionalEmailRequest"
]
