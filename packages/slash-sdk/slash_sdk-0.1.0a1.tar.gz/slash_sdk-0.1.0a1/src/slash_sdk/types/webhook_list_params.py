# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["WebhookListParams"]


class WebhookListParams(TypedDict, total=False):
    cursor: str
    """A cursor string to fetch the next page of results"""

    filter_legal_entity_id: Annotated[str, PropertyInfo(alias="filter:legalEntityId")]
    """Pass in a legal entity ID to filter for webhooks under a specific legal entity."""
