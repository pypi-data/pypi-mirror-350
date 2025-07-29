"""
Email resources package for the Naxai SDK.

This package provides access to various email-related API resources including:
- Activity logs: For tracking email delivery and engagement
- Reporting: For analyzing email performance metrics
- Transactional: For sending transactional emails
"""

from .activity_logs import ActivityLogsResource
from .reporting import ReportingResource
from .transactional import TransactionalResource

__all__ = [
    "ActivityLogsResource",
    "ReportingResource",
    "TransactionalResource",
]
