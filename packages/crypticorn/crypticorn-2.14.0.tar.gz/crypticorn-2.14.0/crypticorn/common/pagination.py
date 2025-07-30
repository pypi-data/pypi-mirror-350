"""Utilities for handling paginated API responses and cursor-based pagination."""

from typing import Generic, Type, TypeVar, List, Optional, Literal
from pydantic import BaseModel, Field, model_validator

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Pydantic model for paginated response
    >>> PaginatedResponse[ItemModel](data=items, total=total_items, page=1, size=10, prev=None, next=2)
    """

    data: List[T]
    total: int = Field(description="The total number of items")
    page: int = Field(description="The current page number")
    size: int = Field(description="The number of items per page")
    prev: Optional[int] = Field(None, description="The previous page number")
    next: Optional[int] = Field(None, description="The next page number")


class PaginationParams(BaseModel, Generic[T]):
    """Standard pagination parameters for usage in API endpoints. Check the [fastapi docs](https://fastapi.tiangolo.com/tutorial/query-param-models/?h=qu#query-parameters-with-a-pydantic-model) for usage examples.
    The default size is 10 items per page, but can be overridden:
    >>> class HeavyPaginationParams(PaginationParams[T]):
    >>>     size: int = Field(default=100, description="The number of items per page")
    """

    page: int = Field(default=1, description="The current page number")
    size: int = Field(default=10, description="The number of items per page")
    order: Literal["asc", "desc"] = Field(
        default="asc", description="The order to sort by"
    )
    sort: Optional[str] = Field(None, description="The field to sort by")

    @model_validator(mode="after")
    def validate(self):
        # Extract the generic argument type
        args: tuple = self.__pydantic_generic_metadata__.get("args")
        if not args or not issubclass(args[0], BaseModel):
            raise TypeError(
                "PaginationParams must be used with a Pydantic BaseModel as a generic parameter"
            )
        if self.sort:
            # check if the sort field is valid
            model: Type[BaseModel] = args[0]
            if self.sort and self.sort not in model.model_fields:
                raise ValueError(
                    f"Invalid sort field: '{self.sort}' — must be one of: {list(model.model_fields)}"
                )
        return self
