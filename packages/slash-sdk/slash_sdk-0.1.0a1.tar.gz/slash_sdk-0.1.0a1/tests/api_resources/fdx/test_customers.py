# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types.fdx import CustomerRetrieveCurrentResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCustomers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_current(self, client: SlashSDK) -> None:
        customer = client.fdx.customers.retrieve_current()
        assert_matches_type(CustomerRetrieveCurrentResponse, customer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_current(self, client: SlashSDK) -> None:
        response = client.fdx.customers.with_raw_response.retrieve_current()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        customer = response.parse()
        assert_matches_type(CustomerRetrieveCurrentResponse, customer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_current(self, client: SlashSDK) -> None:
        with client.fdx.customers.with_streaming_response.retrieve_current() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            customer = response.parse()
            assert_matches_type(CustomerRetrieveCurrentResponse, customer, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCustomers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_current(self, async_client: AsyncSlashSDK) -> None:
        customer = await async_client.fdx.customers.retrieve_current()
        assert_matches_type(CustomerRetrieveCurrentResponse, customer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_current(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.fdx.customers.with_raw_response.retrieve_current()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        customer = await response.parse()
        assert_matches_type(CustomerRetrieveCurrentResponse, customer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_current(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.fdx.customers.with_streaming_response.retrieve_current() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            customer = await response.parse()
            assert_matches_type(CustomerRetrieveCurrentResponse, customer, path=["response"])

        assert cast(Any, response.is_closed) is True
