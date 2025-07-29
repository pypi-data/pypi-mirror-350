"""
Attribute response models for the Naxai SDK.

This module defines the data structures for responses from attribute-related API operations,
including attribute creation, retrieval, and listing for contact management.
"""

import json
from typing import List
from pydantic import BaseModel, Field

class BaseListObject(BaseModel):
    """
    Base model for attribute objects in the Naxai People API.
    
    This class serves as a foundation for attribute-related responses in the People API,
    providing the common field that all attribute objects share.
    
    Attributes:
        name (str): The name of the attribute.
    
    Example:
        >>> attribute = BaseListObject(name="favorite_color")
        >>> print(attribute.name)
        favorite_color
    
    Note:
        - This class is designed to be subclassed by specific attribute response models
        - It inherits from Pydantic's BaseModel for data validation and serialization
        - Subclasses typically add additional fields specific to their attribute type
    """
    name: str

class CreateAttributeResponse(BaseModel):
    """
    Response model for attribute creation in the Naxai People API.
    
    This class represents the response returned by the API when a new attribute is
    successfully created. It contains information about the newly created attribute,
    including its name and the segments it's associated with.
    
    Attributes:
        name (str): The name of the created attribute.
        segment_ids (list[str]): List of segment IDs that this attribute is associated with.
            This field is mapped from the JSON key 'segmentIds'.
    
    Example:
        >>> response = CreateAttributeResponse(
        ...     name="favorite_color",
        ...     segmentIds=["seg_123abc", "seg_456def"]
        ... )
        >>> print(response.name)
        favorite_color
        >>> print(response.segment_ids)
        ['seg_123abc', '456def']
        >>> print(response.segmentIds)  # Can also be accessed via alias
        ['seg_123abc', '456def']
    
    Note:
        - Unlike GetAttributeResponse, this class inherits directly from BaseModel
          rather than BaseListObject
        - The segment_ids field uses Pydantic's Field with alias to map from the
          camelCase 'segmentIds' used in the API to the snake_case 'segment_ids'
          used in Python
        - Both the snake_case and camelCase versions of the field name can be used
          to access the segment IDs
    """
    name: str
    segment_ids: list[str] = Field(alias="segmentIds")

class ListAttributesResponse(BaseModel):
    """
    Response model for listing attributes in the Naxai People API.
    
    This class represents the response returned by the API when retrieving a list of
    attributes. It implements list-like behavior, allowing the response to be used
    as an iterable collection of attribute objects.
    
    Attributes:
        root (List[BaseListObject]): The list of attribute objects returned by the API.
            Defaults to an empty list if no attributes are found.
    
    Example:
        >>> # Creating a response with attribute objects
        >>> attributes = [
        ...     BaseListObject(name="favorite_color"),
        ...     BaseListObject(name="birth_date")
        ... ]
        >>> response = ListAttributesResponse(root=attributes)
        >>> 
        >>> # Using list-like operations
        >>> len(response)  # Returns 2
        >>> response[0]    # Returns the first attribute
        >>> for attr in response:  # Iterating through attributes
        ...     print(attr.name)
        favorite_color
        birth_date
        >>> 
        >>> # Parsing from JSON
        >>> json_data = '[{"name": "favorite_color"}, {"name": "birth_date"}]'
        >>> response = ListAttributesResponse.model_validate_json(json_data)
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
    root: List[BaseListObject] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return the number of attributes in the list."""
        return len(self.root)

    def __getitem__(self, index):
        """Access attribute by index."""
        return self.root[index]

    def __iter__(self):
        """Iterate through attributes."""
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

class GetAttributeResponse(BaseListObject):
    """
    Response model for retrieving a specific attribute in the Naxai People API.
    
    This class represents the response returned by the API when retrieving a single
    attribute by its identifier. It extends BaseListObject to include segment associations.
    
    Attributes:
        name (str): The name of the attribute (inherited from BaseListObject).
        segment_ids (list[str]): List of segment IDs that this attribute is associated with.
            This field is mapped from the JSON key 'segmentIds'.
    
    Example:
        >>> response = GetAttributeResponse(
        ...     name="favorite_color",
        ...     segmentIds=["seg_123abc", "seg_456def"]
        ... )
        >>> print(response.name)
        favorite_color
        >>> print(response.segment_ids)
        ['seg_123abc', 'seg_456def']
        >>> print(response.segmentIds)  # Can also be accessed via alias
        ['seg_123abc', 'seg_456def']
    
    Note:
        - This class inherits from BaseListObject, extending it with segment association data
        - The segment_ids field uses Pydantic's Field with alias to map from the
          camelCase 'segmentIds' used in the API to the snake_case 'segment_ids'
          used in Python
        - Both the snake_case and camelCase versions of the field name can be used
          to access the segment IDs
        - Unlike CreateAttributeResponse, this class inherits the name field from
          BaseListObject rather than defining it directly
    """
    segment_ids: list[str] = Field(alias="segmentIds")
