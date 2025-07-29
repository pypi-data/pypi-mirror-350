"""
Voice reporting resource for the Naxai SDK.

This module serves as a container for specialized voice call reporting resources,
providing access to comprehensive metrics and analytics for different call types.
It includes resources for analyzing outbound calls, inbound calls, and call transfers,
enabling users to monitor and optimize their voice communication performance.

Sub-resources:
    outbound:
        A subresource for retrieving and analyzing outbound call metrics.
        Provides methods for analyzing call volumes, delivery rates, and geographical distribution.
        See OutboundResource for detailed documentation.

    inbound:
        A subresource for retrieving and analyzing inbound call metrics.
        Provides methods for analyzing incoming call patterns and handling statistics.
        See InboundResource for detailed documentation.

    transfer:
        A subresource for retrieving and analyzing transferred call metrics.
        Provides methods for analyzing call transfer volumes, success rates, and durations.
        See TransferResource for detailed documentation.

"""

from .reporting_resources.outbound import OutboundResource
from .reporting_resources.inbound import InboundResource
from .reporting_resources.transfer import TransferResource

class ReportingResource:
    """ reporting resource for voice resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/reporting/metrics"
        self.outbound: OutboundResource = OutboundResource(self._client, self.root_path)
        self.inbound: InboundResource = InboundResource(self._client, self.root_path)
        self.transfer: TransferResource = TransferResource(self._client, self.root_path)
