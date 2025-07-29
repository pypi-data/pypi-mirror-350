# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .commission_details_param import CommissionDetailsParam

__all__ = ["VirtualAccountCreateParams"]


class VirtualAccountCreateParams(TypedDict, total=False):
    account_id: Required[Annotated[str, PropertyInfo(alias="accountId")]]
    """The account ID the virtual account should be created under."""

    name: Required[str]
    """The name of the virtual account"""

    commission_details: Annotated[CommissionDetailsParam, PropertyInfo(alias="commissionDetails")]
    """
    Specifies how much of the virtual account's incoming funds should be diverted to
    the primary account
    """
