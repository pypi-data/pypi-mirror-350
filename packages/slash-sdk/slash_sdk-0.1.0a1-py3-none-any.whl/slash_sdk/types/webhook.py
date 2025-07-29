# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Webhook"]


class Webhook(BaseModel):
    id: str

    created_at: str = FieldInfo(alias="createdAt")

    name: str
    """The name of the webhook"""

    url: str
    """The URL that will receive the webhook payload"""

    archived_at: Optional[str] = FieldInfo(alias="archivedAt", default=None)
