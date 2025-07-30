"""
Segment contacts resource for the Naxai People SDK.

This module provides methods for managing contacts within segments in the Naxai platform,
including adding and removing contacts from manual segments, counting segment members,
and retrieving contacts that belong to specific segments. These operations are essential
for targeted audience management and campaign planning.

Available Functions:
    add(segment_id: str, contact_ids: list[str])
        Add contacts to a manual segment.
        
    delete(segment_id: str, contact_ids: list[str]) 
        Remove contacts from a manual segment.
        
    count(segment_id: str) -> CountContactsInSegmentResponse
        Count the number of contacts in a segment.
        
    list(segment_id: str, page: Optional[int], size: Optional[int]) -> ListContactsOfSegmentResponse
        List contacts that belong to a segment with pagination support.

"""

import json
from typing import Optional
from pydantic import Field, validate_call
from naxai.models.people.responses.segments_responses import (CountContactsInSegmentResponse,
                                                              ListContactsOfSegmentResponse)



class SegmentsContactsResource:
    """contact resource for segments resource"""

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}

    @validate_call
    def add(self, segment_id: str, contact_ids: list[str] = Field(min_length=1)):
        """
        Add contacts to a manual segment in the Naxai People API.
        
        This method allows you to add one or more contacts to a manual segment by their IDs.
        This operation is only applicable to manual segments; dynamic segments automatically
        include contacts based on their defined conditions.
        
        Args:
            segment_id (str): The unique identifier of the segment to add contacts to.
            contact_ids (list[str]): A list of contact IDs to add to the segment.
                Must contain at least one ID.
                examples:
                nxid:
                value: "nxid_{contact_id}"
                phone:
                value: "32478123412"
                email:
                value: "john@example.com"
                externalId:
                value: "ABCD1234"
        
        Returns:
            None
        
        Raises:
            ValueError: If segment_id is empty or contact_ids is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to modify segments.
            NaxaiResourceNotFound: If the specified segment or any of the contacts do not exist.
            NaxaiInvalidRequestError: If the segment is not a manual segment.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                # Add multiple contacts to a manual segment
                segment_id = "seg_123abc"
                contacts_to_add = ["cnt_456def", "cnt_789ghi", "cnt_012jkl"]
                
                try:
                    response = client.people.segments.contacts.add(
                        segment_id=segment_id,
                        contact_ids=contacts_to_add
                    )
                except Exception as e:
                    print(f"Error adding contacts to segment: {str(e)}")
            ```
        
        Note:
            - This method only works with manual segments
            - For dynamic segments, contacts are automatically included based on segment conditions
            - All contacts must exist in your account before they can be added to a segment
            - If a contact is already in the segment, adding it again has no effect
            - This operation is idempotent - calling it multiple times with the same parameters
            will not result in duplicate contacts in the segment
        """
        # pylint: disable=protected-access
        return self._client._request("POST",
                                     self.root_path + "/" + segment_id + "/addContacts",
                                     json={"ids": contact_ids},
                                     headers=self.headers)

    @validate_call
    def delete(self, segment_id: str, contact_ids: list[str] = Field(min_length=1)):
        """
        Remove contacts from a manual segment in the Naxai People API.
        
        This method allows you to remove one or more contacts from a manual segment by their IDs.
        This operation is only applicable to manual segments; dynamic segments automatically
        include or exclude contacts based on their defined conditions.
        
        Args:
            segment_id (str): The unique identifier of the segment to remove contacts from.
            contact_ids (list[str]): A list of contact IDs to remove from the segment.
                Must contain at least one ID.
                examples:
                nxid:
                value: "nxid_{contact_id}"
                phone:
                value: "32478123412"
                email:
                value: "john@example.com"
                externalId:
                value: "ABCD1234"
        
        Returns:
            None
        
        Raises:
            ValueError: If segment_id is empty or contact_ids is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to modify segments.
            NaxaiResourceNotFound: If the specified segment does not exist.
            NaxaiInvalidRequestError: If the segment is not a manual segment.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                # Remove contacts from a manual segment
                segment_id = "seg_123abc"
                contacts_to_remove = ["cnt_456def", "cnt_789ghi"]
                
                try:
                    response = client.people.segments.contacts.delete(
                        segment_id=segment_id,
                        contact_ids=contacts_to_remove
                    )
                    
                    print(f"Contacts removed from segment: {len(contacts_to_remove)}")
                    print(f"Response: {response}")
                except Exception as e:
                    print(f"Error removing contacts from segment: {str(e)}")
            ```
        
        Note:
            - This method only works with manual segments
            - For dynamic segments, contacts cannot be manually removed
            - If a contact is not in the segment, removing it has no effect
            - The operation is idempotent - calling it multiple times with the same parameters
            will not result in an error
        """
        # pylint: disable=protected-access
        return self._client._request("POST",
                                     self.root_path + "/" + segment_id + "/deleteContacts",
                                     json={"ids": contact_ids},
                                     headers=self.headers)

    def count(self, segment_id: str):
        """
        Count the number of contacts in a segment in the Naxai People API.
        
        This method retrieves the total number of contacts that belong to the specified segment.
        This count is useful for understanding segment size and for planning communications
        or campaigns that target the segment.
        
        Args:
            segment_id (str): The unique identifier of the segment to count contacts in.
        
        Returns:
            int: The count of contacts in the segment.
        
        Raises:
            ValueError: If segment_id is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access segment information.
            NaxaiResourceNotFound: If the specified segment does not exist.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                # Count contacts in a segment
                segment_id = "seg_123abc"
                
                try:
                    response = client.people.segments.contacts.count(segment_id=segment_id)
                    
                    print(f"Segment {segment_id} contains {response} contacts")
                    
                    # Use the count for planning
                    if response > 10000:
                        print("Large segment - consider batch processing")
                    elif response == 0:
                        print("Empty segment - no contacts to process")
                    else:
                        print(f"Processing {response} contacts")
                except Exception as e:
                    print(f"Error counting contacts in segment: {str(e)}")
            ```
        
        Note:
            - This method works with both manual and dynamic segments
            - For large segments, the count operation is optimized and faster than
              retrieving all contacts
            - The count represents the current state and may change as contacts are added/removed
              or as they meet/no longer meet the criteria for dynamic segments
        """
        # pylint: disable=protected-access
        return CountContactsInSegmentResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path + "/" + segment_id + "/countContacts",
                                             headers=self.headers))).count

    @validate_call
    def list(self,
            segment_id: str,
            page: Optional[int] = Field(default=1),
            page_size: Optional[int] = Field(default=50),
            sort: Optional[str] = Field(default="createdAt:desc")
            ):
        """
        Retrieve contacts that belong to a specific segment in the Naxai People API.
        
        This method fetches a paginated list of contacts that are members of the specified segment.
        The results can be sorted and paginated to handle large segments efficiently.
        
        Args:
            segment_id (str): The unique identifier of the segment to list contacts from.
            page (Optional[int]): The page number to retrieve, starting from 1.
                Defaults to 1 (first page).
            page_size (Optional[int]): Number of contacts to return per page.
                Defaults to 50. Maximum value may be limited by the API.
            sort (Optional[str]): Sorting criteria in the format "field:direction".
                Defaults to "createdAt:desc" (newest contacts first).
                Examples: "email:asc", "createdAt:desc", "lastName:asc"
        
        Returns:
            ListContactsOfSegmentResponse: A response object containing the paginated list
                of contacts in the segment and pagination information.
        
        Raises:
            ValueError: If segment_id is empty or pagination parameters are invalid.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access segment information.
            NaxaiResourceNotFound: If the specified segment does not exist.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                # List contacts in a segment with pagination
                segment_id = "seg_123abc"
                
                # Get the first page of contacts
                first_page = client.people.segments.contacts.list(
                    segment_id=segment_id,
                    page=1,
                    page_size=25,
                    sort="email:asc"  # Sort alphabetically by email
                )
                
                print(f"Page {first_page.pagination.page} of {first_page.pagination.total_pages}")
                print(f"Showing {len(first_page.contacts)} of "
                      f"{first_page.pagination.total_items} contacts")
                
                # Display the contacts on this page
                for contact in first_page.contacts:
                    print(f"- {contact.email or 'No email'} (ID: {contact.nx_id})")
                
                # If there are more pages, fetch the next one
                if first_page.pagination.has_more_pages:
                    second_page = client.people.segments.contacts.list(
                        segment_id=segment_id,
                        page=2,
                        page_size=25,
                        sort="email:asc"
                    )
                    print(f"\nFetched page 2 with {len(second_page.contacts)} more contacts")
            ```
        
        Note:
            - This method works with both manual and dynamic segments
            - For large segments, use pagination to retrieve contacts in manageable batches
            - The sort parameter accepts various contact fields with "asc" or "desc" direction
            - Contact data may include custom attributes beyond the standard fields
            - For very large segments, consider using the count method first to determine
            the total number of contacts before retrieving them
        """
        params = {"page": page, "pageSize": page_size, "sort": sort}
        # pylint: disable=protected-access
        return ListContactsOfSegmentResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path + "/" + segment_id + "/members",
                                             headers=self.headers,
                                             params=params)))
