# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, cast

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from .statements import (
    StatementsResource,
    AsyncStatementsResource,
    StatementsResourceWithRawResponse,
    AsyncStatementsResourceWithRawResponse,
    StatementsResourceWithStreamingResponse,
    AsyncStatementsResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....types.fdx import (
    account_list_params,
    account_list_transactions_params,
    account_retrieve_payment_networks_params,
)
from ...._base_client import make_request_options
from ....types.fdx.account_list_response import AccountListResponse
from ....types.fdx.account_retrieve_response import AccountRetrieveResponse
from ....types.fdx.account_retrieve_contact_response import AccountRetrieveContactResponse
from ....types.fdx.account_list_transactions_response import AccountListTransactionsResponse
from ....types.fdx.account_retrieve_payment_networks_response import AccountRetrievePaymentNetworksResponse

__all__ = ["AccountsResource", "AsyncAccountsResource"]


class AccountsResource(SyncAPIResource):
    @cached_property
    def statements(self) -> StatementsResource:
        return StatementsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AccountsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrieveResponse:
        """
        Get account balances and liabilities

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return cast(
            AccountRetrieveResponse,
            self._get(
                f"/fdx/accounts/{account_id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, AccountRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        limit: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountListResponse:
        """
        List all accounts

        Args:
          limit: The number of items to return (default 100, max 1000)

          offset: The number of items to skip before starting to collect the result set

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/fdx/accounts",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    account_list_params.AccountListParams,
                ),
            ),
            cast_to=AccountListResponse,
        )

    def list_transactions(
        self,
        account_id: str,
        *,
        end_time: str | NotGiven = NOT_GIVEN,
        limit: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        start_time: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountListTransactionsResponse:
        """
        Search for transactions

        Args:
          end_time: End time for use in retrieval of transactions (ISO 8601).

          limit: The number of items to return (default 100, max 1000)

          offset: The ID of the last item in the previous page of results

          start_time: Start time for use in retrieval of transactions (ISO 8601).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            f"/fdx/accounts/{account_id}/transactions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end_time": end_time,
                        "limit": limit,
                        "offset": offset,
                        "start_time": start_time,
                    },
                    account_list_transactions_params.AccountListTransactionsParams,
                ),
            ),
            cast_to=AccountListTransactionsResponse,
        )

    def retrieve_contact(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrieveContactResponse:
        """
        Get an account's contact information

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            f"/fdx/accounts/{account_id}/contact",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrieveContactResponse,
        )

    def retrieve_payment_networks(
        self,
        account_id: str,
        *,
        limit: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrievePaymentNetworksResponse:
        """
        Get payment networks supported by the account

        Args:
          limit: The number of items to return (default 100, max 1000)

          offset: The ID of the last item in the previous page of results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            f"/fdx/accounts/{account_id}/payment-networks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    account_retrieve_payment_networks_params.AccountRetrievePaymentNetworksParams,
                ),
            ),
            cast_to=AccountRetrievePaymentNetworksResponse,
        )


class AsyncAccountsResource(AsyncAPIResource):
    @cached_property
    def statements(self) -> AsyncStatementsResource:
        return AsyncStatementsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncAccountsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrieveResponse:
        """
        Get account balances and liabilities

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return cast(
            AccountRetrieveResponse,
            await self._get(
                f"/fdx/accounts/{account_id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, AccountRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def list(
        self,
        *,
        limit: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountListResponse:
        """
        List all accounts

        Args:
          limit: The number of items to return (default 100, max 1000)

          offset: The number of items to skip before starting to collect the result set

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/fdx/accounts",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    account_list_params.AccountListParams,
                ),
            ),
            cast_to=AccountListResponse,
        )

    async def list_transactions(
        self,
        account_id: str,
        *,
        end_time: str | NotGiven = NOT_GIVEN,
        limit: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        start_time: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountListTransactionsResponse:
        """
        Search for transactions

        Args:
          end_time: End time for use in retrieval of transactions (ISO 8601).

          limit: The number of items to return (default 100, max 1000)

          offset: The ID of the last item in the previous page of results

          start_time: Start time for use in retrieval of transactions (ISO 8601).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            f"/fdx/accounts/{account_id}/transactions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end_time": end_time,
                        "limit": limit,
                        "offset": offset,
                        "start_time": start_time,
                    },
                    account_list_transactions_params.AccountListTransactionsParams,
                ),
            ),
            cast_to=AccountListTransactionsResponse,
        )

    async def retrieve_contact(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrieveContactResponse:
        """
        Get an account's contact information

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            f"/fdx/accounts/{account_id}/contact",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrieveContactResponse,
        )

    async def retrieve_payment_networks(
        self,
        account_id: str,
        *,
        limit: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrievePaymentNetworksResponse:
        """
        Get payment networks supported by the account

        Args:
          limit: The number of items to return (default 100, max 1000)

          offset: The ID of the last item in the previous page of results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            f"/fdx/accounts/{account_id}/payment-networks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    account_retrieve_payment_networks_params.AccountRetrievePaymentNetworksParams,
                ),
            ),
            cast_to=AccountRetrievePaymentNetworksResponse,
        )


class AccountsResourceWithRawResponse:
    def __init__(self, accounts: AccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = to_raw_response_wrapper(
            accounts.retrieve,
        )
        self.list = to_raw_response_wrapper(
            accounts.list,
        )
        self.list_transactions = to_raw_response_wrapper(
            accounts.list_transactions,
        )
        self.retrieve_contact = to_raw_response_wrapper(
            accounts.retrieve_contact,
        )
        self.retrieve_payment_networks = to_raw_response_wrapper(
            accounts.retrieve_payment_networks,
        )

    @cached_property
    def statements(self) -> StatementsResourceWithRawResponse:
        return StatementsResourceWithRawResponse(self._accounts.statements)


class AsyncAccountsResourceWithRawResponse:
    def __init__(self, accounts: AsyncAccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = async_to_raw_response_wrapper(
            accounts.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            accounts.list,
        )
        self.list_transactions = async_to_raw_response_wrapper(
            accounts.list_transactions,
        )
        self.retrieve_contact = async_to_raw_response_wrapper(
            accounts.retrieve_contact,
        )
        self.retrieve_payment_networks = async_to_raw_response_wrapper(
            accounts.retrieve_payment_networks,
        )

    @cached_property
    def statements(self) -> AsyncStatementsResourceWithRawResponse:
        return AsyncStatementsResourceWithRawResponse(self._accounts.statements)


class AccountsResourceWithStreamingResponse:
    def __init__(self, accounts: AccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = to_streamed_response_wrapper(
            accounts.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            accounts.list,
        )
        self.list_transactions = to_streamed_response_wrapper(
            accounts.list_transactions,
        )
        self.retrieve_contact = to_streamed_response_wrapper(
            accounts.retrieve_contact,
        )
        self.retrieve_payment_networks = to_streamed_response_wrapper(
            accounts.retrieve_payment_networks,
        )

    @cached_property
    def statements(self) -> StatementsResourceWithStreamingResponse:
        return StatementsResourceWithStreamingResponse(self._accounts.statements)


class AsyncAccountsResourceWithStreamingResponse:
    def __init__(self, accounts: AsyncAccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = async_to_streamed_response_wrapper(
            accounts.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            accounts.list,
        )
        self.list_transactions = async_to_streamed_response_wrapper(
            accounts.list_transactions,
        )
        self.retrieve_contact = async_to_streamed_response_wrapper(
            accounts.retrieve_contact,
        )
        self.retrieve_payment_networks = async_to_streamed_response_wrapper(
            accounts.retrieve_payment_networks,
        )

    @cached_property
    def statements(self) -> AsyncStatementsResourceWithStreamingResponse:
        return AsyncStatementsResourceWithStreamingResponse(self._accounts.statements)
