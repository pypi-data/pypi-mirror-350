# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .account import Account
from .._models import BaseModel
from .pagination_response import PaginationResponse

__all__ = ["AccountListResponse"]


class AccountListResponse(BaseModel):
    items: List[Account]

    metadata: PaginationResponse
    """Response sent when requesting a list of data"""
