"""
Segment condition models for the Naxai SDK.

This module defines the data structures used for creating segment definitions,
allowing for complex filtering of contacts based on attributes and events.
These models support building sophisticated audience segments for targeting
and analytics purposes.
"""

from typing import Optional, Literal, Union
from pydantic import BaseModel, Field

CONDITIONS = Literal[
    "eq", "not-eq", "gt", "lt", "exists", "not-exists", 
    "contains", "not-contains", "is-true", "is-false",
    "is-timestamp", "is-timestamp-before", "is-timestamp-after",
    "is-mobile", "is-not-mobile"
]

class EventPropertiesCondObject(BaseModel):
    """
    Model representing a condition for event properties in segment definitions.
    
    This class defines a single condition to match event properties with specific 
    operators when creating segments.
    
    Attributes:
        name (str): The name of the event property to evaluate.
        operator (Literal): The comparison operator to use.
            Supported values: "eq", "not-eq", "gt", "lt", "is-true", "is-false".
        value (Optional[Union[str, int, bool]]): The value to compare against.
            May be None for operators that don't require a value.
    """
    name: str
    operator: Literal["eq", "not-eq", "gt", "lt", "is-true", "is-false"]
    value: Optional[Union[str, int, bool]] = None

class EventProperties(BaseModel):
    """
    Model representing logical groups of event property conditions.
    
    This class allows combining multiple event property conditions with AND/OR logic
    when defining segments based on event properties.
    
    Attributes:
        all (Optional[list[EventPropertiesCondObject]]): List of conditions that must
            all be true (AND logic).
        any (Optional[list[EventPropertiesCondObject]]): List of conditions where at
            least one must be true (OR logic).
    """
    all: Optional[list[EventPropertiesCondObject]]
    any: Optional[list[EventPropertiesCondObject]]

class EventObject(BaseModel):
    """
    Model representing an event condition for segment definitions.
    
    This class defines criteria for matching events with specific properties,
    occurrence counts, and time boundaries when creating segments.
    
    Attributes:
        name (str): The name of the event to match.
        count (int): The number of occurrences to match. Defaults to 1.
        count_boundary (Literal): Whether the count is a minimum or maximum.
            Values: "at-least", "at-most". Defaults to "at-least".
        time_boundary (Literal): The time frame to consider for events.
            Values: "all-time", "within-last", "before", "after".
            Defaults to "all-time".
        period_boundary (Literal): The unit of time for time_boundary.
            Values: "day", "month". Defaults to "day".
        interval_boundary (int): The number of period units for time_boundary.
            Range: 1-366. Defaults to 1.
        date (Optional[int]): Timestamp for before/after time boundaries.
        properties (EventProperties): Property conditions on the event properties.
    
    Example:
        >>> # Create a condition for users who made at least 2 purchases in the last 30 days
        >>> event = EventObject(
        ...     name="purchase",
        ...     count=2,
        ...     count_boundary="at-least",
        ...     time_boundary="within-last",
        ...     period_boundary="day",
        ...     interval_boundary=30,
        ...     properties=EventProperties(
        ...         all=[EventPropertiesCondObject(
        ...             name="status", operator="eq", value="completed"
        ...         )]
        ...     )
        ... )
    """
    name: str
    count: int = Field(default=1)
    count_boundary: Literal["at-least", "at-most"] = Field(
        default="at-least", alias="countBoundary"
    )
    time_boundary: Literal["all-time", "within-last", "before", "after"] = Field(
        default="all-time", alias="timeBoundary"
    )
    period_boundary: Literal["day", "month"] = Field(
        default="day", alias="periodBoundary"
    )
    interval_boundary: int = Field(
        default=1, alias="intervalBoundary", ge=1, le=366
    )
    date: Optional[int] = None
    properties: EventProperties

class AttributeArrayObject(BaseModel):
    """
    Model representing an attribute condition with an array of values.
    
    This class defines conditions for attributes that require multiple values,
    such as range comparisons, used in segment definitions.
    
    Attributes:
        operator (Literal): The comparison operator to use. Must be either
            "between" or "is-timestamp-between".
        field (str): The name of the attribute field to evaluate.
        values (list): A list of exactly two values defining the range.
            For "between", these are the min and max values.
            For "is-timestamp-between", these are the start and end timestamps.
    
    Example:
        >>> # Create a condition for age between 25 and 35
        >>> condition = AttributeArrayObject(
        ...     operator="between",
        ...     field="age",
        ...     values=[25, 35]
        ... )
    """
    operator: Literal["between", "is-timestamp-between"]
    field: str
    values: list = Field(min_length=2, max_length=2)

class AttributeObject(BaseModel):
    """
    Model representing a simple attribute condition in segment definitions.
    
    This class defines conditions for attributes that require a single value comparison,
    used when creating segments.
    
    Attributes:
        operator (CONDITIONS): The comparison operator to use. Must be one of the
            operators defined in the CONDITIONS Literal.
        field (str): The name of the attribute field to evaluate.
        value (Optional[Union[str, int, bool]]): The value to compare against.
            Required for most operators except existence checks like "exists".
    
    Example:
        >>> # Create a condition for country equals "US"
        >>> condition = AttributeObject(
        ...     operator="eq",
        ...     field="country",
        ...     value="US"
        ... )
    """
    operator: CONDITIONS
    field: str
    value: Optional[Union[str, int, bool]]

class EventCond(BaseModel):
    """
    Model representing an event condition wrapper in segment definitions.
    
    This class serves as a wrapper for EventObject instances to be used in
    condition groups within segment definitions.
    
    Attributes:
        event (EventObject): The event condition to apply.
    
    Example:
        >>> # Create an event condition for a purchase event
        >>> event_obj = EventObject(
        ...     name="purchase",
        ...     properties=EventProperties(
        ...         all=[EventPropertiesCondObject(
        ...             name="amount", operator="gt", value=50
        ...         )]
        ...     )
        ... )
        >>> condition = EventCond(event=event_obj)
    """
    event: EventObject = Field(default=None)

class AttributeCondArray(BaseModel):
    """
    Model representing an attribute array condition wrapper in segment definitions.
    
    This class serves as a wrapper for AttributeArrayObject instances to be used in
    condition groups within segment definitions.
    
    Attributes:
        attribute (AttributeArrayObject): The attribute array condition to apply.
    
    Example:
        >>> # Create an attribute condition for age between 25 and 35
        >>> attr_obj = AttributeArrayObject(
        ...     operator="between",
        ...     field="age",
        ...     values=[25, 35]
        ... )
        >>> condition = AttributeCondArray(attribute=attr_obj)
    """
    attribute: AttributeArrayObject = Field(default=None, min_length=1)

class AttributeCondSimple(BaseModel):
    """
    Model representing a simple attribute condition wrapper in segment definitions.
    
    This class serves as a wrapper for AttributeObject instances to be used in
    condition groups within segment definitions.
    
    Attributes:
        attribute (AttributeObject): The attribute condition to apply.
    
    Example:
        >>> # Create a simple attribute condition for country equals "US"
        >>> attr_obj = AttributeObject(
        ...     operator="eq",
        ...     field="country",
        ...     value="US"
        ... )
        >>> condition = AttributeCondSimple(attribute=attr_obj)
    """
    attribute: AttributeObject = Field(default=None)

class AllCondGroup(BaseModel):
    """
    Model representing a group of conditions joined by logical AND.
    
    This class combines multiple conditions where all must be satisfied for a contact
    to be included in a segment.
    
    Attributes:
        all (list[Union[AttributeCondSimple, AttributeCondArray, EventCond]]): 
            List of conditions that must all be satisfied (AND logic).
    
    Example:
        >>> # Create a condition group where country is "US" AND has made a purchase
        >>> all_group = AllCondGroup(
        ...     all=[
        ...         AttributeCondSimple(attribute=AttributeObject(
        ...             operator="eq", field="country", value="US"
        ...         )),
        ...         EventCond(event=EventObject(
        ...             name="purchase", properties=EventProperties(all=[])
        ...         ))
        ...     ]
        ... )
    """
    all: list[Union[AttributeCondSimple, AttributeCondArray, EventCond]] = Field(
        min_length=1
    )

class AnyCondGroup(BaseModel):
    """
    Model representing a group of conditions joined by logical OR.
    
    This class combines multiple conditions where at least one must be satisfied for a
    contact to be included in a segment.
    
    Attributes:
        any (list[Union[AttributeCondSimple, AttributeCondArray, EventCond]]): 
            List of conditions where at least one must be satisfied (OR logic).
    
    Example:
        >>> # Create a condition group where country is either "US" OR "Canada"
        >>> any_group = AnyCondGroup(
        ...     any=[
        ...         AttributeCondSimple(attribute=AttributeObject(
        ...             operator="eq", field="country", value="US"
        ...         )),
        ...         AttributeCondSimple(attribute=AttributeObject(
        ...             operator="eq", field="country", value="Canada"
        ...         ))
        ...     ]
        ... )
    """
    any: list[Union[AttributeCondSimple, AttributeCondArray, EventCond]] = Field(
        min_length=1
    )

class Condition(BaseModel):
    """
    Model representing the top-level condition structure for segment definitions.
    
    This class defines the complete set of conditions for a segment, allowing for
    complex combinations of attribute and event conditions using logical AND/OR operations.
    
    Attributes:
        all (Optional[list]): List of conditions that must all be satisfied (AND logic).
            Can include simple conditions or nested condition groups.
        any (Optional[list]): List of conditions where at least one must be satisfied
            (OR logic). Can include simple conditions or nested condition groups.
    
    Example:
        >>> # Create a condition for active users who are from either US or Canada
        >>> condition = Condition(
        ...     all=[
        ...         AttributeCondSimple(attribute=AttributeObject(
        ...             operator="eq", field="status", value="active"
        ...         )),
        ...         AnyCondGroup(
        ...             any=[
        ...                 AttributeCondSimple(attribute=AttributeObject(
        ...                     operator="eq", field="country", value="US"
        ...                 )),
        ...                 AttributeCondSimple(attribute=AttributeObject(
        ...                     operator="eq", field="country", value="Canada"
        ...                 ))
        ...             ]
        ...         )
        ...     ]
        ... )
    """
    all: Optional[list[Union[
        AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup
    ]]] = Field(default=None, min_length=1)

    any: Optional[list[Union[
        AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup
    ]]] = Field(default=None, min_length=1)
