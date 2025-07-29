# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..card_status import CardStatus
from .spending_constraint import SpendingConstraint

__all__ = ["Card"]


class Card(BaseModel):
    id: str

    account_id: str = FieldInfo(alias="accountId")
    """The account that this card is associated with"""

    expiry_month: str = FieldInfo(alias="expiryMonth")
    """The month the card expires formatted as MM (01, 02, ..., 12)"""

    expiry_year: str = FieldInfo(alias="expiryYear")
    """The year the card expires formatted as YYYY (2024, 2025, ...)"""

    is_physical: bool = FieldInfo(alias="isPhysical")
    """When true, a physical card has been issued. Otherwise, this is a virtual card."""

    last4: str
    """The last 4 digits of the card number"""

    name: str
    """The name assigned to the card that appears on the user dashboard"""

    status: CardStatus
    """The status of the card"""

    card_group_id: Optional[str] = FieldInfo(alias="cardGroupId", default=None)
    """The card group the card belongs to."""

    card_product_id: Optional[str] = FieldInfo(alias="cardProductId", default=None)
    """The ID of the card product this card was created with."""

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)

    cvv: Optional[str] = None
    """
    This field will contain full CVV which will only be sent on a request for a
    single card when you set the query param "include_pan" to "true"
    """

    is_single_use: Optional[bool] = FieldInfo(alias="isSingleUse", default=None)
    """
    When true, the card will be automatically closed after a single authorization
    attempt. Note that the card will be closed even if the authorization declines or
    drops
    """

    pan: Optional[str] = None
    """
    This field contains the full PAN which will only be sent on a request for a
    single card when you set the query param "include_pan" to "true"
    """

    spending_constraint: Optional[SpendingConstraint] = FieldInfo(alias="spendingConstraint", default=None)
    """The spending constraint applied to the card"""

    user_data: Optional[object] = FieldInfo(alias="userData", default=None)
    """Arbitrary information that can be attached to the card.

    See the [`PATCH /card/{cardId}`](api-reference/card-patch) endpoint for more
    details on how to add user data.
    """

    virtual_account_id: Optional[str] = FieldInfo(alias="virtualAccountId", default=None)
    """The virtual account that this card is associated with"""
