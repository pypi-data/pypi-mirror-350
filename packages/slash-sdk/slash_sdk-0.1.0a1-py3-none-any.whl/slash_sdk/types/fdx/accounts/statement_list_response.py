# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["StatementListResponse", "Statement", "StatementLink", "Page"]


class StatementLink(BaseModel):
    href: str

    action: Optional[Literal["GET"]] = None

    rel: Optional[str] = None

    types: Optional[List[Literal["application/pdf"]]] = None


class Statement(BaseModel):
    account_id: str = FieldInfo(alias="accountId")
    """Long-term persistent identity of the account, though not an account number."""

    description: str
    """A description of the statement."""

    links: List[StatementLink]
    """
    Will only contain one element, which is a link to the
    /accounts/{accountId}/statements/{statementId} endpoint.
    """

    statement_date: str = FieldInfo(alias="statementDate")
    """The date of the statement."""

    statement_id: str = FieldInfo(alias="statementId")
    """Long-term persistent identity of the statement."""

    status: Literal["pending", "available"]


class Page(BaseModel):
    next_offset: Optional[str] = FieldInfo(alias="nextOffset", default=None)


class StatementListResponse(BaseModel):
    statements: List[Statement]

    page: Optional[Page] = None
