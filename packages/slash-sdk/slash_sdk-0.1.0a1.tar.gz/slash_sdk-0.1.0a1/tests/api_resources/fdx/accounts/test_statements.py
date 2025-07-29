# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from slash_sdk import SlashSDK, AsyncSlashSDK
from tests.utils import assert_matches_type
from slash_sdk._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)
from slash_sdk.types.fdx.accounts import StatementListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStatements:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: SlashSDK) -> None:
        statement = client.fdx.accounts.statements.list(
            account_id="accountId",
        )
        assert_matches_type(StatementListResponse, statement, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: SlashSDK) -> None:
        statement = client.fdx.accounts.statements.list(
            account_id="accountId",
            end_time="endTime",
            limit="limit",
            offset="offset",
            start_time="startTime",
        )
        assert_matches_type(StatementListResponse, statement, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: SlashSDK) -> None:
        response = client.fdx.accounts.statements.with_raw_response.list(
            account_id="accountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        statement = response.parse()
        assert_matches_type(StatementListResponse, statement, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: SlashSDK) -> None:
        with client.fdx.accounts.statements.with_streaming_response.list(
            account_id="accountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            statement = response.parse()
            assert_matches_type(StatementListResponse, statement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.fdx.accounts.statements.with_raw_response.list(
                account_id="",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve_pdf(self, client: SlashSDK, respx_mock: MockRouter) -> None:
        respx_mock.get("/fdx/accounts/accountId/statements/statementId").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        statement = client.fdx.accounts.statements.retrieve_pdf(
            statement_id="statementId",
            account_id="accountId",
        )
        assert statement.is_closed
        assert statement.json() == {"foo": "bar"}
        assert cast(Any, statement.is_closed) is True
        assert isinstance(statement, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve_pdf(self, client: SlashSDK, respx_mock: MockRouter) -> None:
        respx_mock.get("/fdx/accounts/accountId/statements/statementId").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        statement = client.fdx.accounts.statements.with_raw_response.retrieve_pdf(
            statement_id="statementId",
            account_id="accountId",
        )

        assert statement.is_closed is True
        assert statement.http_request.headers.get("X-Stainless-Lang") == "python"
        assert statement.json() == {"foo": "bar"}
        assert isinstance(statement, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve_pdf(self, client: SlashSDK, respx_mock: MockRouter) -> None:
        respx_mock.get("/fdx/accounts/accountId/statements/statementId").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.fdx.accounts.statements.with_streaming_response.retrieve_pdf(
            statement_id="statementId",
            account_id="accountId",
        ) as statement:
            assert not statement.is_closed
            assert statement.http_request.headers.get("X-Stainless-Lang") == "python"

            assert statement.json() == {"foo": "bar"}
            assert cast(Any, statement.is_closed) is True
            assert isinstance(statement, StreamedBinaryAPIResponse)

        assert cast(Any, statement.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve_pdf(self, client: SlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.fdx.accounts.statements.with_raw_response.retrieve_pdf(
                statement_id="statementId",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `statement_id` but received ''"):
            client.fdx.accounts.statements.with_raw_response.retrieve_pdf(
                statement_id="",
                account_id="accountId",
            )


class TestAsyncStatements:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSlashSDK) -> None:
        statement = await async_client.fdx.accounts.statements.list(
            account_id="accountId",
        )
        assert_matches_type(StatementListResponse, statement, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSlashSDK) -> None:
        statement = await async_client.fdx.accounts.statements.list(
            account_id="accountId",
            end_time="endTime",
            limit="limit",
            offset="offset",
            start_time="startTime",
        )
        assert_matches_type(StatementListResponse, statement, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSlashSDK) -> None:
        response = await async_client.fdx.accounts.statements.with_raw_response.list(
            account_id="accountId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        statement = await response.parse()
        assert_matches_type(StatementListResponse, statement, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSlashSDK) -> None:
        async with async_client.fdx.accounts.statements.with_streaming_response.list(
            account_id="accountId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            statement = await response.parse()
            assert_matches_type(StatementListResponse, statement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.fdx.accounts.statements.with_raw_response.list(
                account_id="",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve_pdf(self, async_client: AsyncSlashSDK, respx_mock: MockRouter) -> None:
        respx_mock.get("/fdx/accounts/accountId/statements/statementId").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        statement = await async_client.fdx.accounts.statements.retrieve_pdf(
            statement_id="statementId",
            account_id="accountId",
        )
        assert statement.is_closed
        assert await statement.json() == {"foo": "bar"}
        assert cast(Any, statement.is_closed) is True
        assert isinstance(statement, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve_pdf(self, async_client: AsyncSlashSDK, respx_mock: MockRouter) -> None:
        respx_mock.get("/fdx/accounts/accountId/statements/statementId").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        statement = await async_client.fdx.accounts.statements.with_raw_response.retrieve_pdf(
            statement_id="statementId",
            account_id="accountId",
        )

        assert statement.is_closed is True
        assert statement.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await statement.json() == {"foo": "bar"}
        assert isinstance(statement, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve_pdf(self, async_client: AsyncSlashSDK, respx_mock: MockRouter) -> None:
        respx_mock.get("/fdx/accounts/accountId/statements/statementId").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.fdx.accounts.statements.with_streaming_response.retrieve_pdf(
            statement_id="statementId",
            account_id="accountId",
        ) as statement:
            assert not statement.is_closed
            assert statement.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await statement.json() == {"foo": "bar"}
            assert cast(Any, statement.is_closed) is True
            assert isinstance(statement, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, statement.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve_pdf(self, async_client: AsyncSlashSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.fdx.accounts.statements.with_raw_response.retrieve_pdf(
                statement_id="statementId",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `statement_id` but received ''"):
            await async_client.fdx.accounts.statements.with_raw_response.retrieve_pdf(
                statement_id="",
                account_id="accountId",
            )
