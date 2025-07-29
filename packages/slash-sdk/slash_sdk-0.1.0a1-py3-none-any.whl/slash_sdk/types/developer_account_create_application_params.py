# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .developer_application_type import DeveloperApplicationType
from .developer_application_data_param import DeveloperApplicationDataParam

__all__ = ["DeveloperAccountCreateApplicationParams"]


class DeveloperAccountCreateApplicationParams(TypedDict, total=False):
    data: Required[DeveloperApplicationDataParam]

    name: Required[str]

    type: Required[DeveloperApplicationType]
