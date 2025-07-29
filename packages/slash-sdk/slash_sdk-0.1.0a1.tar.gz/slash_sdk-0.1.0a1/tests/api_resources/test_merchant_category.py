# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import MerchantCategoryListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMerchantCategory:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: SlashSDK) -> None:
        merchant_category = client.merchant_category.list()
        assert_matches_type(MerchantCategoryListResponse, merchant_category, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: SlashSDK) -> None:
        merchant_category = client.merchant_category.list(
            cursor="cursor",
        )
        assert_matches_type(MerchantCategoryListResponse, merchant_category, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: SlashSDK) -> None:
        response = client.merchant_category.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        merchant_category = response.parse()
        assert_matches_type(MerchantCategoryListResponse, merchant_category, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: SlashSDK) -> None:
        with client.merchant_category.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            merchant_category = response.parse()
            assert_matches_type(MerchantCategoryListResponse, merchant_category, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMerchantCategory:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSlashSDK) -> None:
        merchant_category = await async_client.merchant_category.list()
        assert_matches_type(MerchantCategoryListResponse, merchant_category, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        merchant_category = await async_client.merchant_category.list(
            cursor="cursor",
        )
        assert_matches_type(MerchantCategoryListResponse, merchant_category, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.merchant_category.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        merchant_category = await response.parse()
        assert_matches_type(MerchantCategoryListResponse, merchant_category, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.merchant_category.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            merchant_category = await response.parse()
            assert_matches_type(MerchantCategoryListResponse, merchant_category, path=["response"])

        assert cast(Any, response.is_closed) is True
