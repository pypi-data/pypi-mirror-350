"""
Asynchronous email resources package for the Naxai SDK.

This package provides access to asynchronous email-related API resources including:
- Activity logs: For tracking email delivery and engagement events
- Reporting: For analyzing email performance metrics and campaign results
- Transactional: For sending individual transactional emails

These resources enable non-blocking access to email functionality, allowing for
efficient email operations in asynchronous applications built with the Naxai platform.
"""

from .activity_logs import ActivityLogsResource
from .reporting import ReportingResource
from .transactional import TransactionalResource

__all__ = [
    "ActivityLogsResource",
    "ReportingResource",
    "TransactionalResource",
]
