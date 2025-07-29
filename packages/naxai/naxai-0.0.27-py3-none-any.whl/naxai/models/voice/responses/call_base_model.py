"""
Voice call base model for the Naxai SDK.

This module defines the core data structure for representing voice calls,
including call details, status information, and transfer-related attributes
used throughout the voice API responses.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field

LITERAL_REASONS = Literal["success",
                          "rejected",
                          "busy",
                          "canceled-by-contact",
                          "no-answer",
                          "canceled-by-user",
                          "canceled-by-system",
                          "scheduled",
                          "inbound",
                          "voicemail"]
TRANSFER_REASONS = Literal["success", "busy", "no-answer", "rejected"]
CALL_TYPES = Literal["default", "marketing", "transactional", "otp", "crisis"]

class CallBaseModel(BaseModel):
    """
    Base model representing a voice call in the Naxai system.
    
    This class defines the core structure for call data, including call identification,
    routing information, status, and detailed metrics. It captures both standard call
    attributes and transfer-related information when applicable.
    
    Attributes:
        call_id (str): Unique identifier for the call. Mapped from JSON key 'callId'.
        from_ (str): The originating phone number or identifier. Mapped from JSON key 'from'.
        to (str): The destination phone number or identifier.
        from_app (Optional[str]): The application or service that initiated the call.
            Mapped from JSON key 'fromApp'.
        direction (Literal["outbound", "transfer", "inbound"]): The direction of the call.
            - "outbound": Call initiated from the system to an external number
            - "transfer": Call transferred to another destination
            - "inbound": Call received by the system from an external number
        call_type (Literal["default", "marketing", "transactional", "otp", "crisis"]): 
            The classification of the call. Mapped from JSON key 'callType'.
        call_date (int): Timestamp when the call was initiated, in milliseconds since epoch.
            Mapped from JSON key 'callDate'.
        status (Literal["delivered", "failed"]): The final status of the call.
        reason (Literal): Detailed reason for the call outcome. Possible values include:
            - "success": Call was successfully completed
            - "rejected": Call was rejected by the recipient or carrier
            - "busy": Recipient's line was busy
            - "canceled-by-contact": Call was canceled by the recipient
            - "no-answer": Call was not answered
            - "canceled-by-user": Call was canceled by the user
            - "canceled-by-system": Call was canceled by the system
            - "scheduled": Call is scheduled for future delivery
            - "inbound": Call was inbound
            - "voicemail": Call reached voicemail
        details (str): Additional details or notes about the call.
        input_ (Optional[str]): DTMF input received during the call. Mapped from JSON key 'input'.
        call_duration (int): Duration of the call in seconds. Mapped from JSON key 'callDuration'.
        country (str): Country code where the call was received.
        network (Literal["landline", "mobile"]): Type of network the call was connected to.
        transferred (bool): Whether the call was transferred to another destination.
        transfer_call_id (Optional[str]): Unique identifier for the transferred call, if applicable.
            Mapped from JSON key 'transferCallId'.
        transfer_status (Optional[Literal["delivered", "failed"]]): Status of the transferred call.
            Mapped from JSON key 'transferStatus'.
        transfer_duration (Optional[int]): Duration of the transferred call in seconds.
            Mapped from JSON key 'transferDuration'.
        transfer_reason (Optional[Literal["success", "busy", "no-answer", "rejected"]]):
            Reason for the transfer outcome. Mapped from JSON key 'transferReason'.
        transfer_details (Optional[str]): Additional details about the transfer.
            Mapped from JSON key 'transferDetails'.
        transfer_attempts (Optional[int]): Number of transfer attempts made.
            Mapped from JSON key 'transferAttempts'.
        client_id (Optional[str]): Identifier of the client associated with the call.
            Mapped from JSON key 'clientId'.
        campaign_id (Optional[str]): Identifier of the campaign associated with the call.
            Mapped from JSON key 'campaignId'.
        broadcast_id (Optional[str]): Identifier of the broadcast associated with the call.
            Mapped from JSON key 'broadcastId'.
    
    Example:
        >>> call = CallBaseModel(
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
        >>> print(f"Call {call.call_id} from {call.from_} to {call.to}")
        >>> print(f"Duration: {call.call_duration} seconds, Status: {call.status}")
    
    Note:
        - All timestamp fields are in milliseconds since epoch
        - Transfer-related fields are only populated when transferred=True
        - Optional fields may be None if not applicable or not provided in the API response
        - The model supports both alias-based and direct field name access through populate_by_name
    """
    call_id: str = Field(alias="callId")
    from_: str = Field(alias="from")
    to: str
    from_app: Optional[str] = Field(alias="fromApp", default=None)
    direction: Literal["outbound", "transfer", "inbound"]
    call_type: CALL_TYPES = Field(alias="callType")
    call_date: int = Field(alias="callDate")
    status: Literal["delivered", "failed"]
    reason: LITERAL_REASONS
    details: str
    input_: Optional[str] = Field(alias="input", default=None)
    call_duration: int = Field(alias="callDuration")
    country: str
    network: Literal["landline", "mobile"]
    transferred: bool
    transfer_call_id: Optional[str] = Field(alias="transferCallId", default=None)
    transfer_status: Optional[Literal["delivered", "failed"]] = Field(alias="transferStatus",
                                                                      default=None)
    transfer_duration: Optional[int] = Field(alias="transferDuration", default=None)
    transfer_reason: Optional[TRANSFER_REASONS] = Field(alias="transferReason",
                                                        default=None)
    transfer_details: Optional[str] = Field(alias="transferDetails", default=None)
    transfer_attempts: Optional[int] = Field(alias="transferAttempts", default=None)
    client_id: Optional[str] = Field(alias="clientId", default=None)
    campaign_id: Optional[str] = Field(alias="campaignId", default=None)
    broadcast_id: Optional[str] = Field(alias="broadcastId", default=None)

    model_config = {"populate_by_name": True}
