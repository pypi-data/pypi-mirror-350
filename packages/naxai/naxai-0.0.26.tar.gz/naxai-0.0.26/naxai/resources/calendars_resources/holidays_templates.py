"""
Holiday templates resource for the Naxai SDK.

This module provides methods for interacting with holiday templates in the Naxai API,
including retrieving individual templates and listing all available templates.
Holiday templates contain predefined sets of dates that can be used with calendars.

Available functions:
    get(template_id: str)
        Retrieves a specific holiday template by its ID.
        Returns a GetHolidaysTemplateResponse object containing template details.

    list()
        Lists all available holiday templates.
        Returns a ListHolidaysTemplatesResponse object containing multiple templates.

"""

import json
from naxai.models.calendars.responses.holidays_template_responses import (
    ListHolidaysTemplatesResponse,
    GetHolidaysTemplateResponse)

class HolidaysTemplatesResource:
    """ holidays_template resource for calendars resource"""

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/holidays"
        self.headers = {"Content-Type": "application/json"}

    def get(self, template_id: str):
        """Retrieves a specific holiday template by its ID.

        This method fetches detailed information about a single holiday template,
        including its name and associated dates.

        Args:
            template_id (str): The unique identifier of the holiday template to retrieve.

        Returns:
            GetHolidaysTemplateResponse: An object containing the template's details:
                - id (str): The template's unique identifier
                - name (str): The template's name (max 60 characters)
                - dates (list[str]): List of dates included in this template

        Raises:
            APIError: If there is an error response from the API.
            ValidationError: If the response data cannot be properly validated into
                a HolidayTemplate object.
            NotFoundError: If the template with the specified ID doesn't exist.

        Example:
            >>> template = client.calendars.holidays_templates.get("ht_123abc")
            >>> print(template.name)
            'US Federal Holidays 2024'
            >>> for date in template.dates:
            ...     print(date)
            '2024-01-01'
            '2024-01-15'
            '2024-02-19'

        Note:
            - The request is made with "Content-Type: application/json" header
            - The response is automatically validated and converted to a HolidayTemplate object
            - Dates in the response are in string format

        See Also:
            HolidayTemplate: The model class for holiday template data
            list: Method to retrieve all holiday templates
        """
        # pylint: disable=protected-access
        return GetHolidaysTemplateResponse.model_validate_json(
             json.dumps(self._client._request("GET",
                                              self.root_path + "/" + template_id,
                                              headers=self.headers)))

    def list(self):
        """Retrieves a list of all available holiday templates.

        This method fetches all holiday templates accessible to the authenticated user,
        including their IDs, names, and associated dates.

        Returns:
            ListHolidaysTemplatesResponse: A list of holiday template objects, each containing:
                - id (str): The template's unique identifier
                - name (str): The template's name (max 60 characters)
                - dates (list[str]): List of dates included in this template

        Raises:
            APIError: If there is an error response from the API.
            ValidationError: If the response data cannot be properly validated into
                HolidayTemplate objects.

        Example:
            >>> templates = client.calendars.holidays_templates.list()
            >>> for template in templates:
            ...     print(f"Template: {template.name}")
            ...     print(f"Number of holidays: {len(template.dates)}")
            Template: US Federal Holidays 2024
            Number of holidays: 11
            Template: UK Bank Holidays 2024
            Number of holidays: 8

        Note:
            - The request is made with "Content-Type: application/json" header
            - Each template in the response is validated and converted to a HolidayTemplate object
            - Dates in the response are in string format
            - The response is automatically paginated if supported by the API

        See Also:
            HolidayTemplate: The model class for holiday template data
            get: Method to retrieve a specific holiday template
        """
        # pylint: disable=protected-access
        return ListHolidaysTemplatesResponse.model_validate_json(
             json.dumps(self._client._request("GET",
                                              self.root_path,
                                              headers=self.headers)))
