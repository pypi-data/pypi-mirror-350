# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["CardListParams"]


class CardListParams(TypedDict, total=False):
    cursor: str
    """A cursor string to fetch the next page of results"""

    filter_account_id: Annotated[str, PropertyInfo(alias="filter:accountId")]
    """Pass in an account ID to filter for cards under a specific account."""

    filter_card_group_id: Annotated[str, PropertyInfo(alias="filter:cardGroupId")]
    """
    Pass in a card group ID, This will return all cards that belong to the card
    group ID passed in. Cannot be combined with filter:cardGroupName.
    """

    filter_card_group_name: Annotated[str, PropertyInfo(alias="filter:cardGroupName")]
    """
    Pass in a card group name, This will return all cards that belong to the card
    group name passed in. Cannot be combined with filter:cardGroupId.
    """

    filter_legal_entity_id: Annotated[str, PropertyInfo(alias="filter:legalEntityId")]
    """
    Pass in a legal entity ID to filter for cards in accounts under a specific legal
    entity.
    """

    filter_status: Annotated[Literal["active", "paused", "closed", "inactive"], PropertyInfo(alias="filter:status")]
    """Returns all cards matching the status passed in."""

    filter_virtual_account_id: Annotated[str, PropertyInfo(alias="filter:virtualAccountId")]
    """
    Pass in a virtual account ID to filter for cards under a specific virtual
    account.
    """

    sort: Literal["createdAt", "name"]
    """Sorts card by creation date or name."""

    sort_direction: Annotated[Literal["ASC", "DESC"], PropertyInfo(alias="sortDirection")]
    """The direction to apply the sort filter by. Default ASC."""
