# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .commission_details_param import CommissionDetailsParam

__all__ = ["VirtualAccountUpdateParams", "Variant0", "Variant1"]


class Variant0(TypedDict, total=False):
    action: Required[Literal["update"]]
    """The type of action to take.

    An action of type "update" will update the virtual account with the specified
    properties.
    """

    commission_details: Annotated[CommissionDetailsParam, PropertyInfo(alias="commissionDetails")]

    name: str
    """The name to update the virtual account with."""


class Variant1(TypedDict, total=False):
    action: Required[Literal["close"]]
    """The type of action to take.

    An action of type "close" will close the virtual account.
    """


VirtualAccountUpdateParams: TypeAlias = Union[Variant0, Variant1]
