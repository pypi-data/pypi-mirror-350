"""
Contacts resource for the Naxai People SDK.

This module provides methods for managing contacts in the Naxai platform,
including searching, counting, creating, updating, and retrieving individual
contact profiles. It also serves as a container for more specialized contact
resources such as events, identifiers, and segment memberships.

Available Functions:
    search(page, page_size, sort, condition) -> SearchContactsResponse
        Search for contacts with pagination, sorting and filtering options.
        
    count(condition) -> CountContactsResponse 
        Count total contacts matching the given search condition.
        
    create_or_update(contact_data) -> CreateOrUpdateContactResponse
        Create a new contact or update an existing one.
        
    get(contact_id) -> GetContactResponse
        Retrieve a specific contact by ID.

    delete(identifier: str) -> None
        Delete a contact from the system.
        Permanently removes the contact and all associated data.

Sub-resources:
    events: Methods for managing contact events
    identifier: Methods for contact identification 
    segments: Methods for managing contact segments

"""

import json
from typing import Optional, Union
from pydantic import Field, validate_call
from naxai.models.people.helper_models.search_condition import SearchCondition
from naxai.models.people.responses.contacts_responses import (SearchContactsResponse,
                                                              CountContactsResponse,
                                                              CreateOrUpdateContactResponse,
                                                              GetContactResponse)
from .contacts_resources.events import EventsResource
from .contacts_resources.identifier import IdentifierResource
from .contacts_resources.segments import SegmentsResource

class ContactsResource:
    """ contacts resource for people resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/contacts"
        self.headers = {"Content-Type": "application/json"}
        self.events: EventsResource = EventsResource(client, self.root_path)
        self.identifier: IdentifierResource = IdentifierResource(client, self.root_path)
        self.segments: SegmentsResource = SegmentsResource(client, self.root_path)

    @validate_call
    # pylint: disable=protected-access
    def search(self,
                page: Optional[int] = Field(default=1, ge=1),
                page_size: Optional[int] = Field(default=50, ge=1),
                sort: Optional[str] = Field(default="createdAt:desc"),
                condition: Optional[Union[dict, SearchCondition]] = Field(default=None)):
        """
        Search for contacts in the Naxai People API based on specified criteria.
        
        This method allows you to search for contacts using various filtering conditions,
        with support for pagination and sorting of results. You can search based on standard
        contact fields as well as custom attributes.
        
        Args:
            page (Optional[int]): The page number to retrieve, starting from 1.
                Defaults to 1 (first page). Must be greater than 0.
            page_size (Optional[int]): Number of contacts to return per page.
                Defaults to 50. Must be greater than 0.
            sort (Optional[str]): Sorting criteria in the format "field:direction".
                Defaults to "createdAt:desc" (newest contacts first).
                Examples: "email:asc", "createdAt:desc", "lastName:asc"
            condition (Optional[Union[dict, SearchCondition]]): 
                Search conditions to filter contacts.
                Can be provided as a SearchCondition object or a dictionary with the same structure.
                Defaults to None (no filtering).
        
        Returns:
            SearchContactsResponse: A response object containing the paginated list of
                matching contacts and pagination information.
        
        Raises:
            ValueError: If pagination parameters are invalid.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to search contacts.
            NaxaiInvalidRequestError: If the search condition is invalid.
        
        Example:
            ```python
            from naxai.models.people.search_condition import SearchCondition
            
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # Simple search with default parameters (first page, sorted by creation date)
                    basic_results = client.people.contacts.search()
                    print(f"Found {basic_results.pagination.total_items} total contacts")
                    
                    # Advanced search with conditions
                    condition = SearchCondition(
                        all=[
                            {"attribute": {"field": "country", "operator": "eq", "value": "US"}},
                            {"attribute": {"field": "subscription_status",
                                           "operator": "eq", "value": "active"}}
                        ]
                    )
                    
                    # Search with pagination, sorting, and conditions
                    results = client.people.contacts.search(
                        page=1,
                        page_size=25,
                        sort="email:asc",  # Sort alphabetically by email
                        condition=condition
                    )
                    
                    print(f"Found {results.pagination.total_items} matching contacts")
                    print(f"Showing page {results.pagination.page} of "
                          f"{results.pagination.total_pages}")
                    
                    # Process the contacts on this page
                    for contact in results.contacts:
                        print(f"- {contact.email or 'No email'} (ID: {contact.nx_id})")
                        
                        # Access custom attributes if they exist
                        if hasattr(contact, "subscription_status"):
                            print(f"  Subscription: {contact.subscription_status}")
                        if hasattr(contact, "country"):
                            print(f"  Country: {contact.country}")
                    
                    # If there are more pages, fetch the next one
                    if results.pagination.has_more_pages:
                        next_page = client.people.contacts.search(
                            page=results.pagination.next_page,
                            page_size=25,
                            sort="email:asc",
                            condition=condition
                        )
                        print(f"\nFetched page {next_page.pagination.page} with "
                              f"{len(next_page.contacts)} more contacts")
                        
                except Exception as e:
                    print(f"Error searching contacts: {str(e)}")
            ```
        
        Note:
            - For complex searches, use the SearchCondition class to build structured queries
            - The condition parameter supports logical operators (all/any) and various
              comparison operators
            - For large result sets, use pagination to retrieve contacts in manageable batches
            - The sort parameter accepts various contact fields with "asc" or "desc" direction
            - Contact data may include custom attributes beyond the standard fields
            - Search is case-insensitive for string fields
        """
        params = {"page": page, "pageSize": page_size, "sort": sort}

        body_params = condition.model_dump(by_alias=True, exclude_none=True) \
                      if isinstance(condition, SearchCondition) else condition
        if body_params:
            json_body = {"condition": condition}

            results = self._client._request("POST",
                                            self.root_path,
                                            params=params,
                                            json=json_body,
                                            headers=self.headers)
        else:
            results = self._client._request("POST",
                                            self.root_path,
                                            params=params,
                                            headers=self.headers)

        return SearchContactsResponse.model_validate_json(json.dumps(results))


    def count(self):
        """
        Count the total number of contacts in your Naxai People API account.
        
        This method retrieves the total count of contacts in your account, which is useful
        for understanding the size of your contact database and for planning operations
        that might affect all contacts.
        
        Returns:
            int: the count of contacts.
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access contact information.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # Get the total number of contacts
                    response = client.people.contacts.count()
                    
                    total_contacts = response
                    print(f"Total contacts in account: {total_contacts}")
                    
                    # Use the count for planning
                    if total_contacts > 10000:
                        print("Large contact database - consider batch processing for operations")
                    elif total_contacts == 0:
                        print("No contacts found - you may need to import contacts first")
                    else:
                        print(f"Processing {total_contacts} contacts")
                        
                except Exception as e:
                    print(f"Error counting contacts: {str(e)}")
            ```
        
        Note:
            - This method returns the total count across all contacts in your account
            - For counting contacts in specific segments, use the segments.contacts.count method
            - For counting contacts matching specific criteria, use the search method
              with conditions and check the pagination.total_items value
            - The count represents the current state and may change as contacts are added or removed
        """
        # pylint: disable=protected-access
        return CountContactsResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path + "/count",
                                             headers=self.headers))).count

    #TODO: email validation, phone validation
    @validate_call
    def create_or_update(self,
                        identifier: str,
                        email: Optional[str] = None,
                        external_id: Optional[str] = None,
                        unsubscribe: Optional[bool] = None,
                        language: Optional[str] = None,
                        created_at: Optional[int] = Field(ge=2208988800,
                                                          le=4102444800,
                                                          default=None),
                        **kwargs):
        """
        Create a new contact or update an existing one in the Naxai People API.
        
        This method creates a new contact if the identifier doesn't exist, or updates an
        existing contact if it does. It allows you to set or update standard contact fields
        as well as any custom attributes.
        
        Args:
            identifier (str): The unique identifier for the contact. This can be the Naxai ID,
                email address, phone number, or external ID depending on your account's
                primary identifier configuration.
            email (Optional[str]): The contact's email address. Defaults to None.
            external_id (Optional[str]): An external identifier for the contact, typically
                from your own system. Defaults to None.
            unsubscribe (Optional[bool]): Whether the contact has unsubscribed from communications.
                Defaults to None.
            language (Optional[str]): The contact's preferred language code (e.g., "en", "fr").
                Defaults to None.
            created_at (Optional[int]): Timestamp when the contact was created in your system.
                Must be between Jan 1, 2040 and Jan 1, 2100 (Unix timestamp in milliseconds).
                Defaults to None.
            **kwargs: Additional fields to set on the contact, including custom attributes.
                These will be sent as-is to the API.
        
        Returns:
            CreateOrUpdateContactResponse: A response object containing the contact information
                after the create or update operation.
        
        Raises:
            ValueError: If required parameters are invalid.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to create or update contacts.
            NaxaiInvalidRequestError: If the request contains invalid data.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # Create or update a contact using email as the identifier
                    response = client.people.contacts.create_or_update(
                        identifier="john.doe@example.com",
                        email="john.doe@example.com",  # Same as identifier in this case
                        external_id="cust_12345",
                        language="en",
                        # Custom attributes
                        first_name="John",
                        last_name="Doe",
                        company="Acme Inc.",
                        loyalty_tier="Gold",
                        signup_date=1672531200000,  # Jan 1, 2023
                        preferences={
                            "marketing_emails": True,
                            "product_updates": True
                        }
                    )
                    
                    # Check if this was a create or update operation
                    if response.created_at == response.created_at_naxai:
                        print(f"Created new contact: {response.email} (ID: {response.nx_id})")
                    else:
                        print(f"Updated existing contact: {response.email} (ID: {response.nx_id})")
                    
                    # Access standard fields
                    print(f"External ID: {response.external_id}")
                    print(f"Language: {response.language}")
                    
                    # Access custom attributes
                    print(f"Name: {response.first_name} {response.last_name}")
                    print(f"Loyalty tier: {response.loyalty_tier}")
                    
                except Exception as e:
                    print(f"Error creating or updating contact: {str(e)}")
            ```
        
        Note:
            - This is an upsert operation - it will create or update depending on whether
              the contact exists
            - Only the fields you provide will be updated; omitted fields will remain unchanged
            - Custom attributes must be created first using the attributes.create method
            - The identifier used must match your account's primary identifier type
            - Email addresses should be valid and properly formatted
            - The created_at timestamp allows you to preserve the original creation date
              from your system
            - For bulk operations, consider using the batch API endpoints
        """
        data = {
            "email": email,
            "externalId": external_id,
            "unsubscribe": unsubscribe,
            "language": language,
            "createdAt": created_at,
            **kwargs
        }
        # pylint: disable=protected-access
        return CreateOrUpdateContactResponse.model_validate_json(
            json.dumps(self._client._request("PUT",
                                             self.root_path + "/" + identifier,
                                             json=data,
                                             headers=self.headers)))

    def get(self, identifier: str):
        """
        Retrieve a specific contact from the Naxai People API.
        
        This method fetches detailed information about a single contact, including standard
        fields and any custom attributes that have been set.
        
        Args:
            identifier (str): The unique identifier of the contact to retrieve. This can be
                the Naxai ID, email address, phone number, or external ID depending on your
                account's primary identifier configuration.
        
        Returns:
            GetContactResponse: A response object containing the contact's information.
        
        Raises:
            ValueError: If the identifier is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access contact information.
            NaxaiResourceNotFound: If the specified contact does not exist.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # Retrieve a contact by email
                    contact_id = "john.doe@example.com"
                    contact = client.people.contacts.get(identifier=contact_id)
                    
                    # Display standard contact information
                    print(f"Contact: {contact.email or 'No email'} (ID: {contact.nx_id})")
                    
                    if contact.phone:
                        print(f"Phone: {contact.phone} (SMS capable: {contact.sms_capable})")
                        
                    if contact.external_id:
                        print(f"External ID: {contact.external_id}")
                        
                    print(f"Language: {contact.language or 'Not set'}")
                    print(f"Unsubscribed: {contact.unsubscribed or False}")
                    print(f"Created at: {contact.created_at}")
                    
                    # Display custom attributes
                    print("\nCustom attributes:")
                    
                    # Get all attributes excluding standard ones and internal fields
                    standard_fields = {"nx_id", "email", "phone", "sms_capable", "external_id", 
                                    "unsubscribed", "language", "created_at", "created_at_naxai"}
                    
                    custom_attrs = {k: v for k, v in contact.__dict__.items() 
                                if k not in standard_fields and not k.startswith("_")}
                    
                    if custom_attrs:
                        for key, value in custom_attrs.items():
                            print(f"- {key}: {value}")
                    else:
                        print("No custom attributes found")
                        
                except Exception as e:
                    print(f"Error retrieving contact: {str(e)}")
            ```
        
        Note:
            - The contact object includes both standard fields and any custom attributes
            - Custom attributes can be accessed as properties on the contact object
            - If a field or attribute has no value, it will typically be None
            - The primary identifier used in your account determines which field can be used
              as the identifier
            - For retrieving multiple contacts, use the search method with appropriate conditions
        """
        # pylint: disable=protected-access
        return GetContactResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path + "/" + identifier,
                                             headers=self.headers)))

    def delete(self, identifier: str):
        """
        Delete a contact from the Naxai People API.
        
        This method permanently removes a contact from your account. Once deleted,
        the contact's data cannot be recovered.
        
        Args:
            identifier (str): The unique identifier of the contact to delete. This can be
                the Naxai ID, email address, phone number, or external ID depending on your
                account's primary identifier configuration.
        
        Returns:
            None
        
        Raises:
            ValueError: If the identifier is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to delete contacts.
            NaxaiResourceNotFound: If the specified contact does not exist.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # Delete a contact by email
                    contact_id = "john.doe@example.com"
                    
                    # Optionally, verify the contact exists before deleting
                    try:
                        contact = client.people.contacts.get(identifier=contact_id)
                        print(f"Found contact: {contact.email} (ID: {contact.nx_id})")
                        
                        # Confirm deletion (in a real application, you might prompt the user)
                        print("Proceeding with deletion...")
                        
                        # Delete the contact
                        response = client.people.contacts.delete(identifier=contact_id)
                        print(f"Contact deleted successfully: {response}")
                        
                    except Exception as e:
                        if "not found" in str(e).lower():
                            print(f"Contact {contact_id} does not exist")
                        else:
                            raise
                            
                except Exception as e:
                    print(f"Error deleting contact: {str(e)}")
            ```
        
        Note:
            - This operation cannot be undone
            - Deleting a contact will remove all data associated with it
            - The contact will be removed from all segments it belongs to
            - Event history associated with the contact will also be deleted
            - Consider using the unsubscribe flag instead if you want to stop communications
            but retain the contact's data
            - For compliance with privacy regulations like GDPR, you may need to delete
            contacts upon request
        """
        # pylint: disable=protected-access
        return self._client._request("DELETE",
                                     self.root_path + "/" + identifier,
                                     headers=self.headers)
