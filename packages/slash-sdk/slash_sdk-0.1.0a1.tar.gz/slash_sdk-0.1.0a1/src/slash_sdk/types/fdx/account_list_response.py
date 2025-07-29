# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .loan_account import LoanAccount
from .deposit_account import DepositAccount
from .investment_account import InvestmentAccount
from .line_of_credit_account import LineOfCreditAccount

__all__ = [
    "AccountListResponse",
    "Account",
    "AccountDepositAccount",
    "AccountLoanAccount",
    "AccountLocAccount",
    "AccountInvestmentAccount",
    "AccountInsuranceAccount",
    "AccountInsuranceAccountInsuranceAccount",
    "AccountInsuranceAccountInsuranceAccountCurrency",
    "AccountAnnuityAccount",
    "AccountAnnuityAccountAnnuityAccount",
    "AccountAnnuityAccountAnnuityAccountCurrency",
    "AccountCommercialAccount",
    "AccountCommercialAccountCommercialAccount",
    "AccountCommercialAccountCommercialAccountCurrency",
    "Page",
]


class AccountDepositAccount(BaseModel):
    deposit_account: DepositAccount = FieldInfo(alias="depositAccount")
    """A deposit account. For example, a checking, savings or money market account."""


class AccountLoanAccount(BaseModel):
    loan_account: LoanAccount = FieldInfo(alias="loanAccount")
    """A loan account. For example, mortgage, student loan or auto loan."""


class AccountLocAccount(BaseModel):
    loc_account: LineOfCreditAccount = FieldInfo(alias="locAccount")
    """A line-of-credit account.

    For example, a credit card or home equity line of credit.
    """


class AccountInvestmentAccount(BaseModel):
    investment_account: InvestmentAccount = FieldInfo(alias="investmentAccount")
    """An investment account. For example, a 401K or IRA."""


class AccountInsuranceAccountInsuranceAccountCurrency(BaseModel):
    currency_code: str = FieldInfo(alias="currencyCode")
    """The ISO 4217 currency code for the currency that the account is denominated in.

    For example, "USD" for US Dollars.
    """


class AccountInsuranceAccountInsuranceAccount(BaseModel):
    account_id: str = FieldInfo(alias="accountId")
    """Long-term persistent identity of the account, though not an account number."""

    account_type: Literal["LONGTERMDISABILITY", "SHORTTERMDISABILITY", "UNIVERSALLIFE", "WHOLELIFE"] = FieldInfo(
        alias="accountType"
    )

    currency: AccountInsuranceAccountInsuranceAccountCurrency

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


class AccountInsuranceAccount(BaseModel):
    insurance_account: AccountInsuranceAccountInsuranceAccount = FieldInfo(alias="insuranceAccount")
    """An insurance account.

    For example, whole life insurance or short-term disability.
    """


class AccountAnnuityAccountAnnuityAccountCurrency(BaseModel):
    currency_code: str = FieldInfo(alias="currencyCode")
    """The ISO 4217 currency code for the currency that the account is denominated in.

    For example, "USD" for US Dollars.
    """


class AccountAnnuityAccountAnnuityAccount(BaseModel):
    account_id: str = FieldInfo(alias="accountId")
    """Long-term persistent identity of the account, though not an account number."""

    account_type: Literal["ANNUITY", "FIXEDANNUITY", "VARIABLEANNUITY"] = FieldInfo(alias="accountType")

    currency: AccountAnnuityAccountAnnuityAccountCurrency

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


class AccountAnnuityAccount(BaseModel):
    annuity_account: AccountAnnuityAccountAnnuityAccount = FieldInfo(alias="annuityAccount")
    """An annuity account. For example, a fixed or variable annuity account."""


class AccountCommercialAccountCommercialAccountCurrency(BaseModel):
    currency_code: str = FieldInfo(alias="currencyCode")
    """The ISO 4217 currency code for the currency that the account is denominated in.

    For example, "USD" for US Dollars.
    """


class AccountCommercialAccountCommercialAccount(BaseModel):
    account_id: str = FieldInfo(alias="accountId")
    """Long-term persistent identity of the account, though not an account number."""

    account_type: Literal["COMMERCIALDEPOSIT", "COMMERCIALLOAN", "COMMERCIALLINEOFCREDIT", "COMMERCIALINVESTMENT"] = (
        FieldInfo(alias="accountType")
    )

    currency: AccountCommercialAccountCommercialAccountCurrency

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


class AccountCommercialAccount(BaseModel):
    commercial_account: AccountCommercialAccountCommercialAccount = FieldInfo(alias="commercialAccount")
    """A commercial account. For example, a business deposit account."""


Account: TypeAlias = Union[
    AccountDepositAccount,
    AccountLoanAccount,
    AccountLocAccount,
    AccountInvestmentAccount,
    AccountInsuranceAccount,
    AccountAnnuityAccount,
    AccountCommercialAccount,
]


class Page(BaseModel):
    next_offset: Optional[str] = FieldInfo(alias="nextOffset", default=None)


class AccountListResponse(BaseModel):
    accounts: List[Account]

    page: Optional[Page] = None
