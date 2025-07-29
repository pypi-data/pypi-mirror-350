# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import LegalEntityListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLegalEntity:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: SlashSDK) -> None:
        legal_entity = client.legal_entity.list()
        assert_matches_type(LegalEntityListResponse, legal_entity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: SlashSDK) -> None:
        response = client.legal_entity.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        legal_entity = response.parse()
        assert_matches_type(LegalEntityListResponse, legal_entity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: SlashSDK) -> None:
        with client.legal_entity.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            legal_entity = response.parse()
            assert_matches_type(LegalEntityListResponse, legal_entity, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncLegalEntity:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSlashSDK) -> None:
        legal_entity = await async_client.legal_entity.list()
        assert_matches_type(LegalEntityListResponse, legal_entity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.legal_entity.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        legal_entity = await response.parse()
        assert_matches_type(LegalEntityListResponse, legal_entity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.legal_entity.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            legal_entity = await response.parse()
            assert_matches_type(LegalEntityListResponse, legal_entity, path=["response"])

        assert cast(Any, response.is_closed) is True
