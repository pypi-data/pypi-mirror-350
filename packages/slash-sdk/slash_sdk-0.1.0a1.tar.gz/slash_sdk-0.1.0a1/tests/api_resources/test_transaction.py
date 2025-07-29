# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import (
    Transaction,
    TransactionListResponse,
    TransactionAggregateResponse,
    TransactionUpdateNoteResponse,
    TransactionRetrieveFeeDetailsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTransaction:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: SlashSDK) -> None:
        transaction = client.transaction.retrieve(
            "transactionId",
        )
        assert_matches_type(Transaction, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: SlashSDK) -> None:
        response = client.transaction.with_raw_response.retrieve(
            "transactionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = response.parse()
        assert_matches_type(Transaction, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: SlashSDK) -> None:
        with client.transaction.with_streaming_response.retrieve(
            "transactionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = response.parse()
            assert_matches_type(Transaction, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transaction.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: SlashSDK) -> None:
        transaction = client.transaction.list()
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: SlashSDK) -> None:
        transaction = client.transaction.list(
            account_id="accountId",
            cursor="cursor",
            filter_account_id="filter:accountId",
            filter_card_id="filter:cardId",
            filter_detailed_status="pending",
            filter_from_authorized_at="filter:from_authorized_at",
            filter_from_date="filter:from_date",
            filter_legal_entity_id="filter:legalEntityId",
            filter_status="pending",
            filter_to_authorized_at="filter:to_authorized_at",
            filter_to_date="filter:to_date",
            filter_virtual_account_id="filter:virtualAccountId",
        )
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: SlashSDK) -> None:
        response = client.transaction.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = response.parse()
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: SlashSDK) -> None:
        with client.transaction.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = response.parse()
            assert_matches_type(TransactionListResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_aggregate(self, client: SlashSDK) -> None:
        transaction = client.transaction.aggregate()
        assert_matches_type(TransactionAggregateResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_aggregate_with_all_params(self, client: SlashSDK) -> None:
        transaction = client.transaction.aggregate(
            account_id="accountId",
            filter_account_id="filter:accountId",
            filter_card_id="filter:cardId",
            filter_detailed_status="pending",
            filter_from_authorized_at="filter:from_authorized_at",
            filter_from_date="filter:from_date",
            filter_legal_entity_id="filter:legalEntityId",
            filter_status="pending",
            filter_to_authorized_at="filter:to_authorized_at",
            filter_to_date="filter:to_date",
            filter_virtual_account_id="filter:virtualAccountId",
        )
        assert_matches_type(TransactionAggregateResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_aggregate(self, client: SlashSDK) -> None:
        response = client.transaction.with_raw_response.aggregate()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = response.parse()
        assert_matches_type(TransactionAggregateResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_aggregate(self, client: SlashSDK) -> None:
        with client.transaction.with_streaming_response.aggregate() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = response.parse()
            assert_matches_type(TransactionAggregateResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_fee_details(self, client: SlashSDK) -> None:
        transaction = client.transaction.retrieve_fee_details(
            "transactionId",
        )
        assert_matches_type(TransactionRetrieveFeeDetailsResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_fee_details(self, client: SlashSDK) -> None:
        response = client.transaction.with_raw_response.retrieve_fee_details(
            "transactionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = response.parse()
        assert_matches_type(TransactionRetrieveFeeDetailsResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_fee_details(self, client: SlashSDK) -> None:
        with client.transaction.with_streaming_response.retrieve_fee_details(
            "transactionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = response.parse()
            assert_matches_type(TransactionRetrieveFeeDetailsResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_fee_details(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transaction.with_raw_response.retrieve_fee_details(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update_note(self, client: SlashSDK) -> None:
        transaction = client.transaction.update_note(
            transaction_id="transactionId",
            note="note",
        )
        assert_matches_type(TransactionUpdateNoteResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_note(self, client: SlashSDK) -> None:
        response = client.transaction.with_raw_response.update_note(
            transaction_id="transactionId",
            note="note",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = response.parse()
        assert_matches_type(TransactionUpdateNoteResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_note(self, client: SlashSDK) -> None:
        with client.transaction.with_streaming_response.update_note(
            transaction_id="transactionId",
            note="note",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = response.parse()
            assert_matches_type(TransactionUpdateNoteResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_note(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transaction.with_raw_response.update_note(
                transaction_id="",
                note="note",
            )


class TestAsyncTransaction:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSlashSDK) -> None:
        transaction = await async_client.transaction.retrieve(
            "transactionId",
        )
        assert_matches_type(Transaction, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.transaction.with_raw_response.retrieve(
            "transactionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = await response.parse()
        assert_matches_type(Transaction, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.transaction.with_streaming_response.retrieve(
            "transactionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = await response.parse()
            assert_matches_type(Transaction, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transaction.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSlashSDK) -> None:
        transaction = await async_client.transaction.list()
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        transaction = await async_client.transaction.list(
            account_id="accountId",
            cursor="cursor",
            filter_account_id="filter:accountId",
            filter_card_id="filter:cardId",
            filter_detailed_status="pending",
            filter_from_authorized_at="filter:from_authorized_at",
            filter_from_date="filter:from_date",
            filter_legal_entity_id="filter:legalEntityId",
            filter_status="pending",
            filter_to_authorized_at="filter:to_authorized_at",
            filter_to_date="filter:to_date",
            filter_virtual_account_id="filter:virtualAccountId",
        )
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.transaction.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = await response.parse()
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.transaction.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = await response.parse()
            assert_matches_type(TransactionListResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_aggregate(self, async_client: AsyncSlashSDK) -> None:
        transaction = await async_client.transaction.aggregate()
        assert_matches_type(TransactionAggregateResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_aggregate_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        transaction = await async_client.transaction.aggregate(
            account_id="accountId",
            filter_account_id="filter:accountId",
            filter_card_id="filter:cardId",
            filter_detailed_status="pending",
            filter_from_authorized_at="filter:from_authorized_at",
            filter_from_date="filter:from_date",
            filter_legal_entity_id="filter:legalEntityId",
            filter_status="pending",
            filter_to_authorized_at="filter:to_authorized_at",
            filter_to_date="filter:to_date",
            filter_virtual_account_id="filter:virtualAccountId",
        )
        assert_matches_type(TransactionAggregateResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_aggregate(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.transaction.with_raw_response.aggregate()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = await response.parse()
        assert_matches_type(TransactionAggregateResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_aggregate(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.transaction.with_streaming_response.aggregate() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = await response.parse()
            assert_matches_type(TransactionAggregateResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_fee_details(self, async_client: AsyncSlashSDK) -> None:
        transaction = await async_client.transaction.retrieve_fee_details(
            "transactionId",
        )
        assert_matches_type(TransactionRetrieveFeeDetailsResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_fee_details(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.transaction.with_raw_response.retrieve_fee_details(
            "transactionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = await response.parse()
        assert_matches_type(TransactionRetrieveFeeDetailsResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_fee_details(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.transaction.with_streaming_response.retrieve_fee_details(
            "transactionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = await response.parse()
            assert_matches_type(TransactionRetrieveFeeDetailsResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_fee_details(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transaction.with_raw_response.retrieve_fee_details(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_note(self, async_client: AsyncSlashSDK) -> None:
        transaction = await async_client.transaction.update_note(
            transaction_id="transactionId",
            note="note",
        )
        assert_matches_type(TransactionUpdateNoteResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_note(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.transaction.with_raw_response.update_note(
            transaction_id="transactionId",
            note="note",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = await response.parse()
        assert_matches_type(TransactionUpdateNoteResponse, transaction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_note(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.transaction.with_streaming_response.update_note(
            transaction_id="transactionId",
            note="note",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = await response.parse()
            assert_matches_type(TransactionUpdateNoteResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_note(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transaction.with_raw_response.update_note(
                transaction_id="",
                note="note",
            )
