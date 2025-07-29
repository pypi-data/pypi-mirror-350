# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types.fdx import (
    AccountListResponse,
    AccountRetrieveResponse,
    AccountRetrieveContactResponse,
    AccountListTransactionsResponse,
    AccountRetrievePaymentNetworksResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAccounts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: SlashSDK) -> None:
        account = client.fdx.accounts.retrieve(
            "accountId",
        )
        assert_matches_type(AccountRetrieveResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: SlashSDK) -> None:
        response = client.fdx.accounts.with_raw_response.retrieve(
            "accountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountRetrieveResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: SlashSDK) -> None:
        with client.fdx.accounts.with_streaming_response.retrieve(
            "accountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountRetrieveResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.fdx.accounts.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: SlashSDK) -> None:
        account = client.fdx.accounts.list()
        assert_matches_type(AccountListResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: SlashSDK) -> None:
        account = client.fdx.accounts.list(
            limit="limit",
            offset="offset",
        )
        assert_matches_type(AccountListResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: SlashSDK) -> None:
        response = client.fdx.accounts.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountListResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: SlashSDK) -> None:
        with client.fdx.accounts.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountListResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list_transactions(self, client: SlashSDK) -> None:
        account = client.fdx.accounts.list_transactions(
            account_id="accountId",
        )
        assert_matches_type(AccountListTransactionsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_transactions_with_all_params(self, client: SlashSDK) -> None:
        account = client.fdx.accounts.list_transactions(
            account_id="accountId",
            end_time="endTime",
            limit="limit",
            offset="offset",
            start_time="startTime",
        )
        assert_matches_type(AccountListTransactionsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_transactions(self, client: SlashSDK) -> None:
        response = client.fdx.accounts.with_raw_response.list_transactions(
            account_id="accountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountListTransactionsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_transactions(self, client: SlashSDK) -> None:
        with client.fdx.accounts.with_streaming_response.list_transactions(
            account_id="accountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountListTransactionsResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list_transactions(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.fdx.accounts.with_raw_response.list_transactions(
                account_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_contact(self, client: SlashSDK) -> None:
        account = client.fdx.accounts.retrieve_contact(
            "accountId",
        )
        assert_matches_type(AccountRetrieveContactResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_contact(self, client: SlashSDK) -> None:
        response = client.fdx.accounts.with_raw_response.retrieve_contact(
            "accountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountRetrieveContactResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_contact(self, client: SlashSDK) -> None:
        with client.fdx.accounts.with_streaming_response.retrieve_contact(
            "accountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountRetrieveContactResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_contact(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.fdx.accounts.with_raw_response.retrieve_contact(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_payment_networks(self, client: SlashSDK) -> None:
        account = client.fdx.accounts.retrieve_payment_networks(
            account_id="accountId",
        )
        assert_matches_type(AccountRetrievePaymentNetworksResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_payment_networks_with_all_params(self, client: SlashSDK) -> None:
        account = client.fdx.accounts.retrieve_payment_networks(
            account_id="accountId",
            limit="limit",
            offset="offset",
        )
        assert_matches_type(AccountRetrievePaymentNetworksResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_payment_networks(self, client: SlashSDK) -> None:
        response = client.fdx.accounts.with_raw_response.retrieve_payment_networks(
            account_id="accountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountRetrievePaymentNetworksResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_payment_networks(self, client: SlashSDK) -> None:
        with client.fdx.accounts.with_streaming_response.retrieve_payment_networks(
            account_id="accountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountRetrievePaymentNetworksResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_payment_networks(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.fdx.accounts.with_raw_response.retrieve_payment_networks(
                account_id="",
            )


class TestAsyncAccounts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSlashSDK) -> None:
        account = await async_client.fdx.accounts.retrieve(
            "accountId",
        )
        assert_matches_type(AccountRetrieveResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.fdx.accounts.with_raw_response.retrieve(
            "accountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountRetrieveResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.fdx.accounts.with_streaming_response.retrieve(
            "accountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountRetrieveResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.fdx.accounts.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSlashSDK) -> None:
        account = await async_client.fdx.accounts.list()
        assert_matches_type(AccountListResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        account = await async_client.fdx.accounts.list(
            limit="limit",
            offset="offset",
        )
        assert_matches_type(AccountListResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.fdx.accounts.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountListResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.fdx.accounts.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountListResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_transactions(self, async_client: AsyncSlashSDK) -> None:
        account = await async_client.fdx.accounts.list_transactions(
            account_id="accountId",
        )
        assert_matches_type(AccountListTransactionsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_transactions_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        account = await async_client.fdx.accounts.list_transactions(
            account_id="accountId",
            end_time="endTime",
            limit="limit",
            offset="offset",
            start_time="startTime",
        )
        assert_matches_type(AccountListTransactionsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_transactions(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.fdx.accounts.with_raw_response.list_transactions(
            account_id="accountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountListTransactionsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_transactions(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.fdx.accounts.with_streaming_response.list_transactions(
            account_id="accountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountListTransactionsResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list_transactions(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.fdx.accounts.with_raw_response.list_transactions(
                account_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_contact(self, async_client: AsyncSlashSDK) -> None:
        account = await async_client.fdx.accounts.retrieve_contact(
            "accountId",
        )
        assert_matches_type(AccountRetrieveContactResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_contact(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.fdx.accounts.with_raw_response.retrieve_contact(
            "accountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountRetrieveContactResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_contact(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.fdx.accounts.with_streaming_response.retrieve_contact(
            "accountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountRetrieveContactResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_contact(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.fdx.accounts.with_raw_response.retrieve_contact(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_payment_networks(self, async_client: AsyncSlashSDK) -> None:
        account = await async_client.fdx.accounts.retrieve_payment_networks(
            account_id="accountId",
        )
        assert_matches_type(AccountRetrievePaymentNetworksResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_payment_networks_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        account = await async_client.fdx.accounts.retrieve_payment_networks(
            account_id="accountId",
            limit="limit",
            offset="offset",
        )
        assert_matches_type(AccountRetrievePaymentNetworksResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_payment_networks(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.fdx.accounts.with_raw_response.retrieve_payment_networks(
            account_id="accountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountRetrievePaymentNetworksResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_payment_networks(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.fdx.accounts.with_streaming_response.retrieve_payment_networks(
            account_id="accountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountRetrievePaymentNetworksResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_payment_networks(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.fdx.accounts.with_raw_response.retrieve_payment_networks(
                account_id="",
            )
