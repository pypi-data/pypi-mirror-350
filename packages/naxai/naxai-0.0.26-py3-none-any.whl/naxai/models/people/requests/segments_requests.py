"""
Segment request models for the Naxai SDK.

This module defines the data structures used for segment-related API requests,
including segment creation with conditions for filtering contacts based on
attributes and behaviors.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field
from naxai.models.people.helper_models.segments_condition import Condition

class CreateSegmentRequest(BaseModel):
    """
    Request model for creating a new segment in the Naxai People API.
    
    This class defines the structure for segment creation requests, providing
    all the necessary fields to specify a segment's name, description, conditions,
    and type.
    
    Attributes:
        name (str): The name of the segment to create.
        description (Optional[str]): A description of the segment's purpose or criteria.
            Defaults to None.
        condition (Optional[Condition]): The conditions that define which contacts
            should be included in this segment. Required for dynamic segments.
            Defaults to None.
        type_ (Literal["manual", "dynamic"]): The type of segment to create.
            - "manual": Explicitly defined members that you'll add manually
            - "dynamic": Rule-based segment where members are determined by conditions
            Mapped from JSON key 'type'. Defaults to "manual".
    
    Example:
        >>> # Create a dynamic segment for active US customers
        >>> request = CreateSegmentRequest(
        ...     name="Active US Customers",
        ...     description="Customers from the US who have been active in the last 30 days",
        ...     type="dynamic",
        ...     condition=Condition(
        ...         all=[
        ...             AttributeCondSimple(attribute=AttributeObject(operator="eq",
        ...                                                           field="country",
        ...                                                           value="US")),
        ...             EventCond(
        ...                 event=EventObject(
        ...                     name="login",
        ...                     time_boundary="within-last",
        ...                     period_boundary="day",
        ...                     interval_boundary=30,
        ...                     properties=EventProperties(all=[])
        ...                 )
        ...             )
        ...         ]
        ...     )
        ... )
    
    Note:
        - For manual segments, the condition field is optional
        - For dynamic segments, the condition field is required
        - This model supports both snake_case and camelCase field access through populate_by_name
    """
    name: str
    description: Optional[str] = None
    condition: Optional[Condition] = None
    type_: Literal["manual", "dynamic"] = Field(default="manual", alias="type")

    model_config = {"populate_by_name": True}
