# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["StatementListParams"]


class StatementListParams(TypedDict, total=False):
    end_time: Annotated[str, PropertyInfo(alias="endTime")]
    """End time for use in retrieval of statements (ISO 8601)."""

    limit: str
    """The number of items to return (default 100, max 1000)"""

    offset: str
    """The ID of the last item in the previous page of results"""

    start_time: Annotated[str, PropertyInfo(alias="startTime")]
    """Start time for use in retrieval of statements (ISO 8601)."""
