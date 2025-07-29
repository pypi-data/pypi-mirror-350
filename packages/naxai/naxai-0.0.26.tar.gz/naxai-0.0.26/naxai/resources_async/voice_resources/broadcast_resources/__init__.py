"""
Asynchronous voice broadcast resources package for the Naxai SDK.

This package provides access to asynchronous resources for managing voice broadcast campaigns,
including metrics analysis and recipient management. These resources help users track
performance, engagement, and delivery outcomes for voice broadcasts sent through the
Naxai platform in a non-blocking manner suitable for high-performance asynchronous applications.
"""

from .metrics import MetricsResource
from .recipients import RecipientsResource

__all__ = ["MetricsResource", "RecipientsResource"]
