"""
Calendar resources package for the Naxai SDK.

This package provides resource classes for calendar-related API operations,
including holiday templates management and other calendar functionalities.
"""

from .holidays_templates import HolidaysTemplatesResource

__all__ = ["HolidaysTemplatesResource"]

RESOURCE_CLASSES = {
    "holidays_templates": HolidaysTemplatesResource,
}
