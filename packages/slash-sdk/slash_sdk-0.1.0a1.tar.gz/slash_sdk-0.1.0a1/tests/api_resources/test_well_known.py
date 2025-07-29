# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import WellKnownRetrieveOpenidConfigurationResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWellKnown:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_openid_configuration(self, client: SlashSDK) -> None:
        well_known = client.well_known.retrieve_openid_configuration()
        assert_matches_type(WellKnownRetrieveOpenidConfigurationResponse, well_known, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_openid_configuration(self, client: SlashSDK) -> None:
        response = client.well_known.with_raw_response.retrieve_openid_configuration()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        well_known = response.parse()
        assert_matches_type(WellKnownRetrieveOpenidConfigurationResponse, well_known, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_openid_configuration(self, client: SlashSDK) -> None:
        with client.well_known.with_streaming_response.retrieve_openid_configuration() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            well_known = response.parse()
            assert_matches_type(WellKnownRetrieveOpenidConfigurationResponse, well_known, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncWellKnown:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_openid_configuration(self, async_client: AsyncSlashSDK) -> None:
        well_known = await async_client.well_known.retrieve_openid_configuration()
        assert_matches_type(WellKnownRetrieveOpenidConfigurationResponse, well_known, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_openid_configuration(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.well_known.with_raw_response.retrieve_openid_configuration()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        well_known = await response.parse()
        assert_matches_type(WellKnownRetrieveOpenidConfigurationResponse, well_known, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_openid_configuration(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.well_known.with_streaming_response.retrieve_openid_configuration() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            well_known = await response.parse()
            assert_matches_type(WellKnownRetrieveOpenidConfigurationResponse, well_known, path=["response"])

        assert cast(Any, response.is_closed) is True
