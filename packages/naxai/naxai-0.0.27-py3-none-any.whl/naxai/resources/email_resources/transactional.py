"""
Email transactional resource for the Naxai SDK.

This module provides methods for sending transactional emails through the Naxai platform,
including personalized, event-triggered communications such as account notifications,
password resets, order confirmations, and receipts. It supports both direct HTML content
and template-based emails with variable substitution.

Available Functions:
    send(data: SendTransactionalEmailRequest)
        Send a transactional email to one or more recipients.
        Supports personalized emails with HTML content or template-based emails with
        variable substitution.
        Returns a unique identifier for tracking the email's status.

"""

import json
from naxai.models.email.requests.transactional_requests import SendTransactionalEmailRequest
from naxai.models.email.responses.transactional_responses import SendTransactionalEmailResponse

class TransactionalResource:
    """ transactional resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}

    def send(self, data: SendTransactionalEmailRequest):
        """
        Send a transactional email to one or more recipients.
        
        This method allows sending personalized transactional emails such as account notifications,
        password resets, order confirmations, and other event-triggered communications. The email
        content can be specified using either HTML or a template ID.
        
        Args:
            data (SendTransactionalEmailModel): A model containing all the information
            needed to send
                the transactional email, including:
                - from_email (str): The sender's email address
                - from_name (Optional[str]): The sender's display name
                - to (list[str]): List of recipient email addresses
                - cc (Optional[list[str]]): List of CC recipient email addresses
                - bcc (Optional[list[str]]): List of BCC recipient email addresses
                - reply_to (Optional[str]): Reply-to email address
                - subject (str): Email subject line
                - text (Optional[str]): Plain text version of the email
                - html (Optional[str]): HTML version of the email
                - template_id (Optional[str]): 
                    ID of a template to use instead of providing HTML/text
                - template_data (Optional[dict]): Variables to populate the template
                - attachments (Optional[list[Attachment]]): Files to attach to the email
                - headers (Optional[dict]): Custom email headers
                - tags (Optional[list[str]]): Tags for categorizing the email
                - track_opens (Optional[bool]): Whether to track email opens
                - track_clicks (Optional[bool]): Whether to track link clicks
                - custom_args (Optional[dict]): Custom arguments for tracking
        
        Returns:
            SendTransactionalEmailResponse: A response object containing the unique identifier
            for the sent email.
                This ID can be used for tracking and querying the email's status.
        
        Raises:
            NaxaiAPIRequestError: 
                If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to send emails
            NaxaiRateLimitExceeded: If the rate limit for sending emails is exceeded
        
        Example:
            >>> # Basic email with HTML content
            >>> response = client.email.transactional.send(
            ...     SendTransactionalEmailModel(
            ...         from_email="sender@example.com",
            ...         from_name="Sender Name",
            ...         to=["recipient@example.com"],
            ...         subject="Your Account Verification",
            ...         html="<html><body><h1>Verify Your Account</h1>\
            ...               <p>Click the link to verify your account.</p></body></html>"
            ...     )
            ... )
            >>> print(f"Email sent with ID: {response.id}")
            
            >>> # Using a template with personalization
            >>> response = client.email.transactional.send(
            ...     SendTransactionalEmailModel(
            ...         from_email="orders@example.com",
            ...         from_name="Example Store",
            ...         to=["customer@example.com"],
            ...         subject="Your Order #12345 Has Shipped",
            ...         template_id="template_order_shipped",
            ...         template_data={
            ...             "customer_name": "John Doe",
            ...             "order_number": "12345",
            ...             "tracking_number": "TRK123456789",
            ...             "estimated_delivery": "June 15, 2023"
            ...         },
            ...         track_opens=True,
            ...         track_clicks=True,
            ...         tags=["order", "shipping"]
            ...     )
            ... )
            >>> print(f"Order notification sent with ID: {response.id}")
        
        Note:
            - Either html/text or template_id must be provided, but not both
            - If using a template, the template_data should contain all variables required
              by the template
            - The from_email must be a verified sender in your Naxai account
            - For high deliverability, ensure your sender domain is properly configured
              with SPF and DKIM
            - Tracking options (track_opens, track_clicks) require proper configuration of
              tracking domains
            - Tags and custom_args are useful for categorizing and tracking emails in analytics
            - Attachments should be kept reasonably sized to avoid delivery issues
        
        See Also:
            SendTransactionalEmailModel: For the complete structure of the request data
            CreateEmailResponse: For the structure of the response
        """
        # pylint: disable=protected-access
        return SendTransactionalEmailResponse.model_validate_json(
            json.dumps(self._client._request("POST",
                                             self.root_path + "/send",
                                             json=data.model_dump(by_alias=True,
                                                                  exclude_none=True),
                                             headers=self.headers,
                                             timeout=30.0)))
