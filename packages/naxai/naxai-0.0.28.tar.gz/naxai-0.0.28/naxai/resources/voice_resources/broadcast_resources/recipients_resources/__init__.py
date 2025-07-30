"""
Voice broadcast recipients resources package for the Naxai SDK.

This package provides access to resources for managing recipients of voice broadcasts,
including call-specific operations that allow tracking and analyzing individual call
outcomes within a broadcast campaign.
"""

from .calls import CallsResource

__all__ = ["CallsResource"]
