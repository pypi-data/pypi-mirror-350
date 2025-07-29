# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "AccountListTransactionsResponse",
    "Transaction",
    "TransactionDepositTransaction",
    "TransactionDepositTransactionDepositTransaction",
    "TransactionLoanTransaction",
    "TransactionLoanTransactionLoanTransaction",
    "TransactionLocTransaction",
    "TransactionLocTransactionLocTransaction",
    "TransactionInvestmentTransaction",
    "TransactionInvestmentTransactionInvestmentTransaction",
    "TransactionInvestmentTransactionInvestmentTransactionFiAttribute",
    "Page",
]


class TransactionDepositTransactionDepositTransaction(BaseModel):
    amount: float
    """
    The amount of money in the account currency in that currency's standard unit
    (e.g. dollars for USD). The amount is an absolute value. The debitCreditMemo
    parameter indicates the direction of the transaction.
    """

    debit_credit_memo: Literal["DEBIT", "CREDIT", "MEMO"] = FieldInfo(alias="debitCreditMemo")
    """The posting type of a transaction.

    The transaction amount is an absolute value, and this parameter indicates the
    direction of the transaction. This will always be DEBIT or CREDIT.
    """

    description: str
    """A description of the transaction."""

    status: Literal["AUTHORIZATION", "MEMO", "PENDING", "PENDING_APPROVAL", "POSTED"]
    """The status of the transaction. This will always be PENDING or POSTED."""

    transaction_id: str = FieldInfo(alias="transactionId")
    """Long-term persistent identity of the transaction."""

    transaction_timestamp: str = FieldInfo(alias="transactionTimestamp")
    """The ISO 8601 date and time that the transaction was initiated."""

    category: Optional[str] = None
    """The merchant category code (MCC) of the transaction, if available."""

    check_number: Optional[str] = FieldInfo(alias="checkNumber", default=None)
    """The check number of the transaction, if available.

    Only included if this is a check transaction.
    """

    foreign_amount: Optional[float] = FieldInfo(alias="foreignAmount", default=None)
    """
    This value is only included if the transaction's currency is different than the
    account's default currency.
    """

    foreign_currency: Optional[str] = FieldInfo(alias="foreignCurrency", default=None)
    """ISO 4217 currency code.

    This value is only included if the transaction's currency is different than the
    account's default currency.
    """

    payee: Optional[str] = None

    posted_timestamp: Optional[str] = FieldInfo(alias="postedTimestamp", default=None)
    """The ISO 8601 date and time that the transaction was posted to the account.

    This will be included if status is POSTED.
    """

    reference_transaction_id: Optional[str] = FieldInfo(alias="referenceTransactionId", default=None)
    """For reverse postings, the identity of the transaction being reversed.

    For the correction transaction, the identity of the reversing post. For credit
    card posting transactions, the identity of the authorization transaction
    """

    sub_category: Optional[str] = FieldInfo(alias="subCategory", default=None)
    """Additional information about the transaction category, if available."""


class TransactionDepositTransaction(BaseModel):
    deposit_transaction: TransactionDepositTransactionDepositTransaction = FieldInfo(alias="depositTransaction")


class TransactionLoanTransactionLoanTransaction(BaseModel):
    amount: float
    """
    The amount of money in the account currency in that currency's standard unit
    (e.g. dollars for USD). The amount is an absolute value. The debitCreditMemo
    parameter indicates the direction of the transaction.
    """

    debit_credit_memo: Literal["DEBIT", "CREDIT", "MEMO"] = FieldInfo(alias="debitCreditMemo")
    """The posting type of a transaction.

    The transaction amount is an absolute value, and this parameter indicates the
    direction of the transaction. This will always be DEBIT or CREDIT.
    """

    description: str
    """A description of the transaction."""

    status: Literal["AUTHORIZATION", "MEMO", "PENDING", "POSTED"]
    """The status of the transaction. This will always be PENDING or POSTED."""

    transaction_id: str = FieldInfo(alias="transactionId")
    """Long-term persistent identity of the transaction."""

    transaction_timestamp: str = FieldInfo(alias="transactionTimestamp")
    """The ISO 8601 date and time that the transaction was initiated."""

    category: Optional[str] = None
    """The merchant category code (MCC) of the transaction, if available."""

    foreign_amount: Optional[float] = FieldInfo(alias="foreignAmount", default=None)
    """
    This value is only included if the transaction's currency is different than the
    account's default currency.
    """

    foreign_currency: Optional[str] = FieldInfo(alias="foreignCurrency", default=None)
    """ISO 4217 currency code.

    This value is only included if the transaction's currency is different than the
    account's default currency.
    """

    posted_timestamp: Optional[str] = FieldInfo(alias="postedTimestamp", default=None)
    """The ISO 8601 date and time that the transaction was posted to the account.

    This will be included if status is POSTED.
    """

    reference_transaction_id: Optional[str] = FieldInfo(alias="referenceTransactionId", default=None)
    """For reverse postings, the identity of the transaction being reversed.

    For the correction transaction, the identity of the reversing post. For credit
    card posting transactions, the identity of the authorization transaction
    """

    sub_category: Optional[str] = FieldInfo(alias="subCategory", default=None)
    """Additional information about the transaction category, if available."""

    transaction_type: Optional[
        Literal[
            "ADJUSTMENT",
            "FEE",
            "INTEREST",
            "PAYMENT",
            "LUMP_SUM_PAYMENT",
            "SKIP_PAYMENT",
            "DOUBLE_UP_PAYMENT",
            "PAYOFF",
        ]
    ] = FieldInfo(alias="transactionType", default=None)


class TransactionLoanTransaction(BaseModel):
    loan_transaction: TransactionLoanTransactionLoanTransaction = FieldInfo(alias="loanTransaction")


class TransactionLocTransactionLocTransaction(BaseModel):
    amount: float
    """
    The amount of money in the account currency in that currency's standard unit
    (e.g. dollars for USD). The amount is an absolute value. The debitCreditMemo
    parameter indicates the direction of the transaction.
    """

    debit_credit_memo: Literal["DEBIT", "CREDIT", "MEMO"] = FieldInfo(alias="debitCreditMemo")
    """The posting type of a transaction.

    The transaction amount is an absolute value, and this parameter indicates the
    direction of the transaction. This will always be DEBIT or CREDIT.
    """

    description: str
    """A description of the transaction."""

    status: Literal["AUTHORIZATION", "MEMO", "PENDING", "PENDING_APPROVAL", "POSTED"]
    """The status of the transaction. This will always be PENDING or POSTED."""

    transaction_id: str = FieldInfo(alias="transactionId")
    """Long-term persistent identity of the transaction."""

    transaction_timestamp: str = FieldInfo(alias="transactionTimestamp")
    """The ISO 8601 date and time that the transaction was initiated."""

    category: Optional[str] = None
    """The merchant category code (MCC) of the transaction, if available."""

    check_number: Optional[float] = FieldInfo(alias="checkNumber", default=None)
    """The check number of the transaction, if available.

    Only included if transactionType is CHECK.
    """

    foreign_amount: Optional[float] = FieldInfo(alias="foreignAmount", default=None)
    """
    This value is only included if the transaction's currency is different than the
    account's default currency.
    """

    foreign_currency: Optional[str] = FieldInfo(alias="foreignCurrency", default=None)
    """ISO 4217 currency code.

    This value is only included if the transaction's currency is different than the
    account's default currency.
    """

    posted_timestamp: Optional[str] = FieldInfo(alias="postedTimestamp", default=None)
    """The ISO 8601 date and time that the transaction was posted to the account.

    This will be included if status is POSTED.
    """

    reference_transaction_id: Optional[str] = FieldInfo(alias="referenceTransactionId", default=None)
    """For reverse postings, the identity of the transaction being reversed.

    For the correction transaction, the identity of the reversing post. For credit
    card posting transactions, the identity of the authorization transaction
    """

    sub_category: Optional[str] = FieldInfo(alias="subCategory", default=None)
    """Additional information about the transaction category, if available."""

    transaction_type: Optional[
        Literal["ADJUSTMENT", "CHECK", "FEE", "INTEREST", "PAYMENT", "WITHDRAWAL", "PURCHASE"]
    ] = FieldInfo(alias="transactionType", default=None)


class TransactionLocTransaction(BaseModel):
    loc_transaction: TransactionLocTransactionLocTransaction = FieldInfo(alias="locTransaction")


class TransactionInvestmentTransactionInvestmentTransactionFiAttribute(BaseModel):
    name: str

    value: str


class TransactionInvestmentTransactionInvestmentTransaction(BaseModel):
    amount: float
    """
    The amount of money in the account currency in that currency's standard unit
    (e.g. dollars for USD). The amount is an absolute value. The debitCreditMemo
    parameter indicates the direction of the transaction.
    """

    debit_credit_memo: Literal["DEBIT", "CREDIT", "MEMO"] = FieldInfo(alias="debitCreditMemo")
    """The posting type of a transaction.

    The transaction amount is an absolute value, and this parameter indicates the
    direction of the transaction. This will always be DEBIT or CREDIT.
    """

    description: str
    """A description of the transaction."""

    fees: float

    status: Literal["AUTHORIZATION", "MEMO", "PENDING", "POSTED"]
    """The status of the transaction. This will always be PENDING or POSTED."""

    transaction_id: str = FieldInfo(alias="transactionId")
    """Long-term persistent identity of the transaction."""

    transaction_timestamp: str = FieldInfo(alias="transactionTimestamp")
    """The ISO 8601 date and time that the transaction was initiated."""

    category: Optional[str] = None
    """The merchant category code (MCC) of the transaction, if available."""

    commission: Optional[float] = None

    fi_attributes: Optional[List[TransactionInvestmentTransactionInvestmentTransactionFiAttribute]] = FieldInfo(
        alias="fiAttributes", default=None
    )

    foreign_amount: Optional[float] = FieldInfo(alias="foreignAmount", default=None)
    """
    This value is only included if the transaction's currency is different than the
    account's default currency.
    """

    foreign_currency: Optional[str] = FieldInfo(alias="foreignCurrency", default=None)
    """ISO 4217 currency code.

    This value is only included if the transaction's currency is different than the
    account's default currency.
    """

    posted_timestamp: Optional[str] = FieldInfo(alias="postedTimestamp", default=None)
    """The ISO 8601 date and time that the transaction was posted to the account.

    This will be included if status is POSTED.
    """

    reference_transaction_id: Optional[str] = FieldInfo(alias="referenceTransactionId", default=None)
    """For reverse postings, the identity of the transaction being reversed.

    For the correction transaction, the identity of the reversing post. For credit
    card posting transactions, the identity of the authorization transaction
    """

    security_id: Optional[str] = FieldInfo(alias="securityId", default=None)
    """The security identifier for the transaction, if applicable."""

    security_id_type: Optional[
        Literal["CINS", "CMC", "CME", "CUSIP", "ISIN", "ITSA", "NASDAQ", "SEDOL", "SICC", "VALOR", "WKN"]
    ] = FieldInfo(alias="securityIdType", default=None)

    security_type: Optional[
        Literal["BOND", "DEBT", "DIGITALASSET", "MUTUALFUND", "OPTION", "OTHER", "STOCK", "SWEEP"]
    ] = FieldInfo(alias="securityType", default=None)

    sub_category: Optional[str] = FieldInfo(alias="subCategory", default=None)
    """Additional information about the transaction category, if available."""

    symbol: Optional[str] = None
    """Ticker symbol"""

    transaction_type: Optional[
        Literal[
            "ADJUSTMENT",
            "ATM",
            "CASH",
            "CHECK",
            "CLOSURE",
            "CLOSUREOPT",
            "CONTRIBUTION",
            "DEP",
            "DEPOSIT",
            "DIRECTDEBIT",
            "DIRECTDEP",
            "DIV",
            "DIVIDEND",
            "DIVIDENDREINVEST",
            "EXPENSE",
            "FEE",
            "INCOME",
            "INTEREST",
            "INVEXPENSE",
            "JRNLFUND",
            "JRNLSEC",
            "MARGININTEREST",
            "OPTIONEXERCISE",
            "OPTIONEXPIRATION",
            "OTHER",
            "PAYMENT",
            "POS",
            "PURCHASED",
            "PURCHASEDTOCOVER",
            "PURCHASETOCLOSE",
            "PURCHASETOOPEN",
            "REINVESTOFINCOME",
            "REPEATPMT",
            "RETURNOFCAPITAL",
            "SOLD",
            "SOLDTOCLOSE",
            "SOLDTOOPEN",
            "SPLIT",
            "SRVCHG",
            "TRANSFER",
            "XFER",
        ]
    ] = FieldInfo(alias="transactionType", default=None)

    unit_price: Optional[float] = FieldInfo(alias="unitPrice", default=None)

    units: Optional[float] = None

    unit_type: Optional[Literal["CURRENCY", "SHARES"]] = FieldInfo(alias="unitType", default=None)


class TransactionInvestmentTransaction(BaseModel):
    investment_transaction: TransactionInvestmentTransactionInvestmentTransaction = FieldInfo(
        alias="investmentTransaction"
    )


Transaction: TypeAlias = Union[
    TransactionDepositTransaction,
    TransactionLoanTransaction,
    TransactionLocTransaction,
    TransactionInvestmentTransaction,
]


class Page(BaseModel):
    next_offset: Optional[str] = FieldInfo(alias="nextOffset", default=None)


class AccountListTransactionsResponse(BaseModel):
    transactions: List[Transaction]

    page: Optional[Page] = None
