# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import (
    CardListResponse,
    CardGroupUtilization,
)
from slash_sdk.types.card import Card

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCard:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: SlashSDK) -> None:
        card = client.card.create(
            name="name",
            type="virtual",
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: SlashSDK) -> None:
        card = client.card.create(
            name="name",
            type="virtual",
            account_id="accountId",
            card_group_id="cardGroupId",
            card_product_id="cardProductId",
            is_single_use=True,
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
            user_data={"foo": "bar"},
            virtual_account_id="virtualAccountId",
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: SlashSDK) -> None:
        response = client.card.with_raw_response.create(
            name="name",
            type="virtual",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: SlashSDK) -> None:
        with client.card.with_streaming_response.create(
            name="name",
            type="virtual",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card = response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: SlashSDK) -> None:
        card = client.card.retrieve(
            card_id="cardId",
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: SlashSDK) -> None:
        card = client.card.retrieve(
            card_id="cardId",
            include_cvv="true",
            include_pan="true",
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: SlashSDK) -> None:
        response = client.card.with_raw_response.retrieve(
            card_id="cardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: SlashSDK) -> None:
        with client.card.with_streaming_response.retrieve(
            card_id="cardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card = response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_id` but received ''"):
            client.card.with_raw_response.retrieve(
                card_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: SlashSDK) -> None:
        card = client.card.update(
            card_id="cardId",
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: SlashSDK) -> None:
        card = client.card.update(
            card_id="cardId",
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
            status="active",
            user_data={"foo": "bar"},
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: SlashSDK) -> None:
        response = client.card.with_raw_response.update(
            card_id="cardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: SlashSDK) -> None:
        with client.card.with_streaming_response.update(
            card_id="cardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card = response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_id` but received ''"):
            client.card.with_raw_response.update(
                card_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: SlashSDK) -> None:
        card = client.card.list()
        assert_matches_type(CardListResponse, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: SlashSDK) -> None:
        card = client.card.list(
            cursor="cursor",
            filter_account_id="filter:accountId",
            filter_card_group_id="filter:cardGroupId",
            filter_card_group_name="filter:cardGroupName",
            filter_legal_entity_id="filter:legalEntityId",
            filter_status="active",
            filter_virtual_account_id="filter:virtualAccountId",
            sort="createdAt",
            sort_direction="ASC",
        )
        assert_matches_type(CardListResponse, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: SlashSDK) -> None:
        response = client.card.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card = response.parse()
        assert_matches_type(CardListResponse, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: SlashSDK) -> None:
        with client.card.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card = response.parse()
            assert_matches_type(CardListResponse, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_utilization(self, client: SlashSDK) -> None:
        card = client.card.get_utilization(
            "cardId",
        )
        assert_matches_type(CardGroupUtilization, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_utilization(self, client: SlashSDK) -> None:
        response = client.card.with_raw_response.get_utilization(
            "cardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card = response.parse()
        assert_matches_type(CardGroupUtilization, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_utilization(self, client: SlashSDK) -> None:
        with client.card.with_streaming_response.get_utilization(
            "cardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card = response.parse()
            assert_matches_type(CardGroupUtilization, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_utilization(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_id` but received ''"):
            client.card.with_raw_response.get_utilization(
                "",
            )


class TestAsyncCard:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncSlashSDK) -> None:
        card = await async_client.card.create(
            name="name",
            type="virtual",
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        card = await async_client.card.create(
            name="name",
            type="virtual",
            account_id="accountId",
            card_group_id="cardGroupId",
            card_product_id="cardProductId",
            is_single_use=True,
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
            user_data={"foo": "bar"},
            virtual_account_id="virtualAccountId",
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card.with_raw_response.create(
            name="name",
            type="virtual",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card = await response.parse()
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card.with_streaming_response.create(
            name="name",
            type="virtual",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card = await response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSlashSDK) -> None:
        card = await async_client.card.retrieve(
            card_id="cardId",
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        card = await async_client.card.retrieve(
            card_id="cardId",
            include_cvv="true",
            include_pan="true",
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card.with_raw_response.retrieve(
            card_id="cardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card = await response.parse()
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card.with_streaming_response.retrieve(
            card_id="cardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card = await response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_id` but received ''"):
            await async_client.card.with_raw_response.retrieve(
                card_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncSlashSDK) -> None:
        card = await async_client.card.update(
            card_id="cardId",
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        card = await async_client.card.update(
            card_id="cardId",
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
            status="active",
            user_data={"foo": "bar"},
        )
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card.with_raw_response.update(
            card_id="cardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card = await response.parse()
        assert_matches_type(Card, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card.with_streaming_response.update(
            card_id="cardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card = await response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_id` but received ''"):
            await async_client.card.with_raw_response.update(
                card_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSlashSDK) -> None:
        card = await async_client.card.list()
        assert_matches_type(CardListResponse, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        card = await async_client.card.list(
            cursor="cursor",
            filter_account_id="filter:accountId",
            filter_card_group_id="filter:cardGroupId",
            filter_card_group_name="filter:cardGroupName",
            filter_legal_entity_id="filter:legalEntityId",
            filter_status="active",
            filter_virtual_account_id="filter:virtualAccountId",
            sort="createdAt",
            sort_direction="ASC",
        )
        assert_matches_type(CardListResponse, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card = await response.parse()
        assert_matches_type(CardListResponse, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card = await response.parse()
            assert_matches_type(CardListResponse, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_utilization(self, async_client: AsyncSlashSDK) -> None:
        card = await async_client.card.get_utilization(
            "cardId",
        )
        assert_matches_type(CardGroupUtilization, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_utilization(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card.with_raw_response.get_utilization(
            "cardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        card = await response.parse()
        assert_matches_type(CardGroupUtilization, card, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_utilization(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card.with_streaming_response.get_utilization(
            "cardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            card = await response.parse()
            assert_matches_type(CardGroupUtilization, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_utilization(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_id` but received ''"):
            await async_client.card.with_raw_response.get_utilization(
                "",
            )
