"""
Voice broadcast response models for the Naxai SDK.

This module defines the data structures for responses from voice broadcast API operations,
including broadcast creation, management, recipient tracking, and call attempt details.
"""

import json
from typing import Optional, Literal, Union
from pydantic import BaseModel, Field
from naxai.models.base.pagination import Pagination
from naxai.models.voice.voice_flow import VoiceFlow

REASONS = Literal["success", "rejected", "busy", "canceled-by-contact", "no-answer",
                  "canceled-by-user", "canceled-by-system", "scheduled", "inbound", "voicemail"]
STATES = Literal["draft", "started", "paused", "canceled", "completed", "scheduled",
                 "pausing", "resuming", "canceling"]

class ActionItem(BaseModel):
    """Model representing an action item in a broadcast response.

    This class defines the structure of an action that can be performed during
    a broadcast interaction, such as setting attributes or values.

    Attributes:
        attribute (Optional[str]): The name of the attribute to be modified.
            Mapped from JSON key 'attribute'. Defaults to None.
        value (Optional[Union[str, int, bool]]): The value to be assigned to the attribute.
            Can be a string, integer, or boolean. Mapped from JSON key 'value'.
            Defaults to None.

    Example:
        >>> action = ActionItem(attribute="status", value="completed")
        >>> print(f"Setting {action.attribute} to {action.value}")
        Setting status to completed
    """
    attribute: Optional[str] = Field(alias="attribute", default=None)
    value: Optional[Union[str, int, bool]] = Field(alias="value", default=None)

class Sms(BaseModel):
    """Model representing an SMS message configuration in a broadcast.

    This class defines the structure of SMS messages that can be sent as part
    of broadcast actions.

    Attributes:
        message (Optional[str]): The content of the SMS message.
            Mapped from JSON key 'message'. Defaults to None.
        sender_service_id (Optional[str]): The ID of the service sending the SMS.
            Mapped from JSON key 'senderServiceId'. Defaults to None.

    Example:
        >>> sms = Sms(
        ...     message="Thank you for participating",
        ...     senderServiceId="svc_123"
        ... )
        >>> print(f"SMS from {sms.sender_service_id}: {sms.message}")
        SMS from svc_123: Thank you for participating
    """
    message: Optional[str] = Field(alias="message", default=None)
    sender_service_id: Optional[str] = Field(alias="senderServiceId", default=None)

class Inputs(BaseModel):
    """Model representing input mappings for broadcast interactions.

    This class defines the possible input actions for each DTMF key (0-9, *, #)
    in a voice broadcast flow.

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
        ...     field_2={"sms": Sms(message="Declined")}
        ... )
        >>> print("DTMF 1 configured:", inputs.field_1 is not None)
        DTMF 1 configured: True

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
    """Model representing status-based actions in a broadcast.

    This class defines actions to be taken based on the delivery status
    of the broadcast messages.

    Attributes:
        delivered (Optional[Union[list[ActionItem], dict[str, Sms]]]): 
            Actions or SMS configurations for successfully delivered messages.
        failed (Optional[Union[list[ActionItem], dict[str, Sms]]]): 
            Actions or SMS configurations for failed message deliveries.

    Example:
        >>> status = Status(
        ...     delivered=[ActionItem(attribute="status", value="success")],
        ...     failed={"sms": Sms(message="Delivery failed")}
        ... )
        >>> print("Delivery actions configured:", status.delivered is not None)
        Delivery actions configured: True

    Note:
        - Each status can trigger either a list of actions or an SMS message
        - Both fields are optional and default to None
    """
    delivered: Optional[Union[list[ActionItem], dict[str, Sms]]]
    failed: Optional[Union[list[ActionItem], dict[str, Sms]]]

class Actions(BaseModel):
    """Model representing all possible actions in a broadcast.

    This class combines status-based actions and input-based actions
    for a complete broadcast action configuration.

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
        >>> print("Status actions configured:", actions.status is not None)
        Status actions configured: True

    Note:
        - Both status and input actions are optional
        - Actions can be configured independently for status and inputs
    """
    status: Optional[Status] = Field(alias="actions", default=None)
    inputs: Optional[Inputs] = Field(alias="inputs", default=None)

class BroadcastBase(BaseModel):
    """Base model containing common fields for broadcast operations.

    This class serves as the foundation for all broadcast-related models,
    containing the common fields used across different broadcast operations.

    Attributes:
        name (str): The name of the broadcast.
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
        retry_delays (Optional[list[int]]): Delays between retries.
            Mapped from JSON key 'retryDelays'. Limited to 0-3 values.
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

    Note:
        - Phone numbers must be between 8 and 15 characters
        - Only one segment ID is allowed in segment_ids
        - Retry delays list must contain 0-3 values
        - This is an abstract base class and should not be instantiated directly
    """
    name: str
    from_: str = Field(alias="from", min_length=8, max_length=15)
    source: Optional[str] = Field(alias="source", default="people")
    segment_ids: list[str] = Field(alias="segmentIds", max_length=1)
    inclube_unsubscribed: Optional[bool] = Field(alias="inclubeUnsubscribed", default=False)
    language: Optional[Literal["fr-FR", "fr-BE", "nl-NL", "nl-BE", "en-GB", "de-DE"]] = "fr-BE"
    voice: Optional[Literal["woman", "man"]] = "woman"
    scheduled_at: Optional[str] = Field(alias="scheduledAt", default=None)
    retries: Optional[int] = Field(default=0, ge=0, le=3)
    retry_on_no_input: Optional[bool] = Field(alias="retryOnNoInput", default=False)
    retry_on_failed: Optional[bool] = Field(alias="retryOnFailed", default=False)
    retry_delays: Optional[list[int]] = Field(alias="retryDelays",
                                              default=None,
                                              min_length=0,
                                              max_length=3)
    calendar_id: Optional[str] = Field(alias="calendarId", default=None)
    distribution: Optional[Literal["none", "dynamic"]] = "none"
    dynamic_name: Optional[str] = Field(alias="dynamicName", default=None)
    voice_flow: VoiceFlow = Field(alias="voiceFlow")
    actions: Optional[Actions] = Field(alias="actions", default=None)

class BroadcastResponseBase(BroadcastBase):
    """Base model for broadcast responses including metrics.

    This class extends BroadcastBase to include common response fields
    and metrics that are present in all broadcast response types.

    Attributes:
        broadcast_id (str): The unique identifier of the broadcast.
            Mapped from JSON key 'broadcastId'.
        total_count (Optional[int]): Total number of intended recipients.
            Mapped from JSON key 'totalCount'. Defaults to 0.
        completed_count (Optional[int]): Number of successful deliveries.
            Mapped from JSON key 'completedCount'. Defaults to 0.
        created_at (Optional[int]): Timestamp when the broadcast was created.
            Mapped from JSON key 'createdAt'. In milliseconds since epoch.
        modified_by (Optional[str]): ID of the user who last modified the broadcast.
            Mapped from JSON key 'modifiedBy'. None if not modified.

    Note:
        - All timestamp fields are in milliseconds since epoch
        - This is an abstract base class for response models
        - Inherits all fields from BroadcastBase
    """
    broadcast_id: str = Field(alias="broadcastId")
    total_count: Optional[int] = Field(alias="totalCount", default=0)
    completed_count: Optional[int] = Field(alias="completedCount", default=0)
    created_at: Optional[int] = Field(alias="createdAt", default=None)
    modified_by: Optional[str] = Field(alias="modifiedBy", default=None)

class BroadcastStatusResponse(BaseModel):
    """Model for broadcast status-only responses.

    This class defines the structure for simple status update responses
    received after performing operations on broadcasts.

    Attributes:
        broadcast_id (str): The unique identifier of the broadcast.
            Mapped from JSON key 'broadcastId'.
        status (Literal): The new status of the broadcast. One of:
            - "starting": Broadcast is beginning execution
            - "pausing": Broadcast is being paused
            - "resuming": Broadcast is being resumed
            - "canceling": Broadcast is being canceled

    Example:
        >>> response = BroadcastStatusResponse(
        ...     broadcastId="brd_123abc",
        ...     status="starting"
        ... )
        >>> print(f"Broadcast {response.broadcast_id} is {response.status}")
        Broadcast brd_123abc is starting
    """
    broadcast_id: str = Field(alias="broadcastId")
    state: Literal["starting", "pausing", "resuming", "canceling"]

class CreateBroadcastResponse(BroadcastResponseBase):
    """Model representing the response from creating a new broadcast.

    This class inherits from BroadcastResponseBase and represents the API response
    received after successfully creating a new broadcast.

    Inherits all attributes from BroadcastResponseBase:
        - All fields from BroadcastBase (name, from_, source, etc.)
        - broadcast_id (str): The unique identifier of the created broadcast
        - total_count (Optional[int]): Total number of intended recipients
        - completed_count (Optional[int]): Number of successful deliveries
        - created_at (Optional[int]): Creation timestamp
        - modified_by (Optional[str]): ID of the creator

    Example:
        >>> response = CreateBroadcastResponse(
        ...     broadcastId="brd_123abc",
        ...     name="New Campaign",
        ...     from="1234567890",
        ...     segmentIds=["seg_abc123"],
        ...     voiceFlow=voice_flow_obj,
        ...     createdAt=1703066400000
        ... )
        >>> print(f"Created broadcast: {response.broadcast_id}")
        Created broadcast: brd_123abc

    Note:
        - All timestamp fields are in milliseconds since epoch
        - Inherits all validation rules from parent classes
    """

class UpdateBroadcastResponse(BroadcastResponseBase):
    """Model representing the response from updating an existing broadcast.

    This class inherits from BroadcastResponseBase and represents the API response
    received after successfully updating a broadcast's configuration.

    Inherits all attributes from BroadcastResponseBase:
        - All fields from BroadcastBase (name, from_, source, etc.)
        - broadcast_id (str): The unique identifier of the updated broadcast
        - total_count (Optional[int]): Total number of intended recipients
        - completed_count (Optional[int]): Number of successful deliveries
        - created_at (Optional[int]): Original creation timestamp
        - modified_by (Optional[str]): ID of the user who made the update

    Example:
        >>> response = UpdateBroadcastResponse(
        ...     broadcastId="brd_123abc",
        ...     name="Updated Campaign",
        ...     from="1234567890",
        ...     segmentIds=["seg_abc123"],
        ...     voiceFlow=voice_flow_obj,
        ...     modifiedBy="usr_xyz789"
        ... )
        >>> print(f"Updated by: {response.modified_by}")
        Updated by: usr_xyz789

    Note:
        - All timestamp fields are in milliseconds since epoch
        - Inherits all validation rules from parent classes
        - The modified_by field tracks the last user to update the broadcast
    """

class GetBroadcastResponse(BroadcastResponseBase):
    """Model representing the response from retrieving a specific broadcast.

    This class inherits from BroadcastResponseBase and represents the API response
    received when fetching details of an existing broadcast.

    Inherits all attributes from BroadcastResponseBase:
        - All fields from BroadcastBase (name, from_, source, etc.)
        - broadcast_id (str): The unique identifier of the broadcast
        - total_count (Optional[int]): Total number of intended recipients
        - completed_count (Optional[int]): Number of successful deliveries
        - created_at (Optional[int]): Creation timestamp
        - modified_by (Optional[str]): ID of the last user to modify the broadcast

    Example:
        >>> response = GetBroadcastResponse(
        ...     broadcastId="brd_123abc",
        ...     name="Campaign",
        ...     from="1234567890",
        ...     segmentIds=["seg_abc123"],
        ...     voiceFlow=voice_flow_obj,
        ...     totalCount=1000,
        ...     completedCount=750
        ... )
        >>> print(f"Progress: {response.completed_count}/{response.total_count}")
        Progress: 750/1000

    Note:
        - All timestamp fields are in milliseconds since epoch
        - Inherits all validation rules from parent classes
    """
    state: STATES

class StartBroadcastResponse(BroadcastStatusResponse):
    """Model for broadcast start operation response.

    This class inherits from BroadcastStatusResponse and represents the API response
    received when starting a broadcast.

    Inherits all attributes from BroadcastStatusResponse:
        - broadcast_id (str): The unique identifier of the broadcast
        - status (Literal): Will be "starting" for this response type

    Example:
        >>> response = StartBroadcastResponse(
        ...     broadcastId="brd_123abc",
        ...     status="starting"
        ... )
        >>> print(f"Broadcast {response.broadcast_id} is {response.status}")
        Broadcast brd_123abc is starting
    """

class PauseBroadcastResponse(BroadcastStatusResponse):
    """Model for broadcast pause operation response.

    This class inherits from BroadcastStatusResponse and represents the API response
    received when pausing a broadcast.

    Inherits all attributes from BroadcastStatusResponse:
        - broadcast_id (str): The unique identifier of the broadcast
        - status (Literal): Will be "pausing" for this response type

    Example:
        >>> response = PauseBroadcastResponse(
        ...     broadcastId="brd_123abc",
        ...     status="pausing"
        ... )
        >>> print(f"Broadcast {response.broadcast_id} is {response.status}")
        Broadcast brd_123abc is pausing
    """

class ResumeBroadcastResponse(BroadcastStatusResponse):
    """Model for broadcast resume operation response.

    This class inherits from BroadcastStatusResponse and represents the API response
    received when resuming a paused broadcast.

    Inherits all attributes from BroadcastStatusResponse:
        - broadcast_id (str): The unique identifier of the broadcast
        - status (Literal): Will be "resuming" for this response type

    Example:
        >>> response = ResumeBroadcastResponse(
        ...     broadcastId="brd_123abc",
        ...     status="resuming"
        ... )
        >>> print(f"Broadcast {response.broadcast_id} is {response.status}")
        Broadcast brd_123abc is resuming
    """

class CancelBroadcastResponse(BroadcastStatusResponse):
    """Model for broadcast cancel operation response.

    This class inherits from BroadcastStatusResponse and represents the API response
    received when canceling a broadcast.

    Inherits all attributes from BroadcastStatusResponse:
        - broadcast_id (str): The unique identifier of the broadcast
        - status (Literal): Will be "canceling" for this response type

    Example:
        >>> response = CancelBroadcastResponse(
        ...     broadcastId="brd_123abc",
        ...     status="canceling"
        ... )
        >>> print(f"Broadcast {response.broadcast_id} is {response.status}")
        Broadcast brd_123abc is canceling
    """

class BroadcastResponseItem(BaseModel):
    """Model representing a single broadcast item in list responses.

    This class defines the structure of a broadcast item as it appears in list
    responses, containing essential information about the broadcast's status,
    timing, and distribution metrics.

    Attributes:
        broadcast_id (str): The unique identifier of the broadcast.
            Mapped from JSON key 'broadcastId'.
        name (str): The name or title of the broadcast.
        source (str): The source of the broadcast. Defaults to "people".
        state (Literal): Current state of the broadcast. One of:
            - "draft": Broadcast is created but not started
            - "started": Broadcast is currently running
            - "paused": Broadcast is temporarily halted
            - "completed": Broadcast has finished successfully
            - "canceled": Broadcast was terminated before completion
            - "scheduled": Broadcast is set for future execution
        started_at (Optional[int]): Timestamp when the broadcast started.
            Mapped from JSON key 'startedAt'. None if not started.
        paused_at (Optional[int]): Timestamp when the broadcast was paused.
            Mapped from JSON key 'pausedAt'. None if never paused.
        canceled_at (Optional[int]): Timestamp when the broadcast was canceled.
            Mapped from JSON key 'canceledAt'. None if not canceled.
        completed_at (Optional[int]): Timestamp when the broadcast completed.
            Mapped from JSON key 'completedAt'. None if not completed.
        distribution (Optional[str]): Distribution information for the broadcast.
            None if not specified.
        total_count (Optional[int]): Total number of intended recipients.
            Mapped from JSON key 'totalCount'. Defaults to 0.
        completed_count (Optional[int]): Number of successful deliveries.
            Mapped from JSON key 'completedCount'. Defaults to 0.
        created_at (int): Timestamp when the broadcast was created.
            Mapped from JSON key 'createdAt'.

    Example:
        >>> item = BroadcastResponseItem(
        ...     broadcastId="brd_123abc",
        ...     name="Weekly Campaign",
        ...     state="started",
        ...     totalCount=1000,
        ...     completedCount=750,
        ...     createdAt=1703066400000
        ... )
        >>> print(f"Broadcast: {item.name} ({item.state})")
        >>> print(f"Progress: {item.completed_count}/{item.total_count}")
        Broadcast: Weekly Campaign (started)
        Progress: 750/1000

    Note:
        - All timestamp fields are in milliseconds since epoch
        - State transitions are reflected in the respective timestamp fields
        - The source field defaults to "people" if not specified
        - Count fields default to 0 if not specified
    """
    broadcast_id: str = Field(alias="broadcastId")
    name: str
    source: str = Field(default="people")
    state: Literal["draft", "started", "paused", "completed", "canceled", "scheduled", "processing"]
    started_at: Optional[int] = Field(alias="startedAt", default=None)
    paused_at: Optional[int] = Field(alias="pausedAt", default=None)
    canceled_at: Optional[int] = Field(alias="canceledAt", default=None)
    completed_at: Optional[int] = Field(alias="completedAt", default=None)
    distribution: Optional[str] = Field(default=None)
    total_count: Optional[int] = Field(default=0, alias="totalCount")
    completed_count: Optional[int] = Field(default=0, alias="completedCount")
    created_at: int = Field(alias="createdAt")

class ListBroadcastResponse(BaseModel):
    """Model representing the response for listing broadcasts.

    This class defines the structure of the API response when retrieving a list
    of broadcasts, including pagination information.

    Attributes:
        items (list[BroadcastResponseItem]): List of broadcast items.
            Mapped from JSON key 'items'.
        pagination (Pagination): Pagination information for the list.
            Mapped from JSON key 'pagination'.

    Example:
        >>> response = ListBroadcastResponse(
        ...     items=[
        ...         BroadcastResponseItem(
        ...             broadcastId="brd_123",
        ...             name="Campaign 1",
        ...             state="completed",
        ...             createdAt=1703066400000
        ...         ),
        ...         BroadcastResponseItem(
        ...             broadcastId="brd_456",
        ...             name="Campaign 2",
        ...             state="started",
        ...             createdAt=1703066400000
        ...         )
        ...     ],
        ...     pagination=Pagination(
        ...         page=1,
        ...         pageSize=10,
        ...         totalPages=5,
        ...         totalItems=45
        ...     )
        ... )
        >>> print(f"Found {len(response.items)} broadcasts")
        >>> print(f"Page {response.pagination.page} of {response.pagination.totalPages}")
        Found 2 broadcasts
        Page 1 of 5

    Note:
        - The items list contains BroadcastResponseItem objects
        - Pagination provides information about the current page and total results
        - The response maintains the order of broadcasts as returned by the API
    """
    items: list[BroadcastResponseItem] = Field(alias="items")
    pagination: Pagination = Field(alias="pagination")

class GetBroadcastMetricsResponse(BaseModel):
    """Model representing detailed metrics for a broadcast campaign.

    This class defines the structure for broadcast metrics response, providing
    comprehensive statistics about call statuses and outcomes.

    Attributes:
        total (int): Total number of calls attempted in the broadcast.
        completed (int): Number of calls that successfully completed.
        delivered (int): Number of calls successfully delivered to recipients.
        failed (int): Number of calls that failed to complete.
        canceled (int): Number of calls that were canceled.
        paused (int): Number of calls currently in paused state.
        invalid (int): Number of invalid call attempts (e.g., invalid numbers).
        in_progress (int): Number of calls currently being executed.
            Mapped from JSON key 'inProgress'.
        transferred (int): Number of calls that were transferred.
        calls (int): Total number of call attempts made.

    Example:
        >>> metrics = GetBroadcastMetricsResponse(
        ...     total=1000,
        ...     completed=750,
        ...     delivered=700,
        ...     failed=50,
        ...     canceled=25,
        ...     paused=10,
        ...     invalid=15,
        ...     in_progress=150,
        ...     transferred=0,
        ...     calls=950
        ... )
        >>> success_rate = (metrics.completed / metrics.total) * 100
        >>> print(f"Success rate: {success_rate}%")
        Success rate: 75.0%

    Note:
        - All metrics are represented as integers
        - The sum of completed, failed, canceled, paused, and in_progress
          should equal the total count
        - Delivered count may be less than completed count due to
          post-completion processing
        - Invalid calls are counted separately from failed calls
        - Transferred calls are tracked independently of completion status

    See Also:
        BroadcastResponseBase: For general broadcast response information
        ListBroadcastResponse: For listing multiple broadcasts with basic metrics
    """
    total: int
    completed: int
    delivered: int
    failed: int
    canceled: int
    paused: int
    invalid: int
    in_progress: int = Field(alias="inProgress")
    transferred: int
    calls: int

class GetBroadcastInputMetricsResponse(BaseModel):
    """Model representing DTMF input metrics for a broadcast campaign.

    This class defines the structure for tracking and analyzing recipient 
    interactions through DTMF (touch-tone) inputs during a voice broadcast.

    Attributes:
        input_0 (Optional[int]): Number of times the '0' key was pressed.
            Mapped from JSON key '0'. Defaults to 0.
        input_1 (Optional[int]): Number of times the '1' key was pressed.
            Mapped from JSON key '1'. Defaults to 0.
        input_2 (Optional[int]): Number of times the '2' key was pressed.
            Mapped from JSON key '2'. Defaults to 0.
        input_3 (Optional[int]): Number of times the '3' key was pressed.
            Mapped from JSON key '3'. Defaults to 0.
        input_4 (Optional[int]): Number of times the '4' key was pressed.
            Mapped from JSON key '4'. Defaults to 0.
        input_5 (Optional[int]): Number of times the '5' key was pressed.
            Mapped from JSON key '5'. Defaults to 0.
        input_6 (Optional[int]): Number of times the '6' key was pressed.
            Mapped from JSON key '6'. Defaults to 0.
        input_7 (Optional[int]): Number of times the '7' key was pressed.
            Mapped from JSON key '7'. Defaults to 0.
        input_8 (Optional[int]): Number of times the '8' key was pressed.
            Mapped from JSON key '8'. Defaults to 0.
        input_9 (Optional[int]): Number of times the '9' key was pressed.
            Mapped from JSON key '9'. Defaults to 0.
        input_star (Optional[int]): Number of times the '*' key was pressed.
            Mapped from JSON key 'star'. Defaults to 0.
        input_hash (Optional[int]): Number of times the '#' key was pressed.
            Mapped from JSON key 'hash'. Defaults to 0.
        total (Optional[int]): Total number of DTMF inputs received.
            Defaults to 0.

    Example:
        >>> metrics = GetBroadcastInputMetricsResponse(
        ...     input_1=500,  # 500 recipients pressed 1
        ...     input_2=300,  # 300 recipients pressed 2
        ...     input_9=50,   # 50 recipients pressed 9
        ...     total=850
        ... )
        >>> print(f"Option 1 selected: {metrics.input_1} times")
        >>> print(f"Total inputs: {metrics.total}")
        Option 1 selected: 500 times
        Total inputs: 850

    Note:
        - All input counts default to 0 if not specified
        - The same recipient may be counted multiple times if they
          pressed different keys
        - The total represents all DTMF inputs received during the broadcast
        - The sum of all individual input counts should equal the total

    See Also:
        GetBroadcastMetricsResponse: For general broadcast metrics
    """
    input_0: Optional[int] = Field(alias="0", default=0)
    input_1: Optional[int] = Field(alias="1", default=0)
    input_2: Optional[int] = Field(alias="2", default=0)
    input_3: Optional[int] = Field(alias="3", default=0)
    input_4: Optional[int] = Field(alias="4", default=0)
    input_5: Optional[int] = Field(alias="5", default=0)
    input_6: Optional[int] = Field(alias="6", default=0)
    input_7: Optional[int] = Field(alias="7", default=0)
    input_8: Optional[int] = Field(alias="8", default=0)
    input_9: Optional[int] = Field(alias="9", default=0)
    input_star: Optional[int] = Field(alias="star", default=0)
    input_hash: Optional[int] = Field(alias="hash", default=0)
    total: Optional[int] = Field(default=0)

class BroadcastRecipient(BaseModel):
    """Model representing a recipient of a broadcast campaign.

    This class defines the structure for individual recipient data, including
    their contact information, voice flow configuration, and delivery status.

    Attributes:
        recipient_id (str): Unique identifier for the recipient.
            Mapped from JSON key 'recipientId'.
        phone (str): The recipient's phone number.
            Mapped from JSON key 'phone'.
        contact_id (str): Unique identifier of the associated contact.
            Mapped from JSON key 'contactId'.
        voice_flow (VoiceFlow): The voice flow configuration for this recipient.
            Mapped from JSON key 'voiceFlow'.
        calls (int): Number of call attempts made to this recipient.
        completed (bool): Whether the broadcast was completed for this recipient.
        status (Literal): Current status of the broadcast for this recipient.
            One of: "delivered", "failed", "canceled", "in-progress", 
            "invalid", "paused".
        input_ (str): DTMF input received from the recipient.
            Mapped from JSON key 'input'.
        transferred (bool): Whether the recipient was transferred.
        last_updated_at (int): Timestamp of the last status update.
            Mapped from JSON key 'lastUpdatedAt'. In milliseconds since epoch.

    Example:
        >>> recipient = BroadcastRecipient(
        ...     recipientId="rec_123abc",
        ...     phone="+1234567890",
        ...     contactId="cnt_456def",
        ...     voiceFlow=voice_flow_obj,
        ...     calls=2,
        ...     completed=True,
        ...     status="delivered",
        ...     input="1",
        ...     transferred=False,
        ...     lastUpdatedAt=1703066400000
        ... )
        >>> print(f"Recipient {recipient.phone}: {recipient.status}")
        Recipient +1234567890: delivered

    Note:
        - Status transitions are tracked with lastUpdatedAt timestamp
        - The input field contains the last DTMF input received
        - Multiple call attempts may be made based on retry configuration
        - Voice flow may be customized per recipient
        - All timestamps are in milliseconds since epoch

    See Also:
        VoiceFlow: For voice flow configuration details
        GetBroadcastMetricsResponse: For aggregate recipient metrics
    """
    recipient_id: str = Field(alias="recipientId")
    phone: str = Field(alias="phone")
    contact_id: str = Field(alias="contactId")
    voice_flow: VoiceFlow = Field(alias="voiceFlow")
    calls: int
    completed: bool
    status: Literal["delivered", "failed", "canceled", "in-progress", "invalid", "paused"]
    input_: str = Field(alias="input")
    transferred: bool
    last_updated_at: int = Field(alias="lastUpdatedAt")

    model_config = {"populate_by_name": True}

class ListBroadcastRecipientsResponse(BaseModel):
    """Model representing a paginated list of broadcast recipients.

    This class defines the structure for the response when retrieving a list
    of recipients for a broadcast campaign, including pagination details.

    Attributes:
        items (list[BroadcastRecipient]): List of recipient objects containing
            detailed information about each recipient in the broadcast.
        total (int): Total number of recipients in the broadcast campaign.
        limit (int): Maximum number of recipients returned per page.
        offset (int): Starting position of the current page in the total list.

    Example:
        >>> response = ListBroadcastRecipientsResponse(
        ...     items=[
        ...         BroadcastRecipient(
        ...             recipientId="rec_123",
        ...             phone="+1234567890",
        ...             status="delivered"
        ...         ),
        ...         BroadcastRecipient(
        ...             recipientId="rec_456",
        ...             phone="+0987654321",
        ...             status="failed"
        ...         )
        ...     ],
        ...     total=100,
        ...     limit=10,
        ...     offset=0
        ... )
        >>> print(f"Showing {len(response.items)} of {response.total} recipients")
        >>> print(f"Page {response.offset // response.limit + 1}")
        Showing 2 of 100 recipients
        Page 1

    Note:
        - The items list may be empty if no recipients match the query
        - Use offset and limit for pagination through large recipient lists
        - Total represents all recipients, not just those in current page
        - Recipients are typically sorted by lastUpdatedAt timestamp

    See Also:
        BroadcastRecipient: For detailed recipient information
        GetBroadcastMetricsResponse: For aggregate recipient metrics
    """
    pagination: Pagination
    items: list[BroadcastRecipient]

class GetBroadcastRecipientResponse(BroadcastRecipient):
    """Model representing detailed information for a single broadcast recipient.

    This class defines the structure for retrieving comprehensive information
    about a specific recipient in a broadcast campaign, including their status,
    call attempts, and interaction details.

    Attributes:
        recipient_id (str): Unique identifier for the recipient.
            Mapped from JSON key 'recipientId'.
        broadcast_id (str): Unique identifier of the broadcast campaign.
            Mapped from JSON key 'broadcastId'.
        phone (str): The recipient's phone number.
        contact_id (str): Unique identifier of the associated contact.
            Mapped from JSON key 'contactId'.
        status (str): Current status of the broadcast delivery for this recipient.
            Possible values include: "delivered", "failed", "canceled",
            "in-progress", "invalid", "paused".
        completed (bool): Whether the broadcast was successfully completed
            for this recipient.
        calls (int): Number of call attempts made to this recipient.
        input_ (Optional[str]): DTMF input received from the recipient, if any.
            Mapped from JSON key 'input'.
        transferred (bool): Whether the recipient was transferred during the call.
        last_updated_at (int): Timestamp of the last status update,
            in milliseconds since epoch.
            Mapped from JSON key 'lastUpdatedAt'.

    Example:
        >>> response = GetBroadcastRecipientResponse(
        ...     recipientId="rec_123abc",
        ...     broadcastId="brd_456def",
        ...     phone="+1234567890",
        ...     contactId="cnt_789ghi",
        ...     status="delivered",
        ...     completed=True,
        ...     calls=2,
        ...     input="1",
        ...     transferred=False,
        ...     lastUpdatedAt=1703066400000
        ... )
        >>> print(f"Recipient {response.phone}")
        >>> print(f"Status: {response.status}")
        >>> print(f"Call attempts: {response.calls}")
        Recipient +1234567890
        Status: delivered
        Call attempts: 2

    Note:
        - The input field may be None if no DTMF input was received
        - Multiple call attempts may be recorded based on retry configuration
        - Status updates are tracked with lastUpdatedAt timestamp
        - The completed flag indicates successful completion regardless
          of the number of attempts needed
        - All timestamps are in milliseconds since epoch

    See Also:
        ListBroadcastRecipientsResponse: For retrieving multiple recipients
        BroadcastRecipient: For the base recipient model structure
    """

class RecipientCall(BaseModel):
    """Model representing a single call attempt to a broadcast recipient.

    This class defines the structure for an individual call attempt, including
    its status, outcome, timing, and duration information.

    Attributes:
        call_id (str): Unique identifier for the call attempt.
            Mapped from JSON key 'callId'.
        status (Literal["delivered", "failed", "scheduled", "canceled"]): 
            Current status of the call attempt.
        reason (Literal["success", "rejected", "busy", "canceled-by-contact", 
                       "no-answer", "canceled-by-user", "canceled-by-system", 
                       "scheduled", "inbound", "voicemail"]): 
            Detailed reason for the call outcome.
        attempt_order (int): Sequential number of this call attempt.
            Mapped from JSON key 'attemptOrder'.
        duration (int): Duration of the call in seconds. Will be 0 for
            unsuccessful attempts.
        call_at (int): Timestamp when the call was made or is scheduled,
            in milliseconds since epoch.
            Mapped from JSON key 'callAt'.

    Example:
        >>> call = RecipientCall(
        ...     callId="call_123abc",
        ...     status="delivered",
        ...     reason="success",
        ...     attemptOrder=2,
        ...     duration=45,
        ...     callAt=1703066400000
        ... )
        >>> print(f"Call {call.call_id}: {call.status}")
        >>> print(f"Duration: {call.duration} seconds")
        Call call_123abc: delivered
        Duration: 45 seconds

    Note:
        - attempt_order starts at 1 and increments for each retry
        - duration will be 0 for failed, canceled, or scheduled calls
        - call_at represents actual call time for completed calls
          and scheduled time for future calls
        - status transitions: scheduled -> delivered/failed/canceled
        - reason provides more detailed information about the call outcome
          than the status field

    See Also:
        GetBroadcastRecipientResponse: For list of call attempts
        BroadcastRecipient: For recipient information
    """
    call_id: str = Field(alias="callId")
    status: Literal["delivered", "failed", "scheduled", "canceled"]
    reason: REASONS
    attempt_order: int = Field(alias="attemptOrder")
    duration: int
    call_at: int = Field(alias="callAt")

    model_config = {"populate_by_name": True}

class GetBroadcastRecipientCallsResponse(BaseModel):
    """Model representing a list of call attempts for a broadcast recipient.
    
    This class defines the structure for retrieving the call history for a specific
    recipient in a broadcast campaign, providing details about each call attempt.
    It implements list-like behavior for easy iteration through call attempts.
    
    Attributes:
        root (list[RecipientCall]): List of call attempt objects containing
            detailed information about each call made to the recipient.
    
    Example:
        >>> response = GetBroadcastRecipientCallsResponse(
        ...     root=[
        ...         RecipientCall(
        ...             callId="call_123",
        ...             status="failed",
        ...             reason="no-answer",
        ...             attemptOrder=1,
        ...             duration=0,
        ...             callAt=1703066400000
        ...         ),
        ...         RecipientCall(
        ...             callId="call_456",
        ...             status="delivered",
        ...             reason="success",
        ...             attemptOrder=2,
        ...             duration=45,
        ...             callAt=1703066500000
        ...         )
        ...     ]
        ... )
        >>> print(f"Total call attempts: {len(response)}")
        >>> print(f"First attempt: {response[0].status}")
        >>> print(f"Last attempt: {response[-1].status}")
        >>> for call in response:
        ...     print(f"Attempt {call.attempt_order}: {call.status} - {call.reason}")
        Total call attempts: 2
        First attempt: failed
        Last attempt: delivered
        Attempt 1: failed - no-answer
        Attempt 2: delivered - success
    
    Note:
        - This class implements __len__, __getitem__, and __iter__ methods for list-like behavior
        - Call attempts are typically sorted by attemptOrder (chronological order)
        - The model_validate_json method handles both array-style JSON and object-style JSON
        - Empty list indicates no call attempts have been made to this recipient
        - Multiple attempts may be present based on retry configuration
    
    See Also:
        RecipientCall: For detailed call attempt information
        GetBroadcastRecipientResponse: For recipient information
    """
    root: list[RecipientCall] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return the number of call attempts."""
        return len(self.root)

    def __getitem__(self, index):
        """Access call attempts by index."""
        return self.root[index]

    def __iter__(self):
        """Iterate through call attempts."""
        return iter(self.root)

    @classmethod
    def model_validate_json(cls, json_data: str, **kwargs):
        """Parse JSON data into the model.
        
        This method handles both array-style JSON and object-style JSON with a root field.
        """
        data = json.loads(json_data)

        # If the data is a list, wrap it in a dict with the root field
        if isinstance(data, list):
            return cls(root=data)

        # Otherwise, use the standard Pydantic validation
        return super().model_validate_json(json_data, **kwargs)
