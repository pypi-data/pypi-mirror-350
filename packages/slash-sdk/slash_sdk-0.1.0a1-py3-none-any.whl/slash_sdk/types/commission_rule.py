# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .commission_details import CommissionDetails

__all__ = ["CommissionRule"]


class CommissionRule(BaseModel):
    id: str
    """The ID of the commission rule"""

    commission_details: CommissionDetails = FieldInfo(alias="commissionDetails")
    """Describes details of the commission rule."""

    virtual_account_id: str = FieldInfo(alias="virtualAccountId")
    """The ID of the virtual account the commission rule is applied to"""
