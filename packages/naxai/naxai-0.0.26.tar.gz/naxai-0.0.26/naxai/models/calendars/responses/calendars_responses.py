"""
Calendar response models for the Naxai SDK.

This module defines the data structures for responses from calendar-related API operations,
including calendar creation, retrieval, updates, and exclusion management.
"""

import json
from typing import Optional
from pydantic import BaseModel, Field
from naxai.models.calendars.schedule_object import ScheduleObject
from naxai.models.calendars.calendar import Calendar

class CreateCalendarResponse(BaseModel):
    """
    Model representing the response from creating a calendar in the Naxai API.
    
    This class defines the structure for the API response when a new calendar is created,
    containing the calendar's unique identifier and all its configured properties.
    
    Attributes:
        id (str): Unique identifier for the newly created calendar.
        name (str): The name of the calendar as specified in the creation request.
        timezone (Optional[str]): The timezone associated with the calendar.
            Defaults to None if not specified.
        schedule (list[ScheduleObject]): List of schedule objects defining when the calendar
            is active, typically containing operating hours for each day of the week.
        exclusions (Optional[list]): List of dates or periods when the calendar is inactive,
            such as holidays. Defaults to None if not specified.
    
    Example:
        >>> response = CreateCalendarResponse(
        ...     id="cal_123abc",
        ...     name="Business Hours",
        ...     timezone="America/New_York",
        ...     schedule=[...],  # List of ScheduleObject instances
        ...     exclusions=["2023-12-25"]
        ... )
        >>> print(f"Created calendar with ID: {response.id}")
    """
    id: str
    name: str
    timezone: Optional[str] = None
    schedule: list[ScheduleObject]
    exclusions: Optional[list] = None

class ListCalendarsResponse(BaseModel):
    """
    Model representing the response from listing calendars in the Naxai API.
    
    This class defines the structure for the API response when retrieving a list of calendars.
    It provides list-like behavior for accessing the calendars, including length,
    indexing, and iteration.
    
    Attributes:
        root (list[CreateCalendarResponse]): List of calendar objects returned by the API.
    
    Example:
        >>> response = ListCalendarsResponse(
        ...     root=[
        ...         CreateCalendarResponse(
        ...             id="cal_123abc",
        ...             name="Business Hours",
        ...             timezone="America/New_York",
        ...             schedule=[...],
        ...             exclusions=None
        ...         ),
        ...         CreateCalendarResponse(
        ...             id="cal_456def",
        ...             name="Holiday Schedule",
        ...             timezone="Europe/London",
        ...             schedule=[...],
        ...             exclusions=["2023-12-25"]
        ...         )
        ...     ]
        ... )
        >>> print(f"Number of calendars: {len(response)}")
        >>> print(f"First calendar name: {response[0].name}")
        >>> for calendar in response:
        ...     print(f"Calendar: {calendar.name} ({calendar.id})")
    """
    root: list[Calendar] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return the number of calendars."""
        return len(self.root)

    def __getitem__(self, index):
        """Access calendar by index."""
        return self.root[index]

    def __iter__(self):
        """Iterate through calendars."""
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

class GetCalendarResponse(Calendar):
    """
    Model representing the response from retrieving a specific calendar in the Naxai API.
    
    This class extends the base Calendar model to represent the API response when fetching
    a single calendar by its ID. It inherits all attributes from the Calendar class.
    
    Inherited Attributes:
        id (str): Unique identifier for the calendar.
        name (str): The name of the calendar.
        timezone (Optional[str]): The timezone associated with the calendar.
        schedule (list[ScheduleObject]):
                            List of schedule objects defining when the calendar is active.
        exclusions (Optional[list]): List of exclusion periods when the calendar is inactive.
    
    Example:
        >>> response = GetCalendarResponse(
        ...     id="cal_123abc",
        ...     name="Business Hours",
        ...     timezone="America/New_York",
        ...     schedule=[...],
        ...     exclusions=["2023-12-25"]
        ... )
        >>> print(f"Calendar ID: {response.id}")
        >>> print(f"Calendar Name: {response.name}")
        >>> print(f"Timezone: {response.timezone}")
    """

class UpdateCalendarResponse(Calendar):
    """
    Model representing the response from updating a calendar in the Naxai API.
    
    This class extends the base Calendar model to represent the API response when updating
    an existing calendar. It inherits all attributes from the Calendar class and reflects
    the updated state of the calendar after the changes have been applied.
    
    Inherited Attributes:
        id (str): Unique identifier for the calendar.
        name (str): The updated name of the calendar.
        timezone (Optional[str]): The updated timezone associated with the calendar.
        schedule (list[ScheduleObject]):
                            Updated list of schedule objects defining when the calendar is active.
        exclusions (Optional[list]):
                            Updated list of exclusion periods when the calendar is inactive.
    
    Example:
        >>> response = UpdateCalendarResponse(
        ...     id="cal_123abc",
        ...     name="Updated Business Hours",
        ...     timezone="America/Chicago",
        ...     schedule=[...],
        ...     exclusions=["2023-12-25", "2024-01-01"]
        ... )
        >>> print(f"Updated Calendar: {response.name}")
        >>> print(f"New Timezone: {response.timezone}")
    """

class ExclusionResponse(BaseModel):
    """Response model for calendar exclusion addition/deletion operations.

    This class represents the response received after adding/deleting exclusion dates to a calendar.
    It contains the complete list of exclusions for the calendar after the addition/deletion
    operation.

    Attributes:
        exclusions (list[str]): A list of all exclusion dates for the calendar.
            Each date is represented as a string. This includes both previously existing
            exclusions and newly added ones.

    Example:
        >>> response = AddExclusionResponse(
        ...     exclusions=["2024-12-25", "2024-12-26", "2025-01-01"]
        ... )
        >>> print(response.exclusions)
        ['2024-12-25', '2024-12-26', '2025-01-01']

    Note:
        - The field 'exclusions' is mapped from the JSON key 'exclusions'
        - Dates should be in string format
        - The list contains all exclusions
        - This model is used as the return type for the add_exclusions and delete_exclusions methods

    See Also:
        Calendar: The main calendar model class
    """
    exclusions: list[str] = Field(alias="exclusions")

class AddExclusionsResponse(ExclusionResponse):
    """
    Model representing the response from adding exclusions to a calendar in the Naxai API.
    
    This class defines the structure for the API response when adding new exclusion periods
    to an existing calendar. It contains the complete list of exclusions after the addition.
    
    Attributes:
        exclusions (list[str]):
                    The complete list of exclusion periods for the calendar after the addition.
    
    Example:
        >>> response = AddExclusionsResponse(
        ...     exclusions=["2023-12-25", "2024-01-01", "2024-07-04"]
        ... )
        >>> print(f"Total exclusions: {len(response.exclusions)}")
        >>> print(f"Exclusion dates: {', '.join(response.exclusions)}")
    """

class DeleteExclusionsResponse(ExclusionResponse):
    """
    Model representing the response from deleting exclusions from a calendar in the Naxai API.
    
    This class defines the structure for the API response when removing exclusion periods
    from an existing calendar. It contains the remaining list of exclusions after the deletion.
    
    Attributes:
        exclusions (list[str]):
                        The remaining list of exclusion periods for the calendar after the deletion.
    
    Example:
        >>> response = DeleteExclusionsResponse(
        ...     exclusions=["2024-01-01", "2024-07-04"]
        ... )
        >>> print(f"Remaining exclusions: {len(response.exclusions)}")
        >>> print(f"Remaining exclusion dates: {', '.join(response.exclusions)}")
    """

class CheckCalendarResponse(BaseModel):
    """
    Model representing the response from checking a calendar's availability in the Naxai API.
    
    This class defines the structure for the API response when checking if a specific time
    matches the calendar's active periods. It indicates whether the time matches and, if not,
    provides the next available time.
    
    Attributes:
        match_ (bool): Indicates whether the checked time matches an active period in the calendar.
            Mapped from JSON key 'match'.
        next_ (Optional[int]): If the time doesn't match, this field contains the timestamp of the
            next available time according to the calendar. Mapped from JSON key 'next'.
            Defaults to None if not provided.
    
    Example:
        >>> response = CheckCalendarResponse(match=True, next=None)
        >>> if response.match_:
        ...     print("The time is within an active calendar period")
        ... else:
        ...     print(f"The time is outside active hours. Next available time: {response.next_}")
    
    Note:
        This class uses Pydantic's alias feature to map the Python attributes 'match_' and 'next_'
        to the JSON fields 'match' and 'next', respectively,
        since these are reserved keywords in Python.
    """
    match_: bool = Field(alias="match")
    next_: Optional[int] = Field(alias="next", default=None)

    model_config = {"populate_by_name": True,
                    "validate_by_name": True}
