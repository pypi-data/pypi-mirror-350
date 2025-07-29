# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SlashHandle"]


class SlashHandle(BaseModel):
    id: str
    """The id of the SlashHandle"""

    account_id: str = FieldInfo(alias="accountId")
    """The ID of the account that will send and receive funds for this entity"""

    name: str
    """The display name of the entity"""

    slash_handle: str = FieldInfo(alias="slashHandle")
    """The username that others can use to send money to this entity"""
