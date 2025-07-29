# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import CryptoCreateOfframpResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCrypto:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_offramp(self, client: SlashSDK) -> None:
        crypto = client.crypto.create_offramp(
            currency="usdt",
            payment_rail="ach",
            virtual_account_id="virtualAccountId",
        )
        assert_matches_type(CryptoCreateOfframpResponse, crypto, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_offramp(self, client: SlashSDK) -> None:
        response = client.crypto.with_raw_response.create_offramp(
            currency="usdt",
            payment_rail="ach",
            virtual_account_id="virtualAccountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        crypto = response.parse()
        assert_matches_type(CryptoCreateOfframpResponse, crypto, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_offramp(self, client: SlashSDK) -> None:
        with client.crypto.with_streaming_response.create_offramp(
            currency="usdt",
            payment_rail="ach",
            virtual_account_id="virtualAccountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            crypto = response.parse()
            assert_matches_type(CryptoCreateOfframpResponse, crypto, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCrypto:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_offramp(self, async_client: AsyncSlashSDK) -> None:
        crypto = await async_client.crypto.create_offramp(
            currency="usdt",
            payment_rail="ach",
            virtual_account_id="virtualAccountId",
        )
        assert_matches_type(CryptoCreateOfframpResponse, crypto, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_offramp(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.crypto.with_raw_response.create_offramp(
            currency="usdt",
            payment_rail="ach",
            virtual_account_id="virtualAccountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        crypto = await response.parse()
        assert_matches_type(CryptoCreateOfframpResponse, crypto, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_offramp(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.crypto.with_streaming_response.create_offramp(
            currency="usdt",
            payment_rail="ach",
            virtual_account_id="virtualAccountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            crypto = await response.parse()
            assert_matches_type(CryptoCreateOfframpResponse, crypto, path=["response"])

        assert cast(Any, response.is_closed) is True
