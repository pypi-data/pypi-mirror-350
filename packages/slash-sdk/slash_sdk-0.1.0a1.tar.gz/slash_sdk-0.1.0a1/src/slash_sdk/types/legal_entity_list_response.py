# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .pagination_response import PaginationResponse

__all__ = ["LegalEntityListResponse", "Item"]


class Item(BaseModel):
    id: str

    name: str

    structure: Optional[Literal["person", "llc", "lp", "llp", "gp", "partnership", "ccorp", "scorp"]] = None
    """
    Will be empty in rare cases where the legal entity has not yet been fully
    created.
    """


class LegalEntityListResponse(BaseModel):
    items: List[Item]

    metadata: PaginationResponse
    """Response sent when requesting a list of data"""
