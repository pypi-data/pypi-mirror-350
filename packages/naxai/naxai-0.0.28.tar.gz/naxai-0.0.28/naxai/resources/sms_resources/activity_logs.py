"""
SMS activity logs resource for the Naxai SDK.

This module provides methods for retrieving and analyzing SMS message activity logs,
including listing messages with various filtering options and retrieving detailed
information about specific messages. These logs contain comprehensive data about
message delivery, status, content, and associated metadata for both inbound and
outbound SMS communications.

Available Functions:
    list(page=1, page_size=25, start=None, stop=None, direction=None, status=None, 
         phone_number=None, client_id=None, campaign_id=None, broadcast_id=None)
        Retrieves a paginated list of SMS activity logs with optional filtering.
        Supports filtering by time range, direction, status, phone number and IDs.

    get(message_id)
        Retrieves detailed information about a specific SMS message by its ID.
        Returns comprehensive data about the message's delivery, status and metadata.

"""

import json
from typing import Literal
from pydantic import Field, validate_call
from naxai.models.sms.responses.activity_logs_responses import (ListSMSActivityLogsResponse,
                                                                GetSMSActivityLogsResponse)

class ActivityLogsResource:
    """ activity_logs resource for sms resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/activity-logs"
        self.headers = {"Content-Type": "application/json"}

    @validate_call
    def list(self,
            page: int = Field(default=1),
            page_size: int = Field(default=25),
            start: int = Field(default=None),
            stop: int = Field(default=None),
            direction: Literal["inbound", "outbound"] = Field(default=None),
            status: Literal["delivered", "failed"] = Field(default=None),
            phone_number: str = Field(default=None, max_length=15, min_length=7),
            client_id: str = Field(default=None),
            campaign_id: str = Field(default=None),
            broadcast_id: str = Field(default=None)
            ):
        """
        Retrieves a paginated list of SMS activity logs with optional filtering.
        
        This method fetches SMS message activity logs from the API, allowing filtering by various
        criteria such as time range, direction, status, phone number, and associated IDs.
        
        Args:
            page (int): Page number to retrieve. Defaults to 1.
            page_size (int): Number of items per page. Defaults to 25.
                Mapped from JSON key 'pageSize'.
            start (int, optional): 
                Start timestamp for filtering messages, in milliseconds since epoch.
                Only messages sent/received after this time will be included.
            stop (int, optional): End timestamp for filtering messages, in milliseconds since epoch.
                Only messages sent/received before this time will be included.
            direction (Literal["inbound", "outbound"], optional): Filter by message direction.
                - "inbound": Only include messages received by the platform
                - "outbound": Only include messages sent from the platform
            status (Literal["delivered", "failed"], optional): Filter by message delivery status.
                - "delivered": Only include successfully delivered messages
                - "failed": Only include failed messages
            phone_number (str, optional): Filter by phone number (sender or recipient).
                Must be between 7 and 15 characters. Mapped from JSON key 'phoneNumber'.
            client_id (str, optional): Filter by client identifier.
                Mapped from JSON key 'clientId'.
            campaign_id (str, optional): Filter by campaign identifier.
                Mapped from JSON key 'campaignId'.
            broadcast_id (str, optional): Filter by broadcast identifier.
                Mapped from JSON key 'broadcastId'.
        
        Returns:
            ListSMSActivityLogsResponse: A Pydantic model containing the paginated list of
            SMS activity logs.
            The response includes:
                - pagination: Information about the current page, total pages, and total items
                - messages: List of BaseMessage objects with detailed information about
                  each SMS message
        
        Example:
            >>> # Basic usage with pagination
            >>> response = client.sms.activity_logs.list(
            ...     page=1,
            ...     page_size=50
            ... )
            >>> print(f"Found {response.pagination.total_items} messages")
            >>> print(f"Showing page {response.pagination.page} of "
            >>>       f"{response.pagination.total_pages}")
            >>> for msg in response.messages:
            ...     print(f"{msg.direction} message: {msg.message_id} - Status: {msg.status}")
            
            >>> # Filtering by date range and status
            >>> import time
            >>> one_week_ago = int(time.time() * 1000) - (7 * 24 * 60 * 60 * 1000)
            >>> now = int(time.time() * 1000)
            >>> delivered = client.sms.activity_logs.list(
            ...     start=one_week_ago,
            ...     stop=now,
            ...     direction="outbound",
            ...     status="delivered"
            ... )
            >>> print(f"Successfully delivered messages in the last week: "
                      f"{len(delivered.messages)}")
            
            >>> # Filtering by phone number
            >>> specific_number = client.sms.activity_logs.list(
            ...     phone_number="+1234567890",
            ...     page_size=100
            ... )
            >>> print(f"Messages to/from +1234567890: {len(specific_number.messages)}")
            
            >>> # Filtering by campaign
            >>> campaign_messages = client.sms.activity_logs.list(
            ...     campaign_id="camp_123abc",
            ...     status="failed"
            ... )
            >>> print(f"Failed messages in campaign: {len(campaign_messages.messages)}")
        
        Note:
            - Use pagination parameters (page, page_size) to navigate through large result sets
            - Timestamp parameters (start, stop) are in milliseconds since epoch
            - The phone_number parameter matches against both sender and recipient numbers
            - Multiple filter parameters can be combined for more specific queries
            - Results are typically sorted by sent/received time in descending order
              (most recent first)
            - For detailed information about a specific message, use the get() method
              with its message_id
        """
        params = {
            "page": page,
            "pageSize": page_size,
        }

        if start:
            params["start"] = start
        if stop:
            params["stop"] = stop
        if direction:
            params["direction"] = direction
        if status:
            params["status"] = status
        if phone_number:
            params["phoneNumber"] = phone_number
        if client_id:
            params["clientId"] = client_id
        if campaign_id:
            params["campaignId"] = campaign_id
        if broadcast_id:
            params["broadcastId"] = broadcast_id

        # pylint: disable=protected-access
        return ListSMSActivityLogsResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path,
                                             params=params,
                                             headers=self.headers)))

    def get(self, message_id:str):
        """
        Retrieves detailed information about a specific SMS message by its ID.
        
        This method fetches comprehensive details for a single SMS message activity log
        identified by its unique message ID.
        
        Args:
            message_id (str): The unique identifier of the SMS message to retrieve.
        
        Returns:
            GetSMSActivityLogsResponse: 
                A Pydantic model containing detailed information about the message,
            including routing information, content, status, and associated metadata.
        
        Example:
            >>> message = client.sms.activity_logs.get(
            ...     message_id="msg_123abc456def"
            ... )
            >>> print(f"Message from {message.from_} to {message.to}")
            >>> print(f"Content: {message.body}")
            >>> print(f"Status: {message.status}")
            >>> 
            >>> # Check delivery timeline
            >>> if message.direction == "outbound":
            ...     print(f"Sent at: {message.sent_at}")
            ...     if message.delivered_at:
            ...         delivery_time = message.delivered_at - message.submitted_at
            ...         print(f"Delivered at: {message.delivered_at} (took {delivery_time} ms)")
            ...     elif message.status == "failed":
            ...         print(f"Delivery failed: {message.status_reason}")
            >>> else:
            ...     print(f"Received at: {message.received_at}")
        
        Raises:
            NaxaiAPIError: If the message ID doesn't exist or if there's an API error
        
        Note:
            - This method provides complete details about a single message
            - For outbound messages, you can track the full delivery timeline
            - For inbound messages, you can access the complete message content
            - The message_id is typically obtained from the list() method or from send responses
        """
        # pylint: disable=protected-access
        return GetSMSActivityLogsResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path + "/" + message_id,
                                             headers=self.headers)))
