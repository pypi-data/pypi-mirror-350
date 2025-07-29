# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import SlashHandle, PaySendResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPay:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: SlashSDK) -> None:
        pay = client.pay.retrieve()
        assert_matches_type(SlashHandle, pay, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: SlashSDK) -> None:
        response = client.pay.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pay = response.parse()
        assert_matches_type(SlashHandle, pay, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: SlashSDK) -> None:
        with client.pay.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pay = response.parse()
            assert_matches_type(SlashHandle, pay, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_send(self, client: SlashSDK) -> None:
        pay = client.pay.send(
            amount_cents=0,
            slash_handle="slashHandle",
        )
        assert_matches_type(PaySendResponse, pay, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_send_with_all_params(self, client: SlashSDK) -> None:
        pay = client.pay.send(
            amount_cents=0,
            slash_handle="slashHandle",
            legal_entity_id="legalEntityId",
            source_slash_handle_id="sourceSlashHandleId",
        )
        assert_matches_type(PaySendResponse, pay, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_send(self, client: SlashSDK) -> None:
        response = client.pay.with_raw_response.send(
            amount_cents=0,
            slash_handle="slashHandle",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pay = response.parse()
        assert_matches_type(PaySendResponse, pay, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_send(self, client: SlashSDK) -> None:
        with client.pay.with_streaming_response.send(
            amount_cents=0,
            slash_handle="slashHandle",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pay = response.parse()
            assert_matches_type(PaySendResponse, pay, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPay:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSlashSDK) -> None:
        pay = await async_client.pay.retrieve()
        assert_matches_type(SlashHandle, pay, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.pay.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pay = await response.parse()
        assert_matches_type(SlashHandle, pay, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.pay.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pay = await response.parse()
            assert_matches_type(SlashHandle, pay, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_send(self, async_client: AsyncSlashSDK) -> None:
        pay = await async_client.pay.send(
            amount_cents=0,
            slash_handle="slashHandle",
        )
        assert_matches_type(PaySendResponse, pay, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_send_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        pay = await async_client.pay.send(
            amount_cents=0,
            slash_handle="slashHandle",
            legal_entity_id="legalEntityId",
            source_slash_handle_id="sourceSlashHandleId",
        )
        assert_matches_type(PaySendResponse, pay, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_send(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.pay.with_raw_response.send(
            amount_cents=0,
            slash_handle="slashHandle",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pay = await response.parse()
        assert_matches_type(PaySendResponse, pay, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_send(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.pay.with_streaming_response.send(
            amount_cents=0,
            slash_handle="slashHandle",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pay = await response.parse()
            assert_matches_type(PaySendResponse, pay, path=["response"])

        assert cast(Any, response.is_closed) is True
