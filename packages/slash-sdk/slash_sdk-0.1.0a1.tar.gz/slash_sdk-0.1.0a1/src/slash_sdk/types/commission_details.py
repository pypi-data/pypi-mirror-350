# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .money import Money
from .._models import BaseModel

__all__ = ["CommissionDetails", "UnionMember0", "UnionMember1"]


class UnionMember0(BaseModel):
    amount: Money
    """
    The amount of money to be diverted from the virtual account if the type of rule
    is flat_fee.
    """

    frequency: Literal["monthly", "yearly"]
    """The frequency from the start date that the rule will be applied.

    E.g. a start date of November 26, 2024 with a frequency of "monthly" will have
    the rule applied on December 26, 2024. If the frequency was "yearly", the rule
    would be applied again on November 26, 2025.
    """

    type: Literal["flatFee"]
    """The type of the commission rule.

    A type of flat_fee will take a flat fee from the virtual account and transfer it
    to the primary account with the frequency of the collection defined as monthly
    or yearly.
    """

    start_date: Optional[datetime] = FieldInfo(alias="startDate", default=None)
    """The date that the rule will begin to take effect."""


class UnionMember1(BaseModel):
    take_rate: float = FieldInfo(alias="takeRate")
    """
    The percentage of funds to divert from the virtual account to the primary
    account.
    """

    type: Literal["takeRate"]
    """The type of the commission rule.

    A type of take_rate will take a percent of the virtual account's funds and
    divert them to the primary account.
    """


CommissionDetails: TypeAlias = Union[UnionMember0, UnionMember1]
