# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .merchant import Merchant
from .pagination_response import PaginationResponse

__all__ = ["MerchantListResponse"]


class MerchantListResponse(BaseModel):
    items: List[Merchant]

    metadata: Optional[PaginationResponse] = None
    """Response sent when requesting a list of data"""
