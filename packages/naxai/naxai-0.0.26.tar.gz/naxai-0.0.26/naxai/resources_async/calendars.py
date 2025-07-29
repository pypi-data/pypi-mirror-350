"""
Asynchronous calendars resource for the Naxai SDK.

This module provides asynchronous methods for managing calendars in the Naxai platform,
including creating, retrieving, updating, and checking calendars with their working hours,
schedules, and exclusion dates. Calendars can be used to define business hours, holidays,
and other time-based constraints for various Naxai services such as voice calls and other
scheduled operations, all in a non-blocking manner suitable for high-performance
asynchronous applications.

Available functions:
    check(calendar_id, timestamp) -> CheckCalendarResponse
        Checks calendar availability at a specific time.
        Returns whether timestamp is within working hours and next available time if not.

    create(calendar_id, name, schedule, exclusions) -> CreateCalendarResponse
        Creates a new calendar with specified working hours and exclusions.

    update(calendar_id, name, schedule) -> UpdateCalendarResponse
        Updates an existing calendar's name and/or schedule.

    get(calendar_id) -> GetCalendarResponse
        Retrieves details of a specific calendar.

    list() -> ListCalendarsResponse
        Lists all available calendars.

    delete(calendar_id) -> None
        Deletes a calendar by its ID.

    add_exclusions(calendar_id, exclusions) -> AddExclusionsResponse
        Adds exclusion dates to a calendar.

    delete_exclusions(calendar_id, exclusions) -> DeleteExclusionsResponse
        Removes exclusion dates from a calendar.

Sub-resources:
    holidays_templates
        Provides access to holiday templates that can be used with calendars.
        See HolidaysTemplatesResource for detailed documentation.

"""

import datetime
import json
from typing import Optional
from naxai.base.exceptions import NaxaiValueError
from naxai.models.calendars.responses.calendars_responses import (CreateCalendarResponse,
                                                                  AddExclusionsResponse,
                                                                  CheckCalendarResponse,
                                                                  UpdateCalendarResponse,
                                                                  GetCalendarResponse,
                                                                  ListCalendarsResponse,
                                                                  DeleteExclusionsResponse)
from naxai.models.calendars.requests.calendar_requests import CreateCalendarRequest
from .calendars_resources.holidays_templates import HolidaysTemplatesResource

class CalendarsResource:
    """
    Provides access to calendars related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.root_path = "/calendars"
        self.holidays_templates: HolidaysTemplatesResource = HolidaysTemplatesResource(
            self._client,
            self.root_path)
        self.headers = {"Content-Type": "application/json"}

    async def check(self,
                    calendar_id: str,
                    timestamp: Optional[int] = datetime.datetime.now(tz=datetime.timezone.utc),
                    ):
        """Checks the availability of a calendar at a specific time.

        This method verifies whether a given timestamp falls within the calendar's working hours,
        considering the schedule and exclusions. If the time is outside working hours, it also
        provides the next available time.

        Args:
            calendar_id (str): The unique identifier of the calendar to check.
            timestamp (Optional[int]): The timestamp to check for availability.
                Defaults to the current UTC timestamp if not provided.

        Returns:
            CheckCalendarResponse: An object containing:
                - match_ (bool): Whether the timestamp falls within working hours.
                Mapped from JSON key 'match'.
                - next_ (Optional[int]): If match_ is False, provides the timestamp
                of the next available working time. Mapped from JSON key 'next'.

        Raises:
            APIError: If there is an error response from the API.
            ValidationError: If the response data cannot be properly validated.
            NotFoundError: If the calendar with the specified ID doesn't exist.
            ConnectionError: If there are network connectivity issues.

        Example:
            >>> # Check current time
            >>> response = await client.calendars.check("cal_123abc")
            >>> if response.match_:
            ...     print("Time is within working hours")
            ... else:
            ...     print(f"Next available time: {response.next_}")
            >>>
            >>> # Check specific timestamp
            >>> specific_time = 1703066400000  # Some future timestamp
            >>> response = await client.calendars.check(
            ...     "cal_123abc",
            ...     timestamp=specific_time
            ... )

        Note:
            - The request is made with "Content-Type: application/json" header
            - Timestamps are represented in milliseconds since epoch
            - The check considers both regular and extended hours if configured
            - Exclusion dates are taken into account during availability checking
            - The default timestamp is the current UTC time

        See Also:
            Calendar: The main calendar model class
            CheckCalendarResponse: The response model for availability checks
        """
        params = {"timestamp": timestamp}
        # pylint: disable=protected-access
        return CheckCalendarResponse.model_validate_json(
            json.dumps(
                await self._client._request("GET",
                                            self.root_path + "/" + calendar_id + "/check",
                                            params=params,
                                            headers=self.headers)))

    async def delete_exclusions(self, calendar_id: str, exclusions: list[str]):
        """Deletes exclusion dates from a calendar.

        This method removes specified dates from the calendar's exclusion list. These dates
        will no longer be considered as non-working days in the calendar.

        Args:
            calendar_id (str): The unique identifier of the calendar to update.
            exclusions (list[str]): List of dates to remove from the calendar's exclusions.
                Each date should be in a "YYYY-MM-DD" string format. Maximum of 1000 dates
                can be removed in a single request.

        Returns:
            DeleteExclusionsResponse: An object containing:
                - exclusions (list[str]): The complete list of remaining exclusions for 
                the calendar after removing the specified dates.

        Raises:
            APIError: If there is an error response from the API.
            ValidationError: If the request data or response cannot be properly validated.
            NotFoundError: If the calendar with the specified ID doesn't exist.
            NaxaiValueError: If more than 1000 exclusions are provided.

        Example:
            >>> dates_to_remove = ["2024-12-25", "2024-12-26"]
            >>> result = await client.calendars.delete_exclusions(
            ...     "cal_123abc",
            ...     exclusions=dates_to_remove
            ... )
            >>> print(result.exclusions)  # Shows remaining exclusions after deletion

        Note:
            - The request is made with "Content-Type: application/json" header
            - Maximum of 1000 exclusions can be deleted in a single request
            - Non-existent dates in the exclusion list are ignored
            - The response includes all remaining exclusions after the deletion

        See Also:
            Calendar: The main calendar model class
            ExclusionResponse: The response model containing updated exclusions list
            add_exclusions: Method to add exclusion dates to a calendar
        """
        if len(exclusions) > 1000:
            raise NaxaiValueError("You can only delete up to 1000 exclusions at a time.")

        url = self.root_path + "/" + calendar_id + "/exclusions/remove"
        # pylint: disable=protected-access
        return DeleteExclusionsResponse.model_validate_json(
            json.dumps(await self._client._request("POST",
                                                   url,
                                                   json={"exclusions": exclusions},
                                                   headers=self.headers)))

    async def add_exclusions(self, calendar_id: str, exclusions: list[str]):
        """Adds new exclusion dates to an existing calendar.

        This method allows adding dates to the calendar's exclusion list. These dates
        will be considered as non-working days in the calendar.

        Args:
            calendar_id (str): The unique identifier of the calendar to update.
            exclusions (list[str]): List of dates to be added as exclusions.
                Each date should be in a YYYY-MM-DD string format. Maximum of 1000 dates
                can be added in a single request.

        Returns:
            AddExclusionsResponse: An object containing:
                - exclusions (list[str]): The complete list of exclusions for the calendar
                after adding the new dates.

        Raises:
            APIError: If there is an error response from the API.
            ValidationError: If the request data or response cannot be properly validated.
            NotFoundError: If the calendar with the specified ID doesn't exist.
            ValueError: If more than 1000 exclusions are provided.

        Example:
            >>> new_exclusions = ["2024-12-25", "2024-12-26"]
            >>> result = await client.calendars.add_exclusions(
            ...     "cal_123abc",
            ...     exclusions=new_exclusions
            ... )
            >>> print(result.exclusions)  # Shows all exclusions including the new ones

        Note:
            - The request is made with "Content-Type: application/json" header
            - Maximum of 1000 exclusions can be added in a single request
            - Existing exclusions are preserved and new ones are added to the list

        See Also:
            Calendar: The main calendar model class
            ExclusionResponse: The response model containing updated exclusions list
        """
        if len(exclusions) > 1000:
            raise NaxaiValueError("You can only add up to 1000 exclusions at a time.")

        url = self.root_path + "/" + calendar_id + "/exclusions/add"
        # pylint: disable=protected-access
        return AddExclusionsResponse.model_validate_json(
            json.dumps(await self._client._request("POST",
                                                   url,
                                                   json={"exclusions": exclusions},
                                                   headers=self.headers)))

    async def delete(self, calendar_id):
        """
        Deletes a calendar by its ID.

        Args:
            calendar_id (str): The ID of the calendar to delete.

        Returns:
            None

        Raises:
            APIError: If there is an error response from the API.
            NotFoundError: If the calendar with the specified ID doesn't exist.

        Example:
            >>> response = await client.calendars.delete("calendar_id")
        """
        # pylint: disable=protected-access
        return await self._client._request("DELETE",
                                           self.root_path + "/" + calendar_id,
                                           headers=self.headers)


    async def update(self, calendar_id: str, data: CreateCalendarRequest):
        """Updates an existing calendar with new configuration.

        This method modifies an existing calendar's settings using the provided
        configuration data.

        Args:
            calendar_id (str): The unique identifier of the calendar to update.
            data (CreateCalendarRequest): The request body containing the updated calendar
                configuration with the following fields:
                - name (str): The new name for the calendar
                - timezone (Optional[str]): The timezone setting for the calendar
                - schedule (list[ScheduleObject]): List of exactly 7 schedule objects containing:
                    - day (int): Day of week (1-7)
                    - open (bool): Whether the schedule is open
                    - start (Optional[str]): Opening time in "HH:MM" format
                    - stop (Optional[str]): Closing time in "HH:MM" format
                    - extended (Optional[bool]): Whether extended hours are enabled
                    - extension_start (Optional[str]): Extended hours start time
                    - extension_stop (Optional[str]): Extended hours end time
                - exclusions (Optional[list[str]]): List of dates to exclude

        Returns:
            UpdateCalendarResponse: The updated calendar object containing all calendar properties
                including the modifications made.

        Raises:
            APIError: If there is an error response from the API.
            ValidationError: If the request data or response cannot be properly validated.
            NotFoundError: If the calendar with the specified ID doesn't exist.

        Example:
            >>> update_data = CreateCalendarRequest(
            ...     name="Updated Calendar Name",
            ...     timezone="Europe/London",
            ...     schedule=[
            ...         ScheduleObject(
            ...             day=1,
            ...             open=True,
            ...             start="09:00",
            ...             stop="17:00"
            ...         ),
            ...         # ... repeat for all 7 days
            ...     ]
            ... )
            >>> updated_calendar = await client.calendars.update("cal_123abc", update_data)
            >>> print(updated_calendar.name)  # "Updated Calendar Name"

        Note:
            - The request is made with "Content-Type: application/json" header
            - The request body is automatically serialized using model_dump
            - None values are excluded from the request
            - Schedule must contain exactly 7 ScheduleObject instances
            - Time values must follow the "HH:MM" format

        See Also:
            Calendar: The model class for calendar data
            ScheduleObject: The model class for daily schedule configuration
            CreateCalendarRequest: The model class for update request data
        """
        # pylint: disable=protected-access
        return UpdateCalendarResponse.model_validate_json(
            json.dumps(await self._client._request("PUT",
                                                   self.root_path + "/" + calendar_id,
                                                   json=data.model_dump(by_alias=True,
                                                                        exclude_none=True),
                                                   headers=self.headers)))

    async def get(self, calendar_id: str):
        """Retrieves a specific calendar by its ID.

        This method fetches detailed information about a single calendar using its
        unique identifier and returns it as a Calendar object.

        Args:
            calendar_id (str): The unique identifier of the calendar to retrieve.

        Returns:
            GetCalendarResponse: An object containing the calendar's details including:
                - id (Optional[str]): The calendar's unique identifier
                - name (str): The calendar's name
                - timezone (Optional[str]): The calendar's timezone
                - schedule (list[ScheduleObject]): List of 7 schedule objects containing:
                    - day (int): Day of week (1-7)
                    - open (bool): Whether the schedule is open
                    - start (Optional[str]): Opening time in "HH:MM" format
                    - stop (Optional[str]): Closing time in "HH:MM" format
                    - extended (Optional[bool]): Whether extended hours are enabled
                    - extension_start (Optional[str]): Extended hours start time
                    - extension_stop (Optional[str]): Extended hours end time
                - exclusions (Optional[list[str]]): List of excluded dates

        Raises:
            APIError: If there is an error response from the API.
            ValidationError: 
                If the response data cannot be properly validated into a Calendar object.
            NotFoundError: If the calendar with the specified ID doesn't exist.

        Example:
            >>> calendar = await client.calendars.get("cal_123abc")
            >>> print(calendar.name)
            >>> print(calendar.timezone)
            >>> for day_schedule in calendar.schedule:
            ...     print(f"Day {day_schedule.day}: "
            ...           f"{'Open' if day_schedule.open else 'Closed'} "
            ...           f"from {day_schedule.start} to {day_schedule.stop}")

        Note:
            - The request is made with "Content-Type: application/json" header
            - The response is automatically validated and converted to a Calendar object
            - Schedule must contain exactly 7 ScheduleObject instances
            - Time values must follow the "HH:MM" format
            - The endpoint used is "{root_path}/calendars/{calendar_id}"

        See Also:
            Calendar: The model class for calendar data
            ScheduleObject: The model class for daily schedule configuration
        """
        # pylint: disable=protected-access
        return GetCalendarResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/" + calendar_id,
                                                   headers=self.headers)))

    async def list(self):
        """Retrieve a list of all calendars.

        This method fetches all calendars associated with the account and returns them
        as a list of Calendar objects.

        Returns:
            ListCalendarsResponse: A list of Calendar objects, each representing a calendar
                with its properties and settings. If no calendars exist, returns an
                empty list.

        Raises:
            APIError: If there is an error response from the API.
            ValidationError: 
                If the response data cannot be properly validated into Calendar objects.

        Example:
            >>> calendars = await client.calendars.list()
            >>> for calendar in calendars:
            ...     print(calendar.name)

        Note:
            - The request is made with "Content-Type: application/json" header
            - The response is automatically converted from JSON to Calendar objects
            - This method performs model validation on the response data

        See Also:
            Calendar: The model class used for representing calendar data
        """
        # pylint: disable=protected-access
        return ListCalendarsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path,
                                                   headers=self.headers)))

    async def create(self,
                     data: CreateCalendarRequest):
        """
        Creates a new calendar.

        Args:
            data (CreateCalendarRequest): 
                The request body containing the details of the calendar to be created.

        Returns:
            Calendar: The created calendar with its properties and settings

        Example:
            >>> new_calendar = await client.calendars.create(
            ...     CreateCalendarRequest(
            ...         name="My Calender",
            ...         ...
            ...     )
            ... )
        """
        # pylint: disable=protected-access
        return CreateCalendarResponse.model_validate_json(
            json.dumps(await self._client._request("POST",
                                                   self.root_path,
                                                   json=data.model_dump(by_alias=True,
                                                                        exclude_none=True),
                                                   headers=self.headers)))
