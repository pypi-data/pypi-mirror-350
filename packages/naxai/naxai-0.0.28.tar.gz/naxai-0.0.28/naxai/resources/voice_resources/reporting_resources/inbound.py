"""
Voice inbound reporting resource for the Naxai SDK.

This module provides methods for retrieving and analyzing metrics related to inbound
voice calls, including call volumes, answer rates, and duration statistics. These
reports can be grouped by different time intervals and filtered by specific phone
numbers to help users understand incoming call patterns and optimize their voice
communication strategies.

Available Functions:
    list(group: Literal["hour", "day", "month"], start_date: str, stop_date: str, number: str)
        Retrieves inbound call metrics grouped by time interval.
        Args:
            group: Time interval for grouping ("hour", "day", "month")
            start_date: Start date for reporting period
            stop_date: End date for reporting period 
            number: Optional phone number to filter metrics by
        Returns:
            ListInboundMetricsResponse: Detailed inbound call metrics

"""

import json
from typing import Literal, Optional
from naxai.base.exceptions import NaxaiValueError
from naxai.models.voice.responses.reporting_responses import ListInboundMetricsResponse

class InboundResource:
    """
    Inbound Resource for reporting resource
    """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/inbound"
        self.headers = {"Content-Type": "application/json"}

    def list(self,
                    group: Literal["hour", "day", "month"],
                    start_date: Optional[str] = None,
                    stop_date: Optional[str] = None,
                    number: Optional[str] = None
                    ):
        """
        Retrieve a list of inbound call metrics grouped by the specified time interval.
        
        This method fetches inbound call statistics from the API, allowing filtering by date range
        and specific phone numbers. The results are grouped according to the specified time
        interval.
        
        Args:
            group (Literal["hour", "day", "month"]): The time interval for grouping the metrics.
                - "hour": Group metrics by hour (requires precise timestamp in start_date)
                - "day": Group metrics by day
                - "month": Group metrics by month
            start_date (Optional[str]): The start date for the reporting period.
                - For "hour" grouping: Format must be 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS'
                - For "day"/"month" grouping: Format must be 'YYYY-MM-DD' or 'YY-MM-DD'
                - Required for all grouping types
            stop_date (Optional[str]): The end date for the reporting period.
                - For "hour" grouping: Format must be 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS'
                - For "day"/"month" grouping: Format must be 'YYYY-MM-DD' or 'YY-MM-DD'
                - Required for "day" and "month" grouping, optional for "hour"
            number (Optional[str]): Phone number to filter the metrics by. If provided,
                only metrics for this specific number will be returned.
        
        Returns:
            ListInboundMetricsResponse: A Pydantic model containing the inbound call metrics.
            The response includes:
                - start_date: Start timestamp of the reporting period
                - stop_date: End timestamp of the reporting period
                - direction: Call direction (always "inbound" for this endpoint)
                - number: The phone number associated with these metrics
                - group: The time interval grouping used
                - stats: List of InboundStats objects with detailed metrics
        
        Raises:
            NaxaiValueError: If required parameters are missing or in incorrect format:
                - When start_date is not provided
                - When stop_date is not provided for "day" or "month" grouping
                - When date formats don't match the required format for the specified grouping
        
        Example:
            >>> metrics = client.voice.reporting.inbound.list(
            ...     group="day",
            ...     start_date="2023-01-01",
            ...     stop_date="2023-01-31",
            ...     number="+1234567890"
            ... )
            >>> print(f"Found {len(metrics.stats)} daily records")
            >>> for stat in metrics.stats:
            ...     print(f"Date: {stat.date}, Calls: {stat.calls}, Received: {stat.received}")
        """

        if group == "hour":
            if start_date is None:
                raise NaxaiValueError("startDate must be provided when group is 'hour'")

            if len(start_date) < 17 or len(start_date) > 19:
                raise NaxaiValueError("startDate must be in the format 'YYYY-MM-DD HH:MM:SS' "
                                      "or 'YY-MM-DD HH:MM:SS' when group is 'hour'")

            if stop_date is not None and (len(stop_date) < 17 or len(stop_date) > 19):
                raise NaxaiValueError("stopDate must be in the format 'YYYY-MM-DD HH:MM:SS' "
                                      "or 'YY-MM-DD HH:MM:SS' when group is 'hour'")
        else:
            if start_date is None:
                raise NaxaiValueError("startDate must be provided when group is 'day' or 'month'")

            if len(start_date) < 8 or len(start_date) > 10:
                raise NaxaiValueError("startDate must be in the format 'YYYY-MM-DD' or 'YY-MM-DD'")

            if stop_date is None:
                raise NaxaiValueError("stopDate must be provided when group is 'day' or 'month'")

            if len(stop_date) < 8 or len(stop_date) > 10:
                raise NaxaiValueError("stopDate must be in the format 'YYYY-MM-DD' or 'YY-MM-DD'")

        params = {"group": group}
        if start_date:
            params["startDate"] = start_date
        if stop_date:
            params["stopDate"] = stop_date
        if number:
            params["number"] = number
        # pylint: disable=protected-access
        return ListInboundMetricsResponse.model_validate_json(
            json.dumps(self._client._request("GET",
                                             self.root_path,
                                             params=params,
                                             headers=self.headers)))
