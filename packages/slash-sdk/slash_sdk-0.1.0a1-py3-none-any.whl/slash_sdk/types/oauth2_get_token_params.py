# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["Oauth2GetTokenParams", "Variant0", "Variant1"]


class Variant0(TypedDict, total=False):
    code: Required[str]

    grant_type: Required[Literal["authorization_code"]]

    redirect_uri: Required[str]

    code_verifier: str
    """Unused by Slash, but required in the OAuth spec."""

    prompt: str
    """Unused by Slash, but required in the OAuth spec."""

    scope: str
    """Unused by Slash, but required in the OAuth spec."""


class Variant1(TypedDict, total=False):
    grant_type: Required[Literal["refresh_token"]]

    refresh_token: Required[str]

    code: str
    """Unused by Slash, but required in the OAuth spec."""

    code_verifier: str
    """Unused by Slash, but required in the OAuth spec."""

    prompt: str
    """Unused by Slash, but required in the OAuth spec."""

    redirect_uri: str
    """Unused by Slash, but required in the OAuth spec."""

    scope: str
    """Unused by Slash, but required in the OAuth spec."""


Oauth2GetTokenParams: TypeAlias = Union[Variant0, Variant1]
