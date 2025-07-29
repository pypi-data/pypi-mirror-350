# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .slash_handle import SlashHandle
from .pagination_response import PaginationResponse

__all__ = ["SlashHandleListResponse"]


class SlashHandleListResponse(BaseModel):
    items: List[SlashHandle]

    metadata: PaginationResponse
    """Response sent when requesting a list of data"""
