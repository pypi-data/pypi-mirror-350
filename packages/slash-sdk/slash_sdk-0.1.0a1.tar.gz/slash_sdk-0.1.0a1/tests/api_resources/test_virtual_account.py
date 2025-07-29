# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk.types import (
    VirtualAccount,
    VirtualAccountListResponse,
    VirtualAccountCreateResponse,
    VirtualAccountUpdateResponse,
)
from slash_sdk._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVirtualAccount:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: SlashSDK) -> None:
        virtual_account = client.virtual_account.create(
            account_id="accountId",
            name="name",
        )
        assert_matches_type(VirtualAccountCreateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: SlashSDK) -> None:
        virtual_account = client.virtual_account.create(
            account_id="accountId",
            name="name",
            commission_details={
                "amount": {"amount_cents": 0},
                "frequency": "monthly",
                "type": "flatFee",
                "start_date": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(VirtualAccountCreateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: SlashSDK) -> None:
        response = client.virtual_account.with_raw_response.create(
            account_id="accountId",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        virtual_account = response.parse()
        assert_matches_type(VirtualAccountCreateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: SlashSDK) -> None:
        with client.virtual_account.with_streaming_response.create(
            account_id="accountId",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            virtual_account = response.parse()
            assert_matches_type(VirtualAccountCreateResponse, virtual_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: SlashSDK) -> None:
        virtual_account = client.virtual_account.retrieve(
            "virtualAccountId",
        )
        assert_matches_type(VirtualAccount, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: SlashSDK) -> None:
        response = client.virtual_account.with_raw_response.retrieve(
            "virtualAccountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        virtual_account = response.parse()
        assert_matches_type(VirtualAccount, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: SlashSDK) -> None:
        with client.virtual_account.with_streaming_response.retrieve(
            "virtualAccountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            virtual_account = response.parse()
            assert_matches_type(VirtualAccount, virtual_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `virtual_account_id` but received ''"):
            client.virtual_account.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update_overload_1(self, client: SlashSDK) -> None:
        virtual_account = client.virtual_account.update(
            virtual_account_id="virtualAccountId",
            action="update",
        )
        assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params_overload_1(self, client: SlashSDK) -> None:
        virtual_account = client.virtual_account.update(
            virtual_account_id="virtualAccountId",
            action="update",
            commission_details={
                "amount": {"amount_cents": 0},
                "frequency": "monthly",
                "type": "flatFee",
                "start_date": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
            name="name",
        )
        assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_overload_1(self, client: SlashSDK) -> None:
        response = client.virtual_account.with_raw_response.update(
            virtual_account_id="virtualAccountId",
            action="update",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        virtual_account = response.parse()
        assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_overload_1(self, client: SlashSDK) -> None:
        with client.virtual_account.with_streaming_response.update(
            virtual_account_id="virtualAccountId",
            action="update",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            virtual_account = response.parse()
            assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_overload_1(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `virtual_account_id` but received ''"):
            client.virtual_account.with_raw_response.update(
                virtual_account_id="",
                action="update",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update_overload_2(self, client: SlashSDK) -> None:
        virtual_account = client.virtual_account.update(
            virtual_account_id="virtualAccountId",
            action="close",
        )
        assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_overload_2(self, client: SlashSDK) -> None:
        response = client.virtual_account.with_raw_response.update(
            virtual_account_id="virtualAccountId",
            action="close",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        virtual_account = response.parse()
        assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_overload_2(self, client: SlashSDK) -> None:
        with client.virtual_account.with_streaming_response.update(
            virtual_account_id="virtualAccountId",
            action="close",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            virtual_account = response.parse()
            assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_overload_2(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `virtual_account_id` but received ''"):
            client.virtual_account.with_raw_response.update(
                virtual_account_id="",
                action="close",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: SlashSDK) -> None:
        virtual_account = client.virtual_account.list()
        assert_matches_type(VirtualAccountListResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: SlashSDK) -> None:
        virtual_account = client.virtual_account.list(
            cursor="cursor",
            filter_account_id="filter:accountId",
            filter_include_closed_accounts="true",
        )
        assert_matches_type(VirtualAccountListResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: SlashSDK) -> None:
        response = client.virtual_account.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        virtual_account = response.parse()
        assert_matches_type(VirtualAccountListResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: SlashSDK) -> None:
        with client.virtual_account.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            virtual_account = response.parse()
            assert_matches_type(VirtualAccountListResponse, virtual_account, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncVirtualAccount:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncSlashSDK) -> None:
        virtual_account = await async_client.virtual_account.create(
            account_id="accountId",
            name="name",
        )
        assert_matches_type(VirtualAccountCreateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        virtual_account = await async_client.virtual_account.create(
            account_id="accountId",
            name="name",
            commission_details={
                "amount": {"amount_cents": 0},
                "frequency": "monthly",
                "type": "flatFee",
                "start_date": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(VirtualAccountCreateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.virtual_account.with_raw_response.create(
            account_id="accountId",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        virtual_account = await response.parse()
        assert_matches_type(VirtualAccountCreateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.virtual_account.with_streaming_response.create(
            account_id="accountId",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            virtual_account = await response.parse()
            assert_matches_type(VirtualAccountCreateResponse, virtual_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSlashSDK) -> None:
        virtual_account = await async_client.virtual_account.retrieve(
            "virtualAccountId",
        )
        assert_matches_type(VirtualAccount, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.virtual_account.with_raw_response.retrieve(
            "virtualAccountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        virtual_account = await response.parse()
        assert_matches_type(VirtualAccount, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.virtual_account.with_streaming_response.retrieve(
            "virtualAccountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            virtual_account = await response.parse()
            assert_matches_type(VirtualAccount, virtual_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `virtual_account_id` but received ''"):
            await async_client.virtual_account.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_overload_1(self, async_client: AsyncSlashSDK) -> None:
        virtual_account = await async_client.virtual_account.update(
            virtual_account_id="virtualAccountId",
            action="update",
        )
        assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params_overload_1(self, async_client: AsyncSlashSDK) -> None:
        virtual_account = await async_client.virtual_account.update(
            virtual_account_id="virtualAccountId",
            action="update",
            commission_details={
                "amount": {"amount_cents": 0},
                "frequency": "monthly",
                "type": "flatFee",
                "start_date": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
            name="name",
        )
        assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_overload_1(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.virtual_account.with_raw_response.update(
            virtual_account_id="virtualAccountId",
            action="update",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        virtual_account = await response.parse()
        assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_overload_1(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.virtual_account.with_streaming_response.update(
            virtual_account_id="virtualAccountId",
            action="update",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            virtual_account = await response.parse()
            assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_overload_1(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `virtual_account_id` but received ''"):
            await async_client.virtual_account.with_raw_response.update(
                virtual_account_id="",
                action="update",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_overload_2(self, async_client: AsyncSlashSDK) -> None:
        virtual_account = await async_client.virtual_account.update(
            virtual_account_id="virtualAccountId",
            action="close",
        )
        assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_overload_2(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.virtual_account.with_raw_response.update(
            virtual_account_id="virtualAccountId",
            action="close",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        virtual_account = await response.parse()
        assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_overload_2(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.virtual_account.with_streaming_response.update(
            virtual_account_id="virtualAccountId",
            action="close",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            virtual_account = await response.parse()
            assert_matches_type(VirtualAccountUpdateResponse, virtual_account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_overload_2(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `virtual_account_id` but received ''"):
            await async_client.virtual_account.with_raw_response.update(
                virtual_account_id="",
                action="close",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSlashSDK) -> None:
        virtual_account = await async_client.virtual_account.list()
        assert_matches_type(VirtualAccountListResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        virtual_account = await async_client.virtual_account.list(
            cursor="cursor",
            filter_account_id="filter:accountId",
            filter_include_closed_accounts="true",
        )
        assert_matches_type(VirtualAccountListResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.virtual_account.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        virtual_account = await response.parse()
        assert_matches_type(VirtualAccountListResponse, virtual_account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.virtual_account.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            virtual_account = await response.parse()
            assert_matches_type(VirtualAccountListResponse, virtual_account, path=["response"])

        assert cast(Any, response.is_closed) is True
