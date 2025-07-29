"""
Asynchronous SMS reporting resource for the Naxai SDK.

This module provides asynchronous methods for retrieving and analyzing SMS messaging metrics,
including outgoing message statistics, delivery error reports, incoming message volumes,
and country-based performance data. These reports help users understand messaging patterns,
delivery success rates, and geographical distribution of their SMS communications in a
non-blocking manner suitable for high-performance asynchronous applications.

Available Functions:
    list_outgoing_metrics(group: Literal["hour", "day", "month"], start_date: str, stop_date: str)
        Retrieves time-based metrics for outgoing SMS messages.
        Args:
            group: Time interval for grouping ("hour", "day", "month")
            start_date: Start date for reporting period
            stop_date: End date for reporting period
        Returns:
            ListOutgoingSMSMetricsResponse: Detailed outgoing SMS metrics

    list_outgoing_by_country_metrics(group: Literal["hour", "day", "month"],
                                     start_date: str,
                                     stop_date: str)
        Retrieves country-based metrics for outgoing SMS messages.
        Args:
            group: Time interval for grouping ("hour", "day", "month")
            start_date: Start date for reporting period
            stop_date: End date for reporting period
        Returns:
            ListOutgoingSMSByCountryMetricsResponse: Country-based SMS metrics

    list_incoming_metrics(group: Literal["hour", "day", "month"], start_date: str, stop_date: str)
        Retrieves metrics for incoming SMS messages.
        Args:
            group: Time interval for grouping ("hour", "day", "month")
            start_date: Start date for reporting period
            stop_date: End date for reporting period
        Returns:
            ListIncomingSMSMetricsResponse: Incoming SMS metrics

    list_delivery_error_metrics(group: Literal["hour", "day", "month"],
                                start_date: str,
                                stop_date: str)
        Retrieves metrics about SMS delivery errors.
        Args:
            group: Time interval for grouping ("hour", "day", "month")
            start_date: Start date for reporting period
            stop_date: End date for reporting period
        Returns:
            ListDeliveryErrorMetricsResponse: SMS delivery error metrics

"""

import json
from typing import Literal
from pydantic import Field
from naxai.models.sms.responses.reporting_responses import (ListDeliveryErrorMetricsResponse,
                                                            ListIncomingSMSMetricsResponse,
                                                            ListOutgoingSMSByCountryMetricsResponse,
                                                            ListOutgoingSMSMetricsResponse)
from naxai.base.exceptions import NaxaiValueError

class ReportingResource:
    """ reporting resource for sms resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/reporting/metrics"
        self.headers = {"Content-Type": "application/json"}

    async def list_outgoing_metrics(self,
                                    group: Literal["hour", "day", "month"],
                                    start_date: str = None,
                                    stop_date: str = None
                                    ):
        """
        Retrieves time-based metrics for outgoing SMS messages.
        
        This method fetches detailed statistics about outgoing SMS messages, grouped by the
        specified time interval (hour, day, or month). The metrics include message volumes,
        delivery outcomes, and timing metrics for the specified time period.
        
        Args:
            group (Literal["hour", "day", "month"]): The time interval for grouping the metrics.
                - "hour": Group metrics by hour (requires timestamp format for dates)
                - "day": Group metrics by day
                - "month": Group metrics by month
            start_date (str): The start date for the reporting period.
                - For "hour" grouping: Format must be 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS'
                - For "day"/"month" grouping: Format must be 'YYYY-MM-DD' or 'YY-MM-DD'
                - Required for all grouping types. Mapped from JSON key 'startDate'.
            stop_date (str): The end date for the reporting period.
                - For "hour" grouping: Format must be 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS'
                - For "day"/"month" grouping: Format must be 'YYYY-MM-DD' or 'YY-MM-DD'
                - Required for "day" and "month" grouping, optional for "hour".
                - Mapped from JSON key 'stopDate'.
        
        Returns:
            ListOutgoingSMSMetricsResponse: 
            A Pydantic model containing detailed outgoing SMS metrics.
            The response includes:
                - start_date: Start date of the reporting period
                - stop_date: End date of the reporting period
                - direction: Always "outgoing" for this endpoint
                - group: The time interval grouping used (hour, day, month)
                - stats: List of OutgoingStats objects with detailed metrics for each time interval
        
        Raises:
            NaxaiValueError: If required parameters are missing or in incorrect format:
                - When start_date is not provided
                - When stop_date is not provided for "day" or "month" grouping
                - When date formats don't match the required format for the specified grouping
        
        Example:
            >>> # Get daily metrics for a month
            >>> daily_metrics = await client.sms.reporting.list_outgoing_metrics(
            ...     group="day",
            ...     start_date="2023-01-01",
            ...     stop_date="2023-01-31"
            ... )
            >>> print(f"Period: {daily_metrics.start_date} to {daily_metrics.stop_date}")
            >>> print(f"Number of days: {len(daily_metrics.stats)}")
            >>> 
            >>> # Calculate overall delivery rate
            >>> total_sms = sum(day.sms for day in daily_metrics.stats)
            >>> total_delivered = sum(day.delivered for day in daily_metrics.stats)
            >>> if total_sms > 0:
            ...     delivery_rate = total_delivered / total_sms * 100
            ...     print(f"Overall delivery rate: {delivery_rate:.1f}%")
            >>> 
            >>> # Find day with highest volume
            >>> if daily_metrics.stats:
            ...     busiest_day = max(daily_metrics.stats, key=lambda day: day.sms)
            ...     print(f"Busiest day: {busiest_day.date} with {busiest_day.sms} messages")
            >>> 
            >>> # Get hourly metrics for a specific day
            >>> hourly_metrics = await client.sms.reporting.list_outgoing_metrics(
            ...     group="hour",
            ...     start_date="2023-01-15 00:00:00",
            ...     stop_date="2023-01-15 23:59:59"
            ... )
            >>> print(f"Hourly breakdown for {hourly_metrics.start_date}:")
            >>> for hour in hourly_metrics.stats:
            ...     print(f"{hour.date}: {hour.sms} messages, {hour.delivered} delivered")
        
        Note:
            - The stats list contains entries corresponding to the specified grouping level
            - For hour grouping: One entry per hour in the date range
            - For day grouping: One entry per day in the date range
            - For month grouping: One entry per month in the date range
            - The date format in each stats entry corresponds to the grouping level
            - Each stats entry includes detailed metrics such as:
            * Total SMS count
            * Delivered, failed, expired, unknown, canceled, and rejected counts
            * Average time to deliver and submit (in milliseconds)
            - These metrics provide insights into outgoing message performance over time
            - Analyzing trends can help identify optimal sending times and delivery patterns
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
        # pylint: disable=protected-access
        return ListOutgoingSMSMetricsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/outgoing",
                                                   params=params,
                                                   headers=self.headers)))

    async def list_outgoing_metrics_by_country(self,
                                               start_date: str,
                                               stop_date: str
                                               ):
        """
        Retrieves country-based metrics for outgoing SMS messages.
        
        This method fetches detailed statistics about outgoing SMS messages, grouped by
        destination country and mobile network. The metrics include message volumes,
        delivery outcomes, and timing metrics for each country.
        
        Args:
            start_date (str): The start date for the reporting period in 'YYYY-MM-DD' format.
                Must be exactly 10 characters. Mapped from JSON key 'startDate'.
            stop_date (str): The end date for the reporting period in 'YYYY-MM-DD' format.
                Must be exactly 10 characters. Mapped from JSON key 'stopDate'.
        
        Returns:
            ListOutgoingSMSByCountryMetricsResponse: A Pydantic model containing detailed
            outgoing SMS metrics grouped by country. The response includes:
                - start_date: Start date of the reporting period
                - stop_date: End date of the reporting period
                - direction: Always "outgoing" for this endpoint
                - stats: List of OutgoingCountryStats objects with detailed metrics for each country
        
        Raises:
            NaxaiValueError: If date parameters are not in the correct format 'YYYY-MM-DD'
        
        Example:
            >>> country_metrics = await client.sms.reporting.list_outgoing_metrics_by_country(
            ...     start_date="2023-01-01",
            ...     stop_date="2023-01-31"
            ... )
            >>> print(f"Period: {country_metrics.start_date} to {country_metrics.stop_date}")
            >>> print(f"Number of countries: {len(country_metrics.stats)}")
            >>> 
            >>> # Compare delivery rates by country
            >>> for country in country_metrics.stats:
            ...     if country.sms > 0:
            ...         delivery_rate = country.delivered / country.sms * 100
            ...         print(f"{country.country} ({country.mcc}-{country.mnc}): "
            ...               f"{delivery_rate:.1f}% delivery rate")
            >>> 
            >>> # Find country with highest volume
            >>> if country_metrics.stats:
            ...     top_country = max(country_metrics.stats, key=lambda c: c.sms)
            ...     print(f"Highest volume: {top_country.country} with {top_country.sms} messages")
            >>> 
            >>> # Find country with best delivery rate (minimum 100 messages)
            >>> countries_with_volume = [c for c in country_metrics.stats if c.sms >= 100]
            >>> if countries_with_volume:
            ...     best_country = max(countries_with_volume, key=lambda c: c.delivered/c.sms)
            ...     rate = best_country.delivered / best_country.sms * 100
            ...     print(f"Best delivery rate: {best_country.country} at {rate:.1f}%")
        
        Note:
            - The stats list contains one entry per country/network combination
            - Countries are typically identified by ISO 3166-1 alpha-2 codes (e.g., "US", "GB")
            - The MCC (Mobile Country Code) and MNC (Mobile Network Code) together identify
              a specific mobile network
            - Each stats entry includes detailed metrics such as:
            * Total SMS count
            * Delivered, failed, expired, unknown, canceled, and rejected counts
            * Average time to deliver and submit (in milliseconds)
            - These metrics provide insights into geographical performance differences
            - Analyzing country-specific metrics can help optimize international
              messaging strategies
        """
        if len(start_date) != 10:
            raise NaxaiValueError("startDate must be in the format 'YYYY-MM-DD'")
        if len(stop_date) != 10:
            raise NaxaiValueError("stopDate must be in the format 'YYYY-MM-DD'")

        params = {"startDate": start_date,
                  "stopDate": stop_date}
        # pylint: disable=protected-access
        return ListOutgoingSMSByCountryMetricsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/outgoing-by-country",
                                                   params=params,
                                                   headers=self.headers)))

    async def list_incoming_metrics(self,
                                    group: Literal["hour", "day", "month"],
                                    start_date: str = Field(default=None),
                                    stop_date: str = Field(default=None)
                                    ):
        """
        Retrieves time-based metrics for incoming SMS messages.
        
        This method fetches statistics about incoming SMS messages, grouped by the
        specified time interval (hour, day, or month). The metrics include message
        volumes for the specified time period.
        
        Args:
            group (Literal["hour", "day", "month"]): The time interval for grouping the metrics.
                - "hour": Group metrics by hour (requires timestamp format for dates)
                - "day": Group metrics by day
                - "month": Group metrics by month
            start_date (str): The start date for the reporting period.
                - For "hour" grouping: Format must be 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS'
                - For "day"/"month" grouping: Format must be 'YYYY-MM-DD' or 'YY-MM-DD'
            stop_date (str): The end date for the reporting period.
                - For "hour" grouping: Format must be 'YYYY-MM-DD HH:MM:SS' or 'YY-MM-DD HH:MM:SS'
                - For "day"/"month" grouping: Format must be 'YYYY-MM-DD' or 'YY-MM-DD'
                - Required for "day" and "month" grouping, optional for "hour".
        
        Returns:
            ListIncomingSMSMetricsResponse: A Pydantic model containing incoming SMS metrics.
            The response includes:
                - start_date: Start date of the reporting period
                - stop_date: End date of the reporting period
                - direction: Always "incoming" for this endpoint
                - group: The time interval grouping used (hour, day, month)
                - stats: List of IncomingStats objects with metrics for each time interval
        
        Raises:
            NaxaiValueError: If required parameters are missing or in incorrect format:
                - When start_date is not provided
                - When stop_date is not provided for "day" or "month" grouping
                - When date formats don't match the required format for the specified grouping
        
        Example:
            >>> # Get daily incoming metrics for a month
            >>> daily_metrics = await client.sms.reporting.list_incoming_metrics(
            ...     group="day",
            ...     start_date="2023-01-01",
            ...     stop_date="2023-01-31"
            ... )
            >>> print(f"Period: {daily_metrics.start_date} to {daily_metrics.stop_date}")
            >>> print(f"Number of days: {len(daily_metrics.stats)}")
            >>> 
            >>> # Calculate total incoming messages
            >>> total_incoming = sum(day.sms for day in daily_metrics.stats)
            >>> print(f"Total incoming messages: {total_incoming}")
            >>> 
            >>> # Calculate daily average
            >>> if daily_metrics.stats:
            ...     daily_avg = total_incoming / len(daily_metrics.stats)
            ...     print(f"Average daily incoming messages: {daily_avg:.1f}")
            >>> 
            >>> # Find day with highest volume
            >>> if daily_metrics.stats:
            ...     busiest_day = max(daily_metrics.stats, key=lambda day: day.sms)
            ...     print(f"Busiest day: {busiest_day.date} with "
            ...           f"{busiest_day.sms} incoming messages")
        
        Note:
            - The stats list contains entries corresponding to the specified grouping level
            - For hour grouping: One entry per hour in the date range
            - For day grouping: One entry per day in the date range
            - For month grouping: One entry per month in the date range
            - The date format in each stats entry corresponds to the grouping level
            - Incoming metrics are simpler than outgoing metrics as they only track volume
            - These metrics provide insights into incoming message patterns over time
            - Analyzing trends can help identify peak times for customer engagement
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

        params = {"group": group,
                  "startDate": start_date,
                  "stopDate": stop_date}
        # pylint: disable=protected-access
        return ListIncomingSMSMetricsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/incoming",
                                                   params=params,
                                                   headers=self.headers)))

    async def list_delivery_errors_metrics(self,
                                         start_date: str,
                                         stop_date: str
                                         ):
        """
        Retrieves metrics about SMS delivery errors.
        
        This method fetches detailed statistics about SMS delivery errors, grouped by
        error category and code. The metrics include the frequency of different error
        types during the specified time period.
        
        Args:
            start_date (str): The start date for the reporting period in 'YYYY-MM-DD' format.
                Must be exactly 10 characters. Mapped from JSON key 'startDate'.
            stop_date (str): The end date for the reporting period in 'YYYY-MM-DD' format.
                Must be exactly 10 characters. Mapped from JSON key 'stopDate'.
        
        Returns:
            ListDeliveryErrorMetricsResponse: 
            A Pydantic model containing SMS delivery error metrics.
            The response includes:
                - start_date: Start date of the reporting period
                - stop_date: End date of the reporting period
                - stats: List of DeliveryErrorStats objects with metrics for each error type
        
        Raises:
            NaxaiValueError: If date parameters are not in the correct format 'YYYY-MM-DD'
        
        Example:
            >>> error_metrics = await client.sms.reporting.list_delivery_errors_metrics(
            ...     start_date="2023-01-01",
            ...     stop_date="2023-01-31"
            ... )
            >>> print(f"Period: {error_metrics.start_date} to {error_metrics.stop_date}")
            >>> print(f"Number of error types: {len(error_metrics.stats)}")
            >>> 
            >>> # Calculate total errors
            >>> total_errors = sum(error.sms for error in error_metrics.stats)
            >>> print(f"Total errors: {total_errors}")
            >>> 
            >>> # Group errors by category
            >>> by_category = {}
            >>> for error in error_metrics.stats:
            ...     category = error.status_category
            ...     if category not in by_category:
            ...         by_category[category] = 0
            ...     by_category[category] += error.sms
            >>> 
            >>> # Show error distribution by category
            >>> for category, count in by_category.items():
            ...     percentage = count / total_errors * 100 if total_errors > 0 else 0
            ...     print(f"{category}: {count} errors ({percentage:.1f}%)")
            >>> 
            >>> # Find most common error
            >>> if error_metrics.stats:
            ...     most_common = max(error_metrics.stats, key=lambda error: error.sms)
            ...     print(f"Most common error: {most_common.status_code} "
            ...           f"({most_common.status_category})")
            ...     print(f"Occurrences: {most_common.sms}")
        
        Note:
            - The stats list contains one entry per unique error category and code combination
            - Error categories typically include "carrier", "handset", "network", etc.
            - Error codes provide specific information about what went wrong
            - These metrics help identify common delivery issues and their relative frequency
            - Analyzing error patterns can guide improvements to message delivery strategies
            - High rates of specific errors may indicate issues that need addressing
        """
        if len(start_date) != 10:
            raise NaxaiValueError("startDate must be in the format 'YYYY-MM-DD'")
        if len(stop_date) != 10:
            raise NaxaiValueError("stopDate must be in the format 'YYYY-MM-DD'")

        params = {"startDate": start_date,
                  "stopDate": stop_date}
        # pylint: disable=protected-access
        return ListDeliveryErrorMetricsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/delivery-errors",
                                                   params=params,
                                                   headers=self.headers)))
