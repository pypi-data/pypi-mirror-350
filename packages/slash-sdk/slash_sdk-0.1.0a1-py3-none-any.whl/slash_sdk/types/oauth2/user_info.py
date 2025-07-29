# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["UserInfo"]


class UserInfo(BaseModel):
    email: str

    name: str
    """The user's full name"""

    sub: str
    """The user's ID"""

    phone_number: Optional[str] = None
