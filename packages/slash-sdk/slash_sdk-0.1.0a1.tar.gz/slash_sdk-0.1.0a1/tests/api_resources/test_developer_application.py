# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import DeveloperApplicationModel

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeveloperApplication:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: SlashSDK) -> None:
        developer_application = client.developer_application.retrieve(
            "developerApplicationId",
        )
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: SlashSDK) -> None:
        response = client.developer_application.with_raw_response.retrieve(
            "developerApplicationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        developer_application = response.parse()
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: SlashSDK) -> None:
        with client.developer_application.with_streaming_response.retrieve(
            "developerApplicationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            developer_application = response.parse()
            assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: SlashSDK) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `developer_application_id` but received ''"
        ):
            client.developer_application.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: SlashSDK) -> None:
        developer_application = client.developer_application.update(
            developer_application_id="developerApplicationId",
        )
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: SlashSDK) -> None:
        developer_application = client.developer_application.update(
            developer_application_id="developerApplicationId",
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
        )
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: SlashSDK) -> None:
        response = client.developer_application.with_raw_response.update(
            developer_application_id="developerApplicationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        developer_application = response.parse()
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: SlashSDK) -> None:
        with client.developer_application.with_streaming_response.update(
            developer_application_id="developerApplicationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            developer_application = response.parse()
            assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: SlashSDK) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `developer_application_id` but received ''"
        ):
            client.developer_application.with_raw_response.update(
                developer_application_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_create_or_regenerate_secret(self, client: SlashSDK) -> None:
        developer_application = client.developer_application.create_or_regenerate_secret(
            "developerApplicationId",
        )
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_or_regenerate_secret(self, client: SlashSDK) -> None:
        response = client.developer_application.with_raw_response.create_or_regenerate_secret(
            "developerApplicationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        developer_application = response.parse()
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_or_regenerate_secret(self, client: SlashSDK) -> None:
        with client.developer_application.with_streaming_response.create_or_regenerate_secret(
            "developerApplicationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            developer_application = response.parse()
            assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_or_regenerate_secret(self, client: SlashSDK) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `developer_application_id` but received ''"
        ):
            client.developer_application.with_raw_response.create_or_regenerate_secret(
                "",
            )


class TestAsyncDeveloperApplication:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSlashSDK) -> None:
        developer_application = await async_client.developer_application.retrieve(
            "developerApplicationId",
        )
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.developer_application.with_raw_response.retrieve(
            "developerApplicationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        developer_application = await response.parse()
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.developer_application.with_streaming_response.retrieve(
            "developerApplicationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            developer_application = await response.parse()
            assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `developer_application_id` but received ''"
        ):
            await async_client.developer_application.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncSlashSDK) -> None:
        developer_application = await async_client.developer_application.update(
            developer_application_id="developerApplicationId",
        )
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        developer_application = await async_client.developer_application.update(
            developer_application_id="developerApplicationId",
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
        )
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.developer_application.with_raw_response.update(
            developer_application_id="developerApplicationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        developer_application = await response.parse()
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.developer_application.with_streaming_response.update(
            developer_application_id="developerApplicationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            developer_application = await response.parse()
            assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `developer_application_id` but received ''"
        ):
            await async_client.developer_application.with_raw_response.update(
                developer_application_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_or_regenerate_secret(self, async_client: AsyncSlashSDK) -> None:
        developer_application = await async_client.developer_application.create_or_regenerate_secret(
            "developerApplicationId",
        )
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_or_regenerate_secret(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.developer_application.with_raw_response.create_or_regenerate_secret(
            "developerApplicationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        developer_application = await response.parse()
        assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_or_regenerate_secret(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.developer_application.with_streaming_response.create_or_regenerate_secret(
            "developerApplicationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            developer_application = await response.parse()
            assert_matches_type(DeveloperApplicationModel, developer_application, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_or_regenerate_secret(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `developer_application_id` but received ''"
        ):
            await async_client.developer_application.with_raw_response.create_or_regenerate_secret(
                "",
            )
