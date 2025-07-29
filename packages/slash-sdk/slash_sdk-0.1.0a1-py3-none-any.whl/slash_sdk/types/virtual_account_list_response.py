# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .virtual_account import VirtualAccount
from .pagination_response import PaginationResponse

__all__ = ["VirtualAccountListResponse"]


class VirtualAccountListResponse(BaseModel):
    items: List[VirtualAccount]

    metadata: Optional[PaginationResponse] = None
    """Response sent when requesting a list of data"""
