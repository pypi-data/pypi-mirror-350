# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo
from .card_status import CardStatus
from .card.spending_constraint_param import SpendingConstraintParam

__all__ = ["CardUpdateParams"]


class CardUpdateParams(TypedDict, total=False):
    card_group_id: Annotated[Optional[str], PropertyInfo(alias="cardGroupId")]
    """Explicitly set this value to null to remove the card from a group.

    Omitting this field entirely will not affect the group the card belongs to.
    """

    name: str

    spending_constraint: Annotated[Optional[SpendingConstraintParam], PropertyInfo(alias="spendingConstraint")]
    """
    Explicitly set this value to null to remove all card level spending constraints.
    """

    status: CardStatus

    user_data: Annotated[Optional[Dict[str, object]], PropertyInfo(alias="userData")]
    """Arbitrary information that can be attached to the card.

    This should be a JSON object and cannot exceed 4kb.
    """
