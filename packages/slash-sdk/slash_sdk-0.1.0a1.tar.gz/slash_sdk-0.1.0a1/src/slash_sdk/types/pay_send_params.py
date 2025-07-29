# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PaySendParams"]


class PaySendParams(TypedDict, total=False):
    amount_cents: Required[Annotated[float, PropertyInfo(alias="amountCents")]]
    """The amount of money to send in cents."""

    slash_handle: Required[Annotated[str, PropertyInfo(alias="slashHandle")]]
    """The username of the SlashHandle to send money to.

    You can get this by asking your recipient for their SlashHandle.
    """

    legal_entity_id: Annotated[str, PropertyInfo(alias="legalEntityId")]
    """The ID of the LegalEntity to send money from.

    You can get this by calling `GET /legal-entity`. This field or `slashHandleId`
    is required unless you are authenticating via API key.
    """

    source_slash_handle_id: Annotated[str, PropertyInfo(alias="sourceSlashHandleId")]
    """The ID of the SlashHandle to send money from.

    You can get this by calling `GET /slash-handle`. This field or `legalEntityId`
    is required unless you are authenticating via API key.
    """
