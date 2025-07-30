"""
Voice response models for the Naxai SDK.

This module provides data structures for responses from voice-related API operations,
including broadcasts, calls, activity logs, and reporting metrics.
"""

from .broadcasts_responses import (
    ActionItem,
    Actions,
    BroadcastBase,
    GetBroadcastInputMetricsResponse,
    BroadcastRecipient,
    BroadcastResponseBase,
    BroadcastResponseItem,
    BroadcastStatusResponse,
    CancelBroadcastResponse,
    CreateBroadcastResponse,
    GetBroadcastMetricsResponse,
    GetBroadcastRecipientResponse,
    GetBroadcastResponse,
    Inputs,
    ListBroadcastRecipientsResponse,
    ListBroadcastResponse,
    PauseBroadcastResponse,
    RecipientCall,
    ResumeBroadcastResponse,
    Sms,
    StartBroadcastResponse,
    Status,
    UpdateBroadcastResponse
)
from .call_responses import CreateCallResponse, Call
from .reporting_responses import (
    ListOutboundMetricsResponse,
    ListTransferredMetricsResponse,
    InboundStats,
    CountryStats,
    BaseMetricsResponse,
)
from .call_base_model import CallBaseModel
from .activity_logs_responses import ListActivityLogsResponse, GetActivityLogResponse

__all__ = [
    # Base classes
    "BroadcastBase",
    "BroadcastResponseBase",
    # Core broadcast responses
    "CreateBroadcastResponse",
    "GetBroadcastResponse",
    "UpdateBroadcastResponse",
    "ListBroadcastResponse",
    # Broadcast control responses
    "StartBroadcastResponse",
    "PauseBroadcastResponse",
    "ResumeBroadcastResponse",
    "CancelBroadcastResponse",
    "BroadcastStatusResponse",
    # Broadcast metrics and analytics
    "GetBroadcastMetricsResponse",
    "GetBroadcastInputMetricsResponse",
    "BroadcastResponseItem",
    # Recipient-related responses
    "BroadcastRecipient",
    "ListBroadcastRecipientsResponse",
    "GetBroadcastRecipientResponse",
    "RecipientCall",
    # Component classes
    "ActionItem",
    "Actions",
    "Inputs",
    "Status",
    "Sms",
    # Call
    "CreateCallResponse",
    "Call",
    # Reporting
    "ListOutboundMetricsResponse",
    "ListTransferredMetricsResponse",
    "InboundStats",
    "CountryStats",
    "BaseMetricsResponse",
    # ActivityLogs
    "CallBaseModel",
    "ListActivityLogsResponse",
    "GetActivityLogResponse"

]
