# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .money_param import MoneyParam

__all__ = ["CommissionDetailsParam", "UnionMember0", "UnionMember1"]


class UnionMember0(TypedDict, total=False):
    amount: Required[MoneyParam]
    """
    The amount of money to be diverted from the virtual account if the type of rule
    is flat_fee.
    """

    frequency: Required[Literal["monthly", "yearly"]]
    """The frequency from the start date that the rule will be applied.

    E.g. a start date of November 26, 2024 with a frequency of "monthly" will have
    the rule applied on December 26, 2024. If the frequency was "yearly", the rule
    would be applied again on November 26, 2025.
    """

    type: Required[Literal["flatFee"]]
    """The type of the commission rule.

    A type of flat_fee will take a flat fee from the virtual account and transfer it
    to the primary account with the frequency of the collection defined as monthly
    or yearly.
    """

    start_date: Annotated[Union[str, datetime], PropertyInfo(alias="startDate", format="iso8601")]
    """The date that the rule will begin to take effect."""


class UnionMember1(TypedDict, total=False):
    take_rate: Required[Annotated[float, PropertyInfo(alias="takeRate")]]
    """
    The percentage of funds to divert from the virtual account to the primary
    account.
    """

    type: Required[Literal["takeRate"]]
    """The type of the commission rule.

    A type of take_rate will take a percent of the virtual account's funds and
    divert them to the primary account.
    """


CommissionDetailsParam: TypeAlias = Union[UnionMember0, UnionMember1]
