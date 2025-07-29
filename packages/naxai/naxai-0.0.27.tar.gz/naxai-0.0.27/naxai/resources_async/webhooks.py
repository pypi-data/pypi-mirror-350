"""
Asynchronous webhooks resource for the Naxai SDK.

This module provides asynchronous methods for managing webhook configurations in the
Naxai platform, enabling applications to receive real-time event notifications for
various activities such as message deliveries, contact updates, and other system events.

The WebhooksResource class supports:
- Creating webhook endpoints with various authentication methods
- Listing, retrieving, updating, and deleting webhook configurations
- Viewing recent events sent to webhooks
- Discovering available event types for subscription

Webhooks allow applications to receive push notifications rather than polling the API,
providing a more efficient way to stay synchronized with changes in the Naxai platform.
All methods in this module are asynchronous and designed for use with asyncio.

Available Functions:
    list() -> ListWebhooksResponse
        Retrieves a list of all configured webhooks.
        Returns:
            ListWebhooksResponse: List of webhook configurations

    create(url, events, auth=None, description=None) -> CreateWebhookResponse
        Creates a new webhook endpoint configuration.
        Args:
            url: Webhook endpoint URL
            events: List of event types to subscribe to
            auth: Optional authentication configuration
            description: Optional webhook description
        Returns:
            CreateWebhookResponse: Created webhook details

    get(webhook_id) -> GetWebhookResponse
        Retrieves details of a specific webhook.
        Args:
            webhook_id: ID of webhook to retrieve
        Returns:
            GetWebhookResponse: Webhook configuration details

    delete(webhook_id)
        Deletes a webhook configuration.
        Args:
            webhook_id: ID of webhook to delete

    update(webhook_id, update_operations) -> UpdateWebhookResponse
        Updates a webhook using JSON Patch operations.
        Args:
            webhook_id: ID of webhook to update
            update_operations: List of JSON Patch operations
        Returns:
            UpdateWebhookResponse: Updated webhook details

    list_last_events(webhook_id) -> ListLastWebhookEventsResponse
        Retrieves recent events sent to a webhook.
        Args:
            webhook_id: ID of webhook to get events for
        Returns:
            ListLastWebhookEventsResponse: List of recent events

    list_events() -> ListEventTypesResponse
        Retrieves all available webhook event types.
        Returns:
            ListEventTypesResponse: List of available event types

"""
import json
from typing import Literal, List, Union
from naxai.models.webhooks.requests.webhooks_requests import (
    CreateWebhookRequest,
    UpdateWebhookJsonPathRequestAddReplace,
    UpdateWebhookJsonPathRequestMoveCopy,
    UpdateWebhookJsonPathRequestRemove
)
from naxai.models.webhooks.responses.webhooks_responses import (
    ListWebhooksResponse,
    CreateWebhookResponse,
    GetWebhookResponse,
    UpdateWebhookResponse,
    ListLastWebhookEventsResponse,
    ListEventTypesResponse
)
from naxai.models.webhooks.helper_models.authentication import (
    BasicAuthModel,
    OAuth2AuthModel,
    HeaderAuthModel,
    NoAuthModel
)

class WebhooksResource:
    """
    Provides access to webhooks related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.root_path = "/webhooks/endpoints"
        self.events_root_path = "/webhooks"
        self.headers = {"Content-Type": "application/json"}

    async def list(self):
        """
        Retrieve a list of all configured webhooks.
        
        This method fetches all webhook configurations from the Naxai platform,
        including their endpoints, authentication settings, and event subscriptions.
        
        Returns:
            ListWebhooksResponse: A response object containing the list of webhooks.
                The response behaves like a list and can be iterated over.
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access webhooks.
        
        Example:
            >>> webhooks = await client.webhooks.list()
            >>> print(f"Found {len(webhooks)} webhooks")
            >>> for webhook in webhooks:
            ...     print(f"Webhook: {webhook.name} ({webhook.id})")
            ...     print(f"URL: {webhook.url}")
            ...     print(f"Active: {webhook.active}")
        """
        # pylint: disable=protected-access
        return ListWebhooksResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path,
                                                   headers=self.headers)
                                                   ))

    async def _create(self,
                      data: CreateWebhookRequest):
        """
        Internal method to create a webhook from a request model.
        
        This is a helper method used by the public create() method.
        
        Args:
            data (CreateWebhookRequest): The webhook configuration data.
        
        Returns:
            CreateWebhookResponse: A response object containing the created webhook details.
        """
        # pylint: disable=protected-access
        return CreateWebhookResponse.model_validate_json(
            json.dumps(await self._client._request("POST",
                                                   self.root_path,
                                                   json=data.model_dump(by_alias=True,
                                                    exclude_none=True),
                                                   headers=self.headers)
                                                   ))

    async def create(self,
                     name: str,
                     url: str,
                     authentication: Union[BasicAuthModel,
                                           OAuth2AuthModel,
                                           HeaderAuthModel,
                                           NoAuthModel],
                     event_object: Literal[
                            "All", "People", "Sms",
                            "Email", "Call"],
                     event_filter: List[str],
                     event_names: List[str],
                     active: bool = True):
        """
        Create a new webhook configuration.
        
        This method creates a new webhook endpoint that will receive event notifications
        from the Naxai platform based on the specified filters and event types.
        
        Args:
            name (str): A descriptive name for the webhook.
            url (str): The endpoint URL where events will be sent.
            authentication (Union[BasicAuthModel, OAuth2AuthModel, HeaderAuthModel, NoAuthModel]):
                Authentication configuration for the webhook endpoint.
            event_object (Literal["all", "people", "sms", "email", "call"]):
                The object type to receive events for.
            event_filter (List[str]): Additional filtering criteria for events.
            event_names (List[str]): Specific event names to subscribe to.
            active (bool, optional): Whether the webhook should be active upon creation.
                Defaults to True.
        
        Returns:
            CreateWebhookResponse: A response object containing the created webhook details.
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to create webhooks.
            ValidationError: If the provided parameters fail validation.
        
        Example:
            >>> # Create a webhook for SMS delivery events with no authentication
            >>> webhook = await client.webhooks.create(
            ...     name="SMS Delivery Notifications",
            ...     url="https://example.com/webhooks/sms",
            ...     authentication=NoAuthModel(),
            ...     event_object="sms",
            ...     event_filter=["*"],
            ...     event_names=["sms.delivered", "sms.failed"]
            ... )
            >>> print(f"Created webhook with ID: {webhook.id}")
        """
        data = CreateWebhookRequest(name=name,
                                    url=url,
                                    authentication=authentication,
                                    active=active,
                                    event_object=event_object,
                                    event_filter=event_filter,
                                    event_names=event_names)

        return await self._create(data)

    async def get(self, webhook_id: str):
        """
        Retrieve a specific webhook by its ID.
        
        This method fetches detailed information about a single webhook configuration.
        
        Args:
            webhook_id (str): The unique identifier of the webhook to retrieve.
        
        Returns:
            GetWebhookResponse: A response object containing the webhook details.
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access webhooks.
            NaxaiResourceNotFound: If the specified webhook does not exist.
        
        Example:
            >>> webhook = await client.webhooks.get("wh_123abc")
            >>> print(f"Webhook: {webhook.name}")
            >>> print(f"URL: {webhook.url}")
            >>> print(f"Active: {webhook.active}")
            >>> print(f"Event object: {webhook.event_object}")
            >>> print(f"Event names: {webhook.event_names}")
        """
        # pylint: disable=protected-access
        return GetWebhookResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/" + webhook_id,
                                                   headers=self.headers)
                                                   ))

    async def delete(self, webhook_id: str):
        """
        Delete a webhook configuration.
        
        This method permanently removes a webhook configuration from the Naxai platform.
        Once deleted, the webhook will no longer receive event notifications.
        
        Args:
            webhook_id (str): The unique identifier of the webhook to delete.
        
        Returns:
            None
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to delete webhooks.
            NaxaiResourceNotFound: If the specified webhook does not exist.
        
        Example:
            >>> await client.webhooks.delete("wh_123abc")
            >>> print("Webhook deleted successfully")
        """
        # pylint: disable=protected-access
        return await self._client._request("DELETE",
                                           self.root_path + "/" + webhook_id,
                                           headers=self.headers)

    async def update(self,
                     webhook_id: str,
                     update_operations: List[Union[UpdateWebhookJsonPathRequestAddReplace,
                                                   UpdateWebhookJsonPathRequestMoveCopy,
                                                   UpdateWebhookJsonPathRequestRemove]]):
        """
        Update a webhook configuration using JSON Patch operations.
        
        This method modifies an existing webhook using JSON Patch operations (RFC 6902),
        allowing for precise updates to specific fields without replacing the entire configuration.
        
        Args:
            update_operations (List[Union[UpdateWebhookJsonPathRequestAddReplace,
                                        UpdateWebhookJsonPathRequestMoveCopy,
                                        UpdateWebhookJsonPathRequestRemove]]):
                A list of JSON Patch operations to apply to the webhook.
        
        Returns:
            UpdateWebhookResponse: A response object containing the updated webhook details.
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to update webhooks.
            NaxaiResourceNotFound: If the specified webhook does not exist.
            ValidationError: If the provided operations fail validation.
        
        Example:
            >>> # Update a webhook's URL
            >>> update_op = UpdateWebhookJsonPathRequestAddReplace(
            ...     path="/url",
            ...     value="https://new-endpoint.example.com/webhooks"
            ... )
            >>> updated = await client.webhooks.update([update_op])
            >>> print(f"Updated webhook URL: {updated.url}")
        """
        # pylint: disable=protected-access
        return UpdateWebhookResponse.model_validate_json(
            json.dumps(await self._client._request("PATCH",
                                                   self.root_path + "/" + webhook_id,
                                                   json=update_operations,
                                                   headers=self.headers)
                                                   ))

    async def list_last_events(self, webhook_id: str):
        """
        Retrieve recent events sent to a specific webhook.
        
        This method fetches the most recent events that were sent to the specified webhook,
        including their payloads and delivery timestamps.
        
        Args:
            webhook_id (str): The unique identifier of the webhook to get events for.
        
        Returns:
            ListLastWebhookEventsResponse: A response object containing the list of recent events.
                The response behaves like a list and can be iterated over.
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access webhook events.
            NaxaiResourceNotFound: If the specified webhook does not exist.
        
        Example:
            >>> events = await client.webhooks.list_last_events("wh_123abc")
            >>> print(f"Found {len(events)} recent events")
            >>> for event in events:
            ...     print(f"Event: {event.event_name}")
            ...     print(f"Timestamp: {event.event_timestamp}")
            ...     print(f"Data: {event.event_data}")
        """
        url = self.events_root_path + "/" + webhook_id + "/last"
        # pylint: disable=protected-access
        return ListLastWebhookEventsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   url,
                                                   headers=self.headers)
                                                   ))

    async def list_events(self):
        """
        Retrieve a list of all available event types for webhooks.
        
        This method fetches all event types that can be subscribed to when configuring webhooks,
        helping users understand what events are available for monitoring.
        
        Returns:
            ListEventTypesResponse: A response object containing the list of available event types.
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access event types.
        
        Example:
            >>> event_types = await client.webhooks.list_events()
            >>> print("Available event types:")
            >>> for event_type in event_types.events:
            ...     print(f"- {event_type}")
        """
        # pylint: disable=protected-access
        return ListEventTypesResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.events_root_path + "/events",
                                                   headers=self.headers)
                                                   ))
