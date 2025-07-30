"""
Email metrics response models for the Naxai SDK.

This module defines the data structures for responses from email metrics API operations,
providing models for tracking email engagement statistics, click rates, and performance metrics.
"""

from typing import Optional
from pydantic import BaseModel, Field

class BaseStats(BaseModel):
    """
    Base model representing email engagement statistics in the Naxai email system.
    
    This class defines the structure for email metrics data, providing comprehensive
    information about email delivery, engagement, and negative outcomes. It serves as
    a component in metrics responses and as a foundation for more specialized statistics models.
    
    Attributes:
        date (Optional[int]): Timestamp for the statistics entry, in milliseconds since epoch.
            For grouped metrics, this represents the start of the time period.
            May be None if not applicable or not provided.
        sent (Optional[int]): Number of emails sent during this period.
            May be None if not available or not applicable.
        delivered (Optional[int]): Number of emails successfully delivered to recipients' inboxes.
            May be None if not available or not applicable.
        opened (Optional[int]): 
            Total number of email opens, including multiple opens by the same recipient.
            May be None if not available or not applicable.
        opened_unique (Optional[int]): 
            Number of unique recipients who opened the email at least once.
            Mapped from JSON key 'openedUnique'. May be None if not available or not applicable.
        clicked (Optional[int]): 
            Total number of link clicks within emails, including multiple clicks by the 
            same recipient.
            May be None if not available or not applicable.
        clicked_unique (Optional[int]): 
            Number of unique recipients who clicked at least one link in the email.
            Mapped from JSON key 'clickedUnique'. May be None if not available or not applicable.
        failed (Optional[int]): Number of emails that failed to deliver for any reason.
            May be None if not available or not applicable.
        suppress_bound (Optional[int]): Number of emails suppressed due to hard bounces.
            Mapped from JSON key 'suppressBound'. May be None if not available or not applicable.
        suppress_unsubscribe (Optional[int]): 
            Number of emails suppressed due to unsubscribe requests.
            Mapped from JSON key 'suppressUnsubscribe'. 
            May be None if not available or not applicable.
        bounced (Optional[int]): Number of emails that bounced (both hard and soft bounces).
            May be None if not available or not applicable.
        rejected (Optional[int]): Number of emails rejected by recipient servers.
            May be None if not available or not applicable.
        complained (Optional[int]): Number of spam complaints received.
            May be None if not available or not applicable.
        unsubscribed (Optional[int]): Number of recipients who unsubscribed via the email.
            May be None if not available or not applicable.
    
    Example:
        >>> stats = BaseStats(
        ...     date=1703066400000,  # January 20, 2023
        ...     sent=1000,
        ...     delivered=980,
        ...     opened=450,
        ...     openedUnique=320,
        ...     clicked=200,
        ...     clickedUnique=150,
        ...     failed=20,
        ...     suppressBound=5,
        ...     suppressUnsubscribe=3,
        ...     bounced=12,
        ...     rejected=8,
        ...     complained=2,
        ...     unsubscribed=10
        ... )
        >>> print(f"Date: {stats.date}")
        >>> print(f"Sent: {stats.sent}, Delivered: {stats.delivered}")
        >>> 
        >>> # Calculate key metrics
        >>> if stats.sent > 0:
        ...     delivery_rate = stats.delivered / stats.sent * 100
        ...     print(f"Delivery rate: {delivery_rate:.1f}%")
        >>> 
        >>> if stats.delivered > 0:
        ...     open_rate = stats.opened_unique / stats.delivered * 100
        ...     click_rate = stats.clicked_unique / stats.delivered * 100
        ...     print(f"Open rate: {open_rate:.1f}%")
        ...     print(f"Click rate: {click_rate:.1f}%")
        ...     print(f"Click-to-open rate:{stats.clicked_unique / stats.opened_unique * 100:.1f}%"\
        ...          if stats.opened_unique > 0 else "Click-to-open rate: N/A")
        >>> 
        >>> # Calculate negative metrics
        >>> if stats.sent > 0:
        ...     bounce_rate = stats.bounced / stats.sent * 100
        ...     complaint_rate = stats.complained / stats.sent * 100
        ...     print(f"Bounce rate: {bounce_rate:.2f}%")
        ...     print(f"Complaint rate: {complaint_rate:.2f}%")
        Date: 1703066400000
        Sent: 1000, Delivered: 980
        Delivery rate: 98.0%
        Open rate: 32.7%
        Click rate: 15.3%
        Click-to-open rate: 46.9%
        Bounce rate: 1.20%
        Complaint rate: 0.20%
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - All fields are optional as they may not be included in all API responses or may
          not be applicable
        - The date field format depends on the grouping level used in the API request
        - Key engagement metrics to monitor include:
          * Delivery rate: delivered / sent
          * Open rate: opened_unique / delivered
          * Click rate: clicked_unique / delivered
          * Click-to-open rate: clicked_unique / opened_unique
        - Key negative metrics to monitor include:
          * Bounce rate: bounced / sent
          * Complaint rate: complained / sent
          * Unsubscribe rate: unsubscribed / delivered
        - High bounce or complaint rates may indicate issues with email quality
          or recipient targeting
    
    See Also:
        ListMetricsResponse: For time-based email metrics responses
        BaseClickedUrlsStats: For URL-specific click metrics
    """

    date: Optional[int] = Field(default=None)
    sent: Optional[int] = Field(default=None)
    delivered: Optional[int] = Field(default=None)
    opened: Optional[int] = Field(default=None)
    opened_unique: Optional[int] = Field(default=None, alias="openedUnique")
    clicked: Optional[int] = Field(default=None)
    clicked_unique: Optional[int] = Field(default=None, alias="clickedUnique")
    failed: Optional[int] = Field(default=None)
    suppress_bound: Optional[int] = Field(default=None, alias="suppressBound")
    suppress_unsubscribe: Optional[int] = Field(default=None, alias="suppressUnsubscribe")
    bounced: Optional[int] = Field(default=None)
    rejected: Optional[int] = Field(default=None)
    complained: Optional[int] = Field(default=None)
    unsubscribed: Optional[int] = Field(default=None)

    model_config = {"populate_by_name": True}

class BaseClickedUrlsStats(BaseModel):
    """
    Model representing URL-specific click statistics in the Naxai email system.
    
    This class defines the structure for link click metrics data, providing information
    about how recipients interact with specific URLs within emails. It serves as
    a component in URL metrics responses.
    
    Attributes:
        url (Optional[str]): The URL that was clicked within the email.
            May be None if not available or not applicable.
        clicked (Optional[int]): 
            Total number of clicks on this URL, including multiple clicks by the same recipient.
            May be None if not available or not applicable.
        clicked_unique (Optional[int]): 
            Number of unique recipients who clicked this URL at least once.
            Mapped from JSON key 'clickedUnique'. May be None if not available or not applicable.
    
    Example:
        >>> url_stats = BaseClickedUrlsStats(
        ...     url="https://example.com/product",
        ...     clicked=250,
        ...     clickedUnique=180
        ... )
        >>> print(f"URL: {url_stats.url}")
        >>> print(f"Total clicks: {url_stats.clicked}")
        >>> print(f"Unique clicks: {url_stats.clicked_unique}")
        >>> 
        >>> # Calculate average clicks per user
        >>> if url_stats.clicked_unique > 0:
        ...     avg_clicks = url_stats.clicked / url_stats.clicked_unique
        ...     print(f"Average clicks per user: {avg_clicks:.2f}")
        URL: https://example.com/product
        Total clicks: 250
        Unique clicks: 180
        Average clicks per user: 1.39
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - All fields are optional as they may not be included in all API responses
        - The difference between clicked and clicked_unique indicates
          how many recipients clicked multiple times
        - URLs with high click rates but low conversion might indicate
          misleading content or technical issues
        - Analyzing which URLs get the most clicks can help optimize email content
          and call-to-action placement
    
    See Also:
        ListClickedUrlsMetricsResponse: For responses containing metrics for multiple URLs
        BaseStats: For general email engagement statistics
    """
    url: Optional[str] = Field(default=None)
    clicked: Optional[int] = Field(default=None)
    clicked_unique: Optional[int] = Field(default=None, alias="clickedUnique")

    model_config = {"populate_by_name": True}

class ListMetricsResponse(BaseModel):
    """
    Model representing time-based email metrics in the Naxai email system.
    
    This class defines the structure for the API response when retrieving email metrics
    grouped by time intervals. It includes information about the reporting period,
    grouping level, and detailed statistics for each time interval.
    
    Attributes:
        start (Optional[int]): Start timestamp of the reporting period, in milliseconds since epoch.
            May be None if not specified.
        stop (Optional[int]): End timestamp of the reporting period, in milliseconds since epoch.
            May be None if not specified.
        group (Optional[str]): 
            The time interval grouping used for the metrics (e.g., "hour", "day", "month").
            May be None if not specified.
        stats (list[BaseStats]): List of statistics entries, each representing metrics
            for a specific time interval within the overall period.
    
    Example:
        >>> response = ListMetricsResponse(
        ...     start=1703030400000,  # January 20, 2023
        ...     stop=1703289600000,   # January 23, 2023
        ...     group="day",
        ...     stats=[
        ...         BaseStats(
        ...             date=1703030400000,  # January 20, 2023
        ...             sent=1000,
        ...             delivered=980,
        ...             opened=450,
        ...             openedUnique=320,
        ...             clicked=200,
        ...             clickedUnique=150
        ...         ),
        ...         BaseStats(
        ...             date=1703116800000,  # January 21, 2023
        ...             sent=1200,
        ...             delivered=1170,
        ...             opened=520,
        ...             openedUnique=380,
        ...             clicked=240,
        ...             clickedUnique=180
        ...         )
        ...     ]
        ... )
        >>> print(f"Period: {response.start} to {response.stop}")
        >>> print(f"Grouping: {response.group}")
        >>> print(f"Number of data points: {len(response.stats)}")
        >>> 
        >>> # Calculate overall metrics
        >>> total_sent = sum(day.sent for day in response.stats if day.sent is not None)
        >>> total_delivered = sum(day.delivered for day in response.stats \
        >>>                    if day.delivered is not None)
        >>> total_opened = sum(day.opened_unique for day in response.stats \
        >>>                 if day.opened_unique is not None)
        >>> total_clicked = sum(day.clicked_unique for day in response.stats \
        >>>                 if day.clicked_unique is not None)
        >>> 
        >>> print(f"Total sent: {total_sent}")
        >>> if total_sent > 0:
        ...     print(f"Overall delivery rate: {total_delivered/total_sent*100:.1f}%")
        >>> if total_delivered > 0:
        ...     print(f"Overall open rate: {total_opened/total_delivered*100:.1f}%")
        ...     print(f"Overall click rate: {total_clicked/total_delivered*100:.1f}%")
        Period: 1703030400000 to 1703289600000
        Grouping: day
        Number of data points: 2
        Total sent: 2200
        Overall delivery rate: 97.7%
        Overall open rate: 32.3%
        Overall click rate: 15.1%
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - The stats list contains entries corresponding to the specified grouping level
        - For hour grouping: One entry per hour in the date range
        - For day grouping: One entry per day in the date range
        - For month grouping: One entry per month in the date range
        - The date field in each stats entry corresponds to the start of that time interval
        - These metrics provide insights into email performance over time
        - Analyzing trends can help identify optimal sending times and content strategies
    
    See Also:
        BaseStats: For the structure of individual statistics entries
        ListClickedUrlsMetricsResponse: For URL-specific click metrics
    """
    start: Optional[int] = Field(default=None)
    stop: Optional[int] = Field(default=None)
    group: Optional[str] = Field(default=None)
    stats: list[BaseStats]

    model_config = {"populate_by_name": True}

class ListClickedUrlsMetricsResponse(BaseModel):
    """
    Model representing URL click metrics in the Naxai email system.
    
    This class defines the structure for the API response when retrieving metrics
    about URL clicks within emails. It includes information about the reporting period
    and detailed statistics for each clicked URL.
    
    Attributes:
        start (Optional[int]): Start timestamp of the reporting period, in milliseconds since epoch.
            May be None if not specified.
        stop (Optional[int]): End timestamp of the reporting period, in milliseconds since epoch.
            May be None if not specified.
        stats (list[BaseClickedUrlsStats]): List of statistics entries, each representing metrics
            for a specific URL that was clicked within emails during the reporting period.
    
    Example:
        >>> response = ListClickedUrlsMetricsResponse(
        ...     start=1703030400000,  # January 20, 2023
        ...     stop=1703289600000,   # January 23, 2023
        ...     stats=[
        ...         BaseClickedUrlsStats(
        ...             url="https://example.com/product",
        ...             clicked=250,
        ...             clickedUnique=180
        ...         ),
        ...         BaseClickedUrlsStats(
        ...             url="https://example.com/pricing",
        ...             clicked=150,
        ...             clickedUnique=120
        ...         ),
        ...         BaseClickedUrlsStats(
        ...             url="https://example.com/contact",
        ...             clicked=80,
        ...             clickedUnique=75
        ...         )
        ...     ]
        ... )
        >>> print(f"Period: {response.start} to {response.stop}")
        >>> print(f"Number of tracked URLs: {len(response.stats)}")
        >>> 
        >>> # Sort URLs by popularity (unique clicks)
        >>> sorted_urls = sorted(response.stats, key=lambda x: x.clicked_unique or 0, reverse=True)
        >>> print("Most popular URLs:")
        >>> for i, url_stats in enumerate(sorted_urls[:3], 1):
        ...     print(f"{i}. {url_stats.url}: {url_stats.clicked_unique} unique clicks")
        >>> 
        >>> # Calculate total clicks
        >>> total_clicks = sum(url.clicked for url in response.stats if url.clicked is not None)
        >>> total_unique = sum(url.clicked_unique for url in response.stats \
        >>>                 if url.clicked_unique is not None)
        >>> print(f"Total clicks: {total_clicks} ({total_unique} unique)")
        Period: 1703030400000 to 1703289600000
        Number of tracked URLs: 3
        Most popular URLs:
        1. https://example.com/product: 180 unique clicks
        2. https://example.com/pricing: 120 unique clicks
        3. https://example.com/contact: 75 unique clicks
        Total clicks: 480 (375 unique)
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - The stats list contains one entry per unique URL that was clicked
        - URLs are typically sorted by click count in descending order
        - Analyzing which URLs get the most clicks can help optimize email content
          and call-to-action placement
        - URLs with high click rates but low conversion might indicate misleading content or
          technical issues
        - The difference between clicked and clicked_unique indicates how many recipients clicked
          multiple times
    
    See Also:
        BaseClickedUrlsStats: For the structure of individual URL statistics entries
        ListMetricsResponse: For general time-based email metrics
    """
    start: Optional[int] = Field(default=None)
    stop: Optional[int] = Field(default=None)
    stats: list[BaseClickedUrlsStats]

    model_config = {"populate_by_name": True}
