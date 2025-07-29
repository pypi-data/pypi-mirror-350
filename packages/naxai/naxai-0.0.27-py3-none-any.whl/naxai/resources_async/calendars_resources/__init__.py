"""
Asynchronous calendar resources package for the Naxai SDK.

This package provides access to asynchronous calendar-related API resources,
including holiday templates management for defining non-working days and special
dates that can be applied to calendars in the Naxai platform.
"""

from .holidays_templates import HolidaysTemplatesResource

__all__ = ["HolidaysTemplatesResource"]
