# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["CardGroupListParams"]


class CardGroupListParams(TypedDict, total=False):
    cursor: str
    """A cursor string to fetch the next page of results"""

    filter_name: Annotated[str, PropertyInfo(alias="filter:name")]
    """Pass in a name to filter for card groups with a matching name."""
