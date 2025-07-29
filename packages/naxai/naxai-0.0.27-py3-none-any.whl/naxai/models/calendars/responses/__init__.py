"""
Calendar response models for the Naxai SDK.

This module provides response data models for calendar-related API operations,
including calendar creation, retrieval, updates, and holiday template management.
"""

from .calendars_responses import (CreateCalendarResponse,
                                  ListCalendarsResponse,
                                  GetCalendarResponse,
                                  UpdateCalendarResponse,
                                  AddExclusionsResponse,
                                  DeleteExclusionsResponse,
                                  CheckCalendarResponse)
from .holidays_template_responses import (ListHolidaysTemplatesResponse,
                                          GetHolidaysTemplateResponse,
                                          HolidaysTemplate)

__all__ = ["CreateCalendarResponse",
           "ListCalendarsResponse",
           "GetCalendarResponse",
           "UpdateCalendarResponse",
           "AddExclusionsResponse",
           "DeleteExclusionsResponse",
           "CheckCalendarResponse",
           "ListHolidaysTemplatesResponse",
           "GetHolidaysTemplateResponse",
           "HolidaysTemplate"]
