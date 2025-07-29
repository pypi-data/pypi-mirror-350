# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .pagination_response import PaginationResponse

__all__ = ["MerchantCategoryListResponse", "Item"]


class Item(BaseModel):
    id: str

    name: str


class MerchantCategoryListResponse(BaseModel):
    items: List[Item]

    metadata: Optional[PaginationResponse] = None
    """Response sent when requesting a list of data"""
