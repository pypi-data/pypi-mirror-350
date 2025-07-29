# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TransferCreateVirtualAccountTransferParams"]


class TransferCreateVirtualAccountTransferParams(TypedDict, total=False):
    amount_cents: Required[Annotated[float, PropertyInfo(alias="amountCents")]]
    """The amount of money to send in cents."""

    destination: Required[str]
    """The ID of the virtual account to transfer money to."""

    source: Required[str]
    """The ID of the virtual account to transfer money from.

    Can also be the virtual account linked to a primary Slash account to fund a new
    virtual account (Virtual account with the name 'Primary account').
    """

    x_idempotency_key: Required[Annotated[str, PropertyInfo(alias="X-Idempotency-Key")]]
