"""
Voice reporting resources package for the Naxai SDK.

This package provides access to voice call reporting resources including:
- Inbound: For analyzing incoming call metrics and patterns
- Outbound: For tracking outgoing call performance and outcomes
- Transfer: For monitoring call transfer statistics and success rates
"""

from .inbound import InboundResource
from .outbound import OutboundResource
from .transfer import TransferResource

__all__ = ["InboundResource", "OutboundResource", "TransferResource"]
