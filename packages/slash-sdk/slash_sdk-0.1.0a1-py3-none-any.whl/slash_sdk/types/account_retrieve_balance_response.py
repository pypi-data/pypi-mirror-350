# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .money import Money
from .._models import BaseModel

__all__ = ["AccountRetrieveBalanceResponse", "Balance"]


class Balance(BaseModel):
    account_id: str = FieldInfo(alias="accountId")
    """The ID of the account associated with the balance."""

    available: Money
    """Represents a monetary value"""

    posted: Money
    """Represents a monetary value"""

    timestamp: datetime
    """The UTC timestamp associated with the balance.

    Since the balance can change rapidly, the timestamp is included to indicate the
    time when the balance was computed.
    """

    type: Literal["cash", "credit", "debit"]
    """The type of balance.

    - "cash" represents the excess balance not used as collateral for the charge
      card. Not applicable to debit accounts.
    - "credit" represents the balance that can be spent on the charge card. Not
      applicable to debit accounts.
    - "debit" represents the balance that can be spent or withdrawn. Not applicable
      to charge card accounts.
    """


class AccountRetrieveBalanceResponse(BaseModel):
    balances: List[Balance]
