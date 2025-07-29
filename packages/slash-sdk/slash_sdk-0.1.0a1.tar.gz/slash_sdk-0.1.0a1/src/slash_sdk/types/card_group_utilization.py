# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .money import Money
from .._models import BaseModel

__all__ = ["CardGroupUtilization"]


class CardGroupUtilization(BaseModel):
    spend: Money
    """The amount of money spent in the current period"""

    available_balance: Optional[Money] = FieldInfo(alias="availableBalance", default=None)
    """The amount of money available in the current period.

    Only returned if the card or card group has a spend limit.
    """

    next_reset_date: Optional[datetime] = FieldInfo(alias="nextResetDate", default=None)
    """The date the next reset will occur, undefined if collective"""
