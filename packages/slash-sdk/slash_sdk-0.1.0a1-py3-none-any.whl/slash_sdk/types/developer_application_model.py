# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .developer_application_data import DeveloperApplicationData
from .developer_application_type import DeveloperApplicationType

__all__ = ["DeveloperApplicationModel"]


class DeveloperApplicationModel(BaseModel):
    id: str

    data: DeveloperApplicationData

    developer_account_id: str = FieldInfo(alias="developerAccountId")

    name: str

    status: Literal["test", "under_review", "production"]

    timestamp: str

    type: DeveloperApplicationType

    oauth_client_id: Optional[str] = FieldInfo(alias="oauthClientId", default=None)

    oauth_client_secret: Optional[str] = FieldInfo(alias="oauthClientSecret", default=None)
