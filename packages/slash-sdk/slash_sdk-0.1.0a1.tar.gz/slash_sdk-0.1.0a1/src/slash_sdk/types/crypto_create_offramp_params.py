# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["CryptoCreateOfframpParams"]


class CryptoCreateOfframpParams(TypedDict, total=False):
    currency: Required[Literal["usdt", "usdc"]]

    payment_rail: Required[Annotated[Literal["ach", "wire"], PropertyInfo(alias="paymentRail")]]

    virtual_account_id: Required[Annotated[str, PropertyInfo(alias="virtualAccountId")]]
    """The id of the virtual account to offramp funds to."""
