# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .transaction import Transaction
from .pagination_response import PaginationResponse

__all__ = ["TransactionListResponse"]


class TransactionListResponse(BaseModel):
    items: List[Transaction]

    metadata: Optional[PaginationResponse] = None
    """Response sent when requesting a list of data"""
