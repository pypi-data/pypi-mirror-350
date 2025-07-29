"""
Asynchronous email reporting resource for the Naxai SDK.

This module provides access to asynchronous email reporting functionality, including metrics
analysis and URL click tracking to help users understand email campaign performance and
recipient engagement in a non-blocking manner. It serves as a container for more specialized
reporting resources that provide detailed analytics on different aspects of email performance.

Sub-resources:
    metrics
        Provides methods for retrieving comprehensive email engagement metrics:
        - list(): Retrieve email performance statistics including delivery rates,
          open rates, click rates, and negative metrics like bounces and complaints.

    clicked_urls
        Provides methods for analyzing URL click metrics:
        - list(): Retrieve metrics about clicked URLs in emails, including click
          statistics for each URL over time.

"""

from .reporting_resources.metrics import MetricsResource
from .reporting_resources.clicked_urls import ClickedUrlsResource

class ReportingResource:
    """
    Asynchronous email reporting resource for accessing email analytics.
    
    This class provides access to specialized reporting resources for analyzing email
    performance metrics and engagement data asynchronously. It includes access to
    comprehensive delivery statistics and detailed URL click tracking to help optimize
    email campaigns and understand recipient behavior.
    """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/reporting"
        self.metrics = MetricsResource(client, self.root_path)
        self.clicked_urls = ClickedUrlsResource(client, self.root_path)
