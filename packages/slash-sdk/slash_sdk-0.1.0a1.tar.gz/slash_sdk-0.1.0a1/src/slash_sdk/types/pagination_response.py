# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["PaginationResponse"]


class PaginationResponse(BaseModel):
    count: Optional[float] = None
    """The number of items in the current page of data."""

    next_cursor: Optional[str] = FieldInfo(alias="nextCursor", default=None)
    """The cursor to use to retrieve the next page of data.

    If this is not sent, there is no more data to retrieve.
    """
