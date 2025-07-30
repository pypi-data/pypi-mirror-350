"""Common models for the 1Shot API."""

from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PagedResponse(BaseModel, Generic[T]):
    """A generic paged response model.

    Args:
        T: The type of items in the response
    """

    response: List[T] = Field(..., description="The list of items in the current page")
    page: int = Field(..., description="Which page to return. This is 1 indexed, and default to the first page, 1")
    page_size: int = Field(..., alias="pageSize", description="The size of the page to return. Defaults to 25")
    total_results: int = Field(..., alias="totalResults", description="The total number of results returned by a paged response") 