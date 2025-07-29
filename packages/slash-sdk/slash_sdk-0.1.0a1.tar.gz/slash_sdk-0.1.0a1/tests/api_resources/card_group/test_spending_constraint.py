# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types.card import SpendingConstraint

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSpendingConstraint:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_full(self, client: SlashSDK) -> None:
        spending_constraint = client.card_group.spending_constraint.update_full(
            card_group_id="cardGroupId",
        )
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_full_with_all_params(self, client: SlashSDK) -> None:
        spending_constraint = client.card_group.spending_constraint.update_full(
            card_group_id="cardGroupId",
            country_rule={
                "countries": ["string"],
                "restriction": "allowlist",
            },
            merchant_category_code_rule={
                "merchant_category_codes": ["string"],
                "restriction": "allowlist",
            },
            merchant_category_rule={
                "merchant_categories": ["string"],
                "restriction": "allowlist",
            },
            merchant_rule={
                "merchants": ["string"],
                "restriction": "allowlist",
            },
            spending_rule={
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
        )
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_full(self, client: SlashSDK) -> None:
        response = client.card_group.spending_constraint.with_raw_response.update_full(
            card_group_id="cardGroupId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spending_constraint = response.parse()
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_full(self, client: SlashSDK) -> None:
        with client.card_group.spending_constraint.with_streaming_response.update_full(
            card_group_id="cardGroupId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spending_constraint = response.parse()
            assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_full(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_group_id` but received ''"):
            client.card_group.spending_constraint.with_raw_response.update_full(
                card_group_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update_partial(self, client: SlashSDK) -> None:
        spending_constraint = client.card_group.spending_constraint.update_partial(
            card_group_id="cardGroupId",
        )
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_partial_with_all_params(self, client: SlashSDK) -> None:
        spending_constraint = client.card_group.spending_constraint.update_partial(
            card_group_id="cardGroupId",
            country_rule={
                "countries": ["string"],
                "restriction": "allowlist",
            },
            merchant_category_code_rule={
                "merchant_category_codes": ["string"],
                "restriction": "allowlist",
            },
            merchant_category_rule={
                "merchant_categories": ["string"],
                "restriction": "allowlist",
            },
            merchant_rule={
                "merchants": ["string"],
                "restriction": "allowlist",
            },
            spending_rule={
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
        )
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_partial(self, client: SlashSDK) -> None:
        response = client.card_group.spending_constraint.with_raw_response.update_partial(
            card_group_id="cardGroupId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spending_constraint = response.parse()
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_partial(self, client: SlashSDK) -> None:
        with client.card_group.spending_constraint.with_streaming_response.update_partial(
            card_group_id="cardGroupId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spending_constraint = response.parse()
            assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_partial(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_group_id` but received ''"):
            client.card_group.spending_constraint.with_raw_response.update_partial(
                card_group_id="",
            )


class TestAsyncSpendingConstraint:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_full(self, async_client: AsyncSlashSDK) -> None:
        spending_constraint = await async_client.card_group.spending_constraint.update_full(
            card_group_id="cardGroupId",
        )
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_full_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        spending_constraint = await async_client.card_group.spending_constraint.update_full(
            card_group_id="cardGroupId",
            country_rule={
                "countries": ["string"],
                "restriction": "allowlist",
            },
            merchant_category_code_rule={
                "merchant_category_codes": ["string"],
                "restriction": "allowlist",
            },
            merchant_category_rule={
                "merchant_categories": ["string"],
                "restriction": "allowlist",
            },
            merchant_rule={
                "merchants": ["string"],
                "restriction": "allowlist",
            },
            spending_rule={
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
        )
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_full(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card_group.spending_constraint.with_raw_response.update_full(
            card_group_id="cardGroupId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spending_constraint = await response.parse()
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_full(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card_group.spending_constraint.with_streaming_response.update_full(
            card_group_id="cardGroupId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spending_constraint = await response.parse()
            assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_full(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_group_id` but received ''"):
            await async_client.card_group.spending_constraint.with_raw_response.update_full(
                card_group_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_partial(self, async_client: AsyncSlashSDK) -> None:
        spending_constraint = await async_client.card_group.spending_constraint.update_partial(
            card_group_id="cardGroupId",
        )
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_partial_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        spending_constraint = await async_client.card_group.spending_constraint.update_partial(
            card_group_id="cardGroupId",
            country_rule={
                "countries": ["string"],
                "restriction": "allowlist",
            },
            merchant_category_code_rule={
                "merchant_category_codes": ["string"],
                "restriction": "allowlist",
            },
            merchant_category_rule={
                "merchant_categories": ["string"],
                "restriction": "allowlist",
            },
            merchant_rule={
                "merchants": ["string"],
                "restriction": "allowlist",
            },
            spending_rule={
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
        )
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_partial(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.card_group.spending_constraint.with_raw_response.update_partial(
            card_group_id="cardGroupId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        spending_constraint = await response.parse()
        assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_partial(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.card_group.spending_constraint.with_streaming_response.update_partial(
            card_group_id="cardGroupId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            spending_constraint = await response.parse()
            assert_matches_type(SpendingConstraint, spending_constraint, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_partial(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_group_id` but received ''"):
            await async_client.card_group.spending_constraint.with_raw_response.update_partial(
                card_group_id="",
            )
