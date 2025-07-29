"""
Asynchronous voice broadcast metrics resources package for the Naxai SDK.

This package provides access to specialized asynchronous metrics resources for voice broadcasts,
including input metrics that help analyze the performance and effectiveness of voice broadcast
campaigns in a non-blocking manner suitable for high-performance asynchronous applications.
"""

from .input import InputResource

__all__ = ["InputResource"]
