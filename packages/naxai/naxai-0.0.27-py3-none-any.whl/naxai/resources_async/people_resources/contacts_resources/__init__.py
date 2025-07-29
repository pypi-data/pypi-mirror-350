"""
Asynchronous contact-related resources package for the Naxai People SDK.

This package provides access to asynchronous contact-specific API resources including:
- Events: For tracking and managing contact events and activities
- Identifier: For looking up contacts by various identifiers
- Segments: For managing contact segment memberships

These resources enable non-blocking access to contact management functionality,
allowing for efficient contact operations in asynchronous applications.
"""

from .events import EventsResource
from .identifier import IdentifierResource
from .segments import SegmentsResource

__all__ = ["EventsResource",
           "IdentifierResource",
           "SegmentsResource"]
