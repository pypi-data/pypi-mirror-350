"""
Email reporting resource for the Naxai SDK.

This module provides access to email reporting functionality, including metrics analysis
and URL click tracking to help users understand email campaign performance and recipient
engagement. It serves as a container for more specialized reporting resources.

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
    """ reporting resource for email resource"""

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/reporting"

        self.metrics = MetricsResource(client, self.root_path)
        self.clicked_urls = ClickedUrlsResource(client, self.root_path)
