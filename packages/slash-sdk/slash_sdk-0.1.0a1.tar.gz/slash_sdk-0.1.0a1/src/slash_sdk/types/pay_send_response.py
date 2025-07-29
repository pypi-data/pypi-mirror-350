# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["PaySendResponse", "UnionMember0", "UnionMember1"]


class UnionMember0(BaseModel):
    success: Literal[True]

    redirect: Optional[str] = None


class UnionMember1(BaseModel):
    error: str

    success: Literal[False]


PaySendResponse: TypeAlias = Union[UnionMember0, UnionMember1]
