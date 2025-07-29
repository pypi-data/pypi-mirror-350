# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["CardRetrieveParams"]


class CardRetrieveParams(TypedDict, total=False):
    include_cvv: Literal["true", "false"]

    include_pan: Literal["true", "false"]
