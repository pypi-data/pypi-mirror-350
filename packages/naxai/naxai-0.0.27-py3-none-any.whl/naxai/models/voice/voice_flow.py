"""
Voice flow models for the Naxai SDK.

This module defines the data structures for creating interactive voice experiences,
including welcome messages, menus, transfers, and other components that make up
a complete voice call flow.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class End(BaseModel):
    """
    Model representing the end of a voice call flow.
    
    This class defines the final message or prompt to be played before ending the call.
    
    Attributes:
        say (Optional[str]): Text to be spoken at the end of the call.
            Mapped from JSON key 'say'. Defaults to None.
        prompt (Optional[str]): URL to an audio file to play at the end of the call.
            Mapped from JSON key 'prompt'. Defaults to None.
    
    Note:
        Either 'say' or 'prompt' should be provided, but not both.
        If both are provided, 'prompt' takes precedence.
    """
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None)


class Whisper(BaseModel):
    """
    Model representing a whisper message for transfers.
    
    This class defines a message that is played only to the transfer recipient
    before connecting them with the caller.
    
    Attributes:
        say (Optional[str]): Text to be spoken as a whisper message.
            Mapped from JSON key 'say'. Defaults to None.
        prompt (Optional[str]): URL to an audio file to play as a whisper message.
            Mapped from JSON key 'prompt'. Defaults to None.
    
    Note:
        Either 'say' or 'prompt' should be provided, but not both.
        If both are provided, 'prompt' takes precedence.
        The caller does not hear this message, only the transfer recipient.
    """
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None)


class Transfer(BaseModel):
    """
    Model representing a call transfer configuration.
    
    This class defines how a call should be transferred to another destination,
    including retry attempts and optional whisper messages.
    
    Attributes:
        destination (str): Phone number or SIP address to transfer the call to.
            Mapped from JSON key 'destination'.
        attempts (Optional[int]): Number of transfer attempts if the first fails.
            Range: 1-3. Mapped from JSON key 'attempts'. Defaults to 1.
        timeout (Optional[int]): Seconds to wait for transfer pickup before timing out.
            Range: 5-30. Mapped from JSON key 'timeout'. Defaults to 15.
        whisper (Optional[Whisper]): Whisper message to play to the transfer recipient.
            Mapped from JSON key 'whisper'. Defaults to None.
    
    Note:
        The destination must be a valid phone number or SIP address.
        Multiple attempts will be made only if previous attempts fail.
        The timeout applies to each attempt individually.
    """
    destination: str = Field(alias="destination")
    attempts: Optional[int] = Field(alias="attempts", default=1, ge=1, le=3)
    timeout: Optional[int] = Field(alias="timeout", default=15, ge=5, le=30)
    whisper: Optional[Whisper] = Field(alias="whisper", default=None)


class Choice(BaseModel):
    """
    Model representing a menu choice option.
    
    This class defines a single option in an interactive voice menu,
    including the key to press and the resulting action.
    
    Attributes:
        key (Literal): DTMF key that triggers this choice.
            Must be one of: "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "#".
        say (Optional[str]): Text to be spoken when this choice is selected.
            Mapped from JSON key 'say'. Defaults to None.
        prompt (Optional[str]): URL to an audio file to play when this choice is selected.
            Mapped from JSON key 'prompt'. Defaults to None.
        replay (Optional[int]): Number of times to replay the menu after this choice.
            Mapped from JSON key 'replay'. Defaults to 0.
        transfer (Optional[Transfer]): Transfer configuration if this choice
            should transfer the call. Mapped from JSON key 'transfer'. Defaults to None.
    
    Note:
        Either 'say'/'prompt' or 'transfer' should be provided to define the action.
        If 'transfer' is provided, the call will be transferred instead of playing a message.
        The 'replay' option only applies if 'say' or 'prompt' is used, not for transfers.
    """
    key: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "#"]
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None)
    replay: Optional[int] = Field(alias="replay", default=0)
    transfer: Optional[Transfer] = Field(alias="transfer", default=None)


class Menu(BaseModel):
    """
    Model representing an interactive voice menu.
    
    This class defines a menu presented to the caller with multiple options
    that can be selected using DTMF keys.
    
    Attributes:
        say (Optional[str]): Text to be spoken as the menu prompt.
            Mapped from JSON key 'say'. Defaults to None.
        prompt (Optional[str]): URL to an audio file to play as the menu prompt.
            Mapped from JSON key 'prompt'. Defaults to None.
        replay (Optional[int]): Number of times to replay the menu if no input is received.
            Mapped from JSON key 'replay'. Defaults to 0.
        choices (list[Choice]): List of available choices in this menu.
            Mapped from JSON key 'choices'.
    
    Note:
        Either 'say' or 'prompt' should be provided as the menu introduction.
        The 'choices' list must contain at least one Choice object.
        Each choice must have a unique key within this menu.
        If the caller doesn't select any option and 'replay' is > 0,
        the menu will be repeated that many times.
    """
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None)
    replay: Optional[int] = Field(alias="replay", default=0)
    choices: list[Choice] = Field(alias="choices")


class Welcome(BaseModel):
    """
    Model representing the initial welcome message of a voice call.
    
    This class defines the first message played when a call is answered,
    before any menus or other interactions.
    
    Attributes:
        say (Optional[str]): Text to be spoken as the welcome message.
            Mapped from JSON key 'say'. Defaults to None.
        prompt (Optional[str]): URL to an audio file to play as the welcome message.
            Mapped from JSON key 'prompt'. Defaults to None.
        replay (Optional[int]): 
            Number of times to replay the welcome message if no input is received.
            Mapped from JSON key 'replay'. Defaults to 0.
    
    Note:
        Either 'say' or 'prompt' should be provided, but not both.
        If both are provided, 'prompt' takes precedence.
        The 'replay' option is only relevant if this welcome is followed by a menu.
    """
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None)
    replay: Optional[int] = Field(alias="replay", default=0)


class VoiceMail(BaseModel):
    """
    Model representing a voicemail configuration.
    
    This class defines the message to be played when a call is answered by
    an answering machine or voicemail system.
    
    Attributes:
        say (Optional[str]): Text to be spoken as the voicemail message.
            Mapped from JSON key 'say'. Defaults to None.
        prompt (Optional[str]): URL to an audio file to play as the voicemail message.
            Mapped from JSON key 'prompt'. Defaults to None.
    
    Note:
        Either 'say' or 'prompt' should be provided, but not both.
        If both are provided, 'prompt' takes precedence.
        This message is only played if machine detection is enabled and
        an answering machine is detected.
    """
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None)


class VoiceFlow(BaseModel):
    """
    Model representing a complete voice call flow configuration.
    
    This class defines the entire structure of a voice call interaction,
    from initial greeting through menus, transfers, and ending.
    
    Attributes:
        machine_detection (Optional[bool]): Whether to detect answering machines.
            Mapped from JSON key 'machineDetection'. Defaults to False.
        voicemail (Optional[VoiceMail]): Message to play if an answering machine is detected.
            Defaults to None.
        welcome (Welcome): Initial greeting message configuration.
            Mapped from JSON key 'welcome'.
        menu (Optional[Menu]): Interactive menu configuration.
            Mapped from JSON key 'menu'. Defaults to None.
        end (Optional[End]): Call ending message configuration.
            Mapped from JSON key 'end'. Defaults to None.
    
    Note:
        The 'welcome' field is required and defines the initial interaction.
        If 'machine_detection' is True, the system will attempt to detect answering machines.
        If an answering machine is detected and 'voicemail' is provided, that message
        will be played.
        The 'menu' field is optional; if not provided, the call will proceed directly to 'end'.
        The 'end' field is optional; if not provided, the call will end after 'welcome' or 'menu'.
    """
    machine_detection: Optional[bool] = Field(alias="machineDetection", default=False)
    voicemail: Optional[VoiceMail] = Field(default=None)
    welcome: Welcome = Field(alias="welcome")
    menu: Optional[Menu] = Field(alias="menu", default=None)
    end: Optional[End] = Field(alias="end", default=None)

    model_config = {"populate_by_name": True}
