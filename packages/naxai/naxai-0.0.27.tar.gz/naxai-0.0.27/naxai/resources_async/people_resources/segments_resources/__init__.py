"""
Asynchronous segment-related resources package for the Naxai People SDK.

This package provides access to asynchronous segment-specific API resources including:
- Contacts: For managing contacts within segments and performing segment-based operations

These resources enable non-blocking access to segment management functionality,
allowing for efficient segment operations in asynchronous applications.
"""

from .contacts import SegmentsContactsResource

__all__ = ["SegmentsContactsResource"]
