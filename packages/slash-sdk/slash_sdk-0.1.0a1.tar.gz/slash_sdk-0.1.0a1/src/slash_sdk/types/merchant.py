# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Merchant"]


class Merchant(BaseModel):
    id: str

    name: str

    url: Optional[str] = None
