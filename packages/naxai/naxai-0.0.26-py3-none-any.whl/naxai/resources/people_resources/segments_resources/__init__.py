"""
Segment-related resources package for the Naxai People SDK.

This package provides access to segment-specific API resources including:
- Contacts: For managing contacts within segments and performing segment-based operations
"""

from .contacts import SegmentsContactsResource

__all__ = ["SegmentsContactsResource"]
