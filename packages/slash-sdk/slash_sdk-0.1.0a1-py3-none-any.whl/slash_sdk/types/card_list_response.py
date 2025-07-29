# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .card.card import Card
from .pagination_response import PaginationResponse

__all__ = ["CardListResponse"]


class CardListResponse(BaseModel):
    items: List[Card]

    metadata: Optional[PaginationResponse] = None
    """Response sent when requesting a list of data"""
