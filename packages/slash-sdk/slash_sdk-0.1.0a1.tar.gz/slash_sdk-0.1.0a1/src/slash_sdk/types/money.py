# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Money"]


class Money(BaseModel):
    amount_cents: int = FieldInfo(alias="amountCents")
    """The amount in cents"""
