# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import (
    TransferCreateVirtualAccountTransferResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTransfer:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_virtual_account_transfer(self, client: SlashSDK) -> None:
        transfer = client.transfer.create_virtual_account_transfer(
            amount_cents=0,
            destination="destination",
            source="source",
            x_idempotency_key="X-Idempotency-Key",
        )
        assert_matches_type(TransferCreateVirtualAccountTransferResponse, transfer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_virtual_account_transfer(self, client: SlashSDK) -> None:
        response = client.transfer.with_raw_response.create_virtual_account_transfer(
            amount_cents=0,
            destination="destination",
            source="source",
            x_idempotency_key="X-Idempotency-Key",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transfer = response.parse()
        assert_matches_type(TransferCreateVirtualAccountTransferResponse, transfer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_virtual_account_transfer(self, client: SlashSDK) -> None:
        with client.transfer.with_streaming_response.create_virtual_account_transfer(
            amount_cents=0,
            destination="destination",
            source="source",
            x_idempotency_key="X-Idempotency-Key",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transfer = response.parse()
            assert_matches_type(TransferCreateVirtualAccountTransferResponse, transfer, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTransfer:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_virtual_account_transfer(self, async_client: AsyncSlashSDK) -> None:
        transfer = await async_client.transfer.create_virtual_account_transfer(
            amount_cents=0,
            destination="destination",
            source="source",
            x_idempotency_key="X-Idempotency-Key",
        )
        assert_matches_type(TransferCreateVirtualAccountTransferResponse, transfer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_virtual_account_transfer(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.transfer.with_raw_response.create_virtual_account_transfer(
            amount_cents=0,
            destination="destination",
            source="source",
            x_idempotency_key="X-Idempotency-Key",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transfer = await response.parse()
        assert_matches_type(TransferCreateVirtualAccountTransferResponse, transfer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_virtual_account_transfer(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.transfer.with_streaming_response.create_virtual_account_transfer(
            amount_cents=0,
            destination="destination",
            source="source",
            x_idempotency_key="X-Idempotency-Key",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transfer = await response.parse()
            assert_matches_type(TransferCreateVirtualAccountTransferResponse, transfer, path=["response"])

        assert cast(Any, response.is_closed) is True
