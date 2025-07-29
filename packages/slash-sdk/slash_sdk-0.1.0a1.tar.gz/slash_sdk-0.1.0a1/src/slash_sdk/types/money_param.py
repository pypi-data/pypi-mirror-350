# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["MoneyParam"]


class MoneyParam(TypedDict, total=False):
    amount_cents: Required[Annotated[int, PropertyInfo(alias="amountCents")]]
    """The amount in cents"""
