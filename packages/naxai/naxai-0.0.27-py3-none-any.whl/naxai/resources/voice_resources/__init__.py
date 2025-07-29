"""
Voice resources package for the Naxai SDK.

This package provides access to voice communication resources including:
- Call: For managing individual voice calls and call operations
- Broadcast: For creating and managing voice broadcast campaigns
- Reporting: For analyzing voice call metrics and performance data
- Activity logs: For tracking detailed voice call events and outcomes
"""

from .call import CallResource
from .broadcast import BroadcastsResource
from .reporting import ReportingResource
from .activity_logs import ActivityLogsResource

__all__ = ["CallResource",
           "BroadcastsResource",
           "ReportingResource",
           "ActivityLogsResource"]
