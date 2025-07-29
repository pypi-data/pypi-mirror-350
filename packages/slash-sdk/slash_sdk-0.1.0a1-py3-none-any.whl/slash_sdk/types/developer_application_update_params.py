# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .developer_application_data_param import DeveloperApplicationDataParam

__all__ = ["DeveloperApplicationUpdateParams"]


class DeveloperApplicationUpdateParams(TypedDict, total=False):
    data: DeveloperApplicationDataParam

    name: str
