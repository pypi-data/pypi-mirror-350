# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["TransferCreateVirtualAccountTransferResponse"]


class TransferCreateVirtualAccountTransferResponse(BaseModel):
    transfer_id: str = FieldInfo(alias="transferId")
    """The ID of the transfer that was created."""
