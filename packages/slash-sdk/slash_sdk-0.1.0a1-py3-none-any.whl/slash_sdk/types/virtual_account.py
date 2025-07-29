# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .money import Money
from .._models import BaseModel
from .commission_rule import CommissionRule
from .virtual_account_model import VirtualAccountModel

__all__ = ["VirtualAccount"]


class VirtualAccount(BaseModel):
    balance: Money
    """The total balance of the virtual account"""

    spend: Money
    """The total spend of the virtual account"""

    virtual_account: VirtualAccountModel = FieldInfo(alias="virtualAccount")
    """The virtual account itself"""

    commission_rule: Optional[CommissionRule] = FieldInfo(alias="commissionRule", default=None)
    """The commission rule applied to the virtual account, if any"""
