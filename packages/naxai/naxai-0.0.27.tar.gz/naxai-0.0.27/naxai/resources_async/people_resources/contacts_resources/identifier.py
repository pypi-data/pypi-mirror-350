"""
Asynchronous contact identifier resource for the Naxai People SDK.

This module provides asynchronous methods for managing the primary identifier type
for contacts in the Naxai platform. It allows users to retrieve and update which
identifier (email, phone, or externalId) is used as the unique key for contact
records in a non-blocking manner, which affects how contacts are referenced
throughout the API in asynchronous applications.

Available Functions:
    get()
        Retrieves the current primary identifier type for contacts.
        Returns a GetContactIdentifierResponse containing the identifier type
        (email, phone, or externalId).

    update(identifier)
        Updates the primary identifier type used for contacts.
        Takes an identifier parameter specifying the new type to use
        (email, phone, or externalId).
        Returns an UpdateContactIdentifierResponse confirming the change.

"""

import json
from naxai.models.people.responses.contacts_responses import (GetContactIdentifierResponse,
                                                              UpdateContactIdentifierResponse)

class IdentifierResource:
    """identifier resource for people.contacts resource"""

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/keyIdentifier"
        self.headers = {"Content-Type": "application/json"}

    async def get(self):
        """
        Retrieve the current primary identifier type for contacts in the Naxai People API.
        
        This method fetches information about which identifier type (email, phone, or externalId)
        is currently being used as the primary identifier for contacts in your account.
        The primary identifier determines how contacts are uniquely identified in the system.
        
        Returns:
            GetContactIdentifierResponse: A response object containing the current primary
                identifier type. The identifier field will be one of:
                "email", "phone", or "externalId".
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access this information.
        
        Example:
            ```python
            async with NaxaiAsyncClient(api_client_id="your_id",
                                        api_client_secret="your_secret") as client:
                # Get the current primary identifier type
                response = await client.people.contacts.identifier.get()
                
                # Display the current identifier type
                print(f"Current primary identifier type: {response.identifier}")
                
                # Use the identifier in conditional logic
                if response.identifier == "email":
                    print("Contacts are identified by email address")
                elif response.identifier == "phone":
                    print("Contacts are identified by phone number")
                elif response.identifier == "externalId":
                    print("Contacts are identified by external ID")
            ```
        
        Note:
            - The primary identifier affects how contacts are identified across the entire API
            - This setting applies to all contacts in your account
            - Understanding the current identifier type is important when creating
              or updating contacts
        """
        # pylint: disable=protected-access
        return GetContactIdentifierResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path,
                                                   headers=self.headers)))

    async def update(self):
        """
        Update the primary identifier type for contacts in the Naxai People API.
        
        This method changes which identifier type (email, phone, or externalId) is used
        as the primary identifier for contacts in your account. The primary identifier
        determines how contacts are uniquely identified in the system.
        
        Returns:
            UpdateContactIdentifierResponse: A response object containing the new primary
                identifier type. The identifier field will be one of: 
                "email", "phone", or "externalId".
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to modify this setting.
        
        Example:
            ```python
            async with NaxaiAsyncClient(api_client_id="your_id",
                                        api_client_secret="your_secret") as client:
                # Update the primary identifier type
                response = await client.people.contacts.identifier.update()
                
                # Confirm the change
                print(f"Primary identifier type updated to: {response.identifier}")
                
                # Verify the change by getting the current setting
                current = await client.people.contacts.identifier.get()
                assert current.identifier == response.identifier, "Update failed"
                print("Update confirmed")
            ```
        
        Note:
            - This is a significant change that affects how contacts are identified across 
              the entire API
            - Before changing the identifier type, ensure that all contacts have the new identifier
              type populated
            - Contacts without the new identifier type may become inaccessible
            - This operation may take some time to propagate through the system
            - Consider the impact on any integrations or automations that rely on the current
              identifier type
        """
        # pylint: disable=protected-access
        return UpdateContactIdentifierResponse.model_validate_json(
            json.dumps(await self._client._request("PUT",
                                                   self.root_path,
                                                   headers=self.headers)))
