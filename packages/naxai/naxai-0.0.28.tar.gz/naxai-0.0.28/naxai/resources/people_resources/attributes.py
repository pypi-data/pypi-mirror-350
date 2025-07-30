"""
Contact attributes resource for the Naxai People SDK.

This module provides methods for managing custom contact attributes in the Naxai platform,
including creating, retrieving, listing, and deleting attributes that define the structure
of contact profiles. These attributes can be used to store custom information about contacts
and can be leveraged for segmentation, personalization, and analytics.

Available Functions:
    create(name: str, type: str, description: Optional[str])
        Create a new custom attribute.
        Args:
            name (str): Name of the attribute
            type (str): Data type of the attribute
            description (Optional[str]): Description of the attribute
        Returns:
            CreateAttributeResponse: Details of the created attribute

    get(name: str)
        Retrieve details of a specific attribute.
        Args:
            name (str): Name of the attribute
        Returns:
            GetAttributeResponse: Details of the requested attribute

    list()
        List all available attributes.
        Returns:
            ListAttributesResponse: List of all attributes

    delete(name: str)
        Delete a custom attribute.
        Args:
            name (str): Name of the attribute to delete
        Returns:
            None

"""

import json
from naxai.models.people.responses.attributes_responses import (GetAttributeResponse,
                                                                ListAttributesResponse,
                                                                CreateAttributeResponse,
                                                                )

class AttributesResource:
    """ attributes resource for people resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/attributes"
        self.headers = {"Content-Type": "application/json"}

    def delete(self, name: str):
        """
        Delete an attribute from the Naxai People API.
        
        This method permanently removes a custom attribute from your account. Once deleted,
        the attribute will no longer be available for use in contacts, segments, or other
        features. Any existing data associated with this attribute will also be removed.
        
        Args:
            name (str): The name of the attribute to delete.
        
        Returns:
            None
        
        Raises:
            ValueError: If the name is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to delete attributes.
            NaxaiResourceNotFound: If the specified attribute does not exist.
            NaxaiInvalidRequestError: If the attribute cannot be deleted (e.g., system attributes).
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                # Delete a custom attribute
                attribute_name = "loyalty_points"
                
                try:
                    response = client.people.attributes.delete(name=attribute_name)
                    print(f"Attribute '{attribute_name}' deleted successfully")
                    print(f"Response: {response}")
                except Exception as e:
                    print(f"Error deleting attribute: {str(e)}")
            ```
        
        Note:
            - This operation cannot be undone
            - System attributes cannot be deleted
            - Deleting an attribute will remove all data associated with it from all contacts
            - If the attribute is used in segment conditions, those segments may need to be updated
            - Consider the impact on integrations or automations that rely on this attribute
        """
        # pylint: disable=protected-access
        return self._client._request("DELETE",
                                     self.root_path + "/" + name,
                                     headers=self.headers)

    def get(self, name: str):
        """
        Retrieve information about a specific attribute in the Naxai People API.
        
        This method fetches detailed information about a single attribute, including its
        name and the segments it's associated with.
        
        Args:
            name (str): The name of the attribute to retrieve.
        
        Returns:
            GetAttributeResponse: A response object containing information about the attribute,
                including its name and associated segment IDs.
        
        Raises:
            ValueError: If the name is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: 
                If the account lacks permission to access attribute information.
            NaxaiResourceNotFound: If the specified attribute does not exist.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                # Get information about a specific attribute
                attribute_name = "loyalty_tier"
                
                try:
                    attribute = client.people.attributes.get(name=attribute_name)
                    
                    print(f"Attribute: {attribute.name}")
                    
                    if attribute.segment_ids:
                        print(f"Used in {len(attribute.segment_ids)} segments:")
                        for segment_id in attribute.segment_ids:
                            print(f"- Segment ID: {segment_id}")
                    else:
                        print("Not used in any segments")
                        
                except Exception as e:
                    print(f"Error retrieving attribute: {str(e)}")
            ```
        
        Note:
            - Both custom and system attributes can be retrieved
            - The segment_ids field shows which segments use this attribute in their conditions
            - This information is useful for understanding attribute usage and dependencies
        """
        # pylint: disable=protected-access
        return GetAttributeResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path + "/" + name,
                                             headers=self.headers)))

    def list(self):
        """
        Retrieve all attributes defined in the Naxai People API.
        
        This method fetches a complete list of all attributes available in your account,
        including both system attributes and custom attributes. Attributes are used to
        store information about contacts and can be used in segment conditions.
        
        Returns:
            ListAttributesResponse: A response object containing the list of attributes.
                The response behaves like a list and can be iterated over.
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: 
                If the account lacks permission to access attribute information.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # Retrieve all attributes
                    attributes = client.people.attributes.list()
                    
                    # Display the total number of attributes
                    print(f"Found {len(attributes)} attributes:")
                    
                    # Group attributes by type (system vs custom)
                    system_attributes = []
                    custom_attributes = []
                    
                    for attr in attributes:
                        # This is a simplified example - in reality, you might need
                        # additional logic to determine if an attribute is system or custom
                        if attr.name.startswith("system_"):
                            system_attributes.append(attr.name)
                        else:
                            custom_attributes.append(attr.name)
                    
                    # Display the attributes by type
                    print(f"\n{len(system_attributes)} System Attributes:")
                    for name in sorted(system_attributes):
                        print(f"- {name}")
                        
                    print(f"\n{len(custom_attributes)} Custom Attributes:")
                    for name in sorted(custom_attributes):
                        print(f"- {name}")
                        
                    # Check if a specific attribute exists
                    target_attribute = "loyalty_tier"
                    exists = any(attr.name == target_attribute for attr in attributes)
                    print(f"\nAttribute '{target_attribute}' exists: {exists}")
                    
                except Exception as e:
                    print(f"Error retrieving attributes: {str(e)}")
            ```
        
        Note:
            - This method returns both system attributes and custom attributes
            - System attributes are predefined and cannot be modified or deleted
            - Custom attributes are those that you have created for your specific needs
            - The response is list-like and supports operations like len(), indexing, and iteration
            - There is no pagination for attributes as the total number is typically manageable
        """
        # pylint: disable=protected-access
        return ListAttributesResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path,
                                             headers=self.headers)))

    def create(self, name: str):
        """
        Create a new custom attribute in the Naxai People API.
        
        This method allows you to define a new custom attribute that can be used to store
        additional information about contacts. Once created, the attribute can be populated
        with values for individual contacts and used in segment conditions.
        
        Args:
            name (str): The name of the attribute to create. Must be unique and follow
                naming conventions (typically alphanumeric with underscores).
        
        Returns:
            CreateAttributeResponse: A response object containing information about the
                newly created attribute, including its name and any associated segment IDs
                (which will typically be empty for a new attribute).
        
        Raises:
            ValueError: If the name is empty or invalid.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to create attributes.
            NaxaiInvalidRequestError: If the attribute name is invalid or already exists.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # Create a new custom attribute
                    attribute_name = "loyalty_tier"
                    
                    response = client.people.attributes.create(name=attribute_name)
                    
                    print(f"Attribute '{response.name}' created successfully")
                    
                    # Now that the attribute is created, you can use it when updating contacts
                    contact_id = "cnt_123abc"
                    client.people.contacts.update(
                        identifier=contact_id,
                        data={attribute_name: "Gold"}  # Set the new attribute value
                    )
                    
                    print(f"Updated contact {contact_id} with {attribute_name}='Gold'")
                    
                except Exception as e:
                    print(f"Error creating attribute: {str(e)}")
            ```
        
        Note:
            - Attribute names should follow a consistent naming convention
            - Common conventions include snake_case (e.g., "loyalty_tier") or
              camelCase (e.g., "loyaltyTier")
            - Attribute names should be descriptive and indicate the type of data they store
            - Once created, attributes cannot be renamed (they must be deleted and recreated)
            - Creating an attribute does not automatically populate it with values for
              existing contacts
            - New attributes can be used immediately for updating contacts and creating segments
        """
        # pylint: disable=protected-access
        return CreateAttributeResponse.model_validate_json(
            json.dumps(self._client._request("POST",
                                             self.root_path,
                                             json={"name": name},
                                             headers=self.headers)))
