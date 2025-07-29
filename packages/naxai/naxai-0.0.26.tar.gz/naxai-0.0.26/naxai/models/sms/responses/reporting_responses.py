"""
SMS activity logs response models for the Naxai SDK.

This module defines the data structures for responses from SMS activity log API operations,
providing models for tracking message delivery status, content, and metadata for both
outbound and inbound SMS messages.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field

class BaseResponse(BaseModel):
    """
    Base model representing a time-bounded metrics response in the Naxai messaging system.
    
    This class defines the core structure for metrics API responses, providing essential
    information about the time period covered by the metrics data. It serves as the
    foundation for more specialized metrics response models.
    
    Attributes:
        start_date (str): The beginning of the time period for which metrics are reported,
            in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ).
            Mapped from JSON key 'startDate'.
        stop_date (str): The end of the time period for which metrics are reported,
            in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ).
            Mapped from JSON key 'stopDate'.
    
    Example:
        >>> base_response = BaseResponse(
        ...     startDate="2023-01-01",
        ...     stopDate="2023-01-31"
        ... )
        >>> print(f"Metrics period: {base_response.start_date} to {base_response.stop_date}")
        Metrics period: 2023-01-01 to 2023-01-31
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - It serves as a base class for more specialized metrics response models
        - The date format may vary depending on the specific API endpoint and grouping
        - All derived classes will include these date range fields along with their specific metrics
    """
    start_date: str = Field(alias="startDate")
    stop_date: str = Field(alias="stopDate")

    model_config = {"populate_by_name": True}

class BaseStats(BaseModel):
    """
    Base model representing SMS messaging statistics in the Naxai messaging system.
    
    This class defines the core structure for SMS metrics data, providing comprehensive
    information about message volumes, delivery outcomes, and timing metrics.
    
    Attributes:
        sms (int): Total number of SMS messages processed during the reporting period.
        delivered (int): Number of messages successfully delivered to recipients.
        failed (int): Number of messages that failed to deliver.
        expired (int): Number of messages that expired before delivery could be completed.
        unknown (int): Number of messages with unknown delivery status.
        canceled (int): Number of messages that were canceled before delivery.
        rejected (int): Number of messages rejected by carriers or recipients.
        blocked (int) optional: Number of messages blocked.
        avg_time_to_deliver (int): Average time in milliseconds from submission to delivery.
            Mapped from JSON key 'avgTimeToDeliver'.
        avg_time_to_submit (int): Average time in milliseconds from sending to carrier submission.
            Mapped from JSON key 'avgTimeToSubmit'.
    
    Example:
        >>> stats = BaseStats(
        ...     sms=1000,
        ...     delivered=950,
        ...     failed=20,
        ...     expired=10,
        ...     unknown=5,
        ...     canceled=10,
        ...     rejected=5,
        ...     blocked=0,
        ...     avgTimeToDeliver=2500,
        ...     avgTimeToSubmit=150
        ... )
        >>> print(f"Total SMS: {stats.sms}")
        >>> print(f"Delivered: {stats.delivered} ({stats.delivered/stats.sms*100:.1f}%)")
        >>> print(f"Failed: {stats.failed} ({stats.failed/stats.sms*100:.1f}%)")
        >>> print(f"Avg delivery time: {stats.avg_time_to_deliver} ms")
        Total SMS: 1000
        Delivered: 950 (95.0%)
        Failed: 20 (2.0%)
        Avg delivery time: 2500 ms
    
    Note:
        - The sum of delivered, failed, expired, unknown, canceled, and rejected should
          equal the total sms count
        - Timing metrics (avg_time_to_deliver, avg_time_to_submit) are in milliseconds
        - These statistics provide a high-level overview of messaging performance and reliability
    """
    sms: int
    delivered: int
    failed: int
    expired: int
    unknown: int
    canceled: int
    rejected: int
    blocked: Optional[int] = Field(default=0)
    avg_time_to_deliver: int = Field(alias="avgTimeToDeliver")
    avg_time_to_submit: int = Field(alias="avgTimeToSubmit")

    model_config = {"populate_by_name": True}

class OutgoingStats(BaseStats):
    """
    Model representing time-based outgoing SMS statistics in the Naxai messaging system.
    
    This class extends BaseStats to include a date field, allowing for time-series analysis
    of outgoing SMS metrics grouped by hour, day, or month.
    
    Attributes:
        date (str): The specific date or timestamp for this metrics entry, in a format
            corresponding to the grouping level (YYYY-MM-DD for day grouping,
            YYYY-MM-DDTHH:00:00Z for hour grouping, etc.).
        
        # Inherited from BaseStats:
        sms (int): Total number of outgoing SMS messages for this time period.
        delivered (int): Number of messages successfully delivered.
        failed (int): Number of messages that failed to deliver.
        expired (int): Number of messages that expired before delivery.
        unknown (int): Number of messages with unknown delivery status.
        canceled (int): Number of messages that were canceled.
        rejected (int): Number of messages rejected by carriers or recipients.
        avg_time_to_deliver (int): Average delivery time in milliseconds.
        avg_time_to_submit (int): Average submission time in milliseconds.
    
    Example:
        >>> daily_stats = OutgoingStats(
        ...     date="2023-01-15",
        ...     sms=500,
        ...     delivered=480,
        ...     failed=10,
        ...     expired=5,
        ...     unknown=0,
        ...     canceled=3,
        ...     rejected=2,
        ...     avgTimeToDeliver=2300,
        ...     avgTimeToSubmit=120
        ... )
        >>> print(f"Date: {daily_stats.date}")
        >>> print(f"SMS sent: {daily_stats.sms}")
        >>> print(f"Delivery rate: {daily_stats.delivered/daily_stats.sms*100:.1f}%")
        Date: 2023-01-15
        SMS sent: 500
        Delivery rate: 96.0%
    
    Note:
        - The date format depends on the grouping level used in the API request
        - For hour grouping: YYYY-MM-DDTHH:00:00Z
        - For day grouping: YYYY-MM-DD
        - For month grouping: YYYY-MM
        - These statistics represent outgoing messages only
    """
    date: str

class OutgoingCountryStats(BaseStats):
    """
    Model representing country-based outgoing SMS statistics in the Naxai messaging system.
    
    This class extends BaseStats to include country and network information, allowing for
    geographical analysis of outgoing SMS metrics grouped by destination country and carrier.
    
    Attributes:
        country (str): The country code (typically ISO 3166-1 alpha-2) for this metrics entry.
        mcc (str): Mobile Country Code identifying the country's mobile network system.
        mnc (str): Mobile Network Code identifying the specific mobile network carrier.
        
        # Inherited from BaseStats:
        sms (int): Total number of outgoing SMS messages to this country/network.
        delivered (int): Number of messages successfully delivered.
        failed (int): Number of messages that failed to deliver.
        expired (int): Number of messages that expired before delivery.
        unknown (int): Number of messages with unknown delivery status.
        canceled (int): Number of messages that were canceled.
        rejected (int): Number of messages rejected by carriers or recipients.
        avg_time_to_deliver (int): Average delivery time in milliseconds.
        avg_time_to_submit (int): Average submission time in milliseconds.
    
    Example:
        >>> country_stats = OutgoingCountryStats(
        ...     country="US",
        ...     mcc="310",
        ...     mnc="410",
        ...     sms=1200,
        ...     delivered=1150,
        ...     failed=30,
        ...     expired=10,
        ...     unknown=5,
        ...     canceled=3,
        ...     rejected=2,
        ...     avgTimeToDeliver=1800,
        ...     avgTimeToSubmit=110
        ... )
        >>> print(f"Country: {country_stats.country}")
        >>> print(f"Network: MCC {country_stats.mcc}, MNC {country_stats.mnc}")
        >>> print(f"SMS sent: {country_stats.sms}")
        >>> print(f"Delivery rate: {country_stats.delivered/country_stats.sms*100:.1f}%")
        Country: US
        Network: MCC 310, MNC 410
        SMS sent: 1200
        Delivery rate: 95.8%
    
    Note:
        - The country field typically contains ISO 3166-1 alpha-2 country codes (e.g., "US", "GB")
        - The MCC (Mobile Country Code) and MNC (Mobile Network Code) together identify a
          specific mobile network
        - These statistics represent outgoing messages only, grouped by destination
          country and network
        - Performance metrics can vary significantly between countries and carriers
    """
    country: Optional[str] = Field(default=None)
    mcc: str
    mnc: str

class IncomingStats(BaseModel):
    """
    Model representing time-based incoming SMS statistics in the Naxai messaging system.
    
    This class defines the structure for incoming SMS metrics data, providing information
    about received message volumes grouped by hour, day, or month.
    
    Attributes:
        date (str): The specific date or timestamp for this metrics entry, in a format
            corresponding to the grouping level (YYYY-MM-DD for day grouping,
            YYYY-MM-DDTHH:00:00Z for hour grouping, etc.).
        sms (int): Total number of incoming SMS messages received during this time period.
    
    Example:
        >>> daily_stats = IncomingStats(
        ...     date="2023-01-15",
        ...     sms=250
        ... )
        >>> print(f"Date: {daily_stats.date}")
        >>> print(f"SMS received: {daily_stats.sms}")
        Date: 2023-01-15
        SMS received: 250
    
    Note:
        - The date format depends on the grouping level used in the API request
        - For hour grouping: YYYY-MM-DDTHH:00:00Z
        - For day grouping: YYYY-MM-DD
        - For month grouping: YYYY-MM
        - These statistics represent incoming messages only
        - Incoming messages have simpler metrics as they don't have delivery statuses
    """
    date: str
    sms: int

class DeliveryErrorStats(BaseModel):
    """
    Model representing SMS delivery error statistics in the Naxai messaging system.
    
    This class defines the structure for SMS delivery error metrics, providing detailed
    information about specific error types and their frequencies.
    
    Attributes:
        status_category (str): The general category of the delivery error.
            Mapped from JSON key 'statusCategory'.
        status_code (str): The specific error code identifying the delivery issue.
            Mapped from JSON key 'statusCode'.
        sms (int): Number of SMS messages that encountered this specific error.
    
    Example:
        >>> error_stats = DeliveryErrorStats(
        ...     statusCategory="carrier",
        ...     statusCode="REJECTED_DESTINATION_BLOCKED",
        ...     sms=45
        ... )
        >>> print(f"Error category: {error_stats.status_category}")
        >>> print(f"Error code: {error_stats.status_code}")
        >>> print(f"Affected messages: {error_stats.sms}")
        Error category: carrier
        Error code: REJECTED_DESTINATION_BLOCKED
        Affected messages: 45
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - The status_category field groups errors into broader categories
          (e.g., "carrier", "handset")
        - The status_code field provides the specific error code for detailed troubleshooting
        - These statistics help identify common delivery issues and their impact
        - Error patterns can be used to improve message delivery strategies
    """
    status_category: str = Field(alias="statusCategory")
    status_code: str = Field(alias="statusCode")
    sms: int

    model_config = {"populate_by_name": True}

class ListOutgoingSMSMetricsResponse(BaseResponse):
    """
    Model representing time-based outgoing SMS metrics in the Naxai messaging system.
    
    This class extends BaseResponse to provide detailed metrics about outgoing SMS messages,
    grouped by hour, day, or month. It includes comprehensive statistics about message
    volumes, delivery outcomes, and timing metrics for the specified time period.
    
    Attributes:
        direction (Literal["outgoing"]): Indicates that these metrics are for outgoing messages.
        group (Literal["hour", "day", "month"]): The time interval grouping used for the metrics.
        stats (list[OutgoingStats]): List of statistics entries, each representing metrics
            for a specific time interval within the overall period.
            
        # Inherited from BaseResponse:
        start_date (str): The beginning of the time period for these metrics.
        stop_date (str): The end of the time period for these metrics.
    
    Example:
        >>> response = ListOutgoingSMSMetricsResponse(
        ...     startDate="2023-01-01",
        ...     stopDate="2023-01-31",
        ...     direction="outgoing",
        ...     group="day",
        ...     stats=[
        ...         OutgoingStats(
        ...             date="2023-01-01",
        ...             sms=450,
        ...             delivered=430,
        ...             failed=10,
        ...             expired=5,
        ...             unknown=0,
        ...             canceled=3,
        ...             rejected=2,
        ...             avgTimeToDeliver=2100,
        ...             avgTimeToSubmit=115
        ...         ),
        ...         OutgoingStats(
        ...             date="2023-01-02",
        ...             sms=520,
        ...             delivered=500,
        ...             failed=12,
        ...             expired=3,
        ...             unknown=1,
        ...             canceled=2,
        ...             rejected=2,
        ...             avgTimeToDeliver=2200,
        ...             avgTimeToSubmit=120
        ...         )
        ...     ]
        ... )
        >>> print(f"Period: {response.start_date} to {response.stop_date}")
        >>> print(f"Grouping: {response.group}")
        >>> print(f"Number of data points: {len(response.stats)}")
        >>> 
        >>> # Calculate overall metrics
        >>> total_sms = sum(day.sms for day in response.stats)
        >>> total_delivered = sum(day.delivered for day in response.stats)
        >>> print(f"Total SMS: {total_sms}")
        >>> print(f"Overall delivery rate: {total_delivered/total_sms*100:.1f}%")
        Period: 2023-01-01 to 2023-01-31
        Grouping: day
        Number of data points: 2
        Total SMS: 970
        Overall delivery rate: 95.9%
    
    Note:
        - The stats list contains entries corresponding to the specified grouping level
        - For hour grouping: One entry per hour in the date range
        - For day grouping: One entry per day in the date range
        - For month grouping: One entry per month in the date range
        - These metrics provide insights into outgoing message performance over time
    """
    direction: Literal["outgoing"]
    group: Literal["hour", "day", "month"]
    stats: list[OutgoingStats]

class ListOutgoingSMSByCountryMetricsResponse(BaseResponse):
    """
    Model representing country-based outgoing SMS metrics in the Naxai messaging system.
    
    This class extends BaseResponse to provide detailed metrics about outgoing SMS messages,
    grouped by destination country and mobile network. It includes comprehensive statistics
    about message volumes, delivery outcomes, and timing metrics for each country.
    
    Attributes:
        direction (Literal["outgoing"]): Indicates that these metrics are for outgoing messages.
        stats (list[OutgoingCountryStats]): List of statistics entries, each representing metrics
            for a specific country and mobile network within the overall period.
            
        # Inherited from BaseResponse:
        start_date (str): The beginning of the time period for these metrics.
        stop_date (str): The end of the time period for these metrics.
    
    Example:
        >>> response = ListOutgoingSMSByCountryMetricsResponse(
        ...     startDate="2023-01-01",
        ...     stopDate="2023-01-31",
        ...     direction="outgoing",
        ...     stats=[
        ...         OutgoingCountryStats(
        ...             country="US",
        ...             mcc="310",
        ...             mnc="410",
        ...             sms=1200,
        ...             delivered=1150,
        ...             failed=30,
        ...             expired=10,
        ...             unknown=5,
        ...             canceled=3,
        ...             rejected=2,
        ...             avgTimeToDeliver=1800,
        ...             avgTimeToSubmit=110
        ...         ),
        ...         OutgoingCountryStats(
        ...             country="GB",
        ...             mcc="234",
        ...             mnc="15",
        ...             sms=800,
        ...             delivered=780,
        ...             failed=12,
        ...             expired=5,
        ...             unknown=0,
        ...             canceled=2,
        ...             rejected=1,
        ...             avgTimeToDeliver=1600,
        ...             avgTimeToSubmit=105
        ...         )
        ...     ]
        ... )
        >>> print(f"Period: {response.start_date} to {response.stop_date}")
        >>> print(f"Number of countries: {len(response.stats)}")
        >>> 
        >>> # Compare delivery rates by country
        >>> for country in response.stats:
        ...     delivery_rate = country.delivered / country.sms * 100
        ...     print(f"{country.country}: {delivery_rate:.1f}% delivery rate")
        Period: 2023-01-01 to 2023-01-31
        Number of countries: 2
        US: 95.8% delivery rate
        GB: 97.5% delivery rate
    
    Note:
        - The stats list contains one entry per country/network combination
        - Countries are typically identified by ISO 3166-1 alpha-2 codes (e.g., "US", "GB")
        - The MCC (Mobile Country Code) and MNC (Mobile Network Code) together identify
          a specific mobile network
        - These metrics provide insights into geographical performance differences
    """
    direction: Literal["outgoing"]
    stats: list[OutgoingCountryStats]

class ListIncomingSMSMetricsResponse(BaseResponse):
    """
    Model representing time-based incoming SMS metrics in the Naxai messaging system.
    
    This class extends BaseResponse to provide metrics about incoming SMS messages,
    grouped by hour, day, or month. It includes statistics about received message
    volumes for the specified time period.
    
    Attributes:
        direction (Literal["incoming"]): Indicates that these metrics are for incoming messages.
        group (Literal["hour", "day", "month"]): The time interval grouping used for the metrics.
        stats (list[IncomingStats]): List of statistics entries, each representing metrics
            for a specific time interval within the overall period.
            
        # Inherited from BaseResponse:
        start_date (str): The beginning of the time period for these metrics.
        stop_date (str): The end of the time period for these metrics.
    
    Example:
        >>> response = ListIncomingSMSMetricsResponse(
        ...     startDate="2023-01-01",
        ...     stopDate="2023-01-31",
        ...     direction="incoming",
        ...     group="day",
        ...     stats=[
        ...         IncomingStats(date="2023-01-01", sms=120),
        ...         IncomingStats(date="2023-01-02", sms=145),
        ...         IncomingStats(date="2023-01-03", sms=135)
        ...     ]
        ... )
        >>> print(f"Period: {response.start_date} to {response.stop_date}")
        >>> print(f"Grouping: {response.group}")
        >>> print(f"Total incoming SMS: {sum(day.sms for day in response.stats)}")
        Period: 2023-01-01 to 2023-01-31
        Grouping: day
        Total incoming SMS: 400
    
    Note:
        - The stats list contains entries corresponding to the specified grouping level
        - For hour grouping: One entry per hour in the date range
        - For day grouping: One entry per day in the date range
        - For month grouping: One entry per month in the date range
        - Incoming metrics are simpler than outgoing metrics as they only track volume
    """
    direction: Literal["incoming"]
    group: Literal["hour", "day", "month"]
    stats: list[IncomingStats]

class ListDeliveryErrorMetricsResponse(BaseResponse):
    """
    Model representing SMS delivery error metrics in the Naxai messaging system.
    
    This class extends BaseResponse to provide detailed metrics about SMS delivery errors,
    grouped by error category and code. It includes statistics about the frequency of
    different error types during the specified time period.
    
    Attributes:
        stats (list[DeliveryErrorStats]): List of statistics entries, each representing metrics
            for a specific error category and code within the overall period.
            
        # Inherited from BaseResponse:
        start_date (str): The beginning of the time period for these metrics.
        stop_date (str): The end of the time period for these metrics.
    
    Example:
        >>> response = ListDeliveryErrorMetricsResponse(
        ...     startDate="2023-01-01",
        ...     stopDate="2023-01-31",
        ...     stats=[
        ...         DeliveryErrorStats(
        ...             statusCategory="carrier",
        ...             statusCode="REJECTED_DESTINATION_BLOCKED",
        ...             sms=45
        ...         ),
        ...         DeliveryErrorStats(
        ...             statusCategory="handset",
        ...             statusCode="HANDSET_BUSY",
        ...             sms=28
        ...         ),
        ...         DeliveryErrorStats(
        ...             statusCategory="network",
        ...             statusCode="NETWORK_ERROR",
        ...             sms=17
        ...         )
        ...     ]
        ... )
        >>> print(f"Period: {response.start_date} to {response.stop_date}")
        >>> print(f"Number of error types: {len(response.stats)}")
        >>> 
        >>> # Group errors by category
        >>> by_category = {}
        >>> for error in response.stats:
        ...     category = error.status_category
        ...     if category not in by_category:
        ...         by_category[category] = 0
        ...     by_category[category] += error.sms
        >>> 
        >>> # Show error distribution by category
        >>> for category, count in by_category.items():
        ...     print(f"{category}: {count} errors")
        Period: 2023-01-01 to 2023-01-31
        Number of error types: 3
        carrier: 45 errors
        handset: 28 errors
        network: 17 errors
    
    Note:
        - The stats list contains one entry per unique error category and code combination
        - Error categories typically include "carrier", "handset", "network", etc.
        - Error codes provide specific information about what went wrong
        - These metrics help identify common delivery issues and their relative frequency
    """
    stats: list[DeliveryErrorStats]
