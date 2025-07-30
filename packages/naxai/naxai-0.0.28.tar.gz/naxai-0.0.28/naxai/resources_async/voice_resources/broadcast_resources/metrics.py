"""
Asynchronous voice broadcast metrics resource for the Naxai SDK.

This module provides asynchronous methods for retrieving and analyzing performance metrics
for voice broadcast campaigns, including call outcome statistics, delivery rates, and
engagement data. It also serves as a container for more specialized metrics resources such
as input tracking, helping users evaluate the effectiveness of their voice broadcasts in a
non-blocking manner suitable for high-performance asynchronous applications.

Available Functions:
    get(broadcast_id: str):
        Retrieves detailed metrics for a specific voice broadcast campaign,
        including call outcomes, delivery rates, and engagement statistics.

Sub-resources:
    input:
        A subresource for tracking and analyzing input metrics in voice broadcasts.
        See InputResource for detailed documentation.

"""

import json
from naxai.models.voice.responses.broadcasts_responses import GetBroadcastMetricsResponse
from .broadcast_metrics_resources.input import InputResource

class MetricsResource:
    """
    A class for handling metrics-related operations for voice broadcasts.
    """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.input = InputResource(client, root_path)
        self.headers = {"Content-Type": "application/json"}

    async def get(self, broadcast_id: str):
        """
        Get the metrics for a voice broadcast by id.
        
        Args:
            broadcast_id (str): The unique identifier of the broadcast.
            
        Returns:
            GetBroadcastMetricsResponse: 
            A Pydantic model containing detailed metrics for the broadcast campaign,
            including:
                - total: Total number of calls attempted
                - completed: Number of calls successfully completed
                - delivered: Number of calls successfully delivered
                - failed: Number of failed calls
                - canceled: Number of canceled calls
                - paused: Number of paused calls
                - invalid: Number of invalid call attempts
                - in_progress: Number of calls currently being executed
                - transferred: Number of transferred calls
                - calls: Total number of call attempts made
            
        Example:
            >>> metrics = await client.voice.broadcasts.metrics.get(
            ...     broadcast_id="XXXXXXXXX"
            ... )
            >>> print(f"Total recipients: {metrics.total}")
            >>> print(f"Completed: {metrics.completed} "
            >>>       f"({metrics.completed/metrics.total*100:.1f}%)")
            >>> print(f"Failed: {metrics.failed}")
        """
        # pylint: disable=protected-access
        return GetBroadcastMetricsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/" + broadcast_id + "/metrics",
                                                   headers=self.headers)))
