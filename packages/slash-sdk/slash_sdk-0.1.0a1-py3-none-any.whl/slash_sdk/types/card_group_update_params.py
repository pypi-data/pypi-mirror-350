# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo
from .card.spending_constraint_param import SpendingConstraintParam

__all__ = ["CardGroupUpdateParams"]


class CardGroupUpdateParams(TypedDict, total=False):
    name: str

    spending_constraint: Annotated[Optional[SpendingConstraintParam], PropertyInfo(alias="spendingConstraint")]
    """
    Explicitly set this value to null to remove all card group level spending
    constraints.
    """
