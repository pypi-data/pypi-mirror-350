"""
SMS resources package for the Naxai SDK.

This package provides access to SMS-related API resources including:
- Activity logs: For tracking SMS delivery and engagement
- Reporting: For analyzing SMS performance metrics and campaign results
"""

from .activity_logs import ActivityLogsResource
from .reporting import ReportingResource

__all__ = ["ActivityLogsResource", "ReportingResource"]
