"""
SMS activity logs response models for the Naxai SDK.

This module defines the data structures for responses from SMS activity log API operations,
providing models for tracking message delivery status, content, and metadata for both
outbound and inbound SMS messages.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field
from naxai.models.base.pagination import Pagination

class BaseMessage(BaseModel):
    """
    Base model representing a detailed SMS message in the Naxai messaging system.
    
    This class defines the comprehensive structure for SMS message data, providing
    complete information about a message's routing, content, status, and associated
    metadata. It serves as the foundation for SMS activity logs and detailed message views.
    
    Attributes:
        message_id (str): Unique identifier for the message.
            Mapped from JSON key 'messageId'.
        from_ (str): The sender's phone number or identifier.
            Mapped from JSON key 'from'. May be None for some inbound messages.
        to (str): The recipient's phone number or identifier.
        mcc (str): Mobile Country Code identifying the recipient's mobile network country.
            May be None if not available.
        mnc (str): Mobile Network Code identifying the recipient's specific mobile network.
            May be None if not available.
        body (str): The text content of the SMS message.
        parts (int): Number of message parts/segments used to deliver the SMS.
            May be None if not applicable or not determined.
        encoding (Literal["unicode", "text", "binary"]): 
            The character encoding used for the message:
            - "unicode": Unicode encoding (UTF-16) for messages with special characters
            - "text": Standard GSM 7-bit encoding for basic Latin characters
            - "binary": Binary encoding for data messages
        direction (Literal["outbound", "inbound"]): The direction of the message:
            - "outbound": Message sent from the platform to a recipient
            - "inbound": Message received by the platform from a sender
        sent_at (int): Timestamp when the message was sent, in milliseconds since epoch.
            Mapped from JSON key 'sentAt'. May be None if not yet sent.
        submitted_at (int): Timestamp when the message was submitted to the carrier,
            in milliseconds since epoch. Mapped from JSON key 'submittedAt'.
            May be None if not yet submitted.
        delivered_at (int): Timestamp when the message was delivered to the recipient,
            in milliseconds since epoch. Mapped from JSON key 'deliveredAt'.
            May be None if not yet delivered or delivery confirmation is unavailable.
        received_at (int): Timestamp when an inbound message was received by the platform,
            in milliseconds since epoch. Mapped from JSON key 'receivedAt'.
            May be None for outbound messages.
        status (Literal["delivered", "failed"]): The final delivery status of the message.
            May be None if the final status is not yet determined.
        status_code (int): Numeric code providing detailed status information.
            Mapped from JSON key 'statusCode'. May be None if not available.
        status_reason (str): Short description of the status reason.
            Mapped from JSON key 'statusReason'. May be None if not available.
        status_details (str): Detailed explanation of the message status.
            Mapped from JSON key 'statusDetails'. May be None if not available.
        opt_out (bool): Indicates whether this message resulted in an opt-out request.
            Mapped from JSON key 'optOut'. May be None if not applicable.
        reference (str): Custom reference identifier for the message.
            May be None if not provided.
        client_id (str): Identifier of the client associated with the message.
            Mapped from JSON key 'clientId'. May be None if not applicable.
        campaign_id (str): Identifier of the campaign associated with the message.
            Mapped from JSON key 'campaignId'. May be None if not applicable.
        broadcast_id (str): Identifier of the broadcast associated with the message.
            Mapped from JSON key 'broadcastId'. May be None if not applicable.
    
    Example:
        >>> message = BaseMessage(
        ...     messageId="msg_123abc456def",
        ...     from="+12065550100",
        ...     to="+14255550199",
        ...     mcc="310",
        ...     mnc="410",
        ...     body="Hello! This is a test message.",
        ...     parts=1,
        ...     encoding="text",
        ...     direction="outbound",
        ...     sentAt=1703066400000,
        ...     submittedAt=1703066401000,
        ...     deliveredAt=1703066405000,
        ...     status="delivered",
        ...     statusCode=0,
        ...     statusReason="success",
        ...     reference="order-123",
        ...     campaignId="camp_789xyz"
        ... )
        >>> print(f"Message ID: {message.message_id}")
        >>> print(f"From: {message.from_} to: {message.to}")
        >>> print(f"Content: {message.body}")
        >>> print(f"Status: {message.status} ({message.status_reason})")
        >>> 
        >>> # Calculate delivery time
        >>> if message.delivered_at and message.submitted_at:
        ...     delivery_time_ms = message.delivered_at - message.submitted_at
        ...     print(f"Delivery time: {delivery_time_ms} ms")
        >>> 
        >>> # Check if message is part of a campaign
        >>> if message.campaign_id:
        ...     print(f"Part of campaign: {message.campaign_id}")
        Message ID: msg_123abc456def
        From: +12065550100 to: +14255550199
        Content: Hello! This is a test message.
        Status: delivered (success)
        Delivery time: 4000 ms
        Part of campaign: camp_789xyz
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - The message_id is the primary identifier for tracking and querying messages
        - Timestamps (sent_at, submitted_at, delivered_at, received_at) are in milliseconds
          since epoch
        - For outbound messages, the typical flow is: sent_at -> submitted_at -> delivered_at
        - For inbound messages, received_at is the primary timestamp
        - The encoding field affects how many characters can fit in a single message part:
          * text: Up to 160 characters per part
          * unicode: Up to 70 characters per part
          * binary: Up to 140 bytes per part
        - The status field indicates the final delivery outcome, while status_code, status_reason,
          and status_details provide more granular information about delivery results
        - The mcc and mnc fields can be used to identify the recipient's mobile network
        - The reference field can be used to associate the message with external systems
        - The client_id, campaign_id, and broadcast_id fields link the message to other
          entities within the Naxai system
    
    See Also:
        ListSMSActivityLogsResponse: For retrieving multiple messages with pagination
    """
    message_id: str = Field(alias="messageId")
    from_: str = Field(alias="from", default=None)
    to: str
    mcc: str = Field(default=None)
    mnc: str = Field(default=None)
    body: str
    parts: int = Field(default=None)
    encoding: Literal["unicode", "text", "binary"]
    direction: Literal["outgoing", "incoming"]
    sent_at: int = Field(alias="sentAt", default=None)
    submitted_at: Optional[int] = Field(alias="submittedAt", default=None)
    delivered_at: Optional[int] = Field(alias="deliveredAt", default=None)
    received_at: Optional[int] = Field(alias="receivedAt", default=None)
    status: Optional[Literal["delivered", "failed"]] = Field(default=None)
    status_code: Optional[int] = Field(alias="statusCode", default=None)
    status_reason: Optional[str] = Field(alias="statusReason", default=None)
    status_details: Optional[str] = Field(alias="statusDetails", default=None)
    opt_out: Optional[bool] = Field(alias="optOut", default=None)
    reference: Optional[str] = Field(default=None)
    client_id: Optional[str] = Field(alias="clientId", default=None)
    campaign_id: Optional[str] = Field(alias="campaignId", default=None)
    broadcast_id: Optional[str] = Field(alias="broadcastId", default=None)

    model_config = {"populate_by_name": True}

class ListSMSActivityLogsResponse(BaseModel):
    """
    Model representing a paginated list of SMS messages in the Naxai messaging system.
    
    This class defines the structure for the API response when retrieving SMS activity logs,
    including pagination information and a list of detailed message objects. It provides
    a convenient way to access and analyze message history and delivery status.
    
    Attributes:
        pagination (Pagination): Pagination information for the response, including:
            - page: Current page number
            - page_size: Number of items per page
            - total_pages: Total number of pages available
            - total_items: Total number of messages across all pages
        messages (list[BaseMessage]): List of detailed message objects containing
            comprehensive information about each SMS message.
    
    Example:
        >>> response = ListSMSActivityLogsResponse(
        ...     pagination=Pagination(
        ...         page=1,
        ...         page_size=25,
        ...         total_pages=4,
        ...         total_items=87
        ...     ),
        ...     messages=[
        ...         BaseMessage(
        ...             messageId="msg_123abc",
        ...             from_="+12065550100",
        ...             to="+14255550199",
        ...             body="Hello! This is message 1.",
        ...             encoding="text",
        ...             direction="outbound",
        ...             status="delivered"
        ...         ),
        ...         BaseMessage(
        ...             messageId="msg_456def",
        ...             from_="+12065550100",
        ...             to="+14255550200",
        ...             body="Hello! This is message 2.",
        ...             encoding="text",
        ...             direction="outbound",
        ...             status="failed"
        ...         )
        ...     ]
        ... )
        >>> print(f"Showing page {response.pagination.page} of {response.pagination.total_pages}")
        >>> print(f"Displaying {len(response.messages)} of \
        >>>         {response.pagination.total_items} total messages")
        >>> 
        >>> # Count messages by status
        >>> status_counts = {"delivered": 0, "failed": 0, "pending": 0}
        >>> for msg in response.messages:
        ...     if msg.status in status_counts:
        ...         status_counts[msg.status] += 1
        ...     elif msg.status is None:
        ...         status_counts["pending"] += 1
        >>> 
        >>> print(f"Delivered: {status_counts['delivered']}")
        >>> print(f"Failed: {status_counts['failed']}")
        >>> print(f"Pending: {status_counts['pending']}")
        >>> 
        >>> # Find messages to a specific recipient
        >>> to_specific_number = [msg for msg in response.messages if msg.to == "+14255550199"]
        >>> print(f"Messages to +14255550199: {len(to_specific_number)}")
        Showing page 1 of 4
        Displaying 2 of 87 total messages
        Delivered: 1
        Failed: 1
        Pending: 0
        Messages to +14255550199: 1
    
    Note:
        - Use pagination parameters when making API requests to navigate through large result sets
        - The messages list contains complete message information as defined in BaseMessage
        - Messages in the list may have different statuses, directions, and timestamps
        - The list may be sorted by sent_at, received_at, or other criteria depending on the API
        - Each message in the list contains its unique ID, which can be used for further operations
        - For large collections, request additional pages by incrementing the page parameter
        - Filtering options may be available when querying the API (by date range, status, etc.)
    
    See Also:
        BaseMessage: For the structure of individual message objects
        Pagination: For details about the pagination structure
    """
    pagination: Pagination
    messages: list[BaseMessage]

class GetSMSActivityLogsResponse(BaseMessage):
    """
    Model representing the response from retrieving a specific SMS message in the Naxai
    messaging system.
    
    This class extends BaseMessage to represent the API response when fetching detailed
    information about an individual SMS message by its ID. It includes comprehensive
    information about the message's routing, content, delivery status, and associated metadata.
    
    Inherits all attributes from BaseMessage:
        - message_id (str): Unique identifier for the message
        - from_ (str): The sender's phone number or identifier
        - to (str): The recipient's phone number or identifier
        - mcc (str): Mobile Country Code identifying the recipient's mobile network country
        - mnc (str): Mobile Network Code identifying the recipient's specific mobile network
        - body (str): The text content of the SMS message
        - parts (int): Number of message parts/segments used to deliver the SMS
        - encoding (Literal["unicode", "text", "binary"]):
            The character encoding used for the message
        - direction (Literal["outbound", "inbound"]): The direction of the message
        - sent_at (int): Timestamp when the message was sent
        - submitted_at (int): Timestamp when the message was submitted to the carrier
        - delivered_at (int): Timestamp when the message was delivered to the recipient
        - received_at (int): Timestamp when an inbound message was received by the platform
        - status (Literal["delivered", "failed"]): The final delivery status of the message
        - status_code (int): Numeric code providing detailed status information
        - status_reason (str): Short description of the status reason
        - status_details (str): Detailed explanation of the message status
        - opt_out (bool): Indicates whether this message resulted in an opt-out request
        - reference (str): Custom reference identifier for the message
        - client_id (str): Identifier of the client associated with the message
        - campaign_id (str): Identifier of the campaign associated with the message
        - broadcast_id (str): Identifier of the broadcast associated with the message
    
    Example:
        >>> response = GetSMSActivityLogsResponse(
        ...     messageId="msg_123abc456def",
        ...     from_="+12065550100",
        ...     to="+14255550199",
        ...     mcc="310",
        ...     mnc="410",
        ...     body="Hello! This is a test message.",
        ...     parts=1,
        ...     encoding="text",
        ...     direction="outbound",
        ...     sentAt=1703066400000,
        ...     submittedAt=1703066401000,
        ...     deliveredAt=1703066405000,
        ...     status="delivered",
        ...     statusCode=0,
        ...     statusReason="success",
        ...     statusDetails="Message delivered to handset",
        ...     reference="order-123",
        ...     campaignId="camp_789xyz"
        ... )
        >>> print(f"Message ID: {response.message_id}")
        >>> print(f"From: {response.from_} to: {response.to}")
        >>> print(f"Content: {response.body}")
        >>> print(f"Status: {response.status} ({response.status_reason})")
        >>> print(f"Details: {response.status_details}")
        >>> 
        >>> # Display message timeline
        >>> timeline = []
        >>> if response.sent_at:
        ...     timeline.append(f"Sent: {response.sent_at}")
        >>> if response.submitted_at:
        ...     timeline.append(f"Submitted: {response.submitted_at}")
        >>> if response.delivered_at:
        ...     timeline.append(f"Delivered: {response.delivered_at}")
        >>> print("Message timeline:")
        >>> for event in timeline:
        ...     print(f"- {event}")
        >>> 
        >>> # Calculate delivery metrics
        >>> if response.delivered_at and response.submitted_at:
        ...     delivery_time_ms = response.delivered_at - response.submitted_at
        ...     print(f"Delivery time: {delivery_time_ms} ms")
        Message ID: msg_123abc456def
        From: +12065550100 to: +14255550199
        Content: Hello! This is a test message.
        Status: delivered (success)
        Details: Message delivered to handset
        Message timeline:
        - Sent: 1703066400000
        - Submitted: 1703066401000
        - Delivered: 1703066405000
        Delivery time: 4000 ms
    
    Note:
        - This response provides the complete details of a single SMS message
        - All timestamps (sent_at, submitted_at, delivered_at, received_at) are in milliseconds
          since epoch
        - For outbound messages, the typical flow is: sent_at -> submitted_at -> delivered_at
        - For inbound messages, received_at is the primary timestamp
        - The status field indicates the final delivery outcome, while status_code, status_reason,
          and status_details provide more granular information about delivery results
        - The encoding field affects how many characters can fit in a single message part:
          * text: Up to 160 characters per part
          * unicode: Up to 70 characters per part
          * binary: Up to 140 bytes per part
        - The mcc and mnc fields can be used to identify the recipient's mobile network
        - The reference field can be used to associate the message with external systems
        - The client_id, campaign_id, and broadcast_id fields link the message to other
          entities within the Naxai system
    
    See Also:
        BaseMessage: For the base structure of message information
        ListSMSActivityLogsResponse: For retrieving multiple messages with pagination
    """
    