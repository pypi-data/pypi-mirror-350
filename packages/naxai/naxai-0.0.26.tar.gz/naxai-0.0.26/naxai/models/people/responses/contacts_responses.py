"""
Contact response models for the Naxai SDK.

This module defines the data structures for responses from contact-related API operations,
including contact search, retrieval, creation, and management of contact identifiers.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field
from naxai.models.base.pagination import Pagination

class ContactBaseModel(BaseModel):
    """
    Base model for contact information in the Naxai People API.
    
    This class defines the common structure for contact objects returned by various
    contact-related API endpoints. It contains essential contact information and
    communication preferences.
    
    Attributes:
        nx_id (str): The unique Naxai identifier for the contact.
            Mapped from JSON key 'nxId'.
        email (Optional[str]): The contact's email address.
            Defaults to None if not provided.
        phone (Optional[str]): The contact's phone number.
            Defaults to None if not provided.
        sms_capable (Optional[bool]): Whether the contact's phone can receive SMS messages.
            Mapped from JSON key 'smsCapable'. Defaults to None if not provided.
        external_id (Optional[str]): An external identifier for the contact, typically
            from your own system. Mapped from JSON key 'externalId'.
            Defaults to None if not provided.
        unsubscribed (Optional[bool]): Whether the contact has unsubscribed from communications.
            Defaults to None if not provided.
        language (Optional[str]): The contact's preferred language code (e.g., "en", "fr").
            Defaults to None if not provided.
        created_at (Optional[int]): Timestamp when the contact was created in your system.
            Mapped from JSON key 'createdAt'. Defaults to None if not provided.
        created_at_naxai (Optional[int]): Timestamp when the contact was created in Naxai.
            Mapped from JSON key 'createdAtNaxai'. Defaults to None if not provided.
    
    Example:
        >>> contact = ContactBaseModel(
        ...     nxId="cnt_123abc",
        ...     email="john.doe@example.com",
        ...     phone="+15551234567",
        ...     smsCapable=True,
        ...     externalId="cust_456def",
        ...     unsubscribed=False,
        ...     language="en",
        ...     createdAt=1703066400000,
        ...     createdAtNaxai=1703066400000
        ... )
        >>> print(f"Contact: {contact.email} (ID: {contact.nx_id})")
        Contact: john.doe@example.com (ID: cnt_123abc)
    
    Note:
        - This model supports both snake_case and camelCase field access through populate_by_name
        - The model allows extra fields beyond those explicitly defined, which can
          include custom attributes specific to the contact
        - Custom attributes will be accessible as dynamic properties on the model instance
    """
    nx_id: str = Field(alias="nxId")
    email: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    sms_capable: Optional[bool] = Field(default=None, alias="smsCapable")
    external_id: Optional[str] = Field(default=None, alias="externalId")
    unsubscribed: Optional[bool] = Field(default=None)
    language: Optional[str] = Field(default=None)
    created_at: Optional[int] = Field(default=None, alias="createdAt")
    created_at_naxai: Optional[int] = Field(default=None, alias="createdAtNaxai")

    model_config = {"populate_by_name": True,
                    "extra": "allow"}

class SegmentBaseModel(BaseModel):
    """
    Base model for segment information in the Naxai People API.
    
    This class defines the common structure for segment objects returned by various
    segment-related API endpoints. It contains basic information about a segment.
    
    Attributes:
        id (str): The unique identifier of the segment.
        name (Optional[str]): The name of the segment.
            Defaults to None if not provided.
        description (Optional[str]): A description of the segment's purpose or criteria.
            Defaults to None if not provided.
        type_ (Optional[Literal["manual", "dynamic"]]): The type of segment.
            - "manual": Explicitly defined members
            - "dynamic": Rule-based segment
            Mapped from JSON key 'type'. Defaults to None if not provided.
        predefined (Optional[bool]): Whether this is a predefined system segment.
            Defaults to None if not provided.
    
    Example:
        >>> segment = SegmentBaseModel(
        ...     id="seg_123abc",
        ...     name="Active US Customers",
        ...     description="Customers from the US who have been active in the last 30 days",
        ...     type="dynamic",
        ...     predefined=False
        ... )
        >>> print(f"Segment: {segment.name} (ID: {segment.id}, Type: {segment.type_})")
        Segment: Active US Customers (ID: seg_123abc, Type: dynamic)
    
    Note:
        - This model supports both snake_case and camelCase field access through populate_by_name
        - The type_ field uses an underscore suffix to avoid conflict with Python's type keyword
    """
    id: str
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    type_: Optional[Literal["manual", "dynamic"]] = Field(alias="type", default=None)
    predefined: Optional[bool] = Field(default=None)

    model_config = {"populate_by_name": True}

class SearchContactsResponse(BaseModel):
    """
    Response model for searching contacts in the Naxai People API.
    
    This class represents the response returned by the API when searching for contacts
    based on various criteria. It includes pagination information and the list of
    matching contacts.
    
    Attributes:
        pagination (Pagination): Pagination information for the search results,
            including current page, page size, total pages, and total items.
        contacts (list[ContactBaseModel]): The list of contacts matching the search criteria.
    
    Example:
        >>> response = SearchContactsResponse(
        ...     pagination=Pagination(page=1, page_size=25, total_pages=4, total_items=87),
        ...     contacts=[
        ...         ContactBaseModel(nxId="cnt_123", email="john@example.com"),
        ...         ContactBaseModel(nxId="cnt_456", email="jane@example.com")
        ...     ]
        ... )
        >>> print(f"Found {response.pagination.total_items} contacts")
        >>> print(f"Showing {len(response.contacts)} contacts on page {response.pagination.page}")
        Found 87 contacts
        Showing 2 contacts on page 1
    
    Note:
        - The pagination object provides information about the current page and total results
        - The contacts list contains full contact objects with all available fields
        - Use pagination to navigate through large result sets by requesting subsequent pages
    """
    pagination: Pagination
    items: list[ContactBaseModel]

class CountContactsResponse(BaseModel):
    """
    Response model for counting contacts in the Naxai People API.
    
    This class represents the response returned by the API when requesting the
    total number of contacts matching certain criteria.
    
    Attributes:
        count (int): The number of contacts matching the criteria.
    
    Example:
        >>> response = CountContactsResponse(count=1287)
        >>> print(f"Total contacts: {response.count}")
        Total contacts: 1287
    
    Note:
        - This simple response contains only the count of matching contacts
        - Useful for getting the total size of your contact database or the number
          of contacts matching specific filters without retrieving the actual contacts
    """
    count: int

class GetContactIdentifierResponse(BaseModel):
    """
    Response model for retrieving a contact's primary identifier type.
    
    This class represents the response returned by the API when requesting
    information about which identifier type is used as the primary identifier
    for a contact.
    
    Attributes:
        identifier (Literal["phone", "email", "externalId"]): The type of identifier
            that is used as the primary identifier for the contact.
            Mapped from JSON key 'Identifier'.
    
    Example:
        >>> response = GetContactIdentifierResponse(Identifier="email")
        >>> print(f"Primary identifier: {response.identifier}")
        Primary identifier: email
    
    Note:
        - This model supports both snake_case and camelCase field access through populate_by_name
        - The primary identifier determines which field is used as the main identifier
          for the contact in the Naxai system
    """
    identifier: Literal["phone", "email", "externalId"] = Field(alias="Identifier")

    model_config = {"populate_by_name": True}

class UpdateContactIdentifierResponse(BaseModel):
    """
    Response model for updating a contact's primary identifier type.
    
    This class represents the response returned by the API when changing
    which identifier type is used as the primary identifier for a contact.
    
    Attributes:
        identifier (Literal["phone", "email", "externalId"]): The new type of identifier
            that is now used as the primary identifier for the contact.
            Mapped from JSON key 'Identifier'.
    
    Example:
        >>> response = UpdateContactIdentifierResponse(Identifier="externalId")
        >>> print(f"Primary identifier updated to: {response.identifier}")
        Primary identifier updated to: externalId
    
    Note:
        - This model supports both snake_case and camelCase field access through populate_by_name
        - Changing the primary identifier affects how the contact is identified in the system
        - The new identifier must already exist on the contact record
    """
    identifier: Literal["phone", "email", "externalId"] = Field(alias="Identifier")

    model_config = {"populate_by_name": True}

class CreateOrUpdateContactResponse(ContactBaseModel):
    """
    Response model for creating or updating a contact in the Naxai People API.
    
    This class represents the response returned by the API when creating a new contact
    or updating an existing one. It inherits all fields from ContactBaseModel.
    
    Example:
        >>> response = CreateOrUpdateContactResponse(
        ...     nxId="cnt_123abc",
        ...     email="john.doe@example.com",
        ...     phone="+15551234567",
        ...     smsCapable=True,
        ...     externalId="cust_456def",
        ...     language="en",
        ...     createdAt=1703066400000
        ... )
        >>> print(f"Contact created/updated: {response.email} (ID: {response.nx_id})")
        Contact created/updated: john.doe@example.com (ID: cnt_123abc)
    
    Note:
        - This class inherits all fields and behavior from ContactBaseModel
        - The response includes the complete contact information after the create/update operation
        - Any custom attributes included in the request will also be present in the response
        - For new contacts, the nx_id field will contain the newly generated Naxai ID
    """

class GetContactResponse(ContactBaseModel):
    """
    Response model for retrieving a specific contact in the Naxai People API.
    
    This class represents the response returned by the API when retrieving a single
    contact by its identifier. It inherits all fields from ContactBaseModel.
    
    Example:
        >>> response = GetContactResponse(
        ...     nxId="cnt_123abc",
        ...     email="john.doe@example.com",
        ...     phone="+15551234567",
        ...     smsCapable=True,
        ...     externalId="cust_456def",
        ...     unsubscribed=False,
        ...     language="en",
        ...     createdAt=1703066400000,
        ...     createdAtNaxai=1703066400000,
        ...     custom_field="Custom Value"  # Custom attribute
        ... )
        >>> print(f"Contact: {response.email} (ID: {response.nx_id})")
        >>> print(f"Custom field: {response.custom_field}")
        Contact: john.doe@example.com (ID: cnt_123abc)
        Custom field: Custom Value
    
    Note:
        - This class inherits all fields and behavior from ContactBaseModel
        - The response includes the complete contact information including any custom attributes
        - Custom attributes are accessible as dynamic properties on the model instance
        - If the contact has no value for a particular field, it will be None in the response
    """

class ListSegmentsOfContactResponse(BaseModel):
    """
    Response model for retrieving segments associated with a contact.
    
    This class represents the response returned by the API when requesting all
    segments that a specific contact belongs to.
    
    Attributes:
        segments (list[SegmentBaseModel]): The list of segments that the contact belongs to.
    
    Example:
        >>> response = ListSegmentsOfContactResponse(
        ...     segments=[
        ...         SegmentBaseModel(id="seg_123", name="Active Users"),
        ...         SegmentBaseModel(id="seg_456", name="Newsletter Subscribers")
        ...     ]
        ... )
        >>> print(f"Contact belongs to {len(response.segments)} segments:")
        >>> for segment in response.segments:
        ...     print(f"- {segment.name} (ID: {segment.id})")
        Contact belongs to 2 segments:
        - Active Users (ID: seg_123)
        - Newsletter Subscribers (ID: seg_456)
    
    Note:
        - This response contains basic information about each segment
        - For detailed segment information, use the dedicated segment retrieval endpoints
        - An empty list indicates the contact doesn't belong to any segments
    """
    segments: list[SegmentBaseModel]
