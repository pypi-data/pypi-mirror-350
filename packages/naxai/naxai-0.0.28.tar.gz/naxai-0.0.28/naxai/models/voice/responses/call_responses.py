"""
Voice call response models for the Naxai SDK.

This module defines the data structures for responses from voice call API operations,
including call creation and individual call details.
"""

from pydantic import BaseModel, Field

class Call(BaseModel):
    """
    Model representing a single call in a voice call response.
    
    This class defines the minimal structure for an individual call reference,
    containing just the essential identifiers needed to track the call.
    
    Attributes:
        call_id (str): Unique identifier for the call. Mapped from JSON key 'callId'.
        to (str): The destination phone number or identifier for the call.
    
    Example:
        >>> call = Call(callId="call_123abc", to="+1234567890")
        >>> print(f"Call {call.call_id} to {call.to}")
        Call call_123abc to +1234567890
    """
    call_id: str = Field(alias="callId")
    to: str

class CreateCallResponse(BaseModel):
    """
    Response model for creating voice calls in the Naxai system.
    
    This class defines the structure for the API response when successfully
    initiating one or more voice calls, providing batch information and
    individual call references.
    
    Attributes:
        batch_id (str): Unique identifier for the batch of calls.
            Mapped from JSON key 'batchId'.
        count (int): The number of calls included in this batch.
        calls (list[Call]): List of individual call objects containing
            call IDs and recipient information.
    
    Example:
        >>> response = CreateCallResponse(
        ...     batchId="batch_123abc",
        ...     count=3,
        ...     calls=[
        ...         Call(callId="call_123", to="+1234567890"),
        ...         Call(callId="call_456", to="+2345678901"),
        ...         Call(callId="call_789", to="+3456789012")
        ...     ]
        ... )
        >>> print(f"Batch ID: {response.batch_id}")
        >>> print(f"Calls initiated: {response.count}")
        >>> for call in response.calls:
        ...     print(f"Call to {call.to}: ID {call.call_id}")
        Batch ID: batch_123abc
        Calls initiated: 3
        Call to +1234567890: ID call_123
        Call to +2345678901: ID call_456
        Call to +3456789012: ID call_789
    
    Note:
        - The batch_id can be used to track the entire group of calls
        - Each call in the calls list has its own unique call_id for individual tracking
        - Successful response means the calls were accepted for processing, not that
          they were connected or completed
        - Call status must be checked separately using the call_id or batch_id
    """
    batch_id: str = Field(alias="batchId")
    count: int
    calls: list[Call]
