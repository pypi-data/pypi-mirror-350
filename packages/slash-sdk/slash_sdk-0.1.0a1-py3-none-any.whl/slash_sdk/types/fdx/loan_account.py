# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["LoanAccount", "Currency"]


class Currency(BaseModel):
    currency_code: str = FieldInfo(alias="currencyCode")
    """The ISO 4217 currency code for the currency that the account is denominated in.

    For example, "USD" for US Dollars.
    """


class LoanAccount(BaseModel):
    account_id: str = FieldInfo(alias="accountId")
    """Long-term persistent identity of the account, though not an account number."""

    account_type: Literal[
        "AUTOLOAN",
        "HOMEEQUITYLOAN",
        "INSTALLMENT",
        "LOAN",
        "MILITARYLOAN",
        "MORTGAGE",
        "PERSONALLOAN",
        "SMBLOAN",
        "STUDENTLOAN",
    ] = FieldInfo(alias="accountType")

    currency: Currency

    product_name: str = FieldInfo(alias="productName")
    """Marketed product name for this account.

    You can use this in UIs to assist in account selection. For example, "Slash
    Platinum".
    """

    status: Literal[
        "CLOSED", "DELINQUENT", "NEGATIVECURRENTBALANCE", "OPEN", "PAID", "PENDINGCLOSE", "PENDINGOPEN", "RESTRICTED"
    ]

    account_number_display: Optional[str] = FieldInfo(alias="accountNumberDisplay", default=None)
    """
    A masked version of the account number, which includes the last 4 digits in
    plain text.
    """

    nickname: Optional[str] = None
    """A nickname or label for the account.

    This will be unique to the account, even if the user has multiple accounts with
    the same product name. You can use this in UIs to assist in account selection.
    """
