"""
Asynchronous voice outbound reporting resource for the Naxai SDK.

This module provides asynchronous methods for retrieving and analyzing metrics related to
outbound voice calls, including call volumes, delivery rates, and geographical distribution.
These reports can be grouped by different time intervals or by country, and filtered by
specific phone numbers to help users understand outbound call performance and optimize
their voice communication strategies in a non-blocking manner suitable for high-performance
asynchronous applications.

Available Functions:
    list(group: Literal["hour", "day", "month"], start_date: str, stop_date: str, number: str)
        Retrieves outbound call metrics grouped by time interval.
        Args:
            group: Time interval for grouping ("hour", "day", "month")
            start_date: Start date for reporting period
            stop_date: End date for reporting period
            number: Optional phone number to filter metrics by
        Returns:
            ListOutboundMetricsResponse: Detailed outbound call metrics

    list_by_country(start_date: str, stop_date: str, number: str)
        Retrieves outbound call metrics grouped by country.
        Args:
            start_date: Start date for reporting period
            stop_date: End date for reporting period
            number: Optional phone number to filter metrics by
        Returns:
            ListOutboundCallsByCountryMetricsResponse: Country-wise outbound call metrics

"""

import json
from typing import Optional, Literal
from naxai.base.exceptions import NaxaiValueError
from naxai.models.voice.responses.reporting_responses import (
    ListOutboundMetricsResponse,
    ListOutboundCallsByCountryMetricsResponse)

class OutboundResource:
    """
    Outbound Resource for reporting resource
    """

    def __init__(self, client, root_path):
        self._client = client
        self.previous_path = root_path
        self.root_path = root_path + "/outbound"
        self.headers = {"Content-Type": "application/json"}

    async def list(self,
             group: Literal["hour", "day", "month"],
             start_date: Optional[str] = None,
             stop_date: Optional[str] = None,
             number: Optional[str] = None
             ):
        """
        Retrieve a list of outbound call metrics grouped by the specified time interval.
        
        This method fetches outbound call statistics from the API, allowing filtering by date range
        and specific phone numbers. The results are grouped according to the specified 
        time interval.
        
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
            ListOutboundMetricsResponse: A Pydantic model containing the outbound call metrics.
            The response includes:
                - start_date: Start timestamp of the reporting period
                - stop_date: End timestamp of the reporting period
                - direction: Call direction (always "outbound" for this endpoint)
                - number: The phone number associated with these metrics
                - group: The time interval grouping used
                - stats: List of BaseStats objects with detailed metrics including delivery status
        
        Raises:
            NaxaiValueError: If required parameters are missing or in incorrect format:
                - When start_date is not provided
                - When stop_date is not provided for "day" or "month" grouping
                - When date formats don't match the required format for the specified grouping
        
        Example:
            >>> metrics = await client.voice.reporting.outbound.list(
            ...     group="day",
            ...     start_date="2023-01-01",
            ...     stop_date="2023-01-31",
            ...     number="+1234567890"
            ... )
            >>> print(f"Found {len(metrics.stats)} daily records")
            >>> for stat in metrics.stats:
            ...     print(f"Date: {stat.date}, Calls: {stat.calls}, Delivered: {stat.delivered}")
            ...     print(f"Success rate: "
            ...          f"{stat.delivered/stat.calls*100:.1f}% if stat.calls > 0 else 'N/A'")
        """
        if group == "hour":
            if start_date is None:
                raise NaxaiValueError("startDate must be provided when group is 'hour'")

            if len(start_date) < 17 or len(start_date) > 19:
                raise NaxaiValueError("startDate must be in the format 'YYYY-MM-DD HH:MM:SS' or "
                                      "'YY-MM-DD HH:MM:SS' when group is 'hour'")

            if stop_date is not None and (len(stop_date) < 17 or len(stop_date) > 19):
                raise NaxaiValueError("stopDate must be in the format 'YYYY-MM-DD HH:MM:SS' or "
                                      "'YY-MM-DD HH:MM:SS' when group is 'hour'")
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
        return ListOutboundMetricsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path,
                                                   params=params,
                                                   headers=self.headers)))

    async def list_by_country(self,
                              start_date: str,
                              stop_date: str,
                              number: Optional[str] = None
                              ):
        """
        Retrieve outbound call metrics grouped by country.
        
        This method fetches outbound call statistics organized by country from the API,
        allowing filtering by date range and specific phone numbers.
        
        Args:
            start_date (str): The start date for the reporting period in 'YYYY-MM-DD' format.
                Must be exactly 10 characters.
            stop_date (str): The end date for the reporting period in 'YYYY-MM-DD' format.
                Must be exactly 10 characters.
            number (Optional[str]): Phone number to filter the metrics by. If provided,
                only metrics for this specific number will be returned.
        
        Returns:
            ListOutboundCallsByCountryMetricsResponse: 
            A Pydantic model containing the outbound call metrics by country.
            The response includes:
                - start_date: Start timestamp of the reporting period
                - stop_date: End timestamp of the reporting period
                - direction: Call direction (always "outbound" for this endpoint)
                - number: The phone number associated with these metrics
                - stats: List of CountryStats objects with detailed metrics for each country
        
        Raises:
            NaxaiValueError: If date parameters are not in the correct format 'YYYY-MM-DD'
        
        Example:
            >>> country_metrics = await client.voice.reporting.outbound.list_by_country(
            ...     start_date="2023-01-01",
            ...     stop_date="2023-01-31",
            ...     number="+1234567890"
            ... )
            >>> print(f"Found metrics for {len(country_metrics.stats)} countries")
            >>> for stat in country_metrics.stats:
            ...     print(f"Country: {stat.country}, Calls: {stat.calls}, "
            ...           f"Delivered: {stat.delivered}")
        """
        if len(start_date) != 10:
            raise NaxaiValueError("startDate must be in the format 'YYYY-MM-DD'")
        if len(stop_date) != 10:
            raise NaxaiValueError("stopDate must be in the format 'YYYY-MM-DD'")

        params = {"startDate": start_date,
                  "stopDate": stop_date}

        if number:
            params["number"] = number
        # pylint: disable=protected-access
        return ListOutboundCallsByCountryMetricsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.previous_path + "/outbound-by-country",
                                                   params=params,
                                                   headers=self.headers)))
