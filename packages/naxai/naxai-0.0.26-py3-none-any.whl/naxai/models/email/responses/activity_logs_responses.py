"""
Email activity logs response models for the Naxai SDK.

This module defines the data structures for responses from email activity log API operations,
providing models for tracking email delivery status, engagement metrics, and event history.
"""

from typing import Optional, Literal, Union
from pydantic import BaseModel, Field
from naxai.models.base.pagination import Pagination

class BaseActivityLogs(BaseModel):
    """
    Base model representing an email activity log entry in the Naxai email system.
    
    This class defines the core structure for email activity data, providing essential
    information about an email's routing, status, and engagement metrics. It serves as
    the foundation for more specialized activity log models.
    
    Attributes:
        message_id (str): Unique identifier for the email message.
            Mapped from JSON key 'messageId'.
        from_email (str): The sender's email address.
            Mapped from JSON key 'fromEmail'.
        to_email (str): The recipient's email address.
            Mapped from JSON key 'toEmail'.
        subject (Optional[str]): The subject line of the email.
            May be None if not available or not provided.
        status (Optional[Literal["sent", "delivered", "failed"]]): 
            Current delivery status of the email.
            - "sent": Email has been sent but delivery confirmation is pending
            - "delivered": Email has been successfully delivered to the recipient's inbox
            - "failed": Email delivery has failed
            May be None if the status is unknown or not provided.
        created_at (Optional[int]): 
            Timestamp when the email was created/sent, in milliseconds since epoch.
            Mapped from JSON key 'createdAt'. May be None if not available.
        updated_at (Optional[int]): 
            Timestamp when the email status was last updated, in milliseconds since epoch.
            Mapped from JSON key 'updatedAt'. May be None if not available.
        opens (Optional[int]): Number of times the email has been opened by the recipient.
            May be None if not available or not tracked.
        clicks (Optional[int]): 
            Number of times links within the email have been clicked by the recipient.
            May be None if not available or not tracked.
    
    Example:
        >>> activity = BaseActivityLogs(
        ...     messageId="msg_123abc456def",
        ...     fromEmail="sender@example.com",
        ...     toEmail="recipient@example.com",
        ...     subject="Important Update",
        ...     status="delivered",
        ...     createdAt=1703066400000,
        ...     updatedAt=1703066500000,
        ...     opens=3,
        ...     clicks=2
        ... )
        >>> print(f"Message ID: {activity.message_id}")
        >>> print(f"From: {activity.from_email} to: {activity.to_email}")
        >>> print(f"Subject: {activity.subject}")
        >>> print(f"Status: {activity.status}")
        >>> print(f"Sent at: {activity.created_at}")
        >>> print(f"Engagement: {activity.opens} opens, {activity.clicks} clicks")
        Message ID: msg_123abc456def
        From: sender@example.com to: recipient@example.com
        Subject: Important Update
        Status: delivered
        Sent at: 1703066400000
        Engagement: 3 opens, 2 clicks
        
        >>> # Calculate time to delivery
        >>> if activity.created_at and activity.updated_at and activity.status == "delivered":
        ...     delivery_time = activity.updated_at - activity.created_at
        ...     print(f"Time to delivery: {delivery_time} ms")
        Time to delivery: 100000 ms
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - It serves as a base class for more specialized activity log models
        - The message_id is the primary identifier for tracking and querying emails
        - Timestamps (created_at, updated_at) are in milliseconds since epoch
        - The opens and clicks fields provide basic engagement metrics
        - For detailed event history, use the GetEmailActivityLogsResponse class
        - Email status progression typically follows: sent -> delivered or failed
    
    See Also:
        ListEmailActivityLogsResponse: For retrieving multiple email activity logs
        GetEmailActivityLogsResponse: For detailed information about a specific email
        EmailEvents: For detailed event history of an email
    """
    message_id: str = Field(alias="messageId")
    from_email: str = Field(alias="fromEmail")
    to_email: Optional[str] = Field(alias="toEmail", default=None)
    subject: Optional[str] = Field(default=None)
    status: Optional[Literal["sent", "delivered", "failed"]] = Field(default=None)
    created_at: Optional[int] = Field(alias="createdAt", default=None)
    updated_at: Optional[int] = Field(alias="updatedAt", default=None)
    opens: Optional[int] = Field(default=None)
    clicks: Optional[int] = Field(default=None)

    model_config = {"populate_by_name": True}

class EmailEvents(BaseModel):
    """
    Model representing an individual event in an email's lifecycle in the Naxai email system.
    
    This class defines the structure for email event data, providing information about
    specific events that occur during an email's journey from sending to recipient interaction.
    
    Attributes:
        name (Optional[str]): 
            The name or type of the event (e.g., "sent", "delivered", "opened", "clicked").
            May be None if not available.
        processed (Optional[str]):
            Timestamp when the event was processed, typically in ISO 8601 format.
            May be None if not available.
        reason (Optional[str]): Additional information or reason associated with the event,
            particularly useful for failure events. May be None if not applicable or not provided.
    
    Example:
        >>> event = EmailEvents(
        ...     name="delivered",
        ...     processed="2023-12-20T14:30:00Z",
        ...     reason=None
        ... )
        >>> print(f"Event: {event.name}")
        >>> print(f"Processed at: {event.processed}")
        >>> 
        >>> # Example of a failure event
        >>> failure = EmailEvents(
        ...     name="failed",
        ...     processed="2023-12-20T14:25:00Z",
        ...     reason="Mailbox full"
        ... )
        >>> print(f"Event: {failure.name}")
        >>> print(f"Reason: {failure.reason}")
        Event: delivered
        Processed at: 2023-12-20T14:30:00Z
        Event: failed
        Reason: Mailbox full
    
    Note:
        - All fields are optional as they may not be included in all API responses
        - Common event names include:
          * "sent": Email has been accepted for delivery
          * "delivered": Email has been delivered to the recipient's inbox
          * "opened": Recipient has opened the email
          * "clicked": Recipient has clicked a link in the email
          * "failed": Email delivery has failed
          * "bounced": Email has bounced from the recipient's server
          * "complained": Recipient has marked the email as spam
          * "unsubscribed": Recipient has unsubscribed from future emails
        - The processed timestamp format may vary depending on the API version
        - The reason field is particularly important for diagnosing delivery issues
    
    See Also:
        GetEmailActivityLogsResponse: For the complete email activity log with events
    """
    name: Optional[str] = Field(default=None)
    processed: Optional[int] = Field(default=None)
    reason: Optional[Union[dict, str]] = Field(default=None)

class ListEmailActivityLogsResponse(BaseModel):
    """
    Model representing a paginated list of email activity logs in the Naxai email system.
    
    This class defines the structure for the API response when retrieving multiple
    email activity logs, including pagination information and a list of log entries.
    
    Attributes:
        pagination (Pagination): Pagination information for the response, including:
            - page: Current page number
            - page_size: Number of items per page
            - total_pages: Total number of pages available
            - total_items: Total number of email logs across all pages
        messages (list[BaseActivityLogs]): List of email activity log entries, each containing
            information about an individual email's routing, status, and engagement metrics.
    
    Example:
        >>> response = ListEmailActivityLogsResponse(
        ...     pagination=Pagination(
        ...         page=1,
        ...         page_size=25,
        ...         total_pages=4,
        ...         total_items=87
        ...     ),
        ...     messages=[
        ...         BaseActivityLogs(
        ...             messageId="msg_123abc",
        ...             fromEmail="sender@example.com",
        ...             toEmail="recipient1@example.com",
        ...             subject="Important Update",
        ...             status="delivered",
        ...             createdAt=1703066400000,
        ...             opens=2,
        ...             clicks=1
        ...         ),
        ...         BaseActivityLogs(
        ...             messageId="msg_456def",
        ...             fromEmail="sender@example.com",
        ...             toEmail="recipient2@example.com",
        ...             subject="Important Update",
        ...             status="failed",
        ...             createdAt=1703066500000,
        ...             opens=0,
        ...             clicks=0
        ...         )
        ...     ]
        ... )
        >>> print(f"Showing page {response.pagination.page} of {response.pagination.total_pages}")
        >>> print(f"Displaying {len(response.messages)} of \
        ... {response.pagination.total_items} total emails")
        >>> 
        >>> # Count emails by status
        >>> status_counts = {"sent": 0, "delivered": 0, "failed": 0, "unknown": 0}
        >>> for msg in response.messages:
        ...     if msg.status in status_counts:
        ...         status_counts[msg.status] += 1
        ...     else:
        ...         status_counts["unknown"] += 1
        >>> 
        >>> print(f"Delivered: {status_counts['delivered']}")
        >>> print(f"Failed: {status_counts['failed']}")
        >>> 
        >>> # Calculate engagement metrics
        >>> delivered = [msg for msg in response.messages if msg.status == "delivered"]
        >>> if delivered:
        ...     opened = sum(1 for msg in delivered if msg.opens and msg.opens > 0)
        ...     clicked = sum(1 for msg in delivered if msg.clicks and msg.clicks > 0)
        ...     open_rate = opened / len(delivered) * 100
        ...     click_rate = clicked / len(delivered) * 100
        ...     print(f"Open rate: {open_rate:.1f}%")
        ...     print(f"Click rate: {click_rate:.1f}%")
        Showing page 1 of 4
        Displaying 2 of 87 total emails
        Delivered: 1
        Failed: 1
        Open rate: 100.0%
        Click rate: 100.0%
    
    Note:
        - Use pagination parameters when making API requests to navigate through large result sets
        - The messages list contains email activity logs as defined in BaseActivityLogs
        - Each email in the list contains its unique message_id, which can be used for detailed
          queries
        - For large collections, request additional pages by incrementing the page parameter
        - This response provides a high-level overview of email activity
        - For detailed event history of a specific email, use the GetEmailActivityLogsResponse class
    
    See Also:
        BaseActivityLogs: For the structure of individual email activity log entries
        GetEmailActivityLogsResponse: For detailed information about a specific email
        Pagination: For details about the pagination structure
    """
    pagination: Pagination
    messages: list[BaseActivityLogs]

class GetEmailActivityLogsResponse(BaseActivityLogs):
    """
    Model representing detailed activity logs for a specific email in the Naxai email system.
    
    This class extends BaseActivityLogs to include comprehensive information about
    an email's complete event history and associated metadata. It provides a detailed
    view of an individual email's journey from sending to recipient interaction.
    
    Attributes:
        message_id (str): Unique identifier for the email message.
            Mapped from JSON key 'messageId'.
        events (Optional[list[EmailEvents]]): List of events in the email's lifecycle,
            providing a chronological history of the email's journey.
            May be None if not available.
        from_email (str): The sender's email address.
            Mapped from JSON key 'fromEmail'.
        email (Optional[str]): Alternative representation of the recipient's email address.
            May be None if not available or if to_email is used instead.
        subject (Optional[str]): The subject line of the email.
            May be None if not available.
        status (Optional[Literal["sent", "delivered", "failed"]]):
            Current delivery status of the email.
            May be None if the status is unknown.
        created_at (Optional[int]):
            Timestamp when the email was created/sent, in milliseconds since epoch.
            Mapped from JSON key 'createdAt'. May be None if not available.
        updated_at (Optional[int]): 
            Timestamp when the email status was last updated, in milliseconds since epoch.
            Mapped from JSON key 'updatedAt'. May be None if not available.
        client_id (Optional[str]): Identifier of the client associated with this email.
            Mapped from JSON key 'clientId'. May be None if not applicable.
        campaign_id (Optional[str]): Identifier of the campaign associated with this email.
            Mapped from JSON key 'campaignId'. May be None if not applicable.
            
        # Inherited from BaseActivityLogs but potentially overridden:
        to_email (str): The recipient's email address.
            Mapped from JSON key 'toEmail'.
        opens (Optional[int]): Number of times the email has been opened by the recipient.
            May be None if not available or not tracked.
        clicks (Optional[int]): 
            Number of times links within the email have been clicked by the recipient.
            May be None if not available or not tracked.
    
    Example:
        >>> response = GetEmailActivityLogsResponse(
        ...     messageId="msg_123abc456def",
        ...     fromEmail="sender@example.com",
        ...     toEmail="recipient@example.com",
        ...     email="recipient@example.com",
        ...     subject="Important Update",
        ...     status="delivered",
        ...     createdAt=1703066400000,
        ...     updatedAt=1703066500000,
        ...     opens=3,
        ...     clicks=2,
        ...     clientId="client_789",
        ...     campaignId="campaign_456",
        ...     events=[
        ...         EmailEvents(name="sent", processed="2023-12-20T14:20:00Z"),
        ...         EmailEvents(name="delivered", processed="2023-12-20T14:21:30Z"),
        ...         EmailEvents(name="opened", processed="2023-12-20T15:05:12Z"),
        ...         EmailEvents(name="clicked",
        ...                     processed="2023-12-20T15:05:45Z",
        ...                     reason="https://example.com/link1"),
        ...         EmailEvents(name="opened", processed="2023-12-21T10:15:22Z"),
        ...         EmailEvents(name="clicked",
        ...                     processed="2023-12-21T10:16:03Z",
        ...                     reason="https://example.com/link2")
        ...     ]
        ... )
        >>> print(f"Email: {response.message_id}")
        >>> print(f"From: {response.from_email} to: {response.to_email}")
        >>> print(f"Subject: {response.subject}")
        >>> print(f"Current status: {response.status}")
        >>> print(f"Engagement: {response.opens} opens, {response.clicks} clicks")
        >>> 
        >>> # Display event timeline
        >>> if response.events:
        ...     print("\nEvent Timeline:")
        ...     for event in response.events:
        ...         details = f" - {event.reason}" if event.reason else ""
        ...         print(f"- {event.processed}: {event.name}{details}")
        >>> 
        >>> # Check if part of a campaign
        >>> if response.campaign_id:
        ...     print(f"\nPart of campaign: {response.campaign_id}")
        Email: msg_123abc456def
        From: sender@example.com to: recipient@example.com
        Subject: Important Update
        Current status: delivered
        Engagement: 3 opens, 2 clicks
        
        Event Timeline:
        - 2023-12-20T14:20:00Z: sent
        - 2023-12-20T14:21:30Z: delivered
        - 2023-12-20T15:05:12Z: opened
        - 2023-12-20T15:05:45Z: clicked - https://example.com/link1
        - 2023-12-21T10:15:22Z: opened
        - 2023-12-21T10:16:03Z: clicked - https://example.com/link2
        
        Part of campaign: campaign_456
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - The events list provides a chronological history of the email's journey and recipient
          interactions
        - The message_id is the primary identifier for tracking and querying emails
        - Timestamps (created_at, updated_at) are in milliseconds since epoch
        - Event timestamps (in the events list) may use a different format, typically ISO 8601
        - The to_email and email fields may contain the same information (recipient's address)
        - The client_id and campaign_id fields help associate the email
          with broader marketing efforts
        - This response provides the most comprehensive view of an individual email's activity
    
    See Also:
        BaseActivityLogs: For the base structure of email activity log entries
        EmailEvents: For the structure of individual email events
        ListEmailActivityLogsResponse: For retrieving multiple email activity logs
    """
    message_id: str = Field(alias="messageId")
    events: Optional[list[EmailEvents]] = Field(default=None)
    from_email: Optional[str] = Field(alias="fromEmail", default=None)
    email: Optional[str] = Field(default=None)
    subject: Optional[str] = Field(default=None)
    status: Optional[Literal["sent", "delivered", "failed"]] = Field(default=None)
    created_at: Optional[int] = Field(alias="createdAt", default=None)
    updated_at: Optional[int] = Field(alias="updatedAt", default=None)
    client_id: Optional[str] = Field(alias="clientId", default=None)
    campaign_id: Optional[str] = Field(alias="campaignId", default=None)
