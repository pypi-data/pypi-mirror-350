# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .card.spending_constraint_param import SpendingConstraintParam

__all__ = ["CardGroupCreateParams"]


class CardGroupCreateParams(TypedDict, total=False):
    name: Required[str]

    spending_constraint: Annotated[SpendingConstraintParam, PropertyInfo(alias="spendingConstraint")]
    """A constraint that can be applied to a CardGroupSpendingRule"""

    virtual_account_id: Annotated[str, PropertyInfo(alias="virtualAccountId")]
    """The ID of the virtual account to associate with the card group.

    If not provided, the primary virtual account will be used.
    """
