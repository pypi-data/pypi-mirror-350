"""
Search condition models for the Naxai SDK.

This module defines the data structures used for creating complex search queries
and filters for people and contacts, supporting various operators and conditions.
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
    Model representing a condition for event properties in search queries.
    
    This class defines a single condition to match event properties with specific operators.
    
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
    
    This class allows combining multiple event property conditions with AND/OR logic.
    
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
    Model representing an event condition for searching.
    
    This class defines criteria for matching events with specific properties,
    occurrence counts, and time boundaries.
    
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
        properties (EventProperties): Property conditions for the event.
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

    model_config = {"populate_by_name": True}


class AttributeArrayObject(BaseModel):
    """
    Model representing an attribute condition that requires an array of values.
    
    This class defines conditions for attributes that need multiple values,
    such as range comparisons.
    
    Attributes:
        operator (Literal): The comparison operator requiring multiple values.
            Values: "between", "is-timestamp-between".
        field (str): The attribute field name to evaluate.
        values (list): Exactly two values defining the range for comparison.
    """
    operator: Literal["between", "is-timestamp-between"]
    field: str
    values: list = Field(min_length=2, max_length=2)


class AttributeObject(BaseModel):
    """
    Model representing a simple attribute condition.
    
    This class defines conditions for attributes with single-value comparisons.
    
    Attributes:
        operator (CONDITIONS): The comparison operator to use.
        field (str): The attribute field name to evaluate.
        value (Optional[Union[str, int, bool]]): The value to compare against.
            May be None for operators that don't require a value.
    """
    operator: CONDITIONS
    field: str
    value: Optional[Union[str, int, bool]]


class EventCond(BaseModel):
    """
    Model representing an event condition wrapper.
    
    This class wraps an EventObject for inclusion in condition groups.
    
    Attributes:
        event (EventObject): The event condition to evaluate.
    """
    event: EventObject = Field(default=None)


class AttributeCondArray(BaseModel):
    """
    Model representing an attribute array condition wrapper.
    
    This class wraps an AttributeArrayObject for inclusion in condition groups.
    
    Attributes:
        attribute (AttributeArrayObject): The attribute array condition to evaluate.
    """
    attribute: AttributeArrayObject = Field(default=None, min_length=1)


class AttributeCondSimple(BaseModel):
    """
    Model representing a simple attribute condition wrapper.
    
    This class wraps an AttributeObject for inclusion in condition groups.
    
    Attributes:
        attribute (AttributeObject): The attribute condition to evaluate.
    """
    attribute: AttributeObject = Field(default=None)


class AllCondGroup(BaseModel):
    """
    Model representing a group of conditions that must all be true.
    
    This class combines multiple conditions with AND logic.
    
    Attributes:
        all (list[Union[AttributeCondSimple, AttributeCondArray, EventCond]]):
            List of conditions that must all be true.
    """
    all: list[Union[AttributeCondSimple, AttributeCondArray, EventCond]] = Field(
        min_length=1
    )


class AnyCondGroup(BaseModel):
    """
    Model representing a group of conditions where at least one must be true.
    
    This class combines multiple conditions with OR logic.
    
    Attributes:
        any (list[Union[AttributeCondSimple, AttributeCondArray, EventCond]]):
            List of conditions where at least one must be true.
    """
    any: list[Union[AttributeCondSimple, AttributeCondArray, EventCond]] = Field(
        min_length=1
    )


class SearchCondition(BaseModel):
    """
    Model representing a complete search condition for filtering contacts.
    
    This class defines the top-level structure for complex search queries,
    supporting nested logical groups of conditions.
    
    Attributes:
        all (Optional[list]): List of conditions that must all be true (AND logic).
            Can include simple conditions, array conditions, event conditions,
            and nested condition groups.
        any (Optional[list]): List of conditions where at least one must be true
            (OR logic). Can include simple conditions, array conditions, event
            conditions, and nested condition groups.
    """
    all: Optional[list[Union[
        AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup
    ]]] = Field(default=None, min_length=1)

    any: Optional[list[Union[
        AttributeCondSimple, AttributeCondArray, EventCond, AllCondGroup, AnyCondGroup
    ]]] = Field(default=None, min_length=1)
