# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CryptoCreateOfframpResponse", "Address", "Wallet"]


class Address(BaseModel):
    id: str

    address: str

    chain: Literal["ethereum", "avalanche", "base", "optimism", "polygon", "arbitrum", "solana", "stellar", "tron"]

    currency: Literal["usdc", "usdt"]

    status: Literal["pending_active", "active", "deactivated"]

    timestamp: datetime

    wallet_id: str = FieldInfo(alias="walletId")

    blockchain_memo: Optional[str] = FieldInfo(alias="blockchainMemo", default=None)

    method: Optional[Literal["wire", "ach"]] = None


class Wallet(BaseModel):
    id: str

    slash_account_group_id: str = FieldInfo(alias="slashAccountGroupId")

    status: Literal["pending_active", "active", "deactivated"]

    subaccount_id: str = FieldInfo(alias="subaccountId")

    timestamp: datetime

    type: Literal["off_ramp"]


class CryptoCreateOfframpResponse(BaseModel):
    addresses: List[Address]

    wallet: Wallet
