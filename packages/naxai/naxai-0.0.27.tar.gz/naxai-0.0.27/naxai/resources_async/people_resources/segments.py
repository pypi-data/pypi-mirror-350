"""
Asynchronous contact segments resource for the Naxai People SDK.

This module provides asynchronous methods for managing contact segments in the Naxai platform,
including creating, retrieving, updating, and analyzing segments of contacts based on
various criteria. It supports both manual segments (explicitly defined members) and
dynamic segments (rule-based membership), and provides tools for tracking segment
membership changes over time in high-performance asynchronous applications.

Available Functions:
    list(type_: Optional[str], exclude_predefined: Optional[bool], attribute: Optional[str])
        List segments with optional filtering.
        Args:
            type_ (Optional[str]): Filter by segment type ("manual" or "dynamic")
            exclude_predefined (Optional[bool]): Whether to exclude predefined segments
            attribute (Optional[str]): Filter by segments using this attribute
        Returns:
            ListSegmentsResponse: List of segments matching the filters

    get(segment_id: str)
        Retrieve details of a specific segment.
        Args:
            segment_id (str): ID of the segment to retrieve
        Returns:
            GetSegmentResponse: Details of the requested segment

    create(segment_data: CreateSegmentRequest)
        Create a new segment.
        Args:
            segment_data (CreateSegmentRequest): Data for creating the segment
        Returns:
            CreateSegmentResponse: Details of the created segment

    update(segment_id: str, segment_data: dict)
        Update an existing segment.
        Args:
            segment_id (str): ID of the segment to update
            segment_data (dict): Updated segment data
        Returns:
            UpdateSegmentResponse: Details of the updated segment
    
    delete(segment_id: str)
        Delete a segment from the Naxai People API.
        Permanently removes the segment (but not its contacts).
        Args:
            segment_id (str): The unique identifier of the segment to delete.
        Returns:
            None

    get_history(segment_id: str, start_date: datetime, end_date: datetime)
        Get historical data for a segment.
        Args:
            segment_id (str): ID of the segment
            start_date (datetime): Start of the date range
            end_date (datetime): End of the date range
        Returns:
            GetSegmentsHistoryResponse: Historical data for the segment

    get_usage(segment_id: str)
        Get usage statistics for a segment.
        Args:
            segment_id (str): ID of the segment
        Returns:
            GetSegmentUsageResponse: Usage statistics for the segment

Sub-resources:
    contacts: Methods for managing contacts within segments

"""

import datetime
import json
from typing import Optional
from pydantic import Field, validate_call
from naxai.models.people.requests.segments_requests import CreateSegmentRequest
from naxai.models.people.responses.segments_responses import (ListSegmentsResponse,
                                                              GetSegmentResponse,
                                                              UpdateSegmentResponse,
                                                              CreateSegmentResponse,
                                                              GetSegmentsHistoryResponse,
                                                              GetSegmentUsageResponse)
from .segments_resources.contacts import SegmentsContactsResource

class SegmentsResource:
    """ segments resource for people resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/segments"
        self.headers = {"Content-Type": "application/json"}
        self.contacts = SegmentsContactsResource(client, self.root_path)

    @validate_call
    async def list(self,
                   type_: Optional[str] = Field(default=None),
                   exclude_predefined: Optional[bool] = False,
                   attribute: Optional[str] = None ):
        """
        Retrieve a list of segments from the Naxai People API.
        
        This method fetches all segments in your account, with options to filter by type,
        exclude predefined segments, or filter by segments that use a specific attribute.
        
        Args:
            type_ (Optional[str]): Filter segments by type. Valid values are "manual" or "dynamic".
                Defaults to None (no filtering by type).
            exclude_predefined (Optional[bool]): Whether to exclude predefined system segments.
                Defaults to False (include predefined segments).
            attribute (Optional[str]): 
                Filter segments that use the specified attribute in their conditions.
                Defaults to None (no filtering by attribute).
        
        Returns:
            ListSegmentsResponse: A response object containing the list of segments.
                The response behaves like a list and can be iterated over.
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access segments.
        
        Example:
            ```python
            async with NaxaiAsyncClient(api_client_id="your_id",
                                        api_client_secret="your_secret") as client:
                try:
                    # List all segments
                    all_segments = await client.people.segments.list()
                    print(f"Found {len(all_segments)} total segments")
                    
                    # List only dynamic segments
                    dynamic_segments = await client.people.segments.list(type_="dynamic")
                    print(f"Found {len(dynamic_segments)} dynamic segments")
                    
                    # List only manual segments, excluding predefined ones
                    manual_segments = await client.people.segments.list(
                        type_="manual",
                        exclude_predefined=True
                    )
                    print(f"Found {len(manual_segments)} custom manual segments")
                    
                    # List segments that use a specific attribute
                    attribute_segments = await client.people.segments.list(attribute="country")
                    print(f"Found {len(attribute_segments)} segments using the 'country' attribute")
                    
                    # Display segment details
                    print("\nSegment details:")
                    for segment in all_segments:
                        segment_type = "Manual" if segment.type_ == "manual" else "Dynamic"
                        predefined = "Predefined" if segment.predefined else "Custom"
                        print(f"- {segment.name} (ID: {segment.id}, "
                              f"Type: {segment_type}, {predefined})")
                        if segment.description:
                            print(f"  Description: {segment.description}")
                    
                except Exception as e:
                    print(f"Error listing segments: {str(e)}")
            ```
        
        Note:
            - The response is list-like and supports operations like len(), indexing, and iteration
            - Predefined segments are system-generated segments that cannot be modified or deleted
            - Manual segments have explicitly defined members that you add/remove manually
            - Dynamic segments have members determined by conditions and are updated automatically
            - Filtering by attribute is useful for understanding which segments might be affected
            if you modify or delete an attribute
        """
        params = {"exclude-predefined": exclude_predefined}
        if type_:
            params["type"] = type_
        if attribute:
            params["attribute"] = attribute
        # pylint: disable=protected-access
        return ListSegmentsResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path,
                                                   headers=self.headers,
                                                   params=params)))

    async def get(self, segment_id: str):
        """
        Retrieve detailed information about a specific segment in the Naxai People API.
        
        This method fetches complete information about a single segment, including its
        name, description, type, and conditions (for dynamic segments).
        
        Args:
            segment_id (str): The unique identifier of the segment to retrieve.
        
        Returns:
            GetSegmentResponse: A response object containing detailed information about the segment.
        
        Raises:
            ValueError: If segment_id is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access segment information.
            NaxaiResourceNotFound: If the specified segment does not exist.
        
        Example:
            ```python
            async with NaxaiAsyncClient(api_client_id="your_id",
                                        api_client_secret="your_secret") as client:
                try:
                    # Retrieve a specific segment
                    segment_id = "seg_123abc"
                    segment = await client.people.segments.get(segment_id=segment_id)
                    
                    # Display basic segment information
                    segment_type = "Manual" if segment.type_ == "manual" else "Dynamic"
                    predefined = "Predefined" if segment.predefined else "Custom"
                    print(f"Segment: {segment.name} (ID: {segment.id})")
                    print(f"Type: {segment_type}, {predefined}")
                    
                    if segment.description:
                        print(f"Description: {segment.description}")
                        
                    if segment.modified_at:
                        # Convert timestamp to readable date
                        from datetime import datetime
                        modified_date = datetime.fromtimestamp(segment.modified_at / 1000)
                        print(f"Last modified: {modified_date.strftime('%Y-%m-%d %H:%M:%S')}")
                        print(f"Modified by: {segment.modified_by}")
                    
                    # For dynamic segments, examine the conditions
                    if segment.type_ == "dynamic" and segment.condition:
                        print("\nSegment conditions:")
                        
                        # This is a simplified example - in reality, you would need more
                        # complex logic to parse and display the condition structure
                        if hasattr(segment.condition, "all") and segment.condition.all:
                            print("All of these conditions must be met:")
                            for cond in segment.condition.all:
                                print(f"- {cond}")
                        
                        if hasattr(segment.condition, "any") and segment.condition.any:
                            print("Any of these conditions must be met:")
                            for cond in segment.condition.any:
                                print(f"- {cond}")
                    
                    # Get the number of contacts in this segment
                    count_response = (
                    await client.people.segments.contacts.count(segment_id=segment_id))
                    print(f"\nThis segment contains {count_response.count} contacts")
                    
                except Exception as e:
                    print(f"Error retrieving segment: {str(e)}")
            ```
        
        Note:
            - This method returns complete segment information including conditions
              for dynamic segments
            - For predefined segments, some fields may be read-only
            - To get the contacts in the segment, use the segments.contacts.list method
            - To get the count of contacts in the segment, use the segments.contacts.count method
            - The condition structure for dynamic segments can be complex and may require
            custom parsing logic to display or analyze
        """
        # pylint: disable=protected-access
        return GetSegmentResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/" + segment_id,
                                                   headers=self.headers)))

    async def delete(self, segment_id: str):
        """
        Delete a segment from the Naxai People API.
        
        This method permanently removes a segment from your account. Once deleted,
        the segment cannot be recovered. This operation does not delete the contacts
        in the segment, only the segment itself.
        
        Args:
            segment_id (str): The unique identifier of the segment to delete.
        
        Returns:
            None
        
        Raises:
            ValueError: If segment_id is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to delete segments.
            NaxaiResourceNotFound: If the specified segment does not exist.
            NaxaiInvalidRequestError: If the segment cannot be deleted (e.g., predefined segments).
        
        Example:
            ```python
            async with NaxaiAsyncClient(api_client_id="your_id",
                                        api_client_secret="your_secret") as client:
                try:
                    # Check if the segment is in use before deleting
                    segment_id = "seg_123abc"
                    
                    # Get segment details
                    segment = await client.people.segments.get(segment_id=segment_id)
                    print(f"Found segment: {segment.name} (ID: {segment.id})")
                    
                    # Check if the segment is predefined (cannot be deleted)
                    if segment.predefined:
                        print("Cannot delete predefined segments")
                    else:
                        # Check if the segment is used in campaigns or broadcasts
                        usage = await client.people.segments.usage(segment_id=segment_id)
                        
                        if usage.campaign_ids or usage.broadcast_ids:
                            print("Warning: This segment is in use:")
                            if usage.campaign_ids:
                                print(f"- Used in {len(usage.campaign_ids)} campaigns")
                            if usage.broadcast_ids:
                                print(f"- Used in {len(usage.broadcast_ids)} broadcasts")
                            print("Consider the impact before deleting")
                        
                        # Proceed with deletion (you might prompt for confirmation)
                        print("Proceeding with deletion...")
                        
                        # Delete the segment
                        response = await client.people.segments.delete(segment_id=segment_id)
                        print(f"Segment deleted successfully: {response}")
                        
                except Exception as e:
                    print(f"Error deleting segment: {str(e)}")
            ```
        
        Note:
            - This operation cannot be undone
            - Predefined segments cannot be deleted
            - Deleting a segment does not delete the contacts in the segment
            - Before deleting, check if the segment is used in campaigns or broadcasts
            using the segments.usage method
            - If a segment is in use, deleting it may affect active campaigns or automations
        """
        # pylint: disable=protected-access
        return await self._client._request("DELETE",
                                           self.root_path + "/" + segment_id,
                                           headers=self.headers)

    async def update(self, segment_id: str, data: CreateSegmentRequest):
        """
        Update an existing segment in the Naxai People API.
        
        This method modifies the properties of an existing segment, such as its name,
        description, or conditions (for dynamic segments).
        
        Args:
            segment_id (str): The unique identifier of the segment to update.
            data (CreateSegmentRequest): The updated segment data. This should be a
                CreateSegmentRequest object containing the fields to update.
        
        Returns:
            UpdateSegmentResponse: A response object containing the updated segment information.
        
        Raises:
            ValueError: If segment_id is empty or data is invalid.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to update segments.
            NaxaiResourceNotFound: If the specified segment does not exist.
            NaxaiInvalidRequestError: If the update request contains invalid data or
                attempts to update a predefined segment.
        
        Example:
            ```python
            from naxai.models.people.requests.segments_requests import CreateSegmentRequest
            from naxai.models.people.search_condition import (Condition,
                                                              AttributeCondSimple,
                                                              AttributeObject)
            
            async with NaxaiAsyncClient(api_client_id="your_id",
                                        api_client_secret="your_secret") as client:
                try:
                    # Update a segment's name and description
                    segment_id = "seg_123abc"
                    
                    # First, get the current segment data
                    current_segment = await client.people.segments.get(segment_id=segment_id)
                    
                    # Create an update request with the fields to change
                    update_data = CreateSegmentRequest(
                        name="Updated Segment Name",
                        description="This segment was updated with new criteria",
                        type_=current_segment.type_  # Keep the same type
                    )
                    
                    # For dynamic segments, you might want to update the conditions
                    if current_segment.type_ == "dynamic":
                        # Create a new condition for US customers with high value
                        condition = Condition(
                            all=[
                                AttributeCondSimple(
                                    attribute=AttributeObject(
                                        field="country",
                                        operator="eq",
                                        value="US"
                                    )
                                ),
                                AttributeCondSimple(
                                    attribute=AttributeObject(
                                        field="customer_value",
                                        operator="gt",
                                        value=1000
                                    )
                                )
                            ]
                        )
                        update_data.condition = condition
                    
                    # Update the segment
                    updated_segment = await client.people.segments.update(
                        segment_id=segment_id,
                        data=update_data
                    )
                    
                    print(f"Segment updated successfully: {updated_segment.name}")
                    print(f"Description: {updated_segment.description}")
                    
                    if updated_segment.type_ == "dynamic":
                        print("Segment conditions updated - the segment will be recalculated")
                        if updated_segment.state == "building":
                            print("Segment is currently rebuilding...")
                    
                except Exception as e:
                    print(f"Error updating segment: {str(e)}")
            ```
        
        Note:
            - Predefined segments cannot be updated
            - For dynamic segments, updating conditions will trigger a recalculation of
              segment membership
            - During recalculation, the segment's state will be "building"
            - You cannot change a segment's type (manual/dynamic) after creation
            - For manual segments, use the segments.contacts.add and segments.contacts.delete
            methods to modify segment membership
            - Only include the fields you want to update in the CreateSegmentRequest object
        """
        # pylint: disable=protected-access
        return UpdateSegmentResponse.model_validate_json(
            json.dumps(await self._client._request("PUT",
                                                   self.root_path + "/" + segment_id,
                                                   json=data.model_dump(by_alias=True,
                                                                        exclude_none=True),
                                                   headers=self.headers)))

    async def create(self, data: CreateSegmentRequest):
        """
        Create a new segment in the Naxai People API.
        
        This method creates a new segment with the specified name, description, type,
        and conditions (for dynamic segments).
        
        Args:
            data (CreateSegmentRequest): The segment data. This should be a CreateSegmentRequest
                object containing the segment's name, description, type, and
                conditions (if dynamic).
        
        Returns:
            CreateSegmentResponse: 
                A response object containing information about the newly created segment.
        
        Raises:
            ValueError: If data is invalid.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to create segments.
            NaxaiInvalidRequestError: If the request contains invalid data.
        
        Example:
            ```python
            from naxai.models.people.requests.segments_requests import CreateSegmentRequest
            from naxai.models.people.search_condition import (Condition,
                                                              AttributeCondSimple,
                                                              AttributeObject)
            
            async with NaxaiAsyncClient(api_client_id="your_id",
                                        api_client_secret="your_secret") as client:
                try:
                    # Create a manual segment
                    manual_segment = CreateSegmentRequest(
                        name="VIP Customers",
                        description="Manually curated list of our most important customers",
                        type_="manual"
                    )
                    
                    manual_result = await client.people.segments.create(data=manual_segment)
                    print(f"Manual segment created: {manual_result.name} (ID: {manual_result.id})")
                    
                    # Now add contacts to the manual segment
                    contact_ids = ["cnt_123", "cnt_456", "cnt_789"]
                    await client.people.segments.contacts.add(
                        segment_id=manual_result.id,
                        contact_ids=contact_ids
                    )
                    print(f"Added {len(contact_ids)} contacts to the manual segment")
                    
                    # Create a dynamic segment based on conditions
                    # This example creates a segment for active US customers
                    condition = Condition(
                        all=[
                            AttributeCondSimple(
                                attribute=AttributeObject(
                                    field="country",
                                    operator="eq",
                                    value="US"
                                )
                            ),
                            AttributeCondSimple(
                                attribute=AttributeObject(
                                    field="status",
                                    operator="eq",
                                    value="active"
                                )
                            )
                        ]
                    )
                    
                    dynamic_segment = CreateSegmentRequest(
                        name="Active US Customers",
                        description="Automatically updated segment of active customers in the US",
                        type_="dynamic",
                        condition=condition
                    )
                    
                    dynamic_result = await client.people.segments.create(data=dynamic_segment)
                    print(f"Dynamic segment created: {dynamic_result.name} "
                          f"(ID: {dynamic_result.id})")
                    print(f"Current state: {dynamic_result.state}")
                    
                    # For dynamic segments, you might want to wait until it's ready
                    if dynamic_result.state == "building":
                        print("Dynamic segment is being built. Check its status later.")
                    
                except Exception as e:
                    print(f"Error creating segment: {str(e)}")
            ```
        
        Note:
            - There are two types of segments: manual and dynamic
            - Manual segments require you to explicitly add/remove contacts using the
            segments.contacts.add and segments.contacts.delete methods
            - Dynamic segments automatically include contacts that match the specified conditions
            - For dynamic segments, the condition parameter is required
            - After creating a dynamic segment, it will be in the "building" state until
            the initial calculation of segment membership is complete
            - Segment names should be descriptive and unique within your account
        """
        # pylint: disable=protected-access
        return CreateSegmentResponse.model_validate_json(
            json.dumps(await self._client._request("POST",
                                                   self.root_path,
                                                   json=data.model_dump(by_alias=True,
                                                                        exclude_none=True),
                                                   headers=self.headers)))

    async def history(self, segment_id: str,
                      start: int = (datetime.datetime.now(tz=datetime.timezone.utc) -
                                     datetime.timedelta(days=30)),
                      stop: int = datetime.datetime.now(tz=datetime.timezone.utc)):
        """
        Retrieve the membership history of a segment in the Naxai People API.
        
        This method fetches historical data about how a segment's membership has changed
        over time, including daily counts of contacts added, removed, and the total size.
        
        Args:
            segment_id (str): The unique identifier of the segment to get history for.
            start (int): The start timestamp for the history period. Defaults to 30 days ago.
            stop (int): The end timestamp for the history period. Defaults to the current time.
        
        Returns:
            GetSegmentsHistoryResponse: A response object containing the segment's membership
                history data over the specified time period.
        
        Raises:
            ValueError: If segment_id is empty or date parameters are invalid.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access segment information.
            NaxaiResourceNotFound: If the specified segment does not exist.
        
        Example:
            ```python
            import datetime
            from datetime import timedelta
            
            async with NaxaiAsyncClient(api_client_id="your_id",
                                        api_client_secret="your_secret") as client:
                try:
                    # Get segment history for the last 90 days
                    segment_id = "seg_123abc"
                    now = datetime.datetime.now(tz=datetime.timezone.utc)
                    start_date = now - timedelta(days=90)
                    
                    history = await client.people.segments.history(
                        segment_id=segment_id,
                        start=start_date,
                        stop=now
                    )
                    
                    # Display the history data
                    print(f"Segment history for the last 90 days:")
                    print(f"Total data points: {len(history.history)}")
                    
                    if history.history:
                        # Get the first and last data points
                        first_day = history.history[0]
                        last_day = history.history[-1]
                        
                        # Convert timestamps to readable dates
                        first_date = (
                        datetime.datetime.fromtimestamp(first_day.date / 1000).strftime('%Y-%m-%d'))
                        last_date = (
                        datetime.datetime.fromtimestamp(last_day.date / 1000).strftime('%Y-%m-%d'))
                        
                        print(f"\nInitial size on {first_date}: {first_day.current}")
                        print(f"Final size on {last_date}: {last_day.current}")
                        
                        # Calculate total changes over the period
                        total_added = sum(
                            day.added for day in history.history if day.added is not None)
                        total_removed = sum(
                            day.removed for day in history.history if day.removed is not None)
                        net_change = total_added - total_removed
                        
                        print(f"\nTotal contacts added: {total_added}")
                        print(f"Total contacts removed: {total_removed}")
                        print(f"Net change: {net_change}")
                        
                        # Find the day with the most changes
                        max_change_day = max(
                        history.history,
                        key=lambda day: abs(day.change) if day.change is not None else 0)
                        max_change_date = (
                        datetime.datetime.fromtimestamp(max_change_day.date 
                                                        / 1000).strftime('%Y-%m-%d'))
                        
                        print(f"\nLargest daily change: {max_change_day.change} on "
                              f"{max_change_date}")
                        print(f"  Added: {max_change_day.added}, Removed: {max_change_day.removed}")
                        
                    else:
                        print("No history data available for this "
                                "segment in the specified time range")
                    
                except Exception as e:
                    print(f"Error retrieving segment history: {str(e)}")
            ```
        
        Note:
            - History data is provided on a daily basis
            - Each history record includes the date, number of contacts added, number removed,
            net change, and current total for that day
            - For manual segments, changes reflect manual additions and removals
            - For dynamic segments, changes reflect contacts that started or stopped meeting
            the segment conditions
            - History data is useful for tracking segment growth and analyzing trends
            - The start and stop parameters accept datetime objects or timestamps
            - The default time range is the last 30 days
        """
        params = {"start": start, "stop": stop}
        # pylint: disable=protected-access
        return GetSegmentsHistoryResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/" + segment_id + "/history",
                                                   headers=self.headers,
                                                   params=params)))

    async def usage(self, segment_id: str):
        """
        Retrieve information about where a segment is being used in the Naxai People API.
        
        This method fetches data about which campaigns and broadcasts are using the
        specified segment. This information is valuable when considering segment modifications
        or deletion, as it helps identify potential impacts on active communications.
        
        Args:
            segment_id (str): The unique identifier of the segment to check usage for.
        
        Returns:
            GetSegmentUsageResponse: A response object containing lists of campaign IDs
                and broadcast IDs that use this segment.
        
        Raises:
            ValueError: If segment_id is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access segment information.
            NaxaiResourceNotFound: If the specified segment does not exist.
        
        Example:
            ```python
            async with NaxaiAsyncClient(api_client_id="your_id",
                                        api_client_secret="your_secret") as client:
                try:
                    # Check where a segment is being used
                    segment_id = "seg_123abc"
                    
                    # First, get the segment details for context
                    segment = await client.people.segments.get(segment_id=segment_id)
                    print(f"Checking usage for segment: {segment.name} (ID: {segment.id})")
                    
                    # Get usage information
                    usage = await client.people.segments.usage(segment_id=segment_id)
                    
                    # Check if the segment is used in campaigns
                    if usage.campaign_ids:
                        print(f"This segment is used in {len(usage.campaign_ids)} campaigns:")
                        for campaign_id in usage.campaign_ids:
                            print(f"- Campaign ID: {campaign_id}")
                            
                            # In a real application, you might fetch campaign details
                            # campaign = await client.campaigns.get(campaign_id)
                            # print(f"  Campaign name: {campaign.name}")
                    else:
                        print("This segment is not used in any campaigns")
                    
                    # Check if the segment is used in broadcasts
                    if usage.broadcast_ids:
                        print(f"This segment is used in {len(usage.broadcast_ids)} broadcasts:")
                        for broadcast_id in usage.broadcast_ids:
                            print(f"- Broadcast ID: {broadcast_id}")
                            
                            # In a real application, you might fetch broadcast details
                            # broadcast = await client.broadcasts.get(broadcast_id)
                            # print(f"  Broadcast name: {broadcast.name}")
                    else:
                        print("This segment is not used in any broadcasts")
                    
                    # Determine if it's safe to modify or delete the segment
                    if not usage.campaign_ids and not usage.broadcast_ids:
                        print("\nThis segment is not currently in use and can"
                                " be safely modified or deleted")
                    else:
                        print("\nThis segment is in use - modifications or "
                                "deletion may affect active communications")
                    
                except Exception as e:
                    print(f"Error checking segment usage: {str(e)}")
            ```
        
        Note:
            - This method is particularly useful before modifying or deleting a segment
            - For dynamic segments, changing conditions will affect all campaigns and broadcasts
            that use the segment
            - For manual segments, adding or removing contacts will immediately affect
            any active campaigns or broadcasts using the segment
            - If a segment is in use, consider creating a new segment instead of modifying
            an existing one to avoid disrupting active communications
            - The response includes only the IDs of campaigns and broadcasts; to get detailed
            information about them, you would need to make additional API calls
        """
        # pylint: disable=protected-access
        return GetSegmentUsageResponse.model_validate_json(
            json.dumps(await self._client._request("GET",
                                                   self.root_path + "/" + segment_id + "/usage",
                                                   headers=self.headers)))
