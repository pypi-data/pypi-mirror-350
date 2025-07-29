# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo
from .restriction import Restriction
from ..money_param import MoneyParam

__all__ = [
    "SpendingConstraintUpdatePartialParams",
    "CountryRule",
    "MerchantCategoryCodeRule",
    "MerchantCategoryRule",
    "MerchantRule",
    "SpendingRule",
    "SpendingRuleTransactionSizeLimit",
    "SpendingRuleUtilizationLimit",
    "SpendingRuleUtilizationLimitV2",
]


class SpendingConstraintUpdatePartialParams(TypedDict, total=False):
    country_rule: Annotated[Optional[CountryRule], PropertyInfo(alias="countryRule")]

    merchant_category_code_rule: Annotated[
        Optional[MerchantCategoryCodeRule], PropertyInfo(alias="merchantCategoryCodeRule")
    ]

    merchant_category_rule: Annotated[Optional[MerchantCategoryRule], PropertyInfo(alias="merchantCategoryRule")]

    merchant_rule: Annotated[Optional[MerchantRule], PropertyInfo(alias="merchantRule")]

    spending_rule: Annotated[Optional[SpendingRule], PropertyInfo(alias="spendingRule")]


class CountryRule(TypedDict, total=False):
    countries: List[str]
    """A 2 digit country code"""

    restriction: Restriction


class MerchantCategoryCodeRule(TypedDict, total=False):
    merchant_category_codes: Annotated[List[str], PropertyInfo(alias="merchantCategoryCodes")]

    restriction: Restriction


class MerchantCategoryRule(TypedDict, total=False):
    merchant_categories: Annotated[List[str], PropertyInfo(alias="merchantCategories")]

    restriction: Restriction


class MerchantRule(TypedDict, total=False):
    merchants: List[str]

    restriction: Restriction


class SpendingRuleTransactionSizeLimit(TypedDict, total=False):
    maximum: MoneyParam
    """Represents a monetary value"""

    minimum: MoneyParam
    """Represents a monetary value"""


class SpendingRuleUtilizationLimit(TypedDict, total=False):
    limit_amount: Annotated[MoneyParam, PropertyInfo(alias="limitAmount")]
    """Represents a monetary value"""

    preset: Literal["daily", "weekly", "monthly", "yearly", "collective"]

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """Format ISO-8601.

    A day that equals today or the past. This is optional.If the `preset` is
    "daily", this value is ignored. If the `preset` is "weekly", "monthly" or
    "yearly", then the this value is used to compute when the limit should start
    limit.
    """

    timezone: str
    """IANA timezone string.

    Limits always reset at midnight of the timezone specified. If no timezone is
    specified, then UTC time is used.
    """


class SpendingRuleUtilizationLimitV2(TypedDict, total=False):
    limit_amount: Annotated[MoneyParam, PropertyInfo(alias="limitAmount")]
    """Represents a monetary value"""

    preset: Literal["daily", "weekly", "monthly", "yearly", "collective"]

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """Format ISO-8601.

    A day that equals today or the past. This is optional.If the `preset` is
    "daily", this value is ignored. If the `preset` is "weekly", "monthly" or
    "yearly", then the this value is used to compute when the limit should start
    limit.
    """

    timezone: str
    """IANA timezone string.

    Limits always reset at midnight of the timezone specified. If no timezone is
    specified, then UTC time is used.
    """


class SpendingRule(TypedDict, total=False):
    transaction_size_limit: Annotated[SpendingRuleTransactionSizeLimit, PropertyInfo(alias="transactionSizeLimit")]

    utilization_limit: Annotated[SpendingRuleUtilizationLimit, PropertyInfo(alias="utilizationLimit")]

    utilization_limit_v2: Annotated[Iterable[SpendingRuleUtilizationLimitV2], PropertyInfo(alias="utilizationLimitV2")]
