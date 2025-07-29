# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .card.card import Card
from .transaction import Transaction

__all__ = ["TransactionRetrieveFeeDetailsResponse", "Item"]


class Item(BaseModel):
    id: str

    account_id: str = FieldInfo(alias="accountId")

    date_charged: str = FieldInfo(alias="dateCharged")

    fee_amount_cents: float = FieldInfo(alias="feeAmountCents")

    fee_type: str = FieldInfo(alias="feeType")

    card: Optional[Card] = None

    original_transaction: Optional[Transaction] = FieldInfo(alias="originalTransaction", default=None)


class TransactionRetrieveFeeDetailsResponse(BaseModel):
    items: List[Item]
