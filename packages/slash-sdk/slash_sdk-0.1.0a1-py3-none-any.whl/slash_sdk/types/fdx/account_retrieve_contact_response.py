# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["AccountRetrieveContactResponse", "Address", "Holder", "HolderName", "Telephone"]


class Address(BaseModel):
    city: str

    country: str
    """Iso3166CountryCode"""

    line1: str

    line2: str

    line3: Optional[str] = None

    postal_code: Optional[str] = FieldInfo(alias="postalCode", default=None)

    region: Optional[str] = None
    """State or province or territory."""


class HolderName(BaseModel):
    first: str

    last: str

    middle: str

    prefix: Optional[str] = None

    suffix: Optional[str] = None


class Holder(BaseModel):
    name: HolderName


class Telephone(BaseModel):
    number: str
    """Telephone subscriber number defined by ITU-T recommendation E.164"""

    type: Literal["HOME", "BUSINESS", "CELL", "FAX"]

    country: Optional[str] = None
    """Country calling codes defined by ITU-T recommendations E.123 and E.164"""


class AccountRetrieveContactResponse(BaseModel):
    addresses: List[Address]

    emails: List[str]

    holders: List[Holder]

    telephones: List[Telephone]
