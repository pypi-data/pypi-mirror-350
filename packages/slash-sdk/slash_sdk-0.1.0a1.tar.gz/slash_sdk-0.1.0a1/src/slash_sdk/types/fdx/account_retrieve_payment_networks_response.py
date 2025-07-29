# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["AccountRetrievePaymentNetworksResponse", "PaymentNetwork", "Page"]


class PaymentNetwork(BaseModel):
    bank_id: str = FieldInfo(alias="bankId")
    """Bank identifier used by the payment network ie. Routing Number"""

    identifier: str
    """The number used to identify the account within the payment network."""

    transfer_in: bool = FieldInfo(alias="transferIn")
    """Indicates if the account can receive transfers from the payment network.

    If the account is closed or locked, this will be false.
    """

    transfer_out: bool = FieldInfo(alias="transferOut")
    """Indicates if the account can send transfers to the payment network.

    If the account is closed or locked, this will be false.
    """

    type: Literal["US_ACH", "US_FEDWIRE", "US_CHIPS", "US_RTP", "CA_ACSS", "CA_LVTS"]


class Page(BaseModel):
    next_offset: Optional[str] = FieldInfo(alias="nextOffset", default=None)


class AccountRetrievePaymentNetworksResponse(BaseModel):
    payment_networks: List[PaymentNetwork] = FieldInfo(alias="paymentNetworks")

    page: Optional[Page] = None
