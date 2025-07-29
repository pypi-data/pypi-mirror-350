# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Transaction", "MerchantData", "MerchantDataLocation", "OriginalCurrency"]


class MerchantDataLocation(BaseModel):
    city: str
    """The city of the merchant."""

    country: str
    """The country of the merchant."""

    state: str
    """The state/province of the merchant."""

    zip: str
    """The ZIP/postal code of the merchant."""


class MerchantData(BaseModel):
    category_code: str = FieldInfo(alias="categoryCode")
    """The merchant's category code (MCC)"""

    description: str
    """The raw description provided by the merchant for the transaction."""

    location: Optional[MerchantDataLocation] = None
    """Location details for the merchant/transaction."""


class OriginalCurrency(BaseModel):
    amount_cents: float = FieldInfo(alias="amountCents")
    """The amount of the transaction in its original currency in cents."""

    code: str
    """The original currency code of the transaction"""

    conversion_rate: float = FieldInfo(alias="conversionRate")
    """
    The conversion rate used to convert the transaction amount from its original
    currency to the account currency. The currency rate is computed at the time of
    the transaction.
    """


class Transaction(BaseModel):
    id: str

    account_id: str = FieldInfo(alias="accountId")
    """The account ID associated with the transaction"""

    account_subtype: Literal["cash", "credit"] = FieldInfo(alias="accountSubtype")
    """
    For charge cards, specifies if the transaction belongs to the cash or credit
    account. For debit accounts, this field is always cash.
    """

    amount_cents: float = FieldInfo(alias="amountCents")
    """The amount of the transaction in cents in USD.

    If the transaction amount is negative, the transaction is a debit. If the
    transaction amount is positive, the transaction is a credit.
    """

    date: str
    """The date in UTC time when the transaction was posted.

    If the transaction is pending or failed, this is the date the transaction was
    created.
    """

    description: str

    detailed_status: Literal[
        "pending",
        "pending_approval",
        "canceled",
        "failed",
        "settled",
        "declined",
        "refund",
        "reversed",
        "returned",
        "dispute",
    ] = FieldInfo(alias="detailedStatus")
    """- `pending_approval`: Used for any transaction type that is pending approval.

    This does not affect the account's available or posted balances.

    - `pending`: Used for any transaction type that has not posted to the account
      yet, but is affecting the account's available balance.
    - `canceled`: Used for any transaction that was canceled.
    - `failed`: Used for any transaction that failed to post to the account.
    - `settled`: Used for any transaction that has posted to the account, except for
      card refunds, which use the `refund` status, and ACH returns, which use the
      `returned` status.
    - `declined`: Used for card transactions that were declined.
    - `refund`: Used for card transactions that were refunded, increasing the
      account's available and posted balances.
    - `reversed`: Used for card transactions that were authorized, but reversed by
      the merchant.
    - `returned`: Used for ACH returns. In the case of an ACH return, there are two
      possibilities: (1) if the ACH settled and then returned, then there will be
      one transaction with status `settled` for the ACH settling, and one
      transaction with status `returned` for the ACH return. Both of these are
      posted transactions. (2) if the ACH returned before settling, then there will
      only be one transaction with status `canceled`.
    - `dispute`: Used for disputed card transactions.
    """

    status: Literal["pending", "posted", "failed"]
    """
    - `pending`: The transaction is pending and has not been posted to the account
      yet (the account's posted balance doesn't reflect the transaction yet, but the
      account's available balance does).
    - `posted`: The transaction has been posted to the account and the account's
      posted balance and available balances both reflect the transaction.
    - `failed`: The transaction failed to post to the account and no longer affects
      the account's available or posted balances.
    """

    authorized_at: Optional[str] = FieldInfo(alias="authorizedAt", default=None)
    """The UTC timestamp of when the transaction was authorized.

    Only exists for card transactions.
    """

    card_id: Optional[str] = FieldInfo(alias="cardId", default=None)
    """The card ID associated with the transaction.

    If the transaction is not associated with a card, this field is not sent.
    """

    decline_reason: Optional[str] = FieldInfo(alias="declineReason", default=None)
    """The reason for the decline.

    Only exists for card transactions with `detailedStatus` = `declined`.
    """

    memo: Optional[str] = None
    """The memo associated with the transaction for wires and achs"""

    merchant_data: Optional[MerchantData] = FieldInfo(alias="merchantData", default=None)
    """
    For card transactions, contains description of the transaction as reported by
    the merchant, merchant category code, and location of the merchant or origin of
    the transaction. For other transactions, this field is undefined.
    """

    merchant_description: Optional[str] = FieldInfo(alias="merchantDescription", default=None)
    """DEPRECATED.

    Use `merchantData.description` instead. For card transactions, the description
    of the transaction as reported by the merchant. For other transactions, this
    field is undefined.
    """

    order_id: Optional[str] = FieldInfo(alias="orderId", default=None)
    """
    The order ID, as reported by the merchant, associated with the specific
    transaction.
    """

    original_currency: Optional[OriginalCurrency] = FieldInfo(alias="originalCurrency", default=None)
    """The original currency of the transaction.

    This is only applicable to transactions. If this field is not sent, the original
    currency is in USD.
    """

    reference_number: Optional[str] = FieldInfo(alias="referenceNumber", default=None)
    """The reference number provided by Visa for this transaction."""
