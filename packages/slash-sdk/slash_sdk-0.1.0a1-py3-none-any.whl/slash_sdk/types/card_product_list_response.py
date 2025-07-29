# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .pagination_response import PaginationResponse

__all__ = ["CardProductListResponse", "Item"]


class Item(BaseModel):
    id: str

    prefix: str

    status: Literal["active", "inactive"]


class CardProductListResponse(BaseModel):
    items: List[Item]

    metadata: Optional[PaginationResponse] = None
    """Response sent when requesting a list of data"""
