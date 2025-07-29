"""
Voice call resource for the Naxai SDK.

This module provides methods for creating and managing individual voice calls,
including configuring welcome messages, interactive menus, voicemail handling,
and call endings. It supports features such as machine detection, scheduling,
and language selection to enable sophisticated voice communication workflows.

Available Functions:
    create(from_: str, to: str, welcome: Welcome, menu: Menu, voicemail: VoiceMail, end: End)
        Creates a new voice call with the specified configuration.
        Args:
            from_: The phone number making the call
            to: The phone number receiving the call
            welcome: Welcome message configuration
            menu: Interactive menu configuration
            voicemail: Voicemail handling settings
            end: Call ending configuration
        Returns:
            CreateCallResponse: Details of the created call

    _create(data: CreateCallRequest)
        Internal method to create a new voice call.
        Args:
            data: Call configuration including from/to numbers, welcome message,
                 menu options, voicemail settings, and call ending parameters
        Returns:
            dict: API response containing created call details

"""

import json
from typing import Optional, Literal
from pydantic import Field, validate_call
from naxai.models.voice.requests.call_requests import (CreateCallRequest,
                                                       Welcome,
                                                       End,
                                                       Menu,
                                                       VoiceMail)
from naxai.models.voice.responses.call_responses import CreateCallResponse


class CallResource:
    """ call resource for the voice resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/call"
        self.headers = {"Content-Type": "application/json"}


    def _create(self, data: CreateCallRequest):
        """
        Creates a new call.

        Args:
            data (CreateCallRequest): 
                The request body containing the details of the call to be created.

        Returns:
            dict: The API response containing the details of the created call.

        Example:
            >>> new call = client.voice.call.create(
            ...     CreateCallRequest(
            ...         from_="123456789",
            ...         to="1234567890",
            ...         ...
            ...     )
            ... )
        """
        # pylint: disable=protected-access
        return self._client._request("POST",
                                     "/voice/call",
                                     json=data.model_dump(by_alias=True,
                                                          exclude_none=True),
                                     headers=self.headers)

    @validate_call
    def create(self,
                welcome: Welcome,
                language: Literal["fr-BE", "fr-FR", "nl-BE", "nl-NL", "en-GB", "de-DE"],
                to: list[str] = Field(min_length=1, max_length=1000),
                from_: str = Field(min_length=8, max_length=15),
                batch_id: Optional[str] = Field(max_length=64, default=None),
                voice: Optional[Literal["man", "woman"]] = Field(default="woman"),
                idempotency_key: Optional[str] = Field(max_length=128, min_length=1, default=None),
                calendar_id: Optional[str] = Field(max_length=64, default=None),
                scheduled_at: Optional[int] = Field(default=None),
                machine_detection: Optional[bool] = Field(default=False),
                voicemail: Optional[VoiceMail] = Field(default=None),
                menu: Optional[Menu] = Field(default=None),
                end: Optional[End] = Field(default=None)):
        """Create a new voice call with specified parameters.

        This method initiates a new voice call with the provided configuration, including
        welcome message, language settings, and various optional parameters.

        Args:
            welcome (Welcome): The welcome message configuration for the call.
            language (Literal["fr-BE", "fr-FR", "nl-BE", "nl-NL", "en-GB", "de-DE"]): 
                The language to be used for the call.
            to (list[str]): 
                List of recipient phone numbers. Must contain between 1 and 1000 numbers.
            from_ (str): The sender's phone number. Must be between 8 and 15 characters.
            batch_id (Optional[str], optional): Unique identifier for the batch. Max 64 characters.
            voice (Optional[Literal["man", "woman"]], optional): Voice gender selection. 
                Defaults to "woman".
            idempotency_key (Optional[str], optional): Key to prevent duplicate requests. 
                Between 1 and 128 characters.
            calendar_id (Optional[str], optional): Calendar identifier. Max 64 characters.
            scheduled_at (Optional[str], optional): Scheduled time for the call. Max 64 characters.
            machine_detection (Optional[bool], optional): Enable machine detection. 
                Defaults to False.
            voicemail (Optional[VoiceMail], optional): Voicemail configuration settings.
            menu (Optional[Menu], optional): Interactive menu configuration.
            end (Optional[End], optional): End call configuration.

        Returns:
            CreateCallResponse: Object containing the details of the created call.

        Raises:
            ValueError: If required parameters are missing or invalid.
            ValidationError: If the input parameters fail validation.
            APIError: If there is an error response from the API.

        Example:
            >>> welcome_config = Welcome(text="Hello, welcome to our service")
            >>> call = client.voice.call.create(
            ...     welcome=welcome_config,
            ...     language="en-GB",
            ...     to=["1234567890"],
            ...     from_="9876543210",
            ...     voice="woman"
            ... )

        Note:
            - The 'to' parameter must contain valid phone numbers
            - The 'from_' parameter must be a valid phone number
            - All string lengths are validated according to the specified constraints
            - The request is made with "Content-Type: application/json" header
        """
        create_call_object = CreateCallRequest(batchId=batch_id,
                                               to=to,
                                               from_=from_,
                                               language=language,
                                               welcome=welcome,
                                               voice=voice,
                                               idempotencyKey=idempotency_key,
                                               calendarId=calendar_id,
                                               scheduledAt=scheduled_at,
                                               machineDetection=machine_detection,
                                               voicemail=voicemail,
                                               menu=menu,
                                               end=end)

        return CreateCallResponse.model_validate_json(json.dumps(self._create(create_call_object)))
