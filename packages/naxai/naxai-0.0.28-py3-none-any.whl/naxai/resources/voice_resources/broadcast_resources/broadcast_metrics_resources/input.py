"""
Voice broadcast input metrics resource for the Naxai SDK.

This module provides methods for retrieving and analyzing DTMF input metrics from voice
broadcasts, allowing users to track how recipients interact with interactive voice
messages by pressing keys on their phone keypads. These metrics help measure engagement
and response rates for voice broadcast campaigns.

Available Functions:
    get(broadcast_id: str)
        Get DTMF input metrics for a specific voice broadcast.
        Args:
            broadcast_id (str): ID of the broadcast to get metrics for
        Returns:
            GetBroadcastInputMetricsResponse: Input metrics including counts for each DTMF key

"""

import json
from naxai.models.voice.responses.broadcasts_responses import GetBroadcastInputMetricsResponse

class InputResource:
    """
    This class provides methods to interact with the Voice Broadcast Metrics Input resource
    in the API.

    """
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}

    def get(self, broadcast_id: str):
        """
        Get the inputs for a voice broadcast by id.
        https://docs.naxai.com/reference/voicebroadcastmetricsinputgetbyid

        Args:
            broadcast_id (str): The unique identifier of the broadcast to get the inputs.
            
        Returns:
            GetBroadcastInputMetricsResponse: 
                A Pydantic model containing the input counts for the given broadcast.
                The model includes counts for each DTMF key (0-9, *, #) and a total count.
                
        Example:
            >>> input_result = client.voice.broadcasts.metrics.inputs.get(
            ...     broadcast_id="XXXXXXXXX"
            ... )
            >>> print(f"Total inputs received: {input_result.total}")
            >>> print(f"Option 1 selected: {input_result.input_1} times")
        """
        # pylint: disable=protected-access
        return GetBroadcastInputMetricsResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path + "/" + broadcast_id + "/metrics/input",
                                             headers=self.headers)))
