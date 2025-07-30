"""
Asynchronous email metrics reporting resource for the Naxai SDK.

This module provides asynchronous methods for retrieving comprehensive email performance
metrics from the Naxai platform, including delivery rates, engagement statistics, and
negative indicators. It enables non-blocking access to email analytics data, allowing
applications to efficiently monitor campaign performance, identify trends, and optimize
email marketing strategies without blocking the main execution thread.

vailable Functions:
    list(start: Optional[int], stop: Optional[int], group: Optional[Literal["day", "month"]])
        Retrieve comprehensive email engagement metrics from the Naxai email system.
        Fetches detailed statistics about email performance, including delivery rates,
        open rates, click rates, and negative metrics such as bounces and complaints.

"""

import datetime
import json
from typing import Optional, Literal
from naxai.models.email.responses.metrics_responses import ListMetricsResponse

class MetricsResource:
    """ metrics resource for email.reporting resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/metrics"
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
        Retrieve comprehensive email engagement metrics from the Naxai email system.
        
        This method fetches detailed statistics about email performance, including delivery rates,
        open rates, click rates, and negative metrics such as bounces and complaints. The data
        can be filtered by time period and grouped by day or month to analyze trends over time.
        
        Args:
            start (Optional[int]): Start timestamp for the reporting period, in seconds since epoch.
                Defaults to 7 days ago from the current time.
            stop (Optional[int]): End timestamp for the reporting period, in seconds since epoch.
                Defaults to the current time.
            group (Optional[Literal["day", "month"]]): The time interval grouping for the metrics.
                - "day": Group metrics by day (default)
                - "month": Group metrics by month
        
        Returns:
            ListMetricsResponse: A response object containing comprehensive email metrics.
            The response includes:
                - start: Start timestamp of the reporting period (in milliseconds)
                - stop: End timestamp of the reporting period (in milliseconds)
                - group: The time interval grouping used ("day" or "month")
                - stats: List of BaseStats objects with metrics for each time interval:
                    - date: Timestamp for the time interval
                    - sent: Number of emails sent
                    - delivered: Number of emails successfully delivered
                    - opened: Total number of email opens
                    - opened_unique: Number of unique recipients who opened
                    - clicked: Total number of link clicks
                    - clicked_unique: Number of unique recipients who clicked
                    - failed: Number of emails that failed to deliver
                    - suppress_bound: Number of emails suppressed due to hard bounces
                    - suppress_unsubscribe: Number of emails suppressed due to unsubscribes
                    - bounced: Number of emails that bounced
                    - rejected: Number of emails rejected by recipient servers
                    - complained: Number of spam complaints
                    - unsubscribed: Number of recipients who unsubscribed
        
        Raises:
            NaxaiAPIRequestError: 
                If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to access email metrics
        
        Example:
            >>> # Get email metrics for the past 30 days
            >>> import time
            >>> thirty_days_ago = int(time.time()) - (30 * 24 * 60 * 60)
            >>> current_time = int(time.time())
            >>> 
            >>> metrics = await client.email.reporting.metrics.list(
            ...     start=thirty_days_ago,
            ...     stop=current_time,
            ...     group="day"
            ... )
            >>> 
            >>> print(f"Email metrics from {metrics.start} to {metrics.stop}")
            >>> print(f"Grouped by: {metrics.group}")
            >>> print(f"Data points: {len(metrics.stats)}")
            >>> 
            >>> # Calculate overall metrics
            >>> total_sent = sum(day.sent for day in metrics.stats if day.sent is not None)
            >>> total_delivered = sum(
            >>>     day.delivered for day in metrics.stats if day.delivered is not None)
            >>> total_opened = sum(
            >>>     day.opened_unique for day in metrics.stats if day.opened_unique is not None)
            >>> total_clicked = sum(
            >>>     day.clicked_unique for day in metrics.stats if day.clicked_unique is not None)
            >>> 
            >>> # Calculate key performance indicators
            >>> if total_sent > 0:
            ...     delivery_rate = total_delivered / total_sent * 100
            ...     print(f"Overall delivery rate: {delivery_rate:.1f}%")
            >>> 
            >>> if total_delivered > 0:
            ...     open_rate = total_opened / total_delivered * 100
            ...     click_rate = total_clicked / total_delivered * 100
            ...     print(f"Overall open rate: {open_rate:.1f}%")
            ...     print(f"Overall click rate: {click_rate:.1f}%")
            >>> 
            >>> if total_opened > 0:
            ...     click_to_open_rate = total_clicked / total_opened * 100
            ...     print(f"Click-to-open rate: {click_to_open_rate:.1f}%")
            >>> 
            >>> # Find the day with highest engagement
            >>> if metrics.stats:
            ...     best_day = max(metrics.stats, key=lambda day: day.opened_unique or 0)
            ...     print(f"\nBest performing day: "
            ...           f"{datetime.datetime.fromtimestamp(best_day.date/1000)}")
            ...     print(f"Sent: {best_day.sent}, Opened: "
            ...           f"{best_day.opened_unique}, Clicked: {best_day.clicked_unique}")
            Email metrics from 1703066400000 to 1705658400000
            Grouped by: day
            Data points: 30
            Overall delivery rate: 98.2%
            Overall open rate: 24.5%
            Overall click rate: 3.8%
            Click-to-open rate: 15.5%
            
            Best performing day: 2023-01-15 00:00:00
            Sent: 1200, Opened: 450, Clicked: 85
            
            >>> # Get monthly metrics for the current year
            >>> import datetime
            >>> year_start = int(datetime.datetime(datetime.datetime.now().year, 1, 1).timestamp())
            >>> 
            >>> monthly_metrics = await client.email.reporting.metrics.list(
            ...     start=year_start,
            ...     stop=current_time,
            ...     group="month"
            ... )
            >>> print(f"Monthly email metrics for {datetime.datetime.now().year}")
        
        Note:
            - The start and stop timestamps are provided in seconds since epoch but converted to
            milliseconds in the response
            - The default time range is the past 7 days if no parameters are provided
            - Key engagement metrics to monitor include:
            * Delivery rate: delivered / sent
            * Open rate: opened_unique / delivered
            * Click rate: clicked_unique / delivered
            * Click-to-open rate: clicked_unique / opened_unique
            - Key negative metrics to monitor include:
            * Bounce rate: bounced / sent
            * Complaint rate: complained / sent
            * Unsubscribe rate: unsubscribed / delivered
            - High bounce or complaint rates may indicate issues with email quality or
              recipient targeting
            - The date field in each stats entry is in milliseconds since epoch and represents the
            start of that time interval (day or month)
            - For more detailed click metrics by URL, use the clicked_urls.list() method
            - For best results, use a time range that matches your email sending frequency
        
        See Also:
            ListMetricsResponse: For the structure of the response object
            BaseStats: For the structure of individual time interval statistics
            ClickedUrlsResource.list: For URL-specific click metrics
        """

        params = {
            "start": start,
            "stop": stop,
            "group": group
        }
        # pylint: disable=protected-access
        return ListMetricsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path,
                                                   params=params,
                                                   headers=self.headers)))
