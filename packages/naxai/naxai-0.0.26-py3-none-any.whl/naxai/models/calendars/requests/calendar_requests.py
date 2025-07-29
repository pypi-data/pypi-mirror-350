"""
Calendar request models for the Naxai SDK.

This module defines the data structures used for calendar-related API requests,
including models for creating and configuring calendars with schedules and exclusions.
"""

from typing import Optional
from pydantic import BaseModel, Field
from naxai.models.calendars.schedule_object import ScheduleObject

class CreateCalendarRequest(BaseModel):
    """
    Request model for creating a new calendar in the Naxai system.
    
    This model defines the structure and validation rules for calendar creation requests,
    including the calendar name, timezone, operating schedule, and exclusion dates.
    
    Attributes:
        name (str): The name of the calendar to create.
        timezone (Optional[str]): The timezone for the calendar, defaults to "Europe/Brussels".
            Should be a valid IANA timezone string.
        schedule (list[ScheduleObject]): A list of exactly 7 schedule objects representing
            the operating hours for each day of the week, starting with Monday.
        exclusions (Optional[list[str]]): A list of dates to exclude from the calendar,
            formatted as ISO 8601 date strings (YYYY-MM-DD). Defaults to None.
            
    Example:
        >>> schedule = [
        ...     ScheduleObject(day=1, start="09:00", stop="17:00", open=True),
        ...     # ... other days of the week
        ... ]
        >>> request = CreateCalendarRequest(
        ...     name="Business Hours",
        ...     timezone="America/New_York",
        ...     schedule=schedule,
        ...     exclusions=["2023-12-25", "2024-01-01"]
        ... )
    """
    name: str
    timezone: Optional[str] = "Europe/Brussels"
    schedule: list[ScheduleObject] = Field(max_length=7, min_length=7)
    exclusions: Optional[list[str]] = None
