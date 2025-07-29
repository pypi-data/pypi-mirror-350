# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import (
    DeveloperApplicationModel,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeveloperAccount:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_application(self, client: SlashSDK) -> None:
        developer_account = client.developer_account.create_application(
            developer_account_id="developerAccountId",
            data={
                "allowed_origins": ["string"],
                "description": "description",
                "scopes": ["legal_entity.home.view"],
                "type": "service",
            },
            name="name",
            type="service",
        )
        assert_matches_type(DeveloperApplicationModel, developer_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_application_with_all_params(self, client: SlashSDK) -> None:
        developer_account = client.developer_account.create_application(
            developer_account_id="developerAccountId",
            data={
                "allowed_origins": ["string"],
                "description": "description",
                "scopes": ["legal_entity.home.view"],
                "type": "service",
                "logo_url": "logoUrl",
                "privacy_policy_url": "privacyPolicyUrl",
                "redirect_uris": ["string"],
                "terms_of_service_url": "termsOfServiceUrl",
                "test_user_emails": ["string"],
            },
            name="name",
            type="service",
        )
        assert_matches_type(DeveloperApplicationModel, developer_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_application(self, client: SlashSDK) -> None:
        response = client.developer_account.with_raw_response.create_application(
            developer_account_id="developerAccountId",
            data={
                "allowed_origins": ["string"],
                "description": "description",
                "scopes": ["legal_entity.home.view"],
                "type": "service",
            },
            name="name",
            type="service",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        developer_account = response.parse()
        assert_matches_type(DeveloperApplicationModel, developer_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_application(self, client: SlashSDK) -> None:
        with client.developer_account.with_streaming_response.create_application(
            developer_account_id="developerAccountId",
            data={
                "allowed_origins": ["string"],
                "description": "description",
                "scopes": ["legal_entity.home.view"],
                "type": "service",
            },
            name="name",
            type="service",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            developer_account = response.parse()
            assert_matches_type(DeveloperApplicationModel, developer_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_application(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `developer_account_id` but received ''"):
            client.developer_account.with_raw_response.create_application(
                developer_account_id="",
                data={
                    "allowed_origins": ["string"],
                    "description": "description",
                    "scopes": ["legal_entity.home.view"],
                    "type": "service",
                },
                name="name",
                type="service",
            )


class TestAsyncDeveloperAccount:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_application(self, async_client: AsyncSlashSDK) -> None:
        developer_account = await async_client.developer_account.create_application(
            developer_account_id="developerAccountId",
            data={
                "allowed_origins": ["string"],
                "description": "description",
                "scopes": ["legal_entity.home.view"],
                "type": "service",
            },
            name="name",
            type="service",
        )
        assert_matches_type(DeveloperApplicationModel, developer_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_application_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        developer_account = await async_client.developer_account.create_application(
            developer_account_id="developerAccountId",
            data={
                "allowed_origins": ["string"],
                "description": "description",
                "scopes": ["legal_entity.home.view"],
                "type": "service",
                "logo_url": "logoUrl",
                "privacy_policy_url": "privacyPolicyUrl",
                "redirect_uris": ["string"],
                "terms_of_service_url": "termsOfServiceUrl",
                "test_user_emails": ["string"],
            },
            name="name",
            type="service",
        )
        assert_matches_type(DeveloperApplicationModel, developer_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_application(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.developer_account.with_raw_response.create_application(
            developer_account_id="developerAccountId",
            data={
                "allowed_origins": ["string"],
                "description": "description",
                "scopes": ["legal_entity.home.view"],
                "type": "service",
            },
            name="name",
            type="service",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        developer_account = await response.parse()
        assert_matches_type(DeveloperApplicationModel, developer_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_application(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.developer_account.with_streaming_response.create_application(
            developer_account_id="developerAccountId",
            data={
                "allowed_origins": ["string"],
                "description": "description",
                "scopes": ["legal_entity.home.view"],
                "type": "service",
            },
            name="name",
            type="service",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            developer_account = await response.parse()
            assert_matches_type(DeveloperApplicationModel, developer_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_application(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `developer_account_id` but received ''"):
            await async_client.developer_account.with_raw_response.create_application(
                developer_account_id="",
                data={
                    "allowed_origins": ["string"],
                    "description": "description",
                    "scopes": ["legal_entity.home.view"],
                    "type": "service",
                },
                name="name",
                type="service",
            )
