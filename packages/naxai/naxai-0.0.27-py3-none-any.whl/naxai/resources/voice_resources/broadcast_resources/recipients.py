"""
Voice broadcast recipients resource for the Naxai SDK.

This module provides methods for managing and analyzing recipients of voice broadcast
campaigns, including listing recipients with various filtering options and retrieving
detailed information about specific recipients. It also serves as a container for more
specialized recipient resources such as call tracking, helping users understand delivery
outcomes and recipient engagement.

Available Functions:
    list(broadcast_id: str, page=1, page_size=25, phone=None, completed=None, status=None)
        Retrieves a paginated list of recipients for a voice broadcast with optional filtering.
        Args:
            broadcast_id: ID of the broadcast to get recipients for
            page: Page number to retrieve (default: 1)
            page_size: Number of items per page (default: 25, max: 100)
            phone: Filter by recipient phone number
            completed: Filter by completion status
            status: Filter by delivery status
        Returns:
            ListBroadcastRecipientsResponse: List of recipients with pagination info

    get(broadcast_id: str, recipient_id: str)
        Retrieves detailed information about a specific recipient.
        Args:
            broadcast_id: ID of the broadcast
            recipient_id: ID of the recipient
        Returns:
            GetBroadcastRecipientResponse: Detailed recipient information

Sub-resources:
    calls:
        A subresource for tracking call attempts made to recipients.
        See CallsResource for detailed documentation.

"""

import json
from typing import Annotated, Literal, Optional
from pydantic import Field, validate_call
from naxai.models.voice.responses.broadcasts_responses import (ListBroadcastRecipientsResponse,
                                                               GetBroadcastRecipientResponse)
from .recipients_resources.calls import CallsResource

class RecipientsResource:
    """
        A class for handling recipients-related operations for voice broadcasts.
    """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.calls = CallsResource(client, root_path)
        self.headers = {"Content-Type": "application/json"}


    @validate_call
    def list(self,
            broadcast_id: str,
            page: Optional[int] = 1,
            page_size: Annotated[Optional[int], Field(ge=1, le=100)] = 25,
            phone: Optional[str] = None,
            completed: Optional[bool] = None,
            status: Optional[Literal["delivered", "failed", "in-progress",
                                     "canceled", "invalid", "paused"]] = None):

        """
        Get the recipients for a voice broadcast by broadcast id.
        
        Args:
            broadcast_id (str): The unique identifier of the broadcast.
            page (Optional[int]): Page number to retrieve. Defaults to 1.
            page_size (Optional[int]): Number of items to list per page. Defaults to 25.
            phone (Optional[str]): If provided, only results for this phone number will be returned.
            completed (Optional[bool]): 
                If set, only recipients who completed the broadcast will be returned.
            status (Optional[Literal["delivered",
                                     "failed",
                                     "in-progress",
                                     "canceled",
                                     "invalid",
                                     "paused"]]):
                    If provided, only recipients with provided status will be returned.
            
        Returns:
            ListBroadcastRecipientsResponse: A Pydantic model containing a paginated list of
            broadcast recipients.
            The response includes:
                - items: List of BroadcastRecipient objects with details about each recipient
                - pagination: Information about the current page, total pages, and total items
            
        Example:
            >>> response = client.voice.broadcasts.recipients.list(
            ...     broadcast_id="XXXXXXXXX",
            ...     page=1,
            ...     page_size=50,
            ...     status="delivered"
            ... )
            >>> print(f"Found {len(response.items)} recipients")
            >>> print(f"Page {response.pagination.page} of {response.pagination.total_pages}")
            >>> for recipient in response.items:
            ...     print(f"Phone: {recipient.phone}, Status: {recipient.status}")
        """
        params = {"page": page, "pagesize": page_size}
        if phone is not None:
            params["phone"] = phone
        if completed is not None:
            params["completed"] = completed
        if status is not None:
            params["status"] = status
        # pylint: disable=protected-access
        return ListBroadcastRecipientsResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path + "/" + broadcast_id + "/recipients",
                                             params=params,
                                             headers=self.headers)))

    def get(self, broadcast_id: str, recipient_id: str):
        """
        Get the recipient details for a voice broadcast by broadcast id and recipient id.
        
        Args:
            broadcast_id (str): The unique identifier of the broadcast.
            recipient_id (str): The unique identifier of the recipient.
            
        Returns:
            GetBroadcastRecipientResponse: 
                A Pydantic model containing detailed information about a specific
            broadcast recipient, including:
                - recipient_id: Unique identifier for the recipient
                - broadcast_id: Identifier of the broadcast campaign
                - phone: Recipient's phone number
                - status: Current delivery status
                - completed: Whether the broadcast was completed for this recipient
                - calls: Number of call attempts made
                - input_: DTMF input received from the recipient (if any)
                - transferred: Whether the recipient was transferred
                - last_updated_at: Timestamp of the last status update
            
        Example:
            >>> recipient = client.voice.broadcasts.recipients.get(
            ...     broadcast_id="XXXXXXXXX",
            ...     recipient_id="XXXXXXXXX"
            ... )
            >>> print(f"Recipient {recipient.phone}")
            >>> print(f"Status: {recipient.status}")
            >>> print(f"Call attempts: {recipient.calls}")
        """
        url = self.root_path + "/" + broadcast_id + "/recipients/" + recipient_id
        # pylint: disable=protected-access
        return GetBroadcastRecipientResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             url,
                                             headers=self.headers )))
