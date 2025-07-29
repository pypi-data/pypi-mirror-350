# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .card.spending_constraint_param import SpendingConstraintParam

__all__ = ["CardCreateParams"]


class CardCreateParams(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["virtual"]]
    """Specify the type of card you'd like to create.

    At the moment, only virtual cards are supported.
    """

    account_id: Annotated[str, PropertyInfo(alias="accountId")]
    """The ID of the account to create the card under.

    You can get this by calling `GET /account`. This field is required unless you
    are authenticating via API key, in which case it will default to your first
    commercial account. We recommend supplying this even if you are authenticating
    via API key.
    """

    card_group_id: Annotated[str, PropertyInfo(alias="cardGroupId")]

    card_product_id: Annotated[str, PropertyInfo(alias="cardProductId")]
    """
    The ID of the card product to use when creating this card, if not specified a
    random card product will be chosen.
    """

    is_single_use: Annotated[bool, PropertyInfo(alias="isSingleUse")]
    """Defaults to false.

    When set to true, the card will be automatically closed after a single
    authorization attempt. Note that the card will be closed even if the
    authorization declines or drops
    """

    spending_constraint: Annotated[SpendingConstraintParam, PropertyInfo(alias="spendingConstraint")]
    """A constraint that can be applied to a CardGroupSpendingRule"""

    user_data: Annotated[Dict[str, object], PropertyInfo(alias="userData")]
    """Arbitrary information that can be attached to the card.

    This should be a JSON object and cannot exceed 4kb.
    """

    virtual_account_id: Annotated[str, PropertyInfo(alias="virtualAccountId")]
    """The ID of the virtual account to create the card under.

    Virtual accounts can be retrieved by calling `GET /virtual-account`.
    """
