# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import (
    Webhook,
    WebhookListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWebhook:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: SlashSDK) -> None:
        webhook = client.webhook.create(
            name="name",
            url="url",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: SlashSDK) -> None:
        webhook = client.webhook.create(
            name="name",
            url="url",
            legal_entity_id="legalEntityId",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: SlashSDK) -> None:
        response = client.webhook.with_raw_response.create(
            name="name",
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: SlashSDK) -> None:
        with client.webhook.with_streaming_response.create(
            name="name",
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(Webhook, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: SlashSDK) -> None:
        webhook = client.webhook.update(
            webhook_id="webhookId",
            status="archived",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: SlashSDK) -> None:
        webhook = client.webhook.update(
            webhook_id="webhookId",
            status="archived",
            reason="reason",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: SlashSDK) -> None:
        response = client.webhook.with_raw_response.update(
            webhook_id="webhookId",
            status="archived",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: SlashSDK) -> None:
        with client.webhook.with_streaming_response.update(
            webhook_id="webhookId",
            status="archived",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(Webhook, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            client.webhook.with_raw_response.update(
                webhook_id="",
                status="archived",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: SlashSDK) -> None:
        webhook = client.webhook.list()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: SlashSDK) -> None:
        webhook = client.webhook.list(
            cursor="cursor",
            filter_legal_entity_id="filter:legalEntityId",
        )
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: SlashSDK) -> None:
        response = client.webhook.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: SlashSDK) -> None:
        with client.webhook.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(WebhookListResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncWebhook:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncSlashSDK) -> None:
        webhook = await async_client.webhook.create(
            name="name",
            url="url",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        webhook = await async_client.webhook.create(
            name="name",
            url="url",
            legal_entity_id="legalEntityId",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.webhook.with_raw_response.create(
            name="name",
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.webhook.with_streaming_response.create(
            name="name",
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(Webhook, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncSlashSDK) -> None:
        webhook = await async_client.webhook.update(
            webhook_id="webhookId",
            status="archived",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        webhook = await async_client.webhook.update(
            webhook_id="webhookId",
            status="archived",
            reason="reason",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.webhook.with_raw_response.update(
            webhook_id="webhookId",
            status="archived",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.webhook.with_streaming_response.update(
            webhook_id="webhookId",
            status="archived",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(Webhook, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            await async_client.webhook.with_raw_response.update(
                webhook_id="",
                status="archived",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSlashSDK) -> None:
        webhook = await async_client.webhook.list()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        webhook = await async_client.webhook.list(
            cursor="cursor",
            filter_legal_entity_id="filter:legalEntityId",
        )
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.webhook.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.webhook.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(WebhookListResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True
