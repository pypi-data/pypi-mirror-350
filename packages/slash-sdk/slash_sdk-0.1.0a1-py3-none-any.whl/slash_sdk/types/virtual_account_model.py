# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["VirtualAccountModel"]


class VirtualAccountModel(BaseModel):
    id: str
    """The ID of the virtual account."""

    account_id: str = FieldInfo(alias="accountId")
    """The account ID of the Slash account the virtual account is associated with."""

    account_type: Literal["default", "primary"] = FieldInfo(alias="accountType")
    """The account type of the virtual account.

    Since virtual accounts and Slash accounts exist at the same hierarchy level, an
    account type of 'primary' means it is the main Slash account, while an account
    type of 'default' means it is a virtual account under the main account.
    """

    name: str
    """The name of the virtual account."""

    account_number: Optional[str] = FieldInfo(alias="accountNumber", default=None)
    """The account number of the virtual account."""

    closed_at: Optional[str] = FieldInfo(alias="closedAt", default=None)
    """
    The date the virtual account was closed; will be null if account was never
    closed.
    """

    routing_number: Optional[str] = FieldInfo(alias="routingNumber", default=None)
    """The routing number of the virtual account."""
