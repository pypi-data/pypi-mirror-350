"""
Email resource for the Naxai SDK.

This module provides comprehensive email communication capabilities for the Naxai platform,
including transactional emails, newsletters, templates, domain management, sender identities,
activity tracking, and performance reporting. It serves as a central access point for all
email-related functionality, enabling users to create and manage sophisticated email
communication workflows.

Available Functions:
    send(sender_email, sender_name, subject, to, cc=None, bcc=None, reply_to=None, 
         text=None, html=None, attachments=None, enable_tracking=None)
        Sends a transactional email to one or more recipients.
        Args:
            sender_email: Email address of the sender
            sender_name: Display name of the sender
            subject: Email subject line
            to: List of recipient DestinationObjects (1-1000 recipients)
            cc: Optional list of CC recipients (max 50)
            bcc: Optional list of BCC recipients (max 50) 
            reply_to: Optional reply-to email address
            text: Optional plain text email body
            html: Optional HTML email body
            attachments: Optional list of email attachments
            enable_tracking: Optional flag to enable email tracking
        Returns:
            SendTransactionalEmailResponse: Details of the sent email

Sub-resources:
    transactional:
        A subresource for managing transactional emails.
        See TransactionalResource for detailed documentation.

    activity_logs:
        A subresource for accessing email activity logs.
        See ActivityLogsResource for detailed documentation.

    reporting:
        A subresource for retrieving email metrics and analytics.
        See ReportingResource for detailed documentation.

"""

from typing import List, Optional
from pydantic import Field, validate_call
from naxai.models.email.requests.transactional_requests import (SendTransactionalEmailRequest,
                                                                DestinationObject,
                                                                Attachment,
                                                                CCObject,
                                                                BCCObject)
from .email_resources.transactional import TransactionalResource
from .email_resources.activity_logs import ActivityLogsResource
from .email_resources.reporting import ReportingResource


class EmailResource:
    """
    Provides access to email related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.root_path = "/email"
        self.headers = {"Content-Type": "application/json"}
        self.transactional: TransactionalResource = TransactionalResource(self._client,
                                                                          self.root_path)
        self.activity_logs: ActivityLogsResource = ActivityLogsResource(self._client,
                                                                        self.root_path)
        self.reporting: ReportingResource = ReportingResource(self._client, self.root_path)

    @validate_call
    def send(self,
            sender_email: str,
            sender_name: str,
            subject: str,
            to: List[DestinationObject] = Field(max_length=1000, min_length=1),
            cc: Optional[List[CCObject]] = Field(default=None, max_length=50),
            bcc: Optional[List[BCCObject]] = Field(default=None, max_length=50),
            reply_to: Optional[str] = Field(default=None),
            text: Optional[str] = Field(default=None),
            html: Optional[str] = Field(default=None),
            attachments: List[Attachment] = Field(default=None, ),
            enable_tracking: Optional[bool] = Field(default=None)
            ):
        """
        Send a transactional email to one or more recipients.
        
        This method provides a simplified interface for sending transactional emails such as
        account notifications, password resets, order confirmations, and other event-triggered
        communications. It accepts individual parameters rather than requiring a complete
        SendTransactionalEmailModel object.
        
        Args:
            sender_email (str): 
                The email address of the sender. Must be a verified sender in your account.
            sender_name (str): The display name of the sender that appears in email clients.
            subject (str): The subject line of the email.
            to (List[DestinationObject]): 
                List of primary recipients, each containing email and optional name.
                Must include at least 1 recipient, maximum 1000 recipients.
                Example: [{"email": "recipient@example.com", "name": "Recipient Name"}]
            cc (Optional[List[DestinationObject]]): 
                List of CC (carbon copy) recipients, each containing
                email and optional name. Maximum 50 recipients. Defaults to None.
            bcc (Optional[List[DestinationObject]]): 
                List of BCC (blind carbon copy) recipients, each containing
                email and optional name. Maximum 50 recipients. Defaults to None.
            reply_to (Optional[str]): 
                Email address that will receive replies if recipients reply to the email.
                Defaults to None (replies go to sender_email).
            text (Optional[str]): 
                Plain text version of the email content. At least one of text or html
                must be provided. Defaults to None.
            html (Optional[str]): HTML version of the email content. At least one of text or html
                must be provided. Defaults to None.
            attachments (List[Attachment]): List of file attachments to include with the email.
                Each attachment should include filename, content_type, and content (base64 encoded).
                Defaults to None.
            enable_tracking (Optional[bool]): 
                Whether to enable open and click tracking for this email.
                Defaults to None (system default setting is used).
        
        Returns:
            SendTransactionalEmailResponse: A response object containing the unique identifier
            for the sent email.
                This ID can be used for tracking and querying the email's status.
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters
            or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to send emails
            NaxaiRateLimitExceeded: If the rate limit for sending emails is exceeded
            ValidationError: If the provided parameters fail validation
        
        Example:
            >>> # Basic email with both HTML and text content
            >>> response = client.email.send(
            ...     sender_email="sender@example.com",
            ...     sender_name="Sender Name",
            ...     subject="Your Account Verification",
            ...     to=[{"email": "recipient@example.com", "name": "Recipient Name"}],
            ...     html="<html><body><h1>Verify Your Account</h1>\
            ...           <p>Click the link to verify your account.</p></body></html>",
            ...     text="Verify Your Account\n\nClick the link to verify your account.",
            ...     enable_tracking=True
            ... )
            >>> print(f"Email sent with ID: {response.id}")
            
            >>> # Email with multiple recipients and an attachment
            >>> from base64 import b64encode
            >>> pdf_content = b64encode(open("document.pdf", "rb").read()).decode()
            >>> 
            >>> response = client.email.send(
            ...     sender_email="support@example.com",
            ...     sender_name="Customer Support",
            ...     subject="Your Monthly Statement",
            ...     to=[{"email": "customer@example.com", "name": "Customer Name"}],
            ...     cc=[{"email": "accounting@example.com"}],
            ...     reply_to="no-reply@example.com",
            ...     html="<html><body><p>Please find your monthly statement attached.</p>\
            ...           </body></html>",
            ...     attachments=[{
            ...         "filename": "statement.pdf",
            ...         "content_type": "application/pdf",
            ...         "content": pdf_content
            ...     }]
            ... )
            >>> print(f"Email with attachment sent with ID: {response.id}")
        
        Note:
            - At least one of text or html must be provided
            - The sender_email must be a verified sender in your Naxai account
            - For high deliverability, ensure your sender domain is properly configured with
              SPF and DKIM
            - This method is a convenience wrapper around the transactional.send() method
            - For more advanced options like templates, tags, or custom headers, use 
              transactional.send() directly
            - Attachments should be kept reasonably sized to avoid delivery issues
            - The total size of all attachments should not exceed 10MB
        
        See Also:
            TransactionalResource.send: For more advanced email sending options
            SendTransactionalEmailModel: For the complete structure of the transactional email model
            DestinationObject: For the structure of email recipients
            Attachment: For the structure of email attachments
        """
        data = SendTransactionalEmailRequest(sender={"email": sender_email, "name": sender_name},
                                           to=to,
                                           cc=cc,
                                           bcc=bcc,
                                           reply_to=reply_to,
                                           subject=subject,
                                           text=text,
                                           html=html,
                                           attachments=attachments,
                                           enable_tracking=enable_tracking)
        return self.transactional.send(data=data)
