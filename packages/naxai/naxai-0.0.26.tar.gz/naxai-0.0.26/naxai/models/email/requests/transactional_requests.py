"""
Transactional email request models for the Naxai SDK.

This module defines the data structures used for sending transactional emails,
including sender information, recipients, attachments, and email content options.
"""

from typing import Optional
from pydantic import BaseModel, Field

class BaseObject(BaseModel):
    """
    Base model representing a basic object with an email and name.
    
    This class defines the core structure for email address objects in the Naxai email system,
    providing fields for both the email address and the associated display name.
    
    Attributes:
        email (str): An email address (e.g., "user@example.com").
        name (str): The display name associated with the email address (e.g., "John Doe").
    
    Note:
        - This is a base class that is extended by more specific email address object types
        - The name field is used as the display name in email clients
        - For best results, ensure the name field does not contain special characters
          that might interfere with email headers
    """
    email: str
    name: str

class SenderObject(BaseObject):
    """
    Model representing the sender of an email in the Naxai email system.
    
    This class extends BaseObject to represent the sender (From) field of an email,
    providing information about who is sending the email.
    
    Inherits all attributes from BaseObject:
        - email (str): The sender's email address (e.g., "support@example.com").
            Must be a verified sender in your Naxai account.
        - name (str): 
            The sender's display name that appears in email clients (e.g., "Customer Support").
    
    Example:
        >>> sender = SenderObject(email="support@example.com", name="Customer Support")
        >>> print(f"From: {sender.name} <{sender.email}>")
        From: Customer Support <support@example.com>
    
    Note:
        - The sender's email address must be a verified sender in your Naxai account
        - For high deliverability, ensure the sender's domain is properly configured
          with SPF and DKIM
        - The display name should be recognizable to recipients to reduce the chance of emails
          being marked as spam
    """

class DestinationObject(BaseObject):
    """
    Model representing a destination (recipient) of an email in the Naxai email system.
    
    This class extends BaseObject to represent a primary recipient (To) field of an email,
    providing information about who will receive the email.
    
    Inherits all attributes from BaseObject:
        - email (str): The recipient's email address (e.g., "recipient@example.com").
        - name (str): The recipient's display name (e.g., "John Doe").
    
    Example:
        >>> recipient = DestinationObject(email="customer@example.com", name="John Doe")
        >>> print(f"To: {recipient.name} <{recipient.email}>")
        To: John Doe <customer@example.com>
    
    Note:
        - The name field is optional in practice but required by the model
        - If you don't have a name for the recipient,
          you can use the email address or a generic name
        - Primary recipients (To) can see each other's email addresses in most email clients
    """

class CCObject(BaseObject):
    """
    Model representing a carbon copy (CC) recipient of an email in the Naxai email system.
    
    This class extends BaseObject to represent a CC recipient field of an email,
    providing information about who will receive a copy of the email.
    
    Inherits all attributes from BaseObject:
        - email (str): The CC recipient's email address (e.g., "manager@example.com").
        - name (str): The CC recipient's display name (e.g., "Jane Manager").
    
    Example:
        >>> cc_recipient = CCObject(email="manager@example.com", name="Jane Manager")
        >>> print(f"CC: {cc_recipient.name} <{cc_recipient.email}>")
        CC: Jane Manager <manager@example.com>
    
    Note:
        - The name field is optional in practice but required by the model
        - CC recipients can see all To and other CC recipients' email addresses
        - Use CC when you want to keep someone informed but they are not the primary recipient
        - CC recipients are typically not expected to take action on the email
    """

class BCCObject(BaseObject):
    """
    Model representing a blind carbon copy (BCC) recipient of an email in the Naxai email system.
    
    This class extends BaseObject to represent a BCC recipient field of an email,
    providing information about who will receive a copy of the email without other
    recipients knowing.
    
    Inherits all attributes from BaseObject:
        - email (str): The BCC recipient's email address (e.g., "records@example.com").
        - name (str): The BCC recipient's display name (e.g., "Records Department").
    
    Example:
        >>> bcc_recipient = BCCObject(email="records@example.com", name="Records Department")
        >>> print(f"BCC: {bcc_recipient.name} <{bcc_recipient.email}>")
        BCC: Records Department <records@example.com>
    
    Note:
        - The name field is optional in practice but required by the model
        - BCC recipients cannot see other recipients' email addresses
        - Other recipients (To and CC) cannot see BCC recipients
        - Use BCC when you want to include someone privately or send to multiple recipients
          without revealing their email addresses to each other
    """

class Attachment(BaseModel):
    """
    Model representing an attachment to an email in the Naxai email system.
    
    This class defines the structure for email attachments, providing fields for
    the attachment's identifier, name, content type, and the actual file data.
    
    Attributes:
        id (str): Unique identifier for the attachment. Mapped from JSON key 'id'.
        name (str): The filename of the attachment as it will appear to recipients.
        content_type (str): The MIME type of the attachment (e.g., "application/pdf").
            Mapped from JSON key 'contentType'.
        data (str): The file content, encoded as a base64 string.
    
    Example:
        >>> # Creating an attachment from a file
        >>> import base64
        >>> with open("document.pdf", "rb") as f:
        ...     pdf_data = base64.b64encode(f.read()).decode()
        >>> 
        >>> attachment = Attachment(
        ...     id="att_123",
        ...     name="document.pdf",
        ...     contentType="application/pdf",
        ...     data=pdf_data
        ... )
        >>> print(f"Attachment: {attachment.name} ({attachment.content_type})")
        Attachment: document.pdf (application/pdf)
    
    Note:
        - The data field should contain the file content encoded as a base64 string
        - Common content types include:
          * application/pdf - PDF documents
          * application/msword - Word documents
          * application/vnd.openxmlformats-officedocument.wordprocessingml.document - DOCX documents
          * application/vnd.ms-excel - Excel spreadsheets
          * application/vnd.openxmlformats-officedocument.spreadsheetml.sheet - XLSX spreadsheets
          * image/jpeg - JPEG images
          * image/png - PNG images
          * text/plain - Plain text files
        - Attachments should be kept reasonably sized to avoid delivery issues
        - The total size of all attachments should not exceed 10MB
        - Some email providers may block certain file types for security reasons
    """
    id: str = Field(alias="id")
    name: str
    content_type: str = Field(alias="contentType")
    data: str

    model_config = {"populate_by_name": True}

class SendTransactionalEmailRequest(BaseModel):
    """
    Model representing a request to send a transactional email in the Naxai email system.
    
    This class defines the structure for transactional email requests, providing all the
    necessary fields to specify sender information, recipients, content, and delivery options.
    Transactional emails are typically triggered by specific events or user actions, such as
    account registrations, password resets, order confirmations, and notifications.
    
    Attributes:
        sender (SenderObject): 
            Information about the email sender, including email address and display name.
            Must be a verified sender in your Naxai account.
        to (list[DestinationObject]): List of primary recipients for the email.
            Maximum 1000 recipients allowed.
        cc (Optional[list[CCObject]]): List of carbon copy (CC) recipients who will receive a copy
            of the email with their addresses visible to all recipients.
            Maximum 50 CC recipients allowed. Defaults to None.
        bcc (Optional[list[BCCObject]]): List of blind carbon copy (BCC) recipients who will receive
            a copy of the email without their addresses being visible to other recipients.
            Maximum 50 BCC recipients allowed. Defaults to None.
        reply_to (Optional[str]):
            Email address that will receive replies if recipients reply to the email.
            Maximum 100 characters. Mapped from JSON key 'replyTo'. Defaults to None.
        subject (str): The subject line of the email.
        text (Optional[str]): Plain text version of the email content.
            At least one of text or html must be provided. Defaults to None.
        html (Optional[str]): HTML version of the email content.
            At least one of text or html must be provided. Defaults to None.
        attachments (Optional[list[Attachment]]): List of files to attach to the email.
            Maximum 10 attachments allowed. Defaults to None.
        enable_tracking (Optional[bool]): Whether to enable open and click tracking for this email.
            Mapped from JSON key 'enableTracking'.
            Defaults to None (system default setting is used).
    
    Example:
        >>> # Basic email with HTML content
        >>> request = SendTransactionalEmailRequest(
        ...     sender=SenderObject(email="sender@example.com", name="Sender Name"),
        ...     to=[DestinationObject(email="recipient@example.com", name="Recipient Name")],
        ...     subject="Your Account Verification",
        ...     html="<html><body><h1>Verify Your Account</h1> \
        ...     <p>Click the link to verify your account.</p></body></html>",
        ...     text="Verify Your Account\n\nClick the link to verify your account.",
        ...     enable_tracking=True
        ... )
        >>> 
        >>> # Email with multiple recipients and reply-to address
        >>> request = SendTransactionalEmailRequest(
        ...     sender=SenderObject(email="support@example.com", name="Customer Support"),
        ...     to=[
        ...         DestinationObject(email="customer1@example.com", name="Customer One"),
        ...         DestinationObject(email="customer2@example.com", name="Customer Two")
        ...     ],
        ...     cc=[CCObject(email="manager@example.com", name="Manager")],
        ...     bcc=[BCCObject(email="records@example.com", name="Records")],
        ...     reply_to="no-reply@example.com",
        ...     subject="Important Service Update",
        ...     html="<html><body><p>We're updating our service on June 15th.</p></body></html>"
        ... )
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - At least one of text or html must be provided
        - The sender email must be a verified sender in your Naxai account
        - For high deliverability, ensure your sender domain is
          properly configured with SPF and DKIM
        - When both text and html are provided, email clients will display the appropriate version
          based on their capabilities and user preferences
        - Attachments should be kept reasonably sized to avoid delivery issues
        - The total size of all attachments should not exceed 10MB
        - Tracking options require proper configuration of tracking domains
    
    See Also:
        SenderObject: For the structure of sender information
        DestinationObject: For the structure of primary recipients
        CCObject: For the structure of CC recipients
        BCCObject: For the structure of BCC recipients
        Attachment: For the structure of email attachments
    """

    sender: SenderObject
    to: list[DestinationObject] = Field(max_length=1000)
    cc: Optional[list[CCObject]] = Field(max_length=50, default=None)
    bcc: Optional[list[BCCObject]] = Field(max_length=50, default=None)
    reply_to: Optional[str] = Field(max_length=100, default=None, alias="replyTo")
    subject: str
    text: Optional[str] = None
    html: Optional[str] = None
    attachments: Optional[list[Attachment]] = Field(max_length=10, default=None)
    enable_tracking: Optional[bool] = Field(alias="enableTracking", default=None)

    model_config = {"populate_by_name": True}
