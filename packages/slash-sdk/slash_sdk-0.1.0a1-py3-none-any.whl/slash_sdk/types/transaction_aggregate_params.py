# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TransactionAggregateParams"]


class TransactionAggregateParams(TypedDict, total=False):
    account_id: Annotated[str, PropertyInfo(alias="accountId")]
    """Use filter:accountId to filter by account ID"""

    filter_account_id: Annotated[str, PropertyInfo(alias="filter:accountId")]
    """Pass in an account ID to filter transactions by account ID.

    This will return all transactions that match the account ID passed in.
    """

    filter_card_id: Annotated[str, PropertyInfo(alias="filter:cardId")]
    """Filter transactions by cardId"""

    filter_detailed_status: Annotated[
        Literal["pending", "canceled", "failed", "settled", "declined", "refund", "reversed", "returned", "dispute"],
        PropertyInfo(alias="filter:detailed_status"),
    ]
    """Filter transactions by detailed status"""

    filter_from_authorized_at: Annotated[str, PropertyInfo(alias="filter:from_authorized_at")]
    """
    Pass in a unix timestamp in milliseconds to filter transactions by authorization
    time. This will return all transactions that are authorized on or after the date
    passed in.
    """

    filter_from_date: Annotated[str, PropertyInfo(alias="filter:from_date")]
    """Pass in a unix timestamp in milliseconds to filter transactions by date.

    This will return all transactions that occurred on or after the date passed in.
    """

    filter_legal_entity_id: Annotated[str, PropertyInfo(alias="filter:legalEntityId")]
    """
    Pass in a legal entity ID to filter transactions by accounts under a specific
    legal entity.
    """

    filter_status: Annotated[Literal["pending", "posted", "failed"], PropertyInfo(alias="filter:status")]
    """Filter transactions by status"""

    filter_to_authorized_at: Annotated[str, PropertyInfo(alias="filter:to_authorized_at")]
    """
    Pass in a unix timestamp in milliseconds to filter transactions by authorization
    time. This will return all transactions that are authorized on or before the
    date passed in.
    """

    filter_to_date: Annotated[str, PropertyInfo(alias="filter:to_date")]
    """Pass in a unix timestamp in milliseconds to filter transactions by date.

    This will return all transactions that occurred on or before the date passed in.
    """

    filter_virtual_account_id: Annotated[str, PropertyInfo(alias="filter:virtualAccountId")]
    """Pass in a virtual account ID to filter transactions by virtual account ID.

    This will return all transactions that match the virtual account ID passed in.
    """
