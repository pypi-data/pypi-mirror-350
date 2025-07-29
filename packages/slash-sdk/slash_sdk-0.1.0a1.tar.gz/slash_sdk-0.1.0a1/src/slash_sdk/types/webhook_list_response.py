# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .webhook import Webhook
from .._models import BaseModel
from .pagination_response import PaginationResponse

__all__ = ["WebhookListResponse"]


class WebhookListResponse(BaseModel):
    items: List[Webhook]

    metadata: Optional[PaginationResponse] = None
    """Response sent when requesting a list of data"""
