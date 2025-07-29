"""
People resources package for the Naxai SDK.

This package provides access to customer data management resources including:
- Attributes: For managing custom contact properties and fields
- Contacts: For creating and managing individual customer profiles
- Segments: For grouping contacts based on attributes and behaviors
"""

from .attributes import AttributesResource
from .contacts import ContactsResource
from .segments import SegmentsResource

__all__ = ["AttributesResource",
           "ContactsResource",
           "SegmentsResource"
        ]
