"""
Contact segments resource for the Naxai People SDK.

This module provides methods for retrieving segment memberships for individual contacts
in the Naxai platform. It allows users to determine which segments a specific contact
belongs to, which is useful for understanding how contacts are categorized and which
targeted communications they may receive.

Available Functions:
    list(identifier: str)
        Retrieves all segments that a specific contact belongs to.
        Args:
            identifier (str): Contact's unique identifier (ID, email, phone, or external ID)
        Returns:
            ListSegmentsOfContactResponse: List of segments the contact belongs to

"""

import json
from naxai.models.people.responses.contacts_responses import ListSegmentsOfContactResponse

class SegmentsResource:
    """ segments resource for people.contacts resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}

    def list(self, identifier: str):
        """
        Retrieve all segments that a specific contact belongs to in the Naxai People API.
        
        This method fetches the complete list of segments that the specified contact is a member of.
        This information is useful for understanding how a contact is categorized within your
        segmentation strategy and which targeted communications they may receive.
        
        Args:
            identifier (str): The unique identifier of the contact. This can be the Naxai ID,
                email address, phone number, or external ID depending on your account's
                primary identifier configuration.
        
        Returns:
            ListSegmentsOfContactResponse: A response object containing the list of segments
                that the contact belongs to. Each segment object includes basic information
                such as ID, name, description, and type.
        
        Raises:
            ValueError: If the identifier is empty or invalid.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access segment information.
            NaxaiResourceNotFound: If the specified contact does not exist.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                # Get all segments for a specific contact
                contact_id = "john.doe@example.com"  # Using email as identifier
                response = client.people.contacts.segments.list(identifier=contact_id)
                
                # Display the segments the contact belongs to
                print(f"Contact {contact_id} belongs to {len(response.segments)} segments:")
                
                for segment in response.segments:
                    segment_type = "Manual" if segment.type_ == "manual" else "Dynamic"
                    print(f"- {segment.name} (ID: {segment.id}, Type: {segment_type})")
                    if segment.description:
                        print(f"  Description: {segment.description}")
                
                # Check if the contact is in a specific segment
                target_segment_id = "seg_123abc"
                is_in_segment = any(segment.id == target_segment_id \
                                    for segment in response.segments)
                print(f"Contact is in target segment: {is_in_segment}")
            ```
        
        Note:
            - This method returns only basic segment information
            - For detailed segment definitions including conditions, use the dedicated segment API
            - An empty list indicates the contact doesn't belong to any segments
            - Segment membership can change over time as contacts' attributes and behaviors evolve
            - For dynamic segments, membership is recalculated periodically based on the
              segment conditions
        """
        # pylint: disable=protected-access
        return ListSegmentsOfContactResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path + "/" + identifier + "/segments",
                                             headers=self.headers)))
