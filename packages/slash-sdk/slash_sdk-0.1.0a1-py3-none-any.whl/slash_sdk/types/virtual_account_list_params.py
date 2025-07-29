# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VirtualAccountListParams"]


class VirtualAccountListParams(TypedDict, total=False):
    cursor: str
    """A cursor string to fetch the next page of results"""

    filter_account_id: Annotated[str, PropertyInfo(alias="filter:accountId")]
    """Pass in an account ID to filter virtual accounts by account ID.

    This will return all virtual accounts that match the account ID passed in.
    """

    filter_include_closed_accounts: Annotated[
        Literal["true", "false"], PropertyInfo(alias="filter:includeClosedAccounts")
    ]
    """Include virtual accounts that have been closed in the query results.

    By default, they will not be returned.
    """
