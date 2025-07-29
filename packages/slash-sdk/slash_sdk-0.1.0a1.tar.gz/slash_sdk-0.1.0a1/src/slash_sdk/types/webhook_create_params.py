# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["WebhookCreateParams"]


class WebhookCreateParams(TypedDict, total=False):
    name: Required[str]

    url: Required[str]
    """The URL that will receive the webhook payload"""

    legal_entity_id: Annotated[str, PropertyInfo(alias="legalEntityId")]
    """The ID of the LegalEntity to create the webhook for.

    You can get this by calling `GET /legal-entity`. This field is required unless
    you are authenticating via API key.
    """
