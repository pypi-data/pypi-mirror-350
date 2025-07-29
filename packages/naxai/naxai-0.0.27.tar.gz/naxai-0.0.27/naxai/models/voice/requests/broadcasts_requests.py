"""
Voice broadcast request models for the Naxai SDK.

This module defines the data structures used for creating voice broadcast campaigns,
including call flow configuration, recipient targeting, scheduling options,
and interactive response handling.
"""

from typing import Optional, Literal, Union
from pydantic import BaseModel, Field
from naxai.models.voice.voice_flow import VoiceFlow

class ActionItem(BaseModel):
    """Model representing an action item in a broadcast request.

    This class defines an action that can be performed during a broadcast,
    such as setting attributes or values for contact management.

    Attributes:
        attribute (Optional[str]): The name of the attribute to be modified.
            Mapped from JSON key 'attribute'. Defaults to None.
        value (Optional[Union[str, int, bool]]): The value to be assigned.
            Can be a string, integer, or boolean. Defaults to None.

    Example:
        >>> action = ActionItem(attribute="status", value="completed")
        >>> print(f"Setting {action.attribute} to {action.value}")
        Setting status to completed
    """
    attribute: Optional[str] = Field(alias="attribute", default=None)
    value: Optional[Union[str, int, bool]] = Field(alias="value", default=None)

class Sms(BaseModel):
    """Model representing SMS configuration in a broadcast request.

    This class defines the structure for SMS messages that can be sent
    as part of broadcast actions.

    Attributes:
        message (Optional[str]): The content of the SMS message.
            Mapped from JSON key 'message'. Defaults to None.
        sender_service_id (Optional[str]): The ID of the SMS sending service.
            Mapped from JSON key 'senderServiceId'. Defaults to None.

    Example:
        >>> sms = Sms(message="Thank you for participating", 
        ...          sender_service_id="svc_123")
        >>> print(f"SMS from {sms.sender_service_id}: {sms.message}")
        SMS from svc_123: Thank you for participating
    """
    message: Optional[str] = Field(alias="message", default=None)
    sender_service_id: Optional[str] = Field(alias="senderServiceId", default=None)

class Inputs(BaseModel):
    """Model representing DTMF input mappings for broadcast interactions.

    This class defines possible actions for each DTMF key press (0-9, *, #)
    during a voice broadcast interaction.

    Attributes:
        field_0 through field_9 (Optional[Union[list[ActionItem], dict[str, Sms]]]):
            Actions or SMS configurations for digits 0-9.
        field_star (Optional[Union[list[ActionItem], dict[str, Sms]]]): 
            Actions or SMS configurations for the * key.
        field_hash (Optional[Union[list[ActionItem], dict[str, Sms]]]): 
            Actions or SMS configurations for the # key.

    Example:
        >>> inputs = Inputs(
        ...     field_1=[ActionItem(attribute="status", value="accepted")],
        ...     field_2={"sms": Sms(message="Option 2 selected")}
        ... )

    Note:
        - Each field can contain either a list of actions or an SMS configuration
        - All fields are optional and default to None
        - Field names are mapped from their respective DTMF keys in JSON
    """
    field_0: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="0", default=None)
    field_1: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="1", default=None)
    field_2: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="2", default=None)
    field_3: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="3", default=None)
    field_4: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="4", default=None)
    field_5: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="5", default=None)
    field_6: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="6", default=None)
    field_7: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="7", default=None)
    field_8: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="8", default=None)
    field_9: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="9", default=None)
    field_star: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="star",
                                                                          default=None)
    field_hash: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="hash",
                                                                          default=None)

class Status(BaseModel):
    """Model representing status-based actions in a broadcast request.

    This class defines actions to be taken based on the delivery status
    of broadcast messages.

    Attributes:
        delivered (Optional[Union[list[ActionItem], dict[str, Sms]]]): 
            Actions or SMS configurations for successful deliveries.
        failed (Optional[Union[list[ActionItem], dict[str, Sms]]]): 
            Actions or SMS configurations for failed deliveries.

    Example:
        >>> status = Status(
        ...     delivered=[ActionItem(attribute="status", value="success")],
        ...     failed={"sms": Sms(message="Delivery failed")}
        ... )

    Note:
        - Each status can trigger either a list of actions or an SMS message
        - Both fields are optional
    """
    delivered: Optional[Union[list[ActionItem], dict[str, Sms]]]
    failed: Optional[Union[list[ActionItem], dict[str, Sms]]]

class Actions(BaseModel):
    """Model representing all possible actions in a broadcast request.

    This class combines status-based actions and input-based actions for
    a complete broadcast action configuration.

    Attributes:
        status (Optional[Status]): Actions based on delivery status.
            Mapped from JSON key 'actions'. Defaults to None.
        inputs (Optional[Inputs]): Actions based on DTMF input keys.
            Mapped from JSON key 'inputs'. Defaults to None.

    Example:
        >>> actions = Actions(
        ...     status=Status(delivered=[ActionItem(attribute="status", value="done")]),
        ...     inputs=Inputs(field_1={"sms": Sms(message="Option 1 selected")})
        ... )
    """
    status: Optional[Status] = Field(alias="actions", default=None)
    inputs: Optional[Inputs] = Field(alias="inputs", default=None)

class CreateBroadcastRequest(BaseModel):
    """Request model for creating a new broadcast.

    This class defines the structure of the request payload when creating
    a new voice broadcast campaign.

    Attributes:
        name (str): The name of the broadcast campaign.
        from_ (str): The sender's phone number (8-15 characters).
            Mapped from JSON key 'from'.
        source (Optional[str]): The source of the broadcast.
            Mapped from JSON key 'source'. Defaults to "people".
        segment_ids (list[str]): List of segment IDs to target (max 1 segment).
            Mapped from JSON key 'segmentIds'.
        inclube_unsubscribed (Optional[bool]): Whether to include unsubscribed contacts.
            Mapped from JSON key 'inclubeUnsubscribed'. Defaults to False.
        language (Optional[Literal]): Voice language code. One of:
            "fr-FR", "fr-BE", "nl-NL", "nl-BE", "en-GB", "de-DE".
            Defaults to "fr-BE".
        voice (Optional[Literal]): Voice gender selection.
            Either "woman" or "man". Defaults to "woman".
        scheduled_at (Optional[str]): Scheduled start time.
            Mapped from JSON key 'scheduledAt'. None if not scheduled.
        retries (Optional[int]): Number of retry attempts (0-3).
            Defaults to 0.
        retry_on_no_input (Optional[bool]): Whether to retry on no input.
            Mapped from JSON key 'retryOnNoInput'. Defaults to False.
        retry_on_failed (Optional[bool]): Whether to retry on failure.
            Mapped from JSON key 'retryOnFailed'. Defaults to False.
        retry_delays (Optional[list[int]]): Delays between retries (0-3 values).
            Mapped from JSON key 'retryDelays'. None if not using retries.
        calendar_id (Optional[str]): Associated calendar ID.
            Mapped from JSON key 'calendarId'. None if not using calendar.
        distribution (Optional[Literal]): Distribution type.
            Either "none" or "dynamic". Defaults to "none".
        dynamic_name (Optional[str]): Name for dynamic distribution.
            Mapped from JSON key 'dynamicName'. None if not using dynamic distribution.
        voice_flow (VoiceFlow): The voice flow configuration.
            Mapped from JSON key 'voiceFlow'.
        actions (Optional[Actions]): Action configurations for the broadcast.
            Mapped from JSON key 'actions'. None if no actions configured.

    Example:
        >>> request = CreateBroadcastRequest(
        ...     name="Customer Survey",
        ...     from_="1234567890",
        ...     segment_ids=["seg_abc123"],
        ...     language="en-GB",
        ...     voice="woman",
        ...     voice_flow=voice_flow_obj,
        ...     actions=Actions(...)
        ... )

    Note:
        - Phone numbers must be between 8 and 15 characters
        - Only one segment ID is allowed in segment_ids
        - Retry delays list must contain 0-3 values
        - The voice_flow field is required
        - Most fields are optional with sensible defaults
    """
    name: str
    from_: str = Field(alias="from", min_length=8, max_length=15)
    source: Optional[str] = Field(alias="source", default="people")
    segment_ids: list[str] = Field(alias="segmentIds", max_length=1)
    inclube_unsubscribed: Optional[bool] = Field(alias="inclubeUnsubscribed", default=False)
    language: Optional[Literal["fr-FR", "fr-BE", "nl-NL", "nl-BE", "en-GB", "de-DE"]] = "fr-BE"
    voice: Optional[Literal["woman", "man"]] = "woman"
    scheduled_at: Optional[str] = Field(alias="scheduledAt", default=None)
    retries: Optional[int] = 0
    retry_on_no_input: Optional[bool] = Field(alias="retryOnNoInput", default=False)
    retry_on_failed: Optional[bool] = Field(alias="retryOnFailed", default=False)
    retry_delays: Optional[list[int]] = Field(alias="retryDelays",
                                              default=None,
                                              min_length=0,
                                              max_length=3)
    calendar_id: Optional[str] = Field(alias="calendarId", default=None)
    distribution: Optional[Literal["none", "dynamic"]]= "none"
    dynamic_name: Optional[str] = Field(alias="dynamicName", default=None)
    voice_flow: VoiceFlow = Field(alias="voiceFlow")
    actions: Optional[Actions] = Field(alias="actions", default=None)

    model_config = {"populate_by_name": True,
                    "validate_by_name": True}
