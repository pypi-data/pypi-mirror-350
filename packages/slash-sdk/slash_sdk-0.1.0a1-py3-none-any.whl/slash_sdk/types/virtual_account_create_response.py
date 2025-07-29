# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .commission_rule import CommissionRule
from .virtual_account_model import VirtualAccountModel

__all__ = ["VirtualAccountCreateResponse"]


class VirtualAccountCreateResponse(BaseModel):
    virtual_account: VirtualAccountModel = FieldInfo(alias="virtualAccount")
    """The virtual account object"""

    commission_rule: Optional[CommissionRule] = FieldInfo(alias="commissionRule", default=None)
    """The virtual account commission rule object"""
