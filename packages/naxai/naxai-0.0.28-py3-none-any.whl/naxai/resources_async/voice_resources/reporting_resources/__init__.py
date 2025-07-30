"""
Asynchronous voice reporting resources package for the Naxai SDK.

This package provides access to asynchronous voice call reporting resources including:
- Inbound: For analyzing incoming call metrics and patterns
- Outbound: For tracking outgoing call performance and outcomes
- Transfer: For monitoring call transfer statistics and success rates

These resources enable non-blocking access to voice call analytics, allowing for
efficient reporting operations in high-performance asynchronous applications.
"""

from .inbound import InboundResource
from .outbound import OutboundResource
from .transfer import TransferResource

__all__ = ["InboundResource", "OutboundResource", "TransferResource"]
