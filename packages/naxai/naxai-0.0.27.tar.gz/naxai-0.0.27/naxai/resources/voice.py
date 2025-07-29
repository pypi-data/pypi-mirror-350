"""Voice resource for the Naxai SDK.

This module provides voice communication capabilities for the Naxai platform,
including individual call management, broadcast campaigns for reaching multiple
recipients, detailed activity tracking, and comprehensive performance reporting.
It supports interactive voice features such as menus, voicemail handling, and
call transfers to enable sophisticated voice communication workflows.

Sub-resources:
    call: CallResource
        Manages individual call operations and voice communication workflows

    broadcasts: BroadcastsResource  
        Handles broadcast campaign operations for reaching multiple recipients

    reporting: ReportingResource
        Provides comprehensive reporting and analytics capabilities

    activity_logs: ActivityLogsResource
        Manages detailed activity logging and tracking

"""

from .voice_resources.call import CallResource
from .voice_resources.broadcast import BroadcastsResource
from .voice_resources.reporting import ReportingResource
from .voice_resources.activity_logs import ActivityLogsResource

class VoiceResource:
    """
    Provides access to voice related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.root_path = "/voice"
        self.call: CallResource = CallResource(client, self.root_path)
        self.broadcasts: BroadcastsResource = BroadcastsResource(client, self.root_path)
        self.reporting: ReportingResource = ReportingResource(client, self.root_path)
        self.activity_logs: ActivityLogsResource = ActivityLogsResource(client, self.root_path)
