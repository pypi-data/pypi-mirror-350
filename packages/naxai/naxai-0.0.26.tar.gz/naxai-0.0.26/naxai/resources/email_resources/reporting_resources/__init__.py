"""
Email reporting resources package for the Naxai SDK.

This package provides resource classes for email reporting API operations,
including metrics analysis and URL click tracking for email campaigns.
"""

from .clicked_urls import ClickedUrlsResource
from .metrics import MetricsResource

__all__ = ["ClickedUrlsResource", "MetricsResource"]
