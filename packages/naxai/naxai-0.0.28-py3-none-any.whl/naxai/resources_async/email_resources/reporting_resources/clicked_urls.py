"""
Asynchronous clicked URLs reporting resource for the Naxai SDK.

This module provides asynchronous methods for retrieving and analyzing metrics about
URL clicks in emails sent through the Naxai platform. It enables non-blocking access
to link engagement data, helping users understand which links receive the most clicks,
identify popular content, and optimize email campaigns for better click-through rates.

Available functions:
    list(start: Optional[int], stop: Optional[int], group: Optional[Literal["day", "month"]])
        Retrieves metrics about clicked URLs in emails over a specified time period.
        Returns a ListClickedUrlsMetricsResponse containing click statistics for each URL.

"""

import datetime
import json
from typing import Optional, Literal
from naxai.models.email.responses.metrics_responses import ListClickedUrlsMetricsResponse

class ClickedUrlsResource:
    """ clicked_urls resource for email.reporting resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/clicks"
        self.headers = {"Content-Type": "application/json"}

    async def list(
            self,
            start: Optional[int] = int(
                (datetime.datetime.now(tz=datetime.timezone.utc) -
                datetime.timedelta(days=7)).timestamp()
            ),
            stop: Optional[int] = int(
                datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
            ),
            group: Optional[Literal["day", "month"]] = "day",
        ):
        """
        Retrieve metrics about clicked URLs in emails sent through the Naxai email system.
        
        This method fetches detailed statistics about link clicks within emails, providing
        insights into which URLs received the most engagement and how recipients interacted
        with the content. The data can be filtered by time period and grouped by day or month.
        
        Args:
            start (Optional[int]): Start timestamp for the reporting period, in seconds since epoch.
                Defaults to 7 days ago from the current time.
            stop (Optional[int]): End timestamp for the reporting period, in seconds since epoch.
                Defaults to the current time.
            group (Optional[Literal["day", "month"]]): The time interval grouping for the metrics.
                - "day": Group metrics by day (default)
                - "month": Group metrics by month
        
        Returns:
            ListClickedUrlsMetricsResponse: A response object containing URL click metrics.
            The response includes:
                - start: Start timestamp of the reporting period (in milliseconds)
                - stop: End timestamp of the reporting period (in milliseconds)
                - stats: List of BaseClickedUrlsStats objects with metrics for each URL:
                    - url: The URL that was clicked
                    - clicked: Total number of clicks on this URL
                    - clicked_unique: Number of unique recipients who clicked this URL
        
        Raises:
            NaxaiAPIRequestError: 
                If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to access click metrics
        
        Example:
            >>> # Get URL click metrics for the past 30 days
            >>> import time
            >>> thirty_days_ago = int(time.time()) - (30 * 24 * 60 * 60)
            >>> current_time = int(time.time())
            >>> 
            >>> metrics = await client.email.reporting.clicked_urls.list(
            ...     start=thirty_days_ago,
            ...     stop=current_time,
            ...     group="day"
            ... )
            >>> 
            >>> print(f"URL click metrics from {metrics.start} to {metrics.stop}")
            >>> print(f"Found data for {len(metrics.stats)} URLs")
            >>> 
            >>> # Find the most clicked URLs
            >>> sorted_urls = (
            >>>     sorted(metrics.stats, key=lambda x: x.clicked_unique or 0, reverse=True))
            >>> print("\nTop 3 most clicked URLs:")
            >>> for i, url_stats in enumerate(sorted_urls[:3], 1):
            ...     print(f"{i}. {url_stats.url}")
            ...     print(f"   Total clicks: {url_stats.clicked}")
            ...     print(f"   Unique clicks: {url_stats.clicked_unique}")
            URL click metrics from 1703066400000 to 1705658400000
            Found data for 12 URLs
            
            Top 3 most clicked URLs:
            1. https://example.com/product
            Total clicks: 250
            Unique clicks: 180
            2. https://example.com/pricing
            Total clicks: 150
            Unique clicks: 120
            3. https://example.com/contact
            Total clicks: 80
            Unique clicks: 75
            
            >>> # Get monthly click metrics for the current year
            >>> import datetime
            >>> year_start = int(datetime.datetime(datetime.datetime.now().year, 1, 1).timestamp())
            >>> 
            >>> monthly_metrics = await client.email.reporting.clicked_urls.list(
            ...     start=year_start,
            ...     stop=current_time,
            ...     group="month"
            ... )
            >>> print(f"Monthly URL click metrics for {datetime.datetime.now().year}")
        
        Note:
            - The start and stop timestamps are provided in seconds since epoch but converted to
            milliseconds in the response
            - The default time range is the past 7 days if no parameters are provided
            - The difference between clicked and clicked_unique indicates how many recipients
            clicked multiple times on the same URL
            - URLs with high click rates but low conversion might indicate misleading content
            or technical issues on landing pages
            - Analyzing which URLs get the most clicks can help optimize email content and
            call-to-action placement
            - For best results, use a time range that matches your email sending frequency
            - The group parameter affects the granularity of time-based analysis but not the
            URL-specific metrics themselves
        
        See Also:
            ListClickedUrlsMetricsResponse: For the structure of the response object
            BaseClickedUrlsStats: For the structure of individual URL statistics
        """

        params = {
            "start": start,
            "stop": stop,
            "group": group
        }
        # pylint: disable=protected-access
        return ListClickedUrlsMetricsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path,
                                                   params=params,
                                                   headers=self.headers)))
