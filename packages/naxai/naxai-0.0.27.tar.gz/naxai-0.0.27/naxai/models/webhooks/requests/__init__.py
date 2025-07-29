"""
Webhook request models for the Naxai SDK.

This module exports Pydantic models that represent requests to the Naxai Webhooks API,
providing strongly-typed structures for webhook management operations including:

- CreateWebhookRequest: For creating new webhook configurations
- UpdateWebhookJsonPathRequestAddReplace: For adding or replacing fields in existing webhooks
- UpdateWebhookJsonPathRequestMoveCopy: For moving or copying fields within webhook configurations
- UpdateWebhookJsonPathRequestRemove: For removing fields from webhook configurations

These models handle field validation and provide a consistent interface for making
API requests related to webhook management.
"""

from .webhooks_requests import (
    CreateWebhookRequest,
    UpdateWebhookJsonPathRequestAddReplace,
    UpdateWebhookJsonPathRequestMoveCopy,
    UpdateWebhookJsonPathRequestRemove
)

__all__ = [
    "CreateWebhookRequest",
    "UpdateWebhookJsonPathRequestAddReplace",
    "UpdateWebhookJsonPathRequestMoveCopy",
    "UpdateWebhookJsonPathRequestRemove"
]
