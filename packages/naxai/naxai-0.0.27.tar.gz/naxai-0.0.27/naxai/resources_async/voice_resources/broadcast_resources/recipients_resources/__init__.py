"""
Asynchronous voice broadcast recipients resources package for the Naxai SDK.

This package provides access to asynchronous resources for managing recipients of voice
broadcasts, including call-specific operations that allow tracking and analyzing individual
call outcomes within a broadcast campaign in a non-blocking manner suitable for
high-performance asynchronous applications.
"""

from .calls import CallsResource

__all__ = ["CallsResource"]
