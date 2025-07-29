"""
Asynchronous email reporting resources package for the Naxai SDK.

This package provides access to asynchronous email reporting API resources including:
- Clicked URLs: For analyzing link engagement in email campaigns
- Metrics: For retrieving comprehensive email performance statistics

These resources enable asynchronous access to email analytics data, allowing for
non-blocking retrieval of reporting information in high-performance applications.
"""


from .clicked_urls import ClickedUrlsResource
from .metrics import MetricsResource

__all__ = ["ClickedUrlsResource",
           "MetricsResource"]
