"""
Webhook response models for the Naxai SDK.

This module exports Pydantic models that represent responses from the Naxai Webhooks API,
providing strongly-typed structures for webhook management operations including:

- ListWebhooksResponse: For listing configured webhooks
- CreateWebhookResponse: For webhook creation operations
- GetWebhookResponse: For retrieving specific webhook details
- UpdateWebhookResponse: For webhook update operations
- ListLastWebhookEventsResponse: For retrieving recent webhook event history
- ListEventTypesResponse: For listing available event types that can be subscribed to

These models handle JSON parsing, validation, and provide convenient access to response data.
"""

from .webhooks_responses import (
    ListWebhooksResponse,
    CreateWebhookResponse,
    GetWebhookResponse,
    UpdateWebhookResponse,
    ListLastWebhookEventsResponse,
    ListEventTypesResponse
)

__all__ = [
    "ListWebhooksResponse",
    "CreateWebhookResponse",
    "GetWebhookResponse",
    "UpdateWebhookResponse",
    "ListLastWebhookEventsResponse",
    "ListEventTypesResponse"
]
