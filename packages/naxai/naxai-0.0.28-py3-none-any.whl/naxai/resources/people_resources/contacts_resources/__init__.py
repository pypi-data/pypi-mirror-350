"""
Contact-related resources package for the Naxai People SDK.

This package provides access to contact-specific API resources including:
- Events: For tracking and managing contact events and activities
- Identifier: For looking up contacts by various identifiers
- Segments: For managing contact segment memberships
"""

from .events import EventsResource
from .identifier import IdentifierResource
from .segments import SegmentsResource

__all__ = ["EventsResource",
           "IdentifierResource",
           "SegmentsResource"]
