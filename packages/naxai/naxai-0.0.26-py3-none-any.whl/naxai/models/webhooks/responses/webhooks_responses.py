"""
Response models for the Naxai Webhooks API.

This module defines Pydantic models that represent responses from webhook-related API
endpoints, providing strongly-typed structures for webhook management and event tracking.
It includes models for:

- Webhook configurations: Base models and responses for creating, retrieving, updating,
  and listing webhooks
- Event tracking: Models for webhook event data and event history
- Event types: Models for available event types that can be subscribed to

The models handle JSON parsing with special handling for array responses, field aliases
for snake_case to camelCase conversion, and provide list-like behavior for collection
responses to simplify iteration and access.
"""

import json
from typing import Optional, Union, Literal
from pydantic import BaseModel, Field
from naxai.models.webhooks.helper_models.authentication import (
    NoAuthModel,
    BasicAuthModel,
    OAuth2AuthModel,
    HeaderAuthModel,
)

EVENT_OBJECTS = Literal["All",
                        "People",
                        "Sms",
                        "Call",
                        "Email",
                        "Survey"]

class WebhookBaseModel(BaseModel):
    """
    Base model representing a webhook configuration in the Naxai platform.
    
    This model contains all common fields for webhook configurations, including
    identification, endpoint details, authentication method, event filtering,
    and metadata about modifications.
    
    Attributes:
        id (str): Unique identifier for the webhook
        name (str): Descriptive name for the webhook
        url (str): The endpoint URL where events will be sent
        authentication (Union[NoAuthModel, BasicAuthModel, OAuth2AuthModel, HeaderAuthModel]):
            Authentication configuration for the webhook endpoint
        active (bool): Whether the webhook is currently active and receiving events
        event_object (EVENT_OBJECTS): The object type to receive events for (e.g., "people", "sms")
        event_filter (list[str]): Additional filtering criteria for events
        event_names (list[str]): Specific event names to subscribe to
        modified_at (Optional[int]): Timestamp when the webhook was last modified
        modified_by (Optional[str]): Identifier of the user who last modified the webhook
    """
    id: str
    name: str
    url: str
    authentication: Union[
                            NoAuthModel,
                            BasicAuthModel,
                            OAuth2AuthModel,
                            HeaderAuthModel
                        ] = Field(default=None)
    active: bool = Field(default=True)
    event_object: EVENT_OBJECTS = Field(alias="eventObject")
    event_filter: list[str] = Field(alias="eventFilter")
    event_names: list[str] = Field(alias="eventNames")
    modified_at: Optional[int] = Field(default=None, alias="modifiedAt")
    modified_by: Optional[str] = Field(default=None, alias="modifiedBy")

    model_config = {"populate_by_name": True}

class ListWebhooksResponse(BaseModel):
    """
    Response model for listing webhooks.
    
    This model wraps a list of webhook configurations and provides list-like behavior
    for easy iteration and access to the webhook items.
    
    Attributes:
        root (list[WebhookBaseModel]): List of webhook configurations
        
    Methods:
        __len__: Returns the number of webhooks in the list
        __getitem__: Allows accessing webhooks by index
        __iter__: Enables iteration through the webhooks
        model_validate_json: Custom JSON parsing that handles both array and object formats
    """
    root: list[WebhookBaseModel] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return the number of webhooks in the list."""
        return len(self.root)

    def __getitem__(self, index):
        """Access webhook by index."""
        return self.root[index]

    def __iter__(self):
        """Iterate through webhooks."""
        return iter(self.root)

    @classmethod
    def model_validate_json(cls, json_data: str, **kwargs):
        """Parse JSON data into the model.
        
        This method handles both array-style JSON and object-style JSON with a root field.
        
        Args:
            json_data (str): The JSON string to parse
            **kwargs: Additional arguments to pass to the standard model_validate_json method
            
        Returns:
            ListAttributesResponse: A validated instance of the class
        """
        data = json.loads(json_data)

        # If the data is a list, wrap it in a dict with the root field
        if isinstance(data, list):
            return cls(root=data)

        # Otherwise, use the standard Pydantic validation
        return super().model_validate_json(json_data, **kwargs)

class CreateWebhookResponse(WebhookBaseModel):
    """
    Response model for webhook creation operations.
    
    This model represents the webhook configuration that was created,
    inheriting all fields from WebhookBaseModel.
    """

class GetWebhookResponse(WebhookBaseModel):
    """
    Response model for retrieving a specific webhook.
    
    This model represents the webhook configuration that was retrieved,
    inheriting all fields from WebhookBaseModel.
    """

class UpdateWebhookResponse(WebhookBaseModel):
    """
    Response model for webhook update operations.
    
    This model represents the webhook configuration after an update operation,
    inheriting all fields from WebhookBaseModel.
    """

class EventDataBaseModel(BaseModel):
    """
    Base model for webhook event data.
    
    This model allows for flexible event data structures by permitting
    additional fields beyond those explicitly defined.
    """
    model_config = {"extra": "allow"}

class EventsBaseModel(BaseModel):
    """
    Base model representing a webhook event.
    
    This model contains metadata about an event that was sent to a webhook,
    including identification, timing information, and the event payload.
    
    Attributes:
        event_name (Optional[str]): Name of the event that occurred
        event_webhook_id (Optional[str]): ID of the webhook that received this event
        event_timestamp (Optional[int]): Timestamp when the event occurred
        event_id (Optional[str]): Unique identifier for this event
        event_data (Optional[EventDataBaseModel]): The payload data for this event
    """
    event_name: Optional[str] = Field(alias="eventName", default=None)
    event_webhook_id: Optional[str] = Field(alias="eventWebhookId", default=None)
    event_timestamp: Optional[int] = Field(alias="eventTimestamp", default=None)
    event_id: Optional[str] = Field(alias="eventId", default=None)
    event_data: Optional[EventDataBaseModel] = Field(alias="eventData", default=None)

    model_config = {"populate_by_name": True}

class ListLastWebhookEventsResponse(BaseModel):
    """
    Response model for listing recent webhook events.
    
    This model wraps a list of webhook events and provides list-like behavior
    for easy iteration and access to the event items.
    
    Attributes:
        root (list[EventsBaseModel]): List of webhook events
        
    Methods:
        __len__: Returns the number of events in the list
        __getitem__: Allows accessing events by index
        __iter__: Enables iteration through the events
        model_validate_json: Custom JSON parsing that handles both array and object formats
    """
    root: list[EventsBaseModel] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return the number of events in the list."""
        return len(self.root)

    def __getitem__(self, index):
        """Access event by index."""
        return self.root[index]

    def __iter__(self):
        """Iterate through events."""
        return iter(self.root)

    @classmethod
    def model_validate_json(cls, json_data: str, **kwargs):
        """Parse JSON data into the model.

        This method handles both array-style JSON and object-style JSON with a root field.

        Args:
            json_data (str): The JSON string to parse
            **kwargs: Additional arguments to pass to the standard model_validate_json method

        Returns:
            ListAttributesResponse: A validated instance of the class
        """
        data = json.loads(json_data)

        # If the data is a list, wrap it in a dict with the root field
        if isinstance(data, list):
            return cls(root=data)

        # Otherwise, use the standard Pydantic validation
        return super().model_validate_json(json_data, **kwargs)

class ListEventTypesResponse(BaseModel):
    """
    Response model for listing available event types for webhooks.
    
    This model contains a list of event name strings that can be used when configuring
    webhooks to filter which events they should receive. These event types represent
    the various notifications that can be sent to webhook endpoints, such as contact
    creation, message delivery status changes, or other system events.
    
    Attributes:
        events (list[str]): List of available event type names
    """
    events: list[str]
