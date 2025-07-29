# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Account"]


class Account(BaseModel):
    id: str

    account_number: str = FieldInfo(alias="accountNumber")

    balances: List[Literal["debit", "cash", "credit"]]

    created_at: datetime = FieldInfo(alias="createdAt")

    name: str

    routing_number: str = FieldInfo(alias="routingNumber")

    status: Literal["open", "closed"]

    type: Literal["debit", "charge_card"]
    """The type of account.

    - "debit" represents a debit card account - "charge_card" represents a charge
      card account
    """
