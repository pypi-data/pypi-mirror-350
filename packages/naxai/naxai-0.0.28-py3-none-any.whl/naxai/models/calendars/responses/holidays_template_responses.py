"""
Holiday template response models for the Naxai SDK.

This module defines the data structures for responses from holiday template-related API operations,
including retrieval, and listing. Holiday templates provide reusable
collections of dates that can be applied to calendars.
"""

import json
from pydantic import BaseModel, Field

class HolidaysTemplate(BaseModel):
    """Model representing a holiday template configuration.

    This class defines the structure of a holiday template, which can be used to
    create and manage sets of holiday dates that can be applied to calendars.

    Attributes:
        id (str): The unique identifier of the holiday template.
            Mapped from JSON key 'id'.
        name (str): The name of the holiday template. Limited to 60 characters.
            Mapped from JSON key 'name'.
        dates (list[str]): List of dates included in this holiday template.
            Mapped from JSON key 'dates'.

    Example:
        >>> template = HolidayTemplate(
        ...     id="ht_123abc",
        ...     name="US Federal Holidays 2024",
        ...     dates=[
        ...         "2024-01-01",  # New Year's Day
        ...         "2024-01-15",  # Martin Luther King Jr. Day
        ...         "2024-02-19"   # Presidents' Day
        ...     ]
        ... )
        >>> print(template.name)
        'US Federal Holidays 2024'
        >>> print(len(template.dates))
        3

    Note:
        - The 'id' field is mapped from the JSON key 'id'
        - The 'name' field is mapped from the JSON key 'name'
        - The 'dates' field is mapped from the JSON key 'date'
        - The name field has a maximum length of 60 characters
        - Dates should be provided in a string format
        - This model uses Pydantic's validation and serialization features
    """
    id: str = Field(alias="id")
    name: str = Field(alias="name", max_length=60)
    dates: list[str] = Field(alias="dates")

class ListHolidaysTemplatesResponse(BaseModel):
    """
    Model representing the response from listing holiday templates in the Naxai API.
    
    This class defines the structure for the API response when retrieving
    a list of holiday templates.
    It provides list-like behavior for accessing the templates, including length,
    indexing, and iteration.
    
    Attributes:
        root (list[HolidaysTemplate]): List of holiday template objects returned by the API.
    
    Example:
        >>> response = ListHolidaysTemplatesResponse(
        ...     root=[
        ...         HolidaysTemplate(
        ...             id="ht_123abc",
        ...             name="US Federal Holidays 2024",
        ...             dates=["2024-01-01", "2024-01-15", "2024-02-19"]
        ...         ),
        ...         HolidaysTemplate(
        ...             id="ht_456def",
        ...             name="UK Bank Holidays 2024",
        ...             dates=["2024-01-01", "2024-04-19", "2024-04-22"]
        ...         )
        ...     ]
        ... )
        >>> print(f"Number of templates: {len(response)}")
        Number of templates: 2
        >>> print(f"First template name: {response[0].name}")
        First template name: US Federal Holidays 2024
        >>> for template in response:
        ...     print(f"Template: {template.name} with {len(template.dates)} holidays")
        Template: US Federal Holidays 2024 with 3 holidays
        Template: UK Bank Holidays 2024 with 3 holidays
    
    Note:
        - This class implements list-like behavior through __len__,
          __getitem__, and __iter__ methods
        - The model_validate_json method handles both array-style JSON and object-style JSON
        - When the API returns a plain array of templates,
          it's automatically wrapped in the root field
        - This model uses Pydantic's validation and serialization features
    """
    root: list[HolidaysTemplate] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return the number of holiday templates."""
        return len(self.root)

    def __getitem__(self, index):
        """Access holiday template by index."""
        return self.root[index]

    def __iter__(self):
        """Iterate through holiday templates."""
        return iter(self.root)

    @classmethod
    def model_validate_json(cls, json_data: str, **kwargs):
        """Parse JSON data into the model.
        
        This method handles both array-style JSON and object-style JSON with a root field.
        """
        data = json.loads(json_data)

        # If the data is a list, wrap it in a dict with the root field
        if isinstance(data, list):
            return cls(root=data)

        # Otherwise, use the standard Pydantic validation
        return super().model_validate_json(json_data, **kwargs)

class GetHolidaysTemplateResponse(HolidaysTemplate):
    """Model representing a response for a single holiday template.

    This class is used to represent the response when fetching a single holiday
    template. It contains the holiday template data.

    Attributes:
        root (HolidayTemplate): The holiday template data.

    Example:
        >>> response = GetHolidaysTemplateResponse(
        ...     root=HolidayTemplate(
        ...         id="ht_123abc",
        ...         name="US Federal Holidays 2024",
        ...         dates=[
        ...             "2024-01-01",  # New Year's Day
        ...             "2024-01-15",  # Martin Luther King Jr. Day
        ...             "2024-02-19"   # Presidents' Day
        ...         ]
        ...     )
        ... )
        >>> print(response.root.name)
        'US Federal Holidays 2024'
        >>> print(len(response.root.dates))
        3

    Note:
        - The 'root' field contains the holiday template data
        - This model uses Pydantic's validation and serialization features
    """
