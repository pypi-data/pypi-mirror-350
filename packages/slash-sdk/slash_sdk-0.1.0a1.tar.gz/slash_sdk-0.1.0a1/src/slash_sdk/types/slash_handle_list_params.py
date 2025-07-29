# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["SlashHandleListParams"]


class SlashHandleListParams(TypedDict, total=False):
    cursor: str
    """A cursor string to fetch the next page of results"""
