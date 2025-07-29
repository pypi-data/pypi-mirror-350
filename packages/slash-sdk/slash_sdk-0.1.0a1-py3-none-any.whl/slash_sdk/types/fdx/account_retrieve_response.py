# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from . import loan_account, deposit_account, investment_account
from ..._models import BaseModel
from .line_of_credit_account import LineOfCreditAccount

__all__ = [
    "AccountRetrieveResponse",
    "DepositAccount",
    "DepositAccountDepositAccount",
    "LoanAccount",
    "LoanAccountLoanAccount",
    "LocAccount",
    "LocAccountLocAccount",
    "InvestmentAccount",
    "InvestmentAccountInvestmentAccount",
    "InvestmentAccountInvestmentAccountHolding",
    "InvestmentAccountInvestmentAccountHoldingCurrency",
    "InvestmentAccountInvestmentAccountHoldingFiAttribute",
]


class DepositAccountDepositAccount(deposit_account.DepositAccount):
    available_balance: float = FieldInfo(alias="availableBalance")
    """
    The available balance of the account in the standard unit of the currency (e.g.,
    dollars for USD). Available balance is the balance that is available to
    spend/withdraw.
    """

    current_balance: float = FieldInfo(alias="currentBalance")
    """
    The current balance of the account in the standard unit of the currency (e.g.,
    dollars for USD). Current balance is the balance that is currently in the
    account, including any pending transactions.
    """


class DepositAccount(BaseModel):
    deposit_account: DepositAccountDepositAccount = FieldInfo(alias="depositAccount")
    """A deposit account. For example, a checking, savings or money market account."""


class LoanAccountLoanAccount(loan_account.LoanAccount):
    interest_rate: float = FieldInfo(alias="interestRate")
    """The interest rate on the loan as a floating point number.

    For example, 0.05 for 5%.
    """

    interest_rate_type: Literal["FIXED", "VARIABLE"] = FieldInfo(alias="interestRateType")
    """The type of interest rate on the loan."""

    principal_balance: float = FieldInfo(alias="principalBalance")
    """
    The principal balance of the loan account in the standard unit of the currency
    (e.g., dollars for USD). Principal balance is the amount of the loan that is
    still owed.
    """

    escrow_balance: Optional[float] = FieldInfo(alias="escrowBalance", default=None)
    """
    The escrow balance of the loan account in the standard unit of the currency
    (e.g., dollars for USD). Escrow balance is the amount of money held in escrow to
    pay for property taxes and insurance.
    """

    interest_paid_year_to_date: Optional[float] = FieldInfo(alias="interestPaidYearToDate", default=None)
    """
    The amount of interest paid on the loan year-to-date in the standard unit of the
    currency (e.g., dollars for USD).
    """

    last_payment_amount: Optional[float] = FieldInfo(alias="lastPaymentAmount", default=None)
    """
    The amount of the last payment made on the loan in the standard unit of the
    currency (e.g., dollars for USD).
    """

    last_payment_date: Optional[str] = FieldInfo(alias="lastPaymentDate", default=None)
    """The date the last payment was made."""

    loan_term: Optional[str] = FieldInfo(alias="loanTerm", default=None)
    """The term of the loan in months."""

    maturity_date: Optional[str] = FieldInfo(alias="maturityDate", default=None)
    """The date the loan is scheduled to be paid off."""

    next_payment_amount: Optional[float] = FieldInfo(alias="nextPaymentAmount", default=None)
    """
    The amount of the next payment due on the loan in the standard unit of the
    currency (e.g., dollars for USD).
    """

    next_payment_date: Optional[str] = FieldInfo(alias="nextPaymentDate", default=None)
    """The date the next payment is due."""

    original_principal: Optional[float] = FieldInfo(alias="originalPrincipal", default=None)
    """
    The original principal balance of the loan account in the standard unit of the
    currency (e.g., dollars for USD). Original principal balance is the amount of
    the loan when it was first taken out.
    """

    originating_date: Optional[str] = FieldInfo(alias="originatingDate", default=None)
    """The date the loan was originated."""


class LoanAccount(BaseModel):
    loan_account: LoanAccountLoanAccount = FieldInfo(alias="loanAccount")
    """A loan account. For example, mortgage, student loan or auto loan."""


class LocAccountLocAccount(LineOfCreditAccount):
    available_credit: float = FieldInfo(alias="availableCredit")
    """
    The currently available credit on the account in the standard unit of the
    currency (e.g., dollars for USD).
    """

    current_balance: float = FieldInfo(alias="currentBalance")
    """
    The current balance on the account in the standard unit of the currency (e.g.,
    dollars for USD). This includes any outstanding charges, fees, and interest.
    """

    advances_apr: Optional[float] = FieldInfo(alias="advancesApr", default=None)
    """The annual percentage rate (APR) for cash advances on the account."""

    credit_line: Optional[float] = FieldInfo(alias="creditLine", default=None)
    """
    The total credit line available on the account in the standard unit of the
    currency (e.g., dollars for USD).
    """

    last_payment_amount: Optional[float] = FieldInfo(alias="lastPaymentAmount", default=None)
    """
    The amount of the last payment made on the account in the standard unit of the
    currency (e.g., dollars for USD).
    """

    last_payment_date: Optional[str] = FieldInfo(alias="lastPaymentDate", default=None)
    """The date the last payment was made."""

    last_stmt_balance: Optional[float] = FieldInfo(alias="lastStmtBalance", default=None)
    """
    The balance on the account as of the last statement date in the standard unit of
    the currency (e.g., dollars for USD).
    """

    last_stmt_date: Optional[str] = FieldInfo(alias="lastStmtDate", default=None)
    """The date of the last statement."""

    minimum_payment_amount: Optional[float] = FieldInfo(alias="minimumPaymentAmount", default=None)
    """
    The minimum payment due on the account in the standard unit of the currency
    (e.g., dollars for USD).
    """

    next_payment_amount: Optional[float] = FieldInfo(alias="nextPaymentAmount", default=None)
    """
    The amount of the next payment due on the account in the standard unit of the
    currency (e.g., dollars for USD).
    """

    next_payment_date: Optional[str] = FieldInfo(alias="nextPaymentDate", default=None)
    """The date the next payment is due."""

    past_due_amount: Optional[float] = FieldInfo(alias="pastDueAmount", default=None)
    """
    The amount past due on the account in the standard unit of the currency (e.g.,
    dollars for USD).
    """

    principal_balance: Optional[float] = FieldInfo(alias="principalBalance", default=None)
    """
    The principal balance on the account in the standard unit of the currency (e.g.,
    dollars for USD).
    """

    purchases_apr: Optional[float] = FieldInfo(alias="purchasesApr", default=None)
    """The annual percentage rate (APR) for purchases on the account."""


class LocAccount(BaseModel):
    loc_account: LocAccountLocAccount = FieldInfo(alias="locAccount")
    """A line-of-credit account.

    For example, a credit card or home equity line of credit.
    """


class InvestmentAccountInvestmentAccountHoldingCurrency(BaseModel):
    currency_code: str = FieldInfo(alias="currencyCode")
    """The ISO 4217 currency code."""


class InvestmentAccountInvestmentAccountHoldingFiAttribute(BaseModel):
    name: str

    value: str


class InvestmentAccountInvestmentAccountHolding(BaseModel):
    cash_account: bool = FieldInfo(alias="cashAccount")
    """
    If true, indicates that this holding is used to maintain proceeds from sales,
    dividends, and other cash postings to the investment account.
    """

    market_value: float = FieldInfo(alias="marketValue")
    """
    The market value of the holding in the standard unit of the currency (e.g.,
    dollars for USD).
    """

    currency: Optional[InvestmentAccountInvestmentAccountHoldingCurrency] = None

    current_unit_price: Optional[float] = FieldInfo(alias="currentUnitPrice", default=None)
    """
    The current unit price of the security in the standard unit of the currency
    (e.g., dollars for USD).
    """

    current_unit_price_date: Optional[str] = FieldInfo(alias="currentUnitPriceDate", default=None)
    """The date and time the current unit price was last updated."""

    face_value: Optional[float] = FieldInfo(alias="faceValue", default=None)
    """
    The face value of the holding in the standard unit of the currency (e.g.,
    dollars for USD).
    """

    fi_attributes: Optional[List[InvestmentAccountInvestmentAccountHoldingFiAttribute]] = FieldInfo(
        alias="fiAttributes", default=None
    )

    holding_name: Optional[str] = FieldInfo(alias="holdingName", default=None)
    """The name of the security."""

    holding_sub_type: Optional[Literal["CASH", "MONEYMARKET"]] = FieldInfo(alias="holdingSubType", default=None)

    holding_type: Optional[
        Literal["ANNUITY", "BOND", "CD", "DIGITALASSET", "MUTUALFUND", "OPTION", "OTHER", "STOCK"]
    ] = FieldInfo(alias="holdingType", default=None)
    """The type of the holding."""

    purchased_price: Optional[float] = FieldInfo(alias="purchasedPrice", default=None)
    """
    The price at which the security was purchased in the standard unit of the
    currency (e.g., dollars for USD).
    """

    security_id: Optional[str] = FieldInfo(alias="securityId", default=None)
    """The unique identifier of the security.

    Either securityId and securityIdType or symbol will be provided.
    """

    security_id_type: Optional[
        Literal["CINS", "CMC", "CME", "CUSIP", "ISIN", "ITSA", "NASDAQ", "SEDOL", "SICC", "VALOR", "WKN"]
    ] = FieldInfo(alias="securityIdType", default=None)
    """The type of the security identifier."""

    symbol: Optional[str] = None
    """The symbol of the security.

    Either securityId and securityIdType or symbol will be provided.
    """

    units: Optional[float] = None
    """The number of units of the security held."""


class InvestmentAccountInvestmentAccount(investment_account.InvestmentAccount):
    available_cash_balance: float = FieldInfo(alias="availableCashBalance")
    """
    The amount of cash available in the account across all sub-accounts, including
    sweep funds, in the standard unit of the currency (e.g., dollars for USD).
    """

    current_value: float = FieldInfo(alias="currentValue")
    """
    The total current value of all investments in the standard unit of the currency
    (e.g., dollars for USD).
    """

    balance_as_of: Optional[str] = FieldInfo(alias="balanceAsOf", default=None)
    """The date and time the balance was last updated."""

    holdings: Optional[List[InvestmentAccountInvestmentAccountHolding]] = None
    """The holdings in the account."""


class InvestmentAccount(BaseModel):
    investment_account: InvestmentAccountInvestmentAccount = FieldInfo(alias="investmentAccount")
    """An investment account. For example, a 401K or IRA."""


AccountRetrieveResponse: TypeAlias = Union[DepositAccount, LoanAccount, LocAccount, InvestmentAccount]
