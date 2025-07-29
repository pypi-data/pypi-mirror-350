# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["MerchantListParams"]


class MerchantListParams(TypedDict, total=False):
    cursor: str
    """A cursor string to fetch the next page of results"""

    search_merchant_name: Annotated[str, PropertyInfo(alias="search:merchant_name")]
    """Pass in a merchant name to filter merchants by name."""
