# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["Oauth2GetTokenResponse"]


class Oauth2GetTokenResponse(BaseModel):
    access_token: str

    expires_in: int

    id_token: str

    refresh_token: str
