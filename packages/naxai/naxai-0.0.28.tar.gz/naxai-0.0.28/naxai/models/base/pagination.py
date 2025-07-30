"""
Pagination models for the Naxai SDK.

This module provides the data structures for handling paginated API responses,
allowing for consistent navigation through multi-page results.
"""

from typing import Optional
from pydantic import BaseModel, Field

class Pagination(BaseModel):
    """Model representing pagination information for API responses.

    This class defines the structure of pagination metadata that accompanies
    paginated API responses, providing information about the current page,
    total records, and navigation links.

    Attributes:
        total_record (int): The total number of records available across all pages.
            Mapped from JSON key 'totalRecord'.
        page (int): The current page number.
        page_size (int): The number of records per page.
            Mapped from JSON key 'pageSize'.
        returned_record (int): The number of records returned in the current page.
            Mapped from JSON key 'returnedRecord'.
        remaining_record (int): The number of records remaining after the current page.
            Mapped from JSON key 'remainingRecord'.
        first (Optional[str]): URL to the first page of results.
            Can be None if already on the first page.
        next_ (Optional[str]): URL to the next page of results.
            Mapped from JSON key 'next'. None if on the last page.
        last (Optional[str]): URL to the last page of results.
            Can be None if already on the last page.
        previous (Optional[str]): URL to the previous page of results.
            None if on the first page.

    Example:
        >>> pagination = Pagination(
        ...     totalRecord=100,
        ...     page=2,
        ...     pageSize=20,
        ...     returnedRecord=20,
        ...     remainingRecord=60,
        ...     first="api/v1/resource?page=1",
        ...     next="api/v1/resource?page=3",
        ...     last="api/v1/resource?page=5",
        ...     previous="api/v1/resource?page=1"
        ... )
        >>> print(f"Page {pagination.page} of {pagination.total_record // pagination.page_size}")
        Page 2 of 5
        >>> print(f"Records shown: {pagination.returned_record}")
        Records shown: 20

    Note:
        - All URL fields (first, next_, last, previous) are optional
        - Field names use aliases to match API response keys
        - The model uses Pydantic's validation and serialization features
        - The Config class enables population by name for flexibility
        - Navigation URLs are relative to the API base URL
        - Page numbers are 1-based

    See Also:
        BaseModel: Pydantic's base model class
    """
    total_record: int = Field(alias="totalRecord")
    page: int
    page_size: int = Field(alias="pageSize")
    returned_record: int = Field(alias="returnedRecord")
    remaining_record: int = Field(alias="remainingRecord")
    first: Optional[str] = Field(default=None)
    next_: Optional[str] = Field(alias="next", default=None)
    last: Optional[str] = Field(default=None)
    previous: Optional[str] = Field(default=None)

    model_config = {"populate_by_name": True}
