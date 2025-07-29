# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["AccountListParams"]


class AccountListParams(TypedDict, total=False):
    filter_legal_entity_id: Annotated[str, PropertyInfo(alias="filter:legalEntityId")]
    """Pass in a legal entity ID to filter for accounts under a specific legal entity."""
