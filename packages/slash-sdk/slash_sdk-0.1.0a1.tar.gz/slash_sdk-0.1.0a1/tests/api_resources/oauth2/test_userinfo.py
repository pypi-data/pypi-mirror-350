# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types.oauth2 import UserInfo

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUserinfo:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: SlashSDK) -> None:
        userinfo = client.oauth2.userinfo.retrieve()
        assert_matches_type(UserInfo, userinfo, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: SlashSDK) -> None:
        response = client.oauth2.userinfo.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        userinfo = response.parse()
        assert_matches_type(UserInfo, userinfo, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: SlashSDK) -> None:
        with client.oauth2.userinfo.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            userinfo = response.parse()
            assert_matches_type(UserInfo, userinfo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_submit(self, client: SlashSDK) -> None:
        userinfo = client.oauth2.userinfo.submit()
        assert_matches_type(UserInfo, userinfo, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_submit(self, client: SlashSDK) -> None:
        response = client.oauth2.userinfo.with_raw_response.submit()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        userinfo = response.parse()
        assert_matches_type(UserInfo, userinfo, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_submit(self, client: SlashSDK) -> None:
        with client.oauth2.userinfo.with_streaming_response.submit() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            userinfo = response.parse()
            assert_matches_type(UserInfo, userinfo, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUserinfo:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSlashSDK) -> None:
        userinfo = await async_client.oauth2.userinfo.retrieve()
        assert_matches_type(UserInfo, userinfo, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.oauth2.userinfo.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        userinfo = await response.parse()
        assert_matches_type(UserInfo, userinfo, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.oauth2.userinfo.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            userinfo = await response.parse()
            assert_matches_type(UserInfo, userinfo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_submit(self, async_client: AsyncSlashSDK) -> None:
        userinfo = await async_client.oauth2.userinfo.submit()
        assert_matches_type(UserInfo, userinfo, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_submit(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.oauth2.userinfo.with_raw_response.submit()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        userinfo = await response.parse()
        assert_matches_type(UserInfo, userinfo, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_submit(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.oauth2.userinfo.with_streaming_response.submit() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            userinfo = await response.parse()
            assert_matches_type(UserInfo, userinfo, path=["response"])

        assert cast(Any, response.is_closed) is True
