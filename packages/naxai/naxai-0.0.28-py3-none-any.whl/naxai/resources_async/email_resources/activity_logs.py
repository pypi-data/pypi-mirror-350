"""
Asynchronous email activity logs resource for the Naxai SDK.

This module provides asynchronous methods for retrieving and analyzing email activity logs,
including delivery status, engagement metrics, and event history for individual messages
and across multiple emails. It enables non-blocking access to detailed email tracking data,
allowing applications to efficiently monitor email performance and recipient interactions
without impacting application responsiveness.

Available Functions:
    get(message_id: str, email: str)
        Retrieve detailed activity logs for a specific email message sent to a particular recipient.
        Returns comprehensive information about delivery status, engagement metrics and event
        history.

    list(email: str, status: Optional[str] = None, page: int = 1, limit: int = 10)
        List activity logs for multiple email messages sent to a recipient.
        Returns paginated results with basic delivery and engagement information.

"""

import json
from typing import Optional, Literal
from pydantic import Field, validate_call
from naxai.models.email.responses.activity_logs_responses import (GetEmailActivityLogsResponse,
                                                                  ListEmailActivityLogsResponse)

class ActivityLogsResource:
    """ activity_logs resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/activity-logs"
        self.headers = {"Content-Type": "application/json"}

    #TODO: email validation
    async def get(self, message_id: str, email: str):
        """
        Retrieve detailed activity logs for a specific email message sent to a particular recipient.
        
        This method fetches comprehensive information about an individual email's journey,
        including its delivery status, engagement metrics, and complete event history. It provides
        the most detailed view of what happened with a specific email sent to a specific recipient.
        
        Args:
            message_id (str): Unique identifier of the email message to retrieve.
                This ID is typically obtained from the response when sending an email
                or from the list() method results.
            email (str): The recipient's email address for which to retrieve activity data.
                This must match the email address the message was sent to.
        
        Returns:
            GetEmailActivityLogsResponse: 
                A response object containing detailed information about the email,
            including:
                - message_id: Unique identifier for the email message
                - from_email: The sender's email address
                - to_email: The recipient's email address
                - email: Alternative representation of the recipient's email address
                - subject: The subject line of the email
                - status: Current delivery status ("sent", "delivered", or "failed")
                - created_at: Timestamp when the email was created/sent
                - updated_at: Timestamp when the email status was last updated
                - opens: Number of times the email has been opened
                - clicks: Number of times links within the email have been clicked
                - client_id: Identifier of the client associated with this email
                - campaign_id: Identifier of the campaign associated with this email
                - events: List of events in the email's lifecycle, providing a chronological history
        
        Raises:
            NaxaiAPIRequestError: 
                If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to access email activity logs
            NaxaiResourceNotFound: If the specified message_id or email combination doesn't exist
        
        Example:
            >>> # Retrieve detailed activity for a specific email
            >>> message_details = await client.email.activity_logs.get(
            ...     message_id="msg_123abc456def",
            ...     email="recipient@example.com"
            ... )
            >>> 
            >>> print(f"Email: {message_details.subject}")
            >>> print(f"From: {message_details.from_email} to: {message_details.to_email}")
            >>> print(f"Status: {message_details.status}")
            >>> print(f"Engagement: {message_details.opens or 0} opens, "
            >>>       f"{message_details.clicks or 0} clicks")
            >>> 
            >>> # Display event timeline
            >>> if message_details.events:
            ...     print("\nEvent Timeline:")
            ...     for event in message_details.events:
            ...         details = f" - {event.reason}" if event.reason else ""
            ...         print(f"- {event.processed}: {event.name}{details}")
            Email: Your Account Verification
            From: sender@example.com to: recipient@example.com
            Status: delivered
            Engagement: 3 opens, 2 clicks
            
            Event Timeline:
            - 2023-12-20T14:20:00Z: sent
            - 2023-12-20T14:21:30Z: delivered
            - 2023-12-20T15:05:12Z: opened
            - 2023-12-20T15:05:45Z: clicked - https://example.com/verify
            - 2023-12-21T10:15:22Z: opened
            - 2023-12-21T10:16:03Z: clicked - https://example.com/login
        
        Note:
            - Both message_id and email parameters are required to uniquely identify
              the email activity
            - The message_id is typically obtained from the response when sending an email or
              from list() results
            - The email parameter must match the recipient's email address the message was sent to
            - The events list provides a chronological history of the email's journey and
              recipient interactions
            - Common event types include:
            * "sent": Email has been accepted for delivery
            * "delivered": Email has been delivered to the recipient's inbox
            * "opened": Recipient has opened the email
            * "clicked": Recipient has clicked a link in the email
            * "failed": Email delivery has failed
            * "bounced": Email has bounced from the recipient's server
            * "complained": Recipient has marked the email as spam
            * "unsubscribed": Recipient has unsubscribed from future emails
            - Timestamps in the response (created_at, updated_at) are in milliseconds since epoch
            - Event timestamps (in the events list) may use a different format, typically ISO 8601
            - Email tracking (opens, clicks) requires proper configuration of tracking domains
        
        TODO:
            - Add email validation for the email parameter
        
        See Also:
            list: For retrieving multiple email activity logs with filtering and pagination
            GetEmailActivityLogsResponse: For the structure of the response object
            EmailEvents: For the structure of individual email events
        """
        # pylint: disable=protected-access
        return GetEmailActivityLogsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/" + message_id + "/" + email,
                                                   headers=self.headers)))

    #TODO: email validation
    @validate_call
    async def list(self,
                page: Optional[int] = 1,
                page_size: Optional[int] = Field(default=50, ge=1, le=100),
                start: Optional[int] = None,
                stop: Optional[int] = None,
                sort: Optional[str] = "updatedAt:desc",
                email: Optional[str] = None,
                client_id: Optional[str] = None,
                campaign_id: Optional[str] = None,
                status: Optional[Literal["sent", "delivered", "failed"]] = None
                ):
        """
        Retrieve a paginated list of email activity logs with optional filtering.
        
        This method fetches email activity logs from the API, allowing filtering by various
        criteria such as time range, recipient email, status, and associated IDs. It provides
        a high-level overview of email activity across multiple messages and recipients.
        
        Args:
            page (Optional[int]): Page number to retrieve. Defaults to 1.
            page_size (Optional[int]): Number of items per page. Must be between 1 and 100.
                Defaults to 50.
            start (Optional[int]): 
                Start timestamp for filtering emails, in milliseconds since epoch.
                Only emails sent/received after this time will be included. Defaults to None.
            stop (Optional[int]): End timestamp for filtering emails, in milliseconds since epoch.
                Only emails sent/received before this time will be included. Defaults to None.
            sort (Optional[str]): Sorting criteria in the format "field:direction".
                Defaults to "updatedAt:desc" (most recently updated first).
                Common fields include "createdAt", "updatedAt", "status".
                Direction can be "asc" (ascending) or "desc" (descending).
            email (Optional[str]): Filter by recipient email address.
                Only emails sent to this address will be included. Defaults to None.
            client_id (Optional[str]): Filter by client identifier.
                Only emails associated with this client will be included. Defaults to None.
            campaign_id (Optional[str]): Filter by campaign identifier.
                Only emails associated with this campaign will be included. Defaults to None.
            status (Optional[Literal["sent", "delivered", "failed"]]): 
                Filter by email delivery status.
                Only emails with this status will be included. Defaults to None.
        
        Returns:
            ListEmailActivityLogsResponse: 
                A response object containing the paginated list of email activity logs.
            The response includes:
                - pagination: Information about the current page, total pages, and total items
                - messages: List of BaseActivityLogs objects with information about each email:
                    - message_id: Unique identifier for the email
                    - from_email: The sender's email address
                    - to_email: The recipient's email address
                    - subject: The subject line of the email
                    - status: Current delivery status
                    - created_at: Timestamp when the email was created/sent
                    - updated_at: Timestamp when the email status was last updated
                    - opens: Number of times the email has been opened
                    - clicks: Number of times links within the email have been clicked
        
        Raises:
            NaxaiAPIRequestError: 
                If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to access email activity logs
            ValidationError: If the provided parameters fail validation
        
        Example:
            >>> # Basic usage with pagination
            >>> activity_logs = await client.email.activity_logs.list(
            ...     page=1,
            ...     page_size=25
            ... )
            >>> print(f"Found {activity_logs.pagination.total_items} emails")
            >>> print(f"Showing page {activity_logs.pagination.page} of "
            >>>       f"{activity_logs.pagination.total_pages}")
            >>> for msg in activity_logs.messages:
            ...     print(f"Email: {msg.subject} - Status: {msg.status}")
            Found 87 emails
            Showing page 1 of 4
            Email: Your Account Verification - Status: delivered
            Email: January Newsletter - Status: delivered
            Email: Password Reset - Status: sent
            ...
            
            >>> # Filtering by date range, status, and recipient
            >>> import time
            >>> one_week_ago = int(time.time() * 1000) - (7 * 24 * 60 * 60 * 1000)
            >>> now = int(time.time() * 1000)
            >>> 
            >>> delivered_emails = await client.email.activity_logs.list(
            ...     start=one_week_ago,
            ...     stop=now,
            ...     status="delivered",
            ...     email="customer@example.com",
            ...     sort="createdAt:asc"
            ... )
            >>> print(f"Found {len(delivered_emails.messages)} delivered emails "
            >>>       "to customer@example.com in the last week")
            >>> 
            >>> # Calculate engagement metrics
            >>> if delivered_emails.messages:
            ...     opened = sum(
            ...         1 for msg in delivered_emails.messages if msg.opens and msg.opens > 0)
            ...     clicked = sum(
            ...         1 for msg in delivered_emails.messages if msg.clicks and msg.clicks > 0)
            ...     open_rate = opened / len(delivered_emails.messages) * 100
            ...     click_rate = clicked / len(delivered_emails.messages) * 100
            ...     print(f"Open rate: {open_rate:.1f}%")
            ...     print(f"Click rate: {click_rate:.1f}%")
            Found 12 delivered emails to customer@example.com in the last week
            Open rate: 75.0%
            Click rate: 41.7%
            
            >>> # Filtering by campaign
            >>> campaign_emails = await client.email.activity_logs.list(
            ...     campaign_id="camp_123abc",
            ...     page_size=100
            ... )
            >>> print(f"Found {len(campaign_emails.messages)} emails for campaign camp_123abc")
            >>> 
            >>> # Count emails by status
            >>> status_counts = {"sent": 0, "delivered": 0, "failed": 0}
            >>> for msg in campaign_emails.messages:
            ...     if msg.status in status_counts:
            ...         status_counts[msg.status] += 1
            >>> 
            >>> print(f"Sent: {status_counts['sent']}")
            >>> print(f"Delivered: {status_counts['delivered']}")
            >>> print(f"Failed: {status_counts['failed']}")
            Found 150 emails for campaign camp_123abc
            Sent: 15
            Delivered: 130
            Failed: 5
        
        Note:
            - Use pagination parameters (page, page_size) to navigate through large result sets
            - Timestamp parameters (start, stop) are in milliseconds since epoch
            - The sort parameter accepts various fields; common ones include:
            * "createdAt": Sort by when the email was sent
            * "updatedAt": Sort by when the email status was last updated
            * "status": Sort by delivery status
            - The email parameter filters by recipient email address
            - The client_id and campaign_id parameters help filter emails associated
              with specific entities
            - The status parameter filters by delivery status ("sent", "delivered", "failed")
            - For detailed information about a specific email, use the get() method
              with its message_id
            - The response provides a high-level overview of email activity
            - Email tracking (opens, clicks) requires proper configuration of tracking domains
        
        TODO:
            - Add email validation for the email parameter
        
        See Also:
            get: For retrieving detailed information about a specific email
            ListEmailActivityLogsResponse: For the structure of the response object
            BaseActivityLogs: For the structure of individual email activity log entries
        """

        params = {
            "page": page,
            "pageSize": page_size,
            "sort": sort
        }

        if start:
            params["start"] = start
        if stop:
            params["stop"] = stop
        if email:
            params["email"] = email
        if client_id:
            params["clientId"] = client_id
        if campaign_id:
            params["campaignId"] = campaign_id
        if status:
            params["status"] = status
        # pylint: disable=protected-access
        return ListEmailActivityLogsResponse.model_validate_json(
             json.dumps(await self._client._request("GET",
                                                    self.root_path,
                                                    params=params,
                                                    headers=self.headers)))
