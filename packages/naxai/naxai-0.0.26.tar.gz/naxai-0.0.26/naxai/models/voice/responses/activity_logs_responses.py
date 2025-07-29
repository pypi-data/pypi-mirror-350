"""
Voice activity logs response models for the Naxai SDK.

This module defines the data structures for responses from voice activity log API operations,
providing models for tracking call history, status, and detailed call information.
"""

from pydantic import BaseModel
from naxai.models.base.pagination import Pagination
from naxai.models.voice.responses.call_base_model import CallBaseModel

class ListActivityLogsResponse(BaseModel):
    """
    Response model for listing voice call activity logs.
    
    This class represents the API response when retrieving a paginated list of call activity logs.
    It contains both pagination information and the actual call data for the requested page.
    
    Attributes:
        pagination (Pagination): Pagination information for the response, including:
            - page: Current page number
            - page_size: Number of items per page
            - total_pages: Total number of pages available
            - total_items: Total number of items across all pages
        calls (list[CallBaseModel]): List of call activity log entries for the current page.
            Each entry contains detailed information about a voice call, including:
            - call_id: Unique identifier for the call
            - from_: Originating phone number
            - to: Destination phone number
            - direction: Call direction (outbound, inbound, transfer)
            - status: Call status (delivered, failed)
            - call_duration: Duration of the call in seconds
            - And many other call attributes (see CallBaseModel for details)
    
    Example:
        >>> response = ListActivityLogsResponse(
        ...     pagination=Pagination(
        ...         page=1,
        ...         page_size=25,
        ...         total_pages=4,
        ...         total_items=87
        ...     ),
        ...     calls=[
        ...         CallBaseModel(
        ...             callId="call_123abc",
        ...             from="+1234567890",
        ...             to="+0987654321",
        ...             fromApp="voice-app",
        ...             direction="outbound",
        ...             callType="transactional",
        ...             callDate=1703066400000,
        ...             status="delivered",
        ...             reason="success",
        ...             details="Call completed successfully",
        ...             input="1",
        ...             callDuration=45,
        ...             country="US",
        ...             network="mobile",
        ...             transferred=False
        ...         ),
        ...         # Additional call entries...
        ...     ]
        ... )
        >>> print(f"Showing page {response.pagination.page} of {response.pagination.total_pages}")
        >>> print(f"Displaying {len(response.calls)} of \
        >>>         {response.pagination.total_items} total calls")
        >>> for call in response.calls:
        ...     print(f"Call {call.call_id}: {call.status}, Duration: {call.call_duration}s")
    
    Note:
        - Use pagination parameters when making API requests to navigate through large result sets
        - The calls list may be empty if there are no results for the requested filters
        - Each call in the list contains complete call information as defined in CallBaseModel
        - Typically, calls are sorted by call_date in descending order (most recent first)
    
    See Also:
        CallBaseModel: For detailed information about individual call attributes
        Pagination: For details about the pagination structure
        GetActivityLogResponse: For retrieving a single call's details
    """
    pagination: Pagination
    items: list[CallBaseModel]

class GetActivityLogResponse(CallBaseModel):
    """
    Response model for retrieving a single voice call activity log.
    
    This class represents the API response when fetching detailed information about
    a specific call by its ID. It inherits all fields from CallBaseModel, providing
    comprehensive information about the call's properties, status, and metrics.
    
    The model includes all attributes from CallBaseModel:
        - call_id: Unique identifier for the call
        - from_: Originating phone number
        - to: Destination phone number
        - direction: Call direction (outbound, inbound, transfer)
        - status: Call status (delivered, failed)
        - And many other call attributes (see CallBaseModel for complete details)
    
    Example:
        >>> call_detail = GetActivityLogResponse(
        ...     callId="call_123abc",
        ...     from="+1234567890",
        ...     to="+0987654321",
        ...     fromApp="voice-app",
        ...     direction="outbound",
        ...     callType="transactional",
        ...     callDate=1703066400000,
        ...     status="delivered",
        ...     reason="success",
        ...     details="Call completed successfully",
        ...     input="1",
        ...     callDuration=45,
        ...     country="US",
        ...     network="mobile",
        ...     transferred=False
        ... )
        >>> print(f"Call {call_detail.call_id} from {call_detail.from_} to {call_detail.to}")
        >>> print(f"Duration: {call_detail.call_duration} seconds, Status: {call_detail.status}")
    
    See Also:
        CallBaseModel: For detailed information about all available call attributes
        ListActivityLogsResponse: For retrieving multiple calls with pagination
    """
