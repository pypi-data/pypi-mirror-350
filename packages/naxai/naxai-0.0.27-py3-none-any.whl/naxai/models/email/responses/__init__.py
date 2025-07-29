"""
Email response models for the Naxai SDK.

This module provides data structures for responses from email-related API operations,
including activity logs, metrics and transactional emails.
"""

from .activity_logs_responses import ListEmailActivityLogsResponse, GetEmailActivityLogsResponse
from .metrics_responses import ListClickedUrlsMetricsResponse, ListMetricsResponse
from .transactional_responses import SendTransactionalEmailResponse

__all__ = [
    "ListEmailActivityLogsResponse",
    "GetEmailActivityLogsResponse",
    "ListClickedUrlsMetricsResponse",
    "ListMetricsResponse",
    "SendTransactionalEmailResponse"
]
