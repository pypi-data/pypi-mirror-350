# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["WellKnownRetrieveOpenidConfigurationResponse"]


class WellKnownRetrieveOpenidConfigurationResponse(BaseModel):
    authorization_endpoint: str

    response_types_supported: List[Literal["code", "token", "id_token token"]]

    scopes_supported: List[
        Literal["openid", "offline_access", "profile", "email", "address", "phone", "user.identity.view"]
    ]

    token_endpoint: str

    userinfo_endpoint: str

    token_endpoint_auth_methods_supported: Optional[
        List[Literal["client_secret_post", "client_secret_basic", "client_secret_jwt", "private_key_jwt"]]
    ] = None
    """If omitted, the default is client_secret_basic"""
