# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..card.spending_constraint import SpendingConstraint

__all__ = ["CardGroup"]


class CardGroup(BaseModel):
    id: str

    name: str

    spending_constraint: Optional[SpendingConstraint] = FieldInfo(alias="spendingConstraint", default=None)
    """A constraint that can be applied to a CardGroupSpendingRule"""

    virtual_account_id: Optional[str] = FieldInfo(alias="virtualAccountId", default=None)
    """The ID of the virtual account that the card group is associated with"""
