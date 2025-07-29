# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .pagination_response import PaginationResponse
from .card_group.card_group import CardGroup

__all__ = ["CardGroupListResponse"]


class CardGroupListResponse(BaseModel):
    items: List[CardGroup]

    metadata: Optional[PaginationResponse] = None
    """Response sent when requesting a list of data"""
