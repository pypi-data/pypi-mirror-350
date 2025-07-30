"""
People resource for the Naxai SDK.

This module provides comprehensive customer data management capabilities for the Naxai platform,
including contact profiles, custom attributes, segmentation, data imports, and exports.
It serves as a central access point for all customer data operations, enabling users to
create, manage, and analyze their customer database for targeted communications and
personalized experiences.

Sub-resources:
    attributes:
        A subresource for managing custom attributes for contacts.
        See AttributesResource for detailed documentation.

    contacts:
        A subresource for managing contact profiles and data.
        See ContactsResource for detailed documentation.

    segments:
        A subresource for managing contact segments and segmentation.
        See SegmentsResource for detailed documentation.

"""

from .people_resources.attributes import AttributesResource
from .people_resources.contacts import ContactsResource
from .people_resources.segments import SegmentsResource

class PeopleResource:
    """
    Provides access to people related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.root_path = "/people"
        self.attributes: AttributesResource = AttributesResource(self._client, self.root_path)
        self.contacts: ContactsResource = ContactsResource(self._client, self.root_path)
        self.segments: SegmentsResource = SegmentsResource(self._client, self.root_path)
