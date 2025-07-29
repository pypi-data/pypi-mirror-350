"""
SMS resource for the Naxai SDK.

This module provides SMS messaging capabilities for the Naxai platform, including
sending text messages to individual recipients or groups, tracking message delivery
and engagement through activity logs, and analyzing messaging performance through
comprehensive reporting. It supports features such as message scheduling, unicode
content, delivery constraints, and custom tracking references.

Available Functions:
    send(to, body, from_=None, sender_service_id=None, type_="text", scheduled_at=None,
         validity=None, idempotency_key=None, reference=None, calendar_id=None,
         max_parts=None, truncate=False) -> SendSMSResponse
        Sends SMS messages to one or more recipients.
        Args:
            to: List of recipient phone numbers in E.164 format (max 1000)
            body: Text content of the SMS message (max 1530 chars)
            from_: Optional sender phone number
            sender_service_id: Optional sender service ID
            type_: Message type ("text", "unicode", or "auto")
            scheduled_at: Optional scheduled delivery time
            validity: Optional validity period in minutes (5-4320)
            idempotency_key: Optional idempotency key (max 200 chars)
            reference: Optional tracking reference (max 128 chars)
            calendar_id: Optional calendar ID for delivery constraints
            max_parts: Optional maximum message parts (1-10)
            truncate: Optional flag to truncate long messages
        Returns:
            SendSMSResponse: Details of the sent messages

Sub-resources:
    activity_logs:
        A subresource for accessing SMS activity and delivery logs.
        See ActivityLogsResource for detailed documentation.

    reporting:
        A subresource for retrieving SMS metrics and analytics.
        See ReportingResource for detailed documentation.

"""

import json
from typing import Literal
from pydantic import Field, validate_call
from naxai.models.sms.responses.send_responses import SendSMSResponse
from naxai.base.exceptions import NaxaiValueError
from .sms_resources.activity_logs import ActivityLogsResource
from .sms_resources.reporting import ReportingResource

class SMSResource:
    """
    Provides access to sms related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.root_path = "/sms"
        self.activity_logs = ActivityLogsResource(client, self.root_path)
        self.reporting = ReportingResource(client, self.root_path)
        self.headers = {"Content-Type": "application/json"}


    @validate_call
    def send(self,
            to: list[str] = Field(max_length=1000),
            body: str = Field(max_length=1530),
            from_: str = Field(max_length=15, default=None),
            sender_service_id: str = Field(default=None),
            type_: Literal["text", "unicode", "auto"] = Field(default="text"),
            scheduled_at: str = Field(default=None),
            validity: int = Field(default=None, ge=5, le=4320),
            idempotency_key: str = Field(default=None, max_length=200),
            reference: str = Field(max_length=128, default=None),
            calendar_id: str = Field(default=None),
            max_parts: int = Field(ge=1, le=10, default=None),
            truncate: bool = Field(default=False)
            ) -> SendSMSResponse:
        """
        Sends SMS messages to one or more recipients.
        
        This method allows sending text messages to multiple recipients with various configuration
        options including scheduling, message type, validity period, and more. Either a sender
        phone number (from_) or a sender service ID must be provided.
        
        Args:
            to (list[str]): List of recipient phone numbers in E.164 format (e.g., "+1234567890").
                Maximum 1000 recipients per request.
            body (str): The text content of the SMS message. Maximum 1530 characters.
                Actual character limit depends on the message type and encoding.
            from_ (str, optional): The sender ID or phone number to display as the message sender.
                Maximum 15 characters. Either from_ or sender_service_id must be provided.
                Mapped from JSON key 'from'.
            sender_service_id (str, optional): The ID of a sender service to use for sending.
                Either from_ or sender_service_id must be provided.
                Mapped from JSON key 'senderServiceId'.
            type_ (Literal["text", "unicode", "auto"], optional): The encoding type for the message.
                - "text": Standard GSM 7-bit encoding (max 160 chars per part)
                - "unicode": Unicode encoding for messages with special characters
                  (max 70 chars per part)
                - "auto": Automatically detect required encoding based on content
                Defaults to "text". Mapped from JSON key 'type'.
            scheduled_at (str, optional): 
                ISO 8601 timestamp to schedule the message for future delivery.
                Format: "YYYY-MM-DDTHH:MM:SSZ". If not provided, the message is sent immediately.
                Mapped from JSON key 'scheduledAt'.
            validity (int, optional): The period in minutes during which the message is valid.
                If the message cannot be delivered within this period, it will expire.
                Range: 5-4320 minutes (5 minutes to 3 days).
            idempotency_key (str, optional): A unique key to prevent duplicate message sending.
                If you retry a request with the same idempotency_key, only the first request
                will be processed.
                Maximum 200 characters. Mapped from JSON key 'idempotencyKey'.
            reference (str, optional): Custom reference identifier for the message.
                Maximum 128 characters. Useful for tracking messages in your system.
            calendar_id (str, optional): ID of a calendar to use for scheduling constraints.
                Mapped from JSON key 'calendarId'.
            max_parts (int, optional): Maximum number of message parts to use for the SMS.
                Range: 1-10. If the message requires more parts than specified, it may be truncated
                or rejected depending on the truncate parameter. Mapped from JSON key 'maxParts'.
            truncate (bool, optional): Whether to truncate messages that exceed the maximum length.
                If False and the message exceeds the maximum length or max_parts, an error
                will be returned.
                Defaults to False.
        
        Returns:
            SendSMSResponse: A response object containing:
                - batch_id: Unique identifier for the batch of messages
                - count: Number of messages accepted for delivery
                - messages: List of individual message objects with recipient and message IDs
        
        Raises:
            NaxaiValueError: If neither from_ nor sender_service_id is provided.
            ValidationError: If any parameter fails validation (e.g., exceeds maximum length).
        
        Example:
            >>> # Basic usage with a sender phone number
            >>> response = client.sms.send(
            ...     to=["+1234567890", "+1987654321"],
            ...     body="Your verification code is 123456",
            ...     from_="+18005551234"
            ... )
            >>> print(f"Batch ID: {response.batch_id}")
            >>> print(f"Messages sent: {response.count}")
            >>> for msg in response.messages:
            ...     print(f"Message to {msg.to}: ID {msg.message_id}")
            
            >>> # Scheduled message with unicode support and reference
            >>> response = client.sms.send(
            ...     to=["+1234567890"],
            ...     body="Hello! Your appointment is tomorrow at 2pm. 👍",
            ...     from_="+18005551234",
            ...     type_="unicode",
            ...     scheduled_at="2023-12-31T14:00:00Z",
            ...     reference="appointment-reminder-123",
            ...     idempotency_key="unique-id-123456"
            ... )
            
            >>> # Using a sender service ID instead of a phone number
            >>> response = client.sms.send(
            ...     to=["+1234567890"],
            ...     body="Marketing message from our company",
            ...     sender_service_id="svc_marketing_123",
            ...     max_parts=3,
            ...     truncate=True
            ... )
        
        Note:
            - Either from_ or sender_service_id must be provided
            - Character limits per message part depend on the encoding type:
            * text: 160 characters per part
            * unicode: 70 characters per part
            - When using max_parts, ensure the truncate parameter is set appropriately:
            * truncate=True: Messages exceeding the limit will be truncated
            * truncate=False: Messages exceeding the limit will cause an error
            - The idempotency_key is useful for preventing duplicate messages during retries
            - For scheduled messages, ensure the scheduled_at time is in the future
            - The validity period starts from the scheduled delivery time
        """
        if from_ is None and sender_service_id is None:
            raise NaxaiValueError("Either 'from_' or 'sender_service_id' must be provided.")

        request_body = {"to": to,
                        "body": body,
                        "type": type_,
                        "truncate": truncate}

        if sender_service_id:
            request_body["senderServiceId"] = sender_service_id
        else:
            request_body["from"] = from_

        if scheduled_at:
            request_body["scheduledAt"] = scheduled_at
        if validity:
            request_body["validity"] = validity
        if idempotency_key:
            request_body["idempotencyKey"] = idempotency_key
        if reference:
            request_body["reference"] = reference
        if calendar_id:
            request_body["calendarId"] = calendar_id
        if max_parts:
            request_body["maxParts"] = max_parts
        # pylint: disable=protected-access
        return SendSMSResponse.model_validate_json(
            json.dumps(self._client._request("POST",
                                             self.root_path + "/send",
                                             json=request_body,
                                             headers=self.headers)))
