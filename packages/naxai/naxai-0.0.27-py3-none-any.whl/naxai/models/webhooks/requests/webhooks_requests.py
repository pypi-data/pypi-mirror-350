"""
Request models for the Naxai Webhooks API.

This module defines Pydantic models that represent requests to webhook-related API
endpoints, providing strongly-typed structures for webhook management operations.
It includes models for:

- Creating new webhooks: The CreateWebhookRequest model defines all parameters needed
  to configure a new webhook endpoint
- Updating webhooks: Various JSON Patch operation models (UpdateWebhookJsonPathRequest*)
  that follow RFC 6902 for modifying existing webhook configurations

These models handle field validation, provide snake_case to camelCase field mapping
through aliases, and ensure that requests conform to the API's expected format.
"""

from typing import Union, Optional, Literal
from pydantic import BaseModel, Field
from naxai.models.webhooks.helper_models.authentication import (
    NoAuthModel,
    BasicAuthModel,
    OAuth2AuthModel,
    HeaderAuthModel
)
EVENT_OBJECTS = Literal["All",
                        "People",
                        "Sms",
                        "Call",
                        "Email"]

class CreateWebhookRequest(BaseModel):
    """
    Request model for creating a new webhook in the Naxai platform.
    
    This model defines the required and optional parameters for configuring a webhook,
    including the endpoint URL, authentication method, and event filtering criteria.
    
    Attributes:
        name (str): Descriptive name for the webhook
        url (str): The endpoint URL where events will be sent
        authentication (Union[NoAuthModel, BasicAuthModel, OAuth2AuthModel, HeaderAuthModel]):
            Authentication configuration for the webhook endpoint
        active (Optional[bool]): Whether the webhook should be active upon creation
            Defaults to True
        event_object (EVENT_OBJECTS): The object type to receive events for (e.g., "people", "sms")
        event_filter (list[str]): Additional filtering criteria for events
        event_names (list[str]): Specific event names to subscribe to
    """
    name: str
    url: str
    authentication: Union[
                            NoAuthModel,
                            BasicAuthModel,
                            OAuth2AuthModel,
                            HeaderAuthModel
                        ] = Field(default=None)
    active: Optional[bool] = Field(default=True)
    event_object: EVENT_OBJECTS = Field(alias="eventObject")
    event_filter: list[str] = Field(alias="eventFilter")
    event_names: list[str] = Field(alias="eventNames")

    model_config = {"populate_by_name": True}

class UpdateWebhookJsonPathRequestRemove(BaseModel):
    """
    Request model for removing a field from a webhook using JSON Patch.
    
    This model represents a JSON Patch operation to remove a field from a webhook
    configuration, following the RFC 6902 specification.
    
    Attributes:
        path (str): JSON path to the field that should be removed
        op (Literal["remove"]): The operation type, always "remove" for this model
    """
    path: str
    op: Literal["remove"] = Field(default="remove")

class UpdateWebhookJsonPathRequestAddReplace(BaseModel):
    """
    Request model for adding or replacing a field in a webhook using JSON Patch.
    
    This model represents a JSON Patch operation to add a new field or replace
    an existing field in a webhook configuration, following the RFC 6902 specification.
    
    Attributes:
        path (str): JSON path to the field that should be added or replaced
        value (str): The new value to set at the specified path
    """
    path: str
    value: str

class UpdateWebhookJsonPathRequestMoveCopy(BaseModel):
    """
    Request model for moving or copying a field in a webhook using JSON Patch.
    
    This model represents a JSON Patch operation to move or copy a field from one
    location to another in a webhook configuration, following the RFC 6902 specification.
    
    Attributes:
        path (str): JSON path to the destination where the field should be moved or copied to
        op (Literal["move", "copy"]): The operation type, either "move" or "copy"
    """
    path: str
    op: Literal["move", "copy"] = Field(default="move")
