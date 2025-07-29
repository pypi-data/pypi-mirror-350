# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["TransactionAggregateResponse"]


class TransactionAggregateResponse(BaseModel):
    count: float
    """The total count of transactions."""

    net_change: float = FieldInfo(alias="netChange")
    """The net change, which is `totalIn` + `totalOut`."""

    total_in: float = FieldInfo(alias="totalIn")
    """The total amount of money that arrived into the account, in cents."""

    total_out: float = FieldInfo(alias="totalOut")
    """The total amount of money that was sent out of the account, in cents."""
