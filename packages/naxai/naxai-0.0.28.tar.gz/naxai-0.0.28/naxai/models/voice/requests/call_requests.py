"""
Voice call request models for the Naxai SDK.

This module defines the data structures used for initiating voice calls,
including recipient targeting, call flow configuration, scheduling options,
and voicemail handling.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field
from naxai.models.voice.voice_flow import (VoiceMail,
                                           Welcome,
                                           Menu,
                                           End)

class CreateCallRequest(BaseModel):
    """
    Request model for creating a new voice call.
    
    This class defines the structure of the request payload when initiating
    a voice call to one or more recipients.
    
    Attributes:
        batch_id (Optional[str]): Unique identifier for grouping related calls.
            Mapped from JSON key 'batchId'. Maximum 64 characters.
        to (list[str]): List of recipient phone numbers. Maximum 1000 recipients.
        from_ (str): The sender's phone number (8-15 characters).
            Mapped from JSON key 'from'.
        language (Literal): Voice language code. One of:
            "fr-FR", "fr-BE", "nl-NL", "nl-BE", "en-GB", "de-DE".
        voice (Literal): Voice gender selection. Either "woman" or "man".
        idempotency_key (Optional[str]): Key to prevent duplicate call creation.
            Mapped from JSON key 'idempotencyKey'. 1-128 characters.
        calendar_id (Optional[str]): Associated calendar ID for scheduling.
            Mapped from JSON key 'calendarId'. None if not using calendar.
        scheduled_at (Optional[int]): Timestamp for scheduled calls.
            Mapped from JSON key 'scheduledAt'. None for immediate calls.
        machine_detection (Optional[bool]): Whether to detect answering machines.
            Mapped from JSON key 'machineDetection'. Defaults to False.
        voicemail (Optional[VoiceMail]): Voicemail configuration.
            None if not using voicemail.
        welcome (Welcome): Initial greeting message configuration.
        menu (Optional[Menu]): Interactive menu configuration.
            None if not using interactive menus.
        end (Optional[End]): Call ending message configuration.
            None if not using end message.
    """
    batch_id : Optional[str] = Field(alias="batchId", max_length=64)
    to: list[str] = Field(max_length=1000)
    from_: str = Field(alias="from", min_length=8, max_length=15)
    language: Literal["fr-FR", "fr-BE", "nl-NL", "nl-BE", "en-GB", "de-DE"]
    voice: Literal["woman", "man"]
    idempotency_key: Optional[str] = Field(alias="idempotencyKey", min_length=1, max_length=128)
    calendar_id: Optional[str] = Field(alias="calendarId", default=None)
    scheduled_at: Optional[int] = Field(alias="scheduledAt", default=None)
    machine_detection: Optional[bool] = Field(alias="machineDetection", default=False)
    voicemail: Optional[VoiceMail] = Field(default=None)
    welcome: Welcome = Field(alias="welcome")
    menu: Optional[Menu] = Field(alias="menu", default=None)
    end: Optional[End] = Field(alias="end", default=None)

    model_config = {"populate_by_name": True,
                    "validate_by_name": True}
