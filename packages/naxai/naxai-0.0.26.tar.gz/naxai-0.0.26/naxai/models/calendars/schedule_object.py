"""
Schedule object models for the Naxai SDK.

This module defines the data structures used for representing calendar schedules,
including operating hours and extended hours for each day of the week.
"""

from typing import Optional
from pydantic import BaseModel, Field

HOUR_PATTERN = r'^\d{2}:\d{2}$'

class ScheduleObject(BaseModel):
    """
    Model representing a single day's schedule in a calendar.
    
    This class defines the operating hours for a specific day of the week,
    including regular hours and optional extended hours.
    
    Attributes:
        day (int): Day of the week (1-7, where 1 is Monday and 7 is Sunday).
        open (bool): Whether the calendar is open on this day.
        start (Optional[str]): Opening time in "HH:MM" format. Required if open is True.
        stop (Optional[str]): Closing time in "HH:MM" format. Required if open is True.
        extended (Optional[bool]): Whether extended hours are available. Defaults to False.
        extension_start (Optional[str]): Start time for extended hours in "HH:MM" format.
            Required if extended is True. Maps to "extensionStart" in API.
        extension_stop (Optional[str]): End time for extended hours in "HH:MM" format.
            Required if extended is True. Maps to "extensionStop" in API.
            
    Example:
        >>> monday = ScheduleObject(
        ...     day=1,
        ...     open=True,
        ...     start="09:00",
        ...     stop="17:00",
        ...     extended=True,
        ...     extension_start="17:00",
        ...     extension_stop="19:00"
        ... )
    """
    day: int = Field(ge=1, le=7)
    open: bool
    start: Optional[str] = Field(pattern=HOUR_PATTERN, default=None)
    stop: Optional[str] = Field(pattern=HOUR_PATTERN, default=None)
    extended: Optional[bool] = Field(default=False)
    extension_start: Optional[str] = Field(alias="extensionStart",
                                           pattern=HOUR_PATTERN, default=None)
    extension_stop: Optional[str] = Field(alias="extensionStop", pattern=HOUR_PATTERN, default=None)

    model_config = {"populate_by_name": True,
                    "validate_by_name": True}
