"""
Voice reporting response models for the Naxai SDK.

This module defines the data structures for responses from voice reporting API operations,
providing models for analyzing call metrics, performance statistics, and geographical
distribution of voice traffic across different time periods.
"""

from typing import Literal, TypeVar, Generic, Optional
from pydantic import BaseModel, Field

class BaseStatsFields(BaseModel):
    """
    Base class for all statistics models containing common fields.
    
    This class defines the fundamental fields that are present in all types of call statistics,
    providing a foundation for more specific statistics models.
    
    Attributes:
        date (str) optional: The date for which statistics are reported, in ISO format (YYYY-MM-DD).
        calls (int): Total number of calls recorded during this period.
        duration (int): Total duration of all calls in seconds.
    """
    date: Optional[str] = None
    calls: int
    duration: int

    model_config = {"populate_by_name": True}

class OutboundStatsFields(BaseStatsFields):
    """
    Extended statistics fields specific to outbound calls.
    
    This class extends BaseStatsFields with additional metrics relevant to outbound calls,
    tracking various call outcomes and statuses.
    
    Attributes:
        delivered (int): Number of calls successfully delivered to recipients.
        failed (int): Number of calls that failed to complete.
        no_answer (int): Number of calls that weren't answered by recipients.
        busy (int): Number of calls that received a busy signal.
        rejected (int): Number of calls rejected by the recipient or carrier.
        invalid (int): Number of calls to invalid numbers.
        transferred (int): Number of calls that were transferred.
    """
    delivered: int
    failed: int
    no_answer: int = Field(alias="noAnswer")
    busy: int
    rejected: int
    invalid: int
    transferred: int

    model_config = {"populate_by_name": True}

class BaseStats(OutboundStatsFields):
    """
    Standard statistics model for outbound calls.
    
    This class represents the complete set of statistics for outbound calls,
    inheriting all fields from OutboundStatsFields without adding additional fields.
    It serves as the concrete implementation for general outbound call statistics.
    """


class InboundStats(BaseStatsFields):
    """
    Statistics model specific to inbound calls.
    
    This class extends BaseStatsFields with metrics relevant to inbound calls,
    focusing on call reception and transfers.
    
    Attributes:
        received (int): Number of calls received.
        transferred (int): Number of inbound calls that were transferred.
    """
    received: int
    transferred: int

class CountryStats(OutboundStatsFields):
    """
    Statistics model for calls grouped by country.
    
    This class extends OutboundStatsFields with country information,
    allowing for geographical analysis of call metrics.
    
    Attributes:
        country (str): The country code or name for which statistics are reported.
    """
    country: str
    date: Optional[str] = None

class BaseMetricsResponse(BaseModel):
    """
    Base class for all metrics response models.
    
    This class defines the common fields present in all metrics API responses,
    providing context for the reported statistics.
    
    Attributes:
        start_date (int): Start timestamp of the reporting period in milliseconds since epoch.
        stop_date (int): End timestamp of the reporting period in milliseconds since epoch.
        direction (str): Call direction, typically "inbound" or "outbound".
        number (str): The phone number associated with these metrics.
    """
    start_date: int = Field(alias="startDate")
    stop_date: int = Field(alias="stopDate")
    direction: str
    number: str

    model_config = {"populate_by_name": True}

T = TypeVar('T')
class MetricsResponse(BaseModel, Generic[T]):
    """
    Generic base class for all metrics responses with typed statistics.
    
    This class uses generics to provide type-safe access to different kinds of statistics
    while sharing common response fields.
    
    Type Parameters:
        T: The specific statistics model type contained in the response.
    
    Attributes:
        start_date (str): Start timestamp of the reporting period in milliseconds since epoch.
        stop_date (str): End timestamp of the reporting period in milliseconds since epoch.
        direction (str): Call direction, typically "inbound" or "outbound".
        number (str): The phone number associated with these metrics.
        stats (list[T]): List of statistics entries of type T.
    """
    start_date: str = Field(alias="startDate")
    stop_date: str = Field(alias="stopDate")
    direction: str
    number: str
    stats: list[T]

    model_config = {"populate_by_name": True}

class ListOutboundMetricsResponse(MetricsResponse[BaseStats]):
    """
    Response model for outbound call metrics.
    
    This class represents the API response for outbound call metrics,
    containing a list of BaseStats and grouping information.
    
    Attributes:
        group (Literal["hour", "day", "month"]): The time interval grouping for the statistics.
        stats (list[BaseStats]): List of outbound call statistics.
    """
    group: Literal["hour", "day", "month"]

class TransferredStats(BaseStatsFields):
    """
    Statistics model specific to transferred calls.
    
    This class extends BaseStatsFields with metrics relevant to transferred calls,
    focusing on delivery status and call outcomes without requiring the transferred count.
    
    Attributes:
        delivered (int): Number of calls successfully delivered to recipients.
        failed (int): Number of calls that failed to complete.
        no_answer (int): Number of calls that weren't answered by recipients.
        busy (int): Number of calls that received a busy signal.
        rejected (int): Number of calls rejected by the recipient or carrier.
        invalid (int): Number of calls to invalid numbers.
    """
    delivered: int
    failed: int
    no_answer: int = Field(alias="noAnswer")
    busy: int
    rejected: int
    invalid: int

    model_config = {"populate_by_name": True}

class ListTransferredMetricsResponse(MetricsResponse[TransferredStats]):
    """
    Response model for transferred call metrics.
    
    This class represents the API response for transferred call metrics,
    containing a list of BaseStats and grouping information.
    
    Attributes:
        group (Literal["day", "month"]): The time interval grouping for the statistics.
        stats (list[TransferredStats]): List of transferred call statistics.
    """
    group: Literal["day", "month"]

class ListInboundMetricsResponse(MetricsResponse[InboundStats]):
    """
    Response model for inbound call metrics.
    
    This class represents the API response for inbound call metrics,
    containing a list of InboundStats and grouping information.
    
    Attributes:
        group (Literal["day", "month", "hour"]): The time interval grouping for the statistics.
        stats (list[InboundStats]): List of inbound call statistics.
    """
    group: Literal["day", "month", "hour"]

class ListOutboundCallsByCountryMetricsResponse(MetricsResponse[CountryStats]):
    """
    Response model for outbound call metrics grouped by country.
    
    This class represents the API response for outbound call metrics organized by country,
    containing a list of CountryStats with geographical information.
    
    Attributes:
        stats (list[CountryStats]): List of outbound call statistics by country.
    """
