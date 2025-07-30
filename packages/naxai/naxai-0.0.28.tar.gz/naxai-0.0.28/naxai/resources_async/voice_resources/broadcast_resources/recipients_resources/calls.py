"""
Asynchronous voice broadcast recipient calls resource for the Naxai SDK.

This module provides asynchronous methods for retrieving and analyzing call attempts made
to individual recipients within voice broadcast campaigns. It allows users to track call
statuses, durations, outcomes, and retry attempts for specific recipients in a non-blocking
manner, helping to understand delivery effectiveness and recipient engagement patterns in
high-performance asynchronous applications.

Available Functions:
    list(broadcast_id: str, recipient_id: str)
        Retrieves a list of call attempts made to a specific recipient within a voice broadcast.
        Returns details like call status, duration, attempt order and timestamps.

"""

import json
from naxai.models.voice.responses.broadcasts_responses import GetBroadcastRecipientCallsResponse

class CallsResource:
    """
    This class represents the CallsResource, which provides methods to interact with the
    broadcast recipients calls API.
    """

    def __init__(self, client, root_path: str):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}

    async def list(self, broadcast_id: str, recipient_id: str):
        """
        Get the recipient calls for a voice broadcast by broadcast id and recipient id.

        Args:
            broadcast_id (str): The unique identifier of the broadcast.
            recipient_id (str): The unique identifier of the recipient.

        Returns:
            GetBroadcastRecipientCallsResponse: A Pydantic model containing a list of call attempts 
            for the specified recipient. Each call attempt includes details such as:
                - callId: Unique identifier for the call
                - status: Call status (delivered, failed, scheduled, canceled)
                - reason: Detailed reason for the call outcome
                - attemptOrder: Sequential number of the call attempt
                - duration: Duration of the call in seconds
                - callAt: Timestamp when the call was made/scheduled

        Example:
            >>> calls = await client.voice.broadcasts.recipients.calls.list(
            ...     broadcast_id="XXXXXXXXX",
            ...     recipient_id="XXXXXXXXX"
            ... )
            >>> print(f"Total call attempts: {len(calls)}")
            >>> if len(calls) > 0:
            ...     print(f"Last call status: {calls[-1].status}")
            ...     print(f"Call duration: {calls[-1].duration} seconds")
        """
        url = self.root_path + "/" + broadcast_id + "/recipients/" + recipient_id + "/calls"
        # pylint: disable=protected-access
        return GetBroadcastRecipientCallsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   url,
                                                   headers=self.headers)))
