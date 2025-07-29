# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..money import Money
from ..._models import BaseModel
from .restriction import Restriction

__all__ = [
    "SpendingConstraint",
    "CountryRule",
    "MerchantCategoryCodeRule",
    "MerchantCategoryRule",
    "MerchantRule",
    "SpendingRule",
    "SpendingRuleTransactionSizeLimit",
    "SpendingRuleUtilizationLimit",
    "SpendingRuleUtilizationLimitV2",
]


class CountryRule(BaseModel):
    countries: List[str]
    """A 2 digit country code"""

    restriction: Restriction


class MerchantCategoryCodeRule(BaseModel):
    merchant_category_codes: List[str] = FieldInfo(alias="merchantCategoryCodes")

    restriction: Restriction


class MerchantCategoryRule(BaseModel):
    merchant_categories: List[str] = FieldInfo(alias="merchantCategories")

    restriction: Restriction


class MerchantRule(BaseModel):
    merchants: List[str]

    restriction: Restriction


class SpendingRuleTransactionSizeLimit(BaseModel):
    maximum: Optional[Money] = None
    """Represents a monetary value"""

    minimum: Optional[Money] = None
    """Represents a monetary value"""


class SpendingRuleUtilizationLimit(BaseModel):
    limit_amount: Money = FieldInfo(alias="limitAmount")
    """Represents a monetary value"""

    preset: Literal["daily", "weekly", "monthly", "yearly", "collective"]

    start_date: Optional[str] = FieldInfo(alias="startDate", default=None)
    """Format ISO-8601.

    A day that equals today or the past. This is optional.If the `preset` is
    "daily", this value is ignored. If the `preset` is "weekly", "monthly" or
    "yearly", then the this value is used to compute when the limit should start
    limit.
    """

    timezone: Optional[str] = None
    """IANA timezone string.

    Limits always reset at midnight of the timezone specified. If no timezone is
    specified, then UTC time is used.
    """


class SpendingRuleUtilizationLimitV2(BaseModel):
    limit_amount: Money = FieldInfo(alias="limitAmount")
    """Represents a monetary value"""

    preset: Literal["daily", "weekly", "monthly", "yearly", "collective"]

    start_date: Optional[str] = FieldInfo(alias="startDate", default=None)
    """Format ISO-8601.

    A day that equals today or the past. This is optional.If the `preset` is
    "daily", this value is ignored. If the `preset` is "weekly", "monthly" or
    "yearly", then the this value is used to compute when the limit should start
    limit.
    """

    timezone: Optional[str] = None
    """IANA timezone string.

    Limits always reset at midnight of the timezone specified. If no timezone is
    specified, then UTC time is used.
    """


class SpendingRule(BaseModel):
    transaction_size_limit: Optional[SpendingRuleTransactionSizeLimit] = FieldInfo(
        alias="transactionSizeLimit", default=None
    )

    utilization_limit: Optional[SpendingRuleUtilizationLimit] = FieldInfo(alias="utilizationLimit", default=None)

    utilization_limit_v2: Optional[List[SpendingRuleUtilizationLimitV2]] = FieldInfo(
        alias="utilizationLimitV2", default=None
    )


class SpendingConstraint(BaseModel):
    country_rule: Optional[CountryRule] = FieldInfo(alias="countryRule", default=None)

    merchant_category_code_rule: Optional[MerchantCategoryCodeRule] = FieldInfo(
        alias="merchantCategoryCodeRule", default=None
    )

    merchant_category_rule: Optional[MerchantCategoryRule] = FieldInfo(alias="merchantCategoryRule", default=None)

    merchant_rule: Optional[MerchantRule] = FieldInfo(alias="merchantRule", default=None)

    spending_rule: Optional[SpendingRule] = FieldInfo(alias="spendingRule", default=None)
