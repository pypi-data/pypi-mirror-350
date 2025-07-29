"""
Asynchronous voice activity logs resource for the Naxai SDK.

This module provides asynchronous methods for retrieving and analyzing detailed voice call logs,
including listing calls with various filtering options and retrieving comprehensive information
about specific calls. These logs contain data about call routing, duration, status, and other
attributes for inbound, outbound, and transferred calls, accessible in a non-blocking manner
suitable for high-performance asynchronous applications.

Available Functions:
    list(page=1, page_size=25, start=None, stop=None, direction=None, status=None,
         from_=None, to=None, client_id=None, campaign_id=None, broadcast_id=None)
        Retrieves a paginated list of voice call activity logs with optional filtering.
        Args:
            page: Page number to retrieve (default: 1)
            page_size: Number of items per page (default: 25, max: 100)
            start: Start timestamp in milliseconds since epoch
            stop: End timestamp in milliseconds since epoch
            direction: Filter by call direction ("inbound", "outbound", "transfer")
            status: Filter by call status ("delivered", "failed")
            from_: Filter by originating phone number
            to: Filter by destination phone number
            client_id: Filter by client identifier
            campaign_id: Filter by campaign identifier
            broadcast_id: Filter by broadcast identifier
        Returns:
            ListActivityLogsResponse: List of call logs with pagination info

    get(call_id: str)
        Retrieves detailed information about a specific call.
        Args:
            call_id: ID of the call to retrieve
        Returns:
            GetActivityLogResponse: Detailed call information

"""

import json
from typing import Optional, Literal, Annotated
from pydantic import Field, validate_call
from naxai.models.voice.responses.activity_logs_responses import (ListActivityLogsResponse,
                                                                  GetActivityLogResponse)

class ActivityLogsResource:
    """ activity_logs resource for voice resource """


    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/activity-logs"
        self.headers = {"Content-Type": "application/json"}

    @validate_call
    async def list(self,
                   page: Optional[int] = 1,
                   page_size: Annotated[Optional[int], Field(ge=1, le=100)] = 25,
                   start: Optional[int] = None,
                   stop: Optional[int] = None,
                   direction: Optional[Literal["inbound", "outbound", "transfer"]] = None,
                   status: Optional[Literal["delivered", "failed"]] = None,
                   from_: Optional[str] = None,
                   to: Optional[str] = None,
                   client_id: Optional[str] = None,
                   campaign_id: Optional[str] = None,
                   broadcast_id: Optional[str] = None
                   ):
        """
        Retrieves a paginated list of voice call activity logs with optional filtering.
        
        This method fetches call activity logs from the API, allowing filtering by various
        criteria such as time range, call direction, status, and associated IDs.
        
        Args:
            page (Optional[int]): Page number to retrieve. Defaults to 1.
            page_size (Optional[int]): Number of items per page (1-100). Defaults to 25.
            start (Optional[int]): Start timestamp for filtering calls, in milliseconds since epoch.
            stop (Optional[int]): End timestamp for filtering calls, in milliseconds since epoch.
            direction (Optional[Literal["inbound", "outbound", "transfer"]]): 
                Filter by call direction.
            status (Optional[Literal["delivered", "failed"]]): Filter by call status.
            from_ (Optional[str]): Filter by originating phone number.
            to (Optional[str]): Filter by destination phone number.
            client_id (Optional[str]): Filter by client identifier.
            campaign_id (Optional[str]): Filter by campaign identifier.
            broadcast_id (Optional[str]): Filter by broadcast identifier.
        
        Returns:
            ListActivityLogsResponse: 
            A Pydantic model containing the paginated list of call activity logs.
            The response includes:
                - pagination: Information about the current page, total pages, and total items
                - calls: List of CallBaseModel objects with detailed information about each call
        
        Example:
            >>> response = await client.voice.activity_logs.list(
            ...     page=1,
            ...     page_size=50,
            ...     start=1672531200000,  # Jan 1, 2023
            ...     stop=1704067199000,   # Dec 31, 2023
            ...     direction="outbound",
            ...     status="delivered"
            ... )
            >>> print(f"Found {response.pagination.total_items} calls")
            >>> print(f"Showing page {response.pagination.page} of "
            >>>       f"{response.pagination.total_pages}")
            >>> for call in response.calls:
            ...     print(f"Call {call.call_id}: {call.from_} → {call.to}, {call.status}")
            ...     print(f"Duration: {call.call_duration}s, Date: {call.call_date}")
        
        Note:
            - Timestamp parameters (start, stop) are in milliseconds since epoch
            - Multiple filter parameters can be combined for more specific queries
            - Results are typically sorted by call_date in descending order (most recent first)
            - The page_size parameter is limited to a maximum of 100 items per page
        """
        params = {
            "page": page,
            "page_size": page_size,
        }

        if start:
            params["start"] = start
        if stop:
            params["stop"] = stop
        if direction:
            params["direction"] = direction
        if status:
            params["status"] = status
        if from_:
            params["from"] = from_
        if to:
            params["to"] = to
        if client_id:
            params["clientId"] = client_id
        if campaign_id:
            params["campaignId"] = campaign_id
        if broadcast_id:
            params["broadcastId"] = broadcast_id
        # pylint: disable=protected-access
        return ListActivityLogsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path,
                                                   params=params,
                                                   headers=self.headers)))

    async def get(self, call_id:str):
        """
        Retrieves detailed information about a specific call by its ID.
        
        This method fetches comprehensive details for a single call activity log
        identified by its unique call ID.
        
        Args:
            call_id (str): The unique identifier of the call to retrieve.
        
        Returns:
            GetActivityLogResponse: A Pydantic model containing detailed information about the call,
            including routing information, status, duration, and other call-specific attributes.
            The response includes all fields from CallBaseModel such as:
                - call_id: Unique identifier for the call
                - from_: Originating phone number
                - to: Destination phone number
                - direction: Call direction (outbound, inbound, transfer)
                - status: Call status (delivered, failed)
                - call_duration: Duration of the call in seconds
                - And many other call attributes
        
        Example:
            >>> call = await client.voice.activity_logs.get(
            ...     call_id="call_123abc"
            ... )
            >>> print(f"Call from {call.from_} to {call.to}")
            >>> print(f"Status: {call.status}, Reason: {call.reason}")
            >>> print(f"Duration: {call.call_duration} seconds")
            >>> if call.transferred:
            ...     print(f"Transferred to call: {call.transfer_call_id}")
            ...     print(f"Transfer status: {call.transfer_status}")
        
        Raises:
            NaxaiAPIError: If the call ID doesn't exist or if there's an API error
        
        See Also:
            CallBaseModel: For detailed information about all available call attributes
            ListActivityLogsResponse: For retrieving multiple calls with pagination
        """
        # pylint: disable=protected-access
        return GetActivityLogResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/" + call_id,
                                                   headers=self.headers)))
