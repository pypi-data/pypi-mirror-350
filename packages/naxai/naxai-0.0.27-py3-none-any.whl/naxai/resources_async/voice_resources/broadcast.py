"""
Asynchronous voice broadcast resource for the Naxai SDK.

This module provides asynchronous methods for creating and managing voice broadcast campaigns,
including creating, retrieving, updating, and controlling broadcasts. It supports operations
such as starting, pausing, resuming, and canceling broadcasts, as well as accessing detailed
metrics and recipient information through specialized sub-resources, all in a non-blocking
manner suitable for high-performance asynchronous applications.

Available Functions:
    list(page=1, page_size=25)
        Retrieves a paginated list of all broadcasts.
        Args:
            page: Page number to retrieve (default: 1)
            page_size: Number of items per page (default: 25, max: 100)
        Returns:
            ListBroadcastResponse: List of broadcasts with pagination info

    create(request: CreateBroadcastRequest)
        Creates a new broadcast campaign.
        Args:
            request: Broadcast configuration details
        Returns:
            CreateBroadcastResponse: Created broadcast details

    get(broadcast_id: str)
        Retrieves details about a specific broadcast.
        Args:
            broadcast_id: ID of the broadcast to retrieve
        Returns:
            GetBroadcastResponse: Detailed broadcast information

    update(broadcast_id: str, request: UpdateBroadcastRequest)
        Updates an existing broadcast's configuration.
        Args:
            broadcast_id: ID of the broadcast to update
            request: Updated broadcast configuration
        Returns:
            UpdateBroadcastResponse: Updated broadcast details

    start(broadcast_id: str)
        Starts a broadcast campaign.
        Args:
            broadcast_id: ID of the broadcast to start
        Returns:
            StartBroadcastResponse: Start operation result

    pause(broadcast_id: str)
        Pauses an active broadcast campaign.
        Args:
            broadcast_id: ID of the broadcast to pause
        Returns:
            PauseBroadcastResponse: Pause operation result

    resume(broadcast_id: str)
        Resumes a paused broadcast campaign.
        Args:
            broadcast_id: ID of the broadcast to resume
        Returns:
            ResumeBroadcastResponse: Resume operation result

    cancel(broadcast_id: str)
        Cancels an active or paused broadcast campaign.
        Args:
            broadcast_id: ID of the broadcast to cancel
        Returns:
            CancelBroadcastResponse: Cancel operation result

Sub-resources:
    metrics:
        A subresource for retrieving broadcast metrics and analytics.
        See MetricsResource for detailed documentation.

    recipients:
        A subresource for managing broadcast recipients and tracking delivery.
        See RecipientsResource for detailed documentation.

"""

import json
from typing import Optional, Annotated
from pydantic import Field, validate_call
from naxai.models.voice.requests.broadcasts_requests import CreateBroadcastRequest
from naxai.models.voice.responses.broadcasts_responses import (ListBroadcastResponse,
                                                               CreateBroadcastResponse,
                                                               GetBroadcastResponse,
                                                               UpdateBroadcastResponse,
                                                               StartBroadcastResponse,
                                                               PauseBroadcastResponse,
                                                               ResumeBroadcastResponse,
                                                               CancelBroadcastResponse)
from .broadcast_resources.metrics import MetricsResource
from .broadcast_resources.recipients import RecipientsResource

class BroadcastsResource:
    """ broadcasts resource for voice resource"""

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/broadcasts"
        self.metrics = MetricsResource(self._client, self.root_path)
        self.recipients = RecipientsResource(self._client, self.root_path)
        self.headers = {"Content-Type": "application/json"}

    @validate_call
    async def list(self,
                   page: Optional[int] = 1,
                   page_size: Annotated[Optional[int], Field(ge=1, le=100)] = 25):
        """
        Retrieves a list of all broadcasts.

        Args:
            page (Optional[int]): Page number to retrieve. Defaults to 1.
            page_size (Optional[int]): Number of items to list per page (1-100). Defaults to 25.

        Returns:
            ListBroadcastResponse: A Pydantic model containing a paginated list of broadcasts.
            The response includes:
                - items: List of BroadcastResponseItem objects with details about each broadcast
                - pagination: Information about the current page, total pages, and total items

        Example:
            >>> response = await client.voice.broadcasts.list(page=1, page_size=50)
            >>> print(f"Found {len(response.items)} broadcasts")
            >>> print(f"Page {response.pagination.page} of {response.pagination.total_pages}")
            >>> for broadcast in response.items:
            ...     print(f"Broadcast: {broadcast.name} ({broadcast.state})")
            ...     print(f"Progress: {broadcast.completed_count}/{broadcast.total_count}")
        """
        params = {"page": page, "pageSize": page_size}
        # pylint: disable=protected-access
        return ListBroadcastResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path,
                                                   headers=self.headers,
                                                   params=params)))

    async def create(self, data: CreateBroadcastRequest):
        """
        Creates a new broadcast.

        Args:
            data (CreateBroadcastRequest): 
                The request body containing the details of the broadcast to be created.

        Returns:
            CreateBroadcastResponse: 
            A Pydantic model containing the details of the created broadcast,
            including the broadcast_id, name, configuration, and other metadata.

        Example:
            >>> new_broadcast = await client.voice.broadcasts.create(
            ...     CreateBroadcastRequest(
            ...         name="My Broadcast",
            ...         from_="123456789",
            ...         segment_ids=["seg_abc123"],
            ...         voice_flow=voice_flow_obj
            ...     )
            ... )
            >>> print(f"Created broadcast with ID: {new_broadcast.broadcast_id}")
        """
        # pylint: disable=protected-access
        return CreateBroadcastResponse.model_validate_json(
            json.dumps(await self._client._request("POST",
                                                   self.root_path,
                                                   json=data.model_dump(by_alias=True,
                                                                        exclude_none=True),
                                                   headers=self.headers)))

    async def get(self, broadcast_id: str):
        """
        Retrieves a specific broadcast by its ID.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to retrieve.

        Returns:
            GetBroadcastResponse: A Pydantic model containing the complete details of the broadcast,
            including configuration, metrics, and status information.

        Example:
            >>> broadcast = await client.voice.broadcasts.get(
            ...     broadcast_id="XXXXXXXXX"
            ... )
            >>> print(f"Broadcast: {broadcast.name}")
            >>> print(f"Progress: {broadcast.completed_count}/{broadcast.total_count}")
        """
        # pylint: disable=protected-access
        return GetBroadcastResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/" + broadcast_id,
                                                   headers=self.headers)))

    async def delete(self, broadcast_id: str):
        """
        Deletes a specific broadcast by its ID.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to delete.

        Returns:
            None

        Example:
            >>> deletion_result = await client.voice.broadcasts.delete(
            ...     broadcast_id="XXXXXXXXX"
            ... )
        """
        # pylint: disable=protected-access
        return await self._client._request("DELETE",
                                           self.root_path + "/" + broadcast_id,
                                           headers=self.headers)

    async def update(self, broadcast_id: str, data: CreateBroadcastRequest):
        """
        Updates a specific broadcast by its ID.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to update.
            data (CreateBroadcastRequest): 
                The request body containing the updated details of the broadcast.

        Returns:
            UpdateBroadcastResponse: 
            A Pydantic model containing the details of the updated broadcast,
            including any modified fields and metadata.

        Example:
            >>> updated_broadcast = await client.voice.broadcasts.update(
            ...     broadcast_id="XXXXXXXXX",
            ...     CreateBroadcastRequest(
            ...         name="Updated Broadcast",
            ...         from_="123456789",
            ...         segment_ids=["seg_abc123"],
            ...         voice_flow=voice_flow_obj
            ...     )
            ... )
            >>> print(f"Updated broadcast: {updated_broadcast.name}")
        """
        # pylint: disable=protected-access
        return UpdateBroadcastResponse.model_validate_json(
            json.dumps(await self._client._request("PUT",
                                                   self.root_path + "/" + broadcast_id,
                                                   json=data.model_dump(by_alias=True,
                                                                        exclude_none=True),
                                                   headers=self.headers)))

    async def start(self, broadcast_id: str):
        """
        Starts a broadcast.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to start.

        Returns:
            StartBroadcastResponse: A Pydantic model confirming the broadcast is starting,
            containing the broadcast_id and state ("starting").

        Example:
            >>> result = await client.voice.broadcasts.start(
            ...     broadcast_id="XXXXXXXXX"
            ... )
            >>> print(f"Broadcast {result.broadcast_id} is {result.state}")
        """
        # pylint: disable=protected-access
        return StartBroadcastResponse.model_validate_json(
            json.dumps(await self._client._request("POST",
                                                   self.root_path + "/" + broadcast_id + "/start",
                                                   headers=self.headers)))

    async def pause(self, broadcast_id: str):
        """
        Pauses a broadcast.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to pause.

        Returns:
            PauseBroadcastResponse: A Pydantic model confirming the broadcast is pausing,
            containing the broadcast_id and state ("pausing").

        Example:
            >>> result = await client.voice.broadcasts.pause(
            ...     broadcast_id="XXXXXXXXX"
            ... )
            >>> print(f"Broadcast {result.broadcast_id} is {result.state}")
        """
        # pylint: disable=protected-access
        return PauseBroadcastResponse.model_validate_json(
            json.dumps(await self._client._request("POST",
                                                   self.root_path + "/" + broadcast_id + "/pause",
                                                   headers=self.headers)))

    async def resume(self, broadcast_id: str):
        """
        Resumes a broadcast.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to resume.

        Returns:
            ResumeBroadcastResponse: A Pydantic model confirming the broadcast is resuming,
            containing the broadcast_id and state ("resuming").

        Example:
            >>> result = await client.voice.broadcasts.resume(
            ...     broadcast_id="XXXXXXXXX"
            ... )
            >>> print(f"Broadcast {result.broadcast_id} is {result.state}")
        """
        # pylint: disable=protected-access
        return ResumeBroadcastResponse.model_validate_json(
            json.dumps(await self._client._request("POST",
                                                   self.root_path + "/" + broadcast_id + "/resume",
                                                   headers=self.headers)))

    async def cancel(self, broadcast_id: str):
        """
        Cancels a broadcast.

        Args:
            broadcast_id (str): The unique identifier of the broadcast to cancel.

        Returns:
            CancelBroadcastResponse: A Pydantic model confirming the broadcast is canceling,
            containing the broadcast_id and state ("canceling").

        Example:
            >>> result = await client.voice.broadcasts.cancel(
            ...     broadcast_id="XXXXXXXXX"
            ... )
            >>> print(f"Broadcast {result.broadcast_id} is {result.state}")
        """
        # pylint: disable=protected-access
        return CancelBroadcastResponse.model_validate_json(
            json.dumps(await self._client._request("POST",
                                                   self.root_path + "/" + broadcast_id + "/cancel",
                                                   headers=self.headers)))
