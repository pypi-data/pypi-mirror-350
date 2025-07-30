"""
Segment response models for the Naxai SDK.

This module defines the data structures for responses from segment-related API operations,
including segment creation, retrieval, updates, and membership management for
targeted audience segmentation.
"""

import json
from typing import Optional, Literal, List
from pydantic import BaseModel, Field
from naxai.models.base.pagination import Pagination
from naxai.models.people.helper_models.segments_condition import Condition

class SegmentBaseModel(BaseModel):
    """
    Base model for segment objects in the Naxai People API.
    
    This class serves as the foundation for segment-related responses in the People API,
    providing the common fields that all segment objects share.
    
    Attributes:
        id (str): The unique identifier of the segment.
        name (str): The name of the segment.
        description (Optional[str]): A description of the segment's purpose or criteria.
            Maximum length is 300 characters.
        state (Optional[Literal["ready", "building"]]): The current state of the segment.
        predefined (Optional[bool]): Whether this is a predefined segment.
        condition (Optional[Condition]): The condition structure defining the segment's criteria.
        modified_by (Optional[str]): The ID of the user who last modified the segment.
            Mapped from the JSON key 'modifiedBy'.
        modified_at (Optional[int]): Timestamp when the segment was last modified.
            Mapped from the JSON key 'modifiedAt'.
        type_ (Optional[Literal["manual", "dynamic"]]): The type of segment.
            Mapped from the JSON key 'type'.
    
    Example:
        >>> # Create a basic segment
        >>> segment = SegmentBaseModel(
        ...     id="seg_123abc",
        ...     name="US Customers",
        ...     description="All customers from the United States",
        ...     state="ready",
        ...     type_="dynamic",
        ...     condition=Condition(
        ...         all=[
        ...             AttributeCondSimple(
        ...                 attribute=AttributeObject(operator="eq", field="country", value="US")
        ...             )
        ...         ]
        ...     )
        ... )
    
    Note:
        - This class is designed to be subclassed by specific segment response models
        - It uses populate_by_name=True to support both direct field names and aliases
        - The type field uses type_ to avoid conflict with Python's built-in type keyword
    """
    id: str
    name: str
    description: Optional[str] = Field(default=None, max_length=300)
    state: Optional[Literal["ready", "building"]] = Field(default=None)
    predefined: Optional[bool] = Field(default=None)
    condition: Optional[Condition] = Field(default=None)
    modified_by: Optional[str] = Field(default=None, alias="modifiedBy")
    modified_at: Optional[int] = Field(default=None, alias="modifiedAt")
    type_: Optional[Literal["manual", "dynamic"]] = Field(default=None, alias="type")

    model_config = {"populate_by_name": True}

class SegmentHistoryDay(BaseModel):
    """
    Model representing a single day's history for a segment.
    
    This class contains information about how a segment's membership changed on a specific day,
    including additions, removals, and the total count.
    
    Attributes:
        date (Optional[int]): The timestamp representing the day.
        added (Optional[int]): The number of contacts added to the segment on this day.
        removed (Optional[int]): The number of contacts removed from the segment on this day.
        change (Optional[int]): The net change in segment membership (added - removed).
        current (Optional[int]): The total number of contacts in the segment at the end of this day.
    
    Example:
        >>> # Create a history entry for a specific day
        >>> history_day = SegmentHistoryDay(
        ...     date=1703066400000,  # December 20, 2023
        ...     added=15,
        ...     removed=3,
        ...     change=12,
        ...     current=250
        ... )
    """
    date: Optional[int] = Field(default=None)
    added: Optional[int] = Field(default=None)
    removed: Optional[int] = Field(default=None)
    change: Optional[int] = Field(default=None)
    current: Optional[int] = Field(default=None)

class ContactBaseModel(BaseModel):
    """
    Base model for contact objects in the Naxai People API.
    
    This class represents a contact in the Naxai system, containing their basic
    identification and communication information.
    
    Attributes:
        nx_id (str): The unique Naxai identifier for the contact.
            Mapped from the JSON key 'nxId'.
        email (Optional[str]): The contact's email address.
        phone (Optional[str]): The contact's phone number.
        sms_capable (Optional[bool]): Whether the contact's phone number can receive SMS.
            Mapped from the JSON key 'smsCapable'.
        external_id (Optional[str]): An external identifier for the contact.
            Mapped from the JSON key 'externalId'.
        unsubscribed (Optional[bool]): Whether the contact has unsubscribed from communications.
        language (Optional[str]): The contact's preferred language.
        created_at (Optional[int]): Timestamp when the contact was created.
            Mapped from the JSON key 'createdAt'.
        created_at_naxai (Optional[int]): Timestamp when the contact was created in Naxai.
            Mapped from the JSON key 'createdAtNaxai'.
    
    Example:
        >>> # Create a basic contact
        >>> contact = ContactBaseModel(
        ...     nxId="cnt_123abc",
        ...     email="john.doe@example.com",
        ...     phone="+1234567890",
        ...     smsCapable=True,
        ...     externalId="cust_456",
        ...     language="en",
        ...     createdAt=1703066400000
        ... )
    
    Note:
        - This class uses populate_by_name=True to support both direct field names and aliases
        - The extra="allow" config allows additional fields to be included for custom attributes
    """
    nx_id: str = Field(alias="nxId")
    email: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    sms_capable: Optional[bool] = Field(alias="smsCapable", default=None)
    external_id: Optional[str] = Field(alias="externalId", default=None)
    unsubscribed: Optional[bool] = Field(default=None)
    language: Optional[str] = Field(default=None)
    created_at: Optional[int] = Field(alias="createdAt", default=None)
    created_at_naxai: Optional[int] = Field(alias="createdAtNaxai", default=None)

    model_config = {"populate_by_name": True,
                    "extra": "allow"}

class ListSegmentsResponse(BaseModel):
    """
    Response model for listing segments in the Naxai People API.
    
    This class represents the response returned by the API when retrieving a list of
    segments. It implements list-like behavior, allowing the response to be used
    as an iterable collection of segment objects.
    
    Attributes:
        root (List[SegmentBaseModel]): The list of segment objects returned by the API.
            Defaults to an empty list if no segments are found.
    
    Example:
        >>> # Creating a response with segment objects
        >>> segments = [
        ...     SegmentBaseModel(id="seg_123", name="US Customers"),
        ...     SegmentBaseModel(id="seg_456", name="High Value Customers")
        ... ]
        >>> response = ListSegmentsResponse(root=segments)
        >>> 
        >>> # Using list-like operations
        >>> len(response)  # Returns 2
        >>> response[0]    # Returns the first segment
        >>> for segment in response:  # Iterating through segments
        ...     print(segment.name)
        US Customers
        High Value Customers
        >>> 
        >>> # Parsing from JSON
        >>> json_data = '[{"id": "seg_123","name": "US Customers"},
        >>>               {"id": "seg_456", "name": "High Value Customers"}]'
        >>> response = ListSegmentsResponse.model_validate_json(json_data)
        >>> len(response)  # Returns 2
    
    Note:
        - This class implements __len__, __getitem__, and __iter__ methods to provide
          list-like behavior
        - The model_validate_json method handles both array-style JSON and object-style
          JSON with a root field
        - When a JSON array is provided, it's automatically wrapped in a 'root' field
        - The class uses Pydantic's default_factory to initialize the root as an empty
          list when no data is provided
    """
    root: List[SegmentBaseModel] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return the number of segments in the list."""
        return len(self.root)

    def __getitem__(self, index):
        """Access segment by index."""
        return self.root[index]

    def __iter__(self):
        """Iterate through segments."""
        return iter(self.root)

    @classmethod
    def model_validate_json(cls, json_data: str, **kwargs):
        """Parse JSON data into the model.
        
        This method handles both array-style JSON and object-style JSON with a root field.
        
        Args:
            json_data (str): The JSON string to parse
            **kwargs: Additional arguments to pass to the standard model_validate_json method
            
        Returns:
            ListAttributesResponse: A validated instance of the class
        """
        data = json.loads(json_data)

        # If the data is a list, wrap it in a dict with the root field
        if isinstance(data, list):
            return cls(root=data)

        # Otherwise, use the standard Pydantic validation
        return super().model_validate_json(json_data, **kwargs)

class CreateSegmentResponse(SegmentBaseModel):
    """
    Response model for segment creation in the Naxai People API.
    
    This class represents the response returned by the API when a new segment is
    successfully created. It inherits all fields from SegmentBaseModel.
    
    Example:
        >>> response = CreateSegmentResponse(
        ...     id="seg_123abc",
        ...     name="New Customers",
        ...     description="Customers who joined in the last 30 days",
        ...     state="building",
        ...     type_="dynamic"
        ... )
        >>> print(f"Created segment: {response.name} (ID: {response.id})")
        Created segment: New Customers (ID: seg_123abc)
    
    Note:
        - This class inherits all fields and behavior from SegmentBaseModel
        - The response typically includes the segment's ID and initial state
    """

class GetSegmentResponse(SegmentBaseModel):
    """
    Response model for retrieving a specific segment in the Naxai People API.
    
    This class represents the response returned by the API when retrieving a single
    segment by its identifier. It inherits all fields from SegmentBaseModel.
    
    Example:
        >>> response = GetSegmentResponse(
        ...     id="seg_123abc",
        ...     name="Active US Customers",
        ...     description="Customers from the US who have been active in the last 30 days",
        ...     state="ready",
        ...     predefined=False,
        ...     type_="dynamic",
        ...     modified_at=1703066400000,
        ...     modified_by="usr_456def"
        ... )
        >>> print(f"Segment: {response.name} (State: {response.state})")
        Segment: Active US Customers (State: ready)
    
    Note:
        - This class inherits all fields and behavior from SegmentBaseModel
        - The response typically includes the complete segment definition and metadata
    """

class UpdateSegmentResponse(SegmentBaseModel):
    """
    Response model for segment updates in the Naxai People API.
    
    This class represents the response returned by the API when an existing segment
    is successfully updated. It inherits all fields from SegmentBaseModel.
    
    Example:
        >>> response = UpdateSegmentResponse(
        ...     id="seg_123abc",
        ...     name="Updated Segment Name",
        ...     description="Updated segment description",
        ...     state="building",
        ...     modified_at=1703066500000,
        ...     modified_by="usr_456def"
        ... )
        >>> print(f"Updated segment: {response.name} (State: {response.state})")
        Updated segment: Updated Segment Name (State: building)
    
    Note:
        - This class inherits all fields and behavior from SegmentBaseModel
        - The response typically includes the updated segment definition and metadata
        - The state may change to "building" if the segment needs to be recalculated
    """

class GetSegmentsHistoryResponse(BaseModel):
    """
    Response model for segment history in the Naxai People API.
    
    This class represents the response returned by the API when retrieving the
    historical membership data for a segment.
    
    Attributes:
        history (list[SegmentHistoryDay]): A list of daily history records for the segment.
    
    Example:
        >>> response = GetSegmentsHistoryResponse(
        ...     history=[
        ...         SegmentHistoryDay(date=1703066400000,
        ...                           added=25,
        ...                           removed=10,
        ...                           change=15,
        ...                           current=1250),
        ...         SegmentHistoryDay(date=1703152800000,
        ...                           added=18,
        ...                           removed=5,
        ...                           change=13,
        ...                           current=1263)
        ...     ]
        ... )
        >>> print(f"History entries: {len(response.history)}")
        >>> print(f"Current size: {response.history[-1].current}")
        History entries: 2
        Current size: 1263
    """
    history: list[SegmentHistoryDay]

class CountContactsInSegmentResponse(BaseModel):
    """
    Response model for counting contacts in a segment.
    
    This class represents the response returned by the API when requesting the
    number of contacts in a specific segment.
    
    Attributes:
        count (int): The number of contacts in the segment.
    
    Example:
        >>> response = CountContactsInSegmentResponse(count=1263)
        >>> print(f"The segment contains {response.count} contacts")
        The segment contains 1263 contacts
    """
    count: int

class GetSegmentUsageResponse(BaseModel):
    """
    Response model for segment usage information.
    
    This class represents the response returned by the API when retrieving information
    about where a segment is being used in campaigns and broadcasts.
    
    Attributes:
        campaign_ids (Optional[list[str]]): List of campaign IDs that use this segment.
        broadcast_ids (Optional[list[str]]): List of broadcast IDs that use this segment.
    
    Example:
        >>> response = GetSegmentUsageResponse(
        ...     campaignIds=["cmp_123", "cmp_456"],
        ...     broadcastIds=["brd_789"]
        ... )
        >>> print(f"Used in {len(response.campaign_ids)} campaigns and\
        >>>        {len(response.broadcast_ids)} broadcasts")
        Used in 2 campaigns and 1 broadcasts
    
    Note:
        - This model supports both snake_case and camelCase field access
    """
    campaign_ids: Optional[list[str]] = Field(alias="campaignIds", default=None)
    broadcast_ids: Optional[list[str]] = Field(alias="broadcastIds", default=None)

    model_config = {"populate_by_name": True}

class ListContactsOfSegmentResponse(BaseModel):
    """
    Response model for retrieving contacts in a segment.
    
    This class represents the response returned by the API when retrieving the
    contacts that belong to a specific segment.
    
    Attributes:
        pagination (Pagination): Pagination information for the response.
        contacts (list[ContactBaseModel]): The list of contacts in the segment.
    
    Example:
        >>> response = ListContactsOfSegmentResponse(
        ...     pagination=Pagination(page=1, page_size=25, total_pages=5, total_items=123),
        ...     items=[
        ...         ContactBaseModel(nx_id="cnt_123", email="john@example.com"),
        ...         ContactBaseModel(nx_id="cnt_456", email="jane@example.com")
        ...     ]
        ... )
        >>> print(f"Page {response.pagination.page} of {response.pagination.total_pages}")
        >>> print(f"Showing {len(response.items)} of {response.pagination.total_record} contacts")
        Page 1 of 5
        Showing 2 of 123 contacts
    """
    pagination: Pagination
    items: list[ContactBaseModel]
