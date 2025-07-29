"""
People response models for the Naxai SDK.

This module provides data structures for responses from people-related API operations,
including contacts, segments, attributes, exports, and imports management.
"""

from .attributes_responses import (CreateAttributeResponse,
                                   ListAttributesResponse,
                                   GetAttributeResponse)
from .contacts_responses import (SearchContactsResponse,
                                 CountContactsResponse,
                                 GetContactIdentifierResponse,
                                 UpdateContactIdentifierResponse,
                                 CreateOrUpdateContactResponse,
                                 GetContactResponse,
                                 ListSegmentsOfContactResponse)
from .segments_responses import (ListSegmentsResponse,
                                 CreateSegmentResponse,
                                 GetSegmentResponse,
                                 UpdateSegmentResponse,
                                 GetSegmentsHistoryResponse,
                                 CountContactsInSegmentResponse,
                                 GetSegmentUsageResponse,
                                 ListContactsOfSegmentResponse)

__all__ = ["CreateAttributeResponse",
           "ListAttributesResponse",
           "GetAttributeResponse",
           "SearchContactsResponse",
           "CountContactsResponse",
           "GetContactIdentifierResponse",
           "UpdateContactIdentifierResponse",
           "CreateOrUpdateContactResponse",
           "GetContactResponse",
           "ListSegmentsOfContactResponse",
           "ListSegmentsResponse",
           "CreateSegmentResponse",
           "GetSegmentResponse",
           "UpdateSegmentResponse",
           "GetSegmentsHistoryResponse",
           "CountContactsInSegmentResponse",
           "GetSegmentUsageResponse",
           "ListContactsOfSegmentResponse"
]
