# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import Oauth2GetTokenResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOauth2:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_token_overload_1(self, client: SlashSDK) -> None:
        oauth2 = client.oauth2.get_token(
            code="code",
            grant_type="authorization_code",
            redirect_uri="redirect_uri",
        )
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_token_with_all_params_overload_1(self, client: SlashSDK) -> None:
        oauth2 = client.oauth2.get_token(
            code="code",
            grant_type="authorization_code",
            redirect_uri="redirect_uri",
            code_verifier="code_verifier",
            prompt="prompt",
            scope="scope",
        )
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_token_overload_1(self, client: SlashSDK) -> None:
        response = client.oauth2.with_raw_response.get_token(
            code="code",
            grant_type="authorization_code",
            redirect_uri="redirect_uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth2 = response.parse()
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_token_overload_1(self, client: SlashSDK) -> None:
        with client.oauth2.with_streaming_response.get_token(
            code="code",
            grant_type="authorization_code",
            redirect_uri="redirect_uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth2 = response.parse()
            assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_token_overload_2(self, client: SlashSDK) -> None:
        oauth2 = client.oauth2.get_token(
            grant_type="refresh_token",
            refresh_token="refresh_token",
        )
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_token_with_all_params_overload_2(self, client: SlashSDK) -> None:
        oauth2 = client.oauth2.get_token(
            grant_type="refresh_token",
            refresh_token="refresh_token",
            code="code",
            code_verifier="code_verifier",
            prompt="prompt",
            redirect_uri="redirect_uri",
            scope="scope",
        )
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_token_overload_2(self, client: SlashSDK) -> None:
        response = client.oauth2.with_raw_response.get_token(
            grant_type="refresh_token",
            refresh_token="refresh_token",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth2 = response.parse()
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_token_overload_2(self, client: SlashSDK) -> None:
        with client.oauth2.with_streaming_response.get_token(
            grant_type="refresh_token",
            refresh_token="refresh_token",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth2 = response.parse()
            assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOauth2:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_token_overload_1(self, async_client: AsyncSlashSDK) -> None:
        oauth2 = await async_client.oauth2.get_token(
            code="code",
            grant_type="authorization_code",
            redirect_uri="redirect_uri",
        )
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_token_with_all_params_overload_1(self, async_client: AsyncSlashSDK) -> None:
        oauth2 = await async_client.oauth2.get_token(
            code="code",
            grant_type="authorization_code",
            redirect_uri="redirect_uri",
            code_verifier="code_verifier",
            prompt="prompt",
            scope="scope",
        )
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_token_overload_1(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.oauth2.with_raw_response.get_token(
            code="code",
            grant_type="authorization_code",
            redirect_uri="redirect_uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth2 = await response.parse()
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_token_overload_1(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.oauth2.with_streaming_response.get_token(
            code="code",
            grant_type="authorization_code",
            redirect_uri="redirect_uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth2 = await response.parse()
            assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_token_overload_2(self, async_client: AsyncSlashSDK) -> None:
        oauth2 = await async_client.oauth2.get_token(
            grant_type="refresh_token",
            refresh_token="refresh_token",
        )
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_token_with_all_params_overload_2(self, async_client: AsyncSlashSDK) -> None:
        oauth2 = await async_client.oauth2.get_token(
            grant_type="refresh_token",
            refresh_token="refresh_token",
            code="code",
            code_verifier="code_verifier",
            prompt="prompt",
            redirect_uri="redirect_uri",
            scope="scope",
        )
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_token_overload_2(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.oauth2.with_raw_response.get_token(
            grant_type="refresh_token",
            refresh_token="refresh_token",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth2 = await response.parse()
        assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_token_overload_2(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.oauth2.with_streaming_response.get_token(
            grant_type="refresh_token",
            refresh_token="refresh_token",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth2 = await response.parse()
            assert_matches_type(Oauth2GetTokenResponse, oauth2, path=["response"])

        assert cast(Any, response.is_closed) is True
