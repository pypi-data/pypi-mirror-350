# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import (
    CardGroupUtilization,
    CardGroupListResponse,
)
from slash_sdk.types.card_group import CardGroup

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCardGroup:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: SlashSDK) -> None:
        card_group = client.card_group.create(
            name="name",
        )
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: SlashSDK) -> None:
        card_group = client.card_group.create(
            name="name",
            spending_constraint={
                "country_rule": {
                    "countries": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_category_code_rule": {
                    "merchant_category_codes": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_category_rule": {
                    "merchant_categories": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_rule": {
                    "merchants": ["string"],
                    "restriction": "allowlist",
                },
                "spending_rule": {
                    "transaction_size_limit": {
                        "maximum": {"amount_cents": 0},
                        "minimum": {"amount_cents": 0},
                    },
                    "utilization_limit": {
                        "limit_amount": {"amount_cents": 0},
                        "preset": "daily",
                        "start_date": "startDate",
                        "timezone": "timezone",
                    },
                    "utilization_limit_v2": [
                        {
                            "limit_amount": {"amount_cents": 0},
                            "preset": "daily",
                            "start_date": "startDate",
                            "timezone": "timezone",
                        }
                    ],
                },
            },
            virtual_account_id="virtualAccountId",
        )
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: SlashSDK) -> None:
        response = client.card_group.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card_group = response.parse()
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: SlashSDK) -> None:
        with client.card_group.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card_group = response.parse()
            assert_matches_type(CardGroup, card_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: SlashSDK) -> None:
        card_group = client.card_group.retrieve(
            "cardGroupId",
        )
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: SlashSDK) -> None:
        response = client.card_group.with_raw_response.retrieve(
            "cardGroupId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card_group = response.parse()
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: SlashSDK) -> None:
        with client.card_group.with_streaming_response.retrieve(
            "cardGroupId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card_group = response.parse()
            assert_matches_type(CardGroup, card_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_group_id` but received ''"):
            client.card_group.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: SlashSDK) -> None:
        card_group = client.card_group.update(
            card_group_id="cardGroupId",
        )
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: SlashSDK) -> None:
        card_group = client.card_group.update(
            card_group_id="cardGroupId",
            name="name",
            spending_constraint={
                "country_rule": {
                    "countries": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_category_code_rule": {
                    "merchant_category_codes": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_category_rule": {
                    "merchant_categories": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_rule": {
                    "merchants": ["string"],
                    "restriction": "allowlist",
                },
                "spending_rule": {
                    "transaction_size_limit": {
                        "maximum": {"amount_cents": 0},
                        "minimum": {"amount_cents": 0},
                    },
                    "utilization_limit": {
                        "limit_amount": {"amount_cents": 0},
                        "preset": "daily",
                        "start_date": "startDate",
                        "timezone": "timezone",
                    },
                    "utilization_limit_v2": [
                        {
                            "limit_amount": {"amount_cents": 0},
                            "preset": "daily",
                            "start_date": "startDate",
                            "timezone": "timezone",
                        }
                    ],
                },
            },
        )
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: SlashSDK) -> None:
        response = client.card_group.with_raw_response.update(
            card_group_id="cardGroupId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card_group = response.parse()
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: SlashSDK) -> None:
        with client.card_group.with_streaming_response.update(
            card_group_id="cardGroupId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card_group = response.parse()
            assert_matches_type(CardGroup, card_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_group_id` but received ''"):
            client.card_group.with_raw_response.update(
                card_group_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: SlashSDK) -> None:
        card_group = client.card_group.list()
        assert_matches_type(CardGroupListResponse, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: SlashSDK) -> None:
        card_group = client.card_group.list(
            cursor="cursor",
            filter_name="filter:name",
        )
        assert_matches_type(CardGroupListResponse, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: SlashSDK) -> None:
        response = client.card_group.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card_group = response.parse()
        assert_matches_type(CardGroupListResponse, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: SlashSDK) -> None:
        with client.card_group.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card_group = response.parse()
            assert_matches_type(CardGroupListResponse, card_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_utilization(self, client: SlashSDK) -> None:
        card_group = client.card_group.get_utilization(
            "cardGroupId",
        )
        assert_matches_type(CardGroupUtilization, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_utilization(self, client: SlashSDK) -> None:
        response = client.card_group.with_raw_response.get_utilization(
            "cardGroupId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card_group = response.parse()
        assert_matches_type(CardGroupUtilization, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_utilization(self, client: SlashSDK) -> None:
        with client.card_group.with_streaming_response.get_utilization(
            "cardGroupId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card_group = response.parse()
            assert_matches_type(CardGroupUtilization, card_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_utilization(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_group_id` but received ''"):
            client.card_group.with_raw_response.get_utilization(
                "",
            )


class TestAsyncCardGroup:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncSlashSDK) -> None:
        card_group = await async_client.card_group.create(
            name="name",
        )
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        card_group = await async_client.card_group.create(
            name="name",
            spending_constraint={
                "country_rule": {
                    "countries": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_category_code_rule": {
                    "merchant_category_codes": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_category_rule": {
                    "merchant_categories": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_rule": {
                    "merchants": ["string"],
                    "restriction": "allowlist",
                },
                "spending_rule": {
                    "transaction_size_limit": {
                        "maximum": {"amount_cents": 0},
                        "minimum": {"amount_cents": 0},
                    },
                    "utilization_limit": {
                        "limit_amount": {"amount_cents": 0},
                        "preset": "daily",
                        "start_date": "startDate",
                        "timezone": "timezone",
                    },
                    "utilization_limit_v2": [
                        {
                            "limit_amount": {"amount_cents": 0},
                            "preset": "daily",
                            "start_date": "startDate",
                            "timezone": "timezone",
                        }
                    ],
                },
            },
            virtual_account_id="virtualAccountId",
        )
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card_group.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card_group = await response.parse()
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card_group.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card_group = await response.parse()
            assert_matches_type(CardGroup, card_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSlashSDK) -> None:
        card_group = await async_client.card_group.retrieve(
            "cardGroupId",
        )
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card_group.with_raw_response.retrieve(
            "cardGroupId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card_group = await response.parse()
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card_group.with_streaming_response.retrieve(
            "cardGroupId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card_group = await response.parse()
            assert_matches_type(CardGroup, card_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_group_id` but received ''"):
            await async_client.card_group.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncSlashSDK) -> None:
        card_group = await async_client.card_group.update(
            card_group_id="cardGroupId",
        )
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        card_group = await async_client.card_group.update(
            card_group_id="cardGroupId",
            name="name",
            spending_constraint={
                "country_rule": {
                    "countries": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_category_code_rule": {
                    "merchant_category_codes": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_category_rule": {
                    "merchant_categories": ["string"],
                    "restriction": "allowlist",
                },
                "merchant_rule": {
                    "merchants": ["string"],
                    "restriction": "allowlist",
                },
                "spending_rule": {
                    "transaction_size_limit": {
                        "maximum": {"amount_cents": 0},
                        "minimum": {"amount_cents": 0},
                    },
                    "utilization_limit": {
                        "limit_amount": {"amount_cents": 0},
                        "preset": "daily",
                        "start_date": "startDate",
                        "timezone": "timezone",
                    },
                    "utilization_limit_v2": [
                        {
                            "limit_amount": {"amount_cents": 0},
                            "preset": "daily",
                            "start_date": "startDate",
                            "timezone": "timezone",
                        }
                    ],
                },
            },
        )
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card_group.with_raw_response.update(
            card_group_id="cardGroupId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card_group = await response.parse()
        assert_matches_type(CardGroup, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card_group.with_streaming_response.update(
            card_group_id="cardGroupId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card_group = await response.parse()
            assert_matches_type(CardGroup, card_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_group_id` but received ''"):
            await async_client.card_group.with_raw_response.update(
                card_group_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSlashSDK) -> None:
        card_group = await async_client.card_group.list()
        assert_matches_type(CardGroupListResponse, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        card_group = await async_client.card_group.list(
            cursor="cursor",
            filter_name="filter:name",
        )
        assert_matches_type(CardGroupListResponse, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card_group.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card_group = await response.parse()
        assert_matches_type(CardGroupListResponse, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card_group.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card_group = await response.parse()
            assert_matches_type(CardGroupListResponse, card_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_utilization(self, async_client: AsyncSlashSDK) -> None:
        card_group = await async_client.card_group.get_utilization(
            "cardGroupId",
        )
        assert_matches_type(CardGroupUtilization, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_utilization(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card_group.with_raw_response.get_utilization(
            "cardGroupId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card_group = await response.parse()
        assert_matches_type(CardGroupUtilization, card_group, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_utilization(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card_group.with_streaming_response.get_utilization(
            "cardGroupId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card_group = await response.parse()
            assert_matches_type(CardGroupUtilization, card_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_utilization(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_group_id` but received ''"):
            await async_client.card_group.with_raw_response.get_utilization(
                "",
            )
