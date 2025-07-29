"""
Calendar model definitions for the Naxai SDK.

This module provides the core data structures for representing calendars and their schedules,
including day-by-day operating hours and exclusion dates.
"""

from typing import Optional
from pydantic import BaseModel, Field
from .schedule_object import ScheduleObject

HOUR_PATTERN = r'^\d{2}:\d{2}$'

class Calendar(BaseModel):
    """A model representing a calendar with schedule and time settings.

    This class defines the structure of a calendar, including its identification,
    scheduling rules, and time-related configurations.

    Attributes:
        id (Optional[str]): The unique identifier of the calendar. Defaults to None.
        name (str): The name of the calendar.
        timezone (Optional[str]):
                    The timezone setting for the calendar. Defaults to Europe/Brussels.
        schedule (list[ScheduleObject]): A list of exactly 7 ScheduleObject instances,
            representing the schedule for each day of the week.
        exclusions (Optional[list[str]]): A list of dates to be excluded from the
            calendar schedule. Defaults to None.

    Example:
        >>> schedule_objects = [
        ...     ScheduleObject(
        ...         day=1,
        ...         open=True,
        ...         start="09:00",
        ...         stop="17:00"
        ...     ),
        ...     # ... repeat for all 7 days
        ... ]
        >>> calendar = Calendar(
        ...     name="Business Hours",
        ...     timezone="UTC",
        ...     schedule=schedule_objects
        ... )

    Note:
        - The schedule must contain exactly 7 ScheduleObject instances (one per day)
        - Time values in ScheduleObject must follow the format "HH:MM"
        - Days in ScheduleObject are numbered 1-7
        - The model uses Pydantic for validation and serialization

    See Also:
        ScheduleObject: The model class used for daily schedule configuration
    """
    id: Optional[str] = None
    name: str
    timezone: Optional[str] = "Europe/Brussels"
    schedule: list[ScheduleObject] = Field(max_length=7, min_length=7)
    exclusions: Optional[list[str]] = None
