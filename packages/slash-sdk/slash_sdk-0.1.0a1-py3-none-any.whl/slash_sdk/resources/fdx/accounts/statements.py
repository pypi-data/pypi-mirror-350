# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.fdx.accounts import statement_list_params
from ....types.fdx.accounts.statement_list_response import StatementListResponse

__all__ = ["StatementsResource", "AsyncStatementsResource"]


class StatementsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StatementsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return StatementsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StatementsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return StatementsResourceWithStreamingResponse(self)

    def list(
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
    ) -> StatementListResponse:
        """
        Search for statements

        Args:
          end_time: End time for use in retrieval of statements (ISO 8601).

          limit: The number of items to return (default 100, max 1000)

          offset: The ID of the last item in the previous page of results

          start_time: Start time for use in retrieval of statements (ISO 8601).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            f"/fdx/accounts/{account_id}/statements",
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
                    statement_list_params.StatementListParams,
                ),
            ),
            cast_to=StatementListResponse,
        )

    def retrieve_pdf(
        self,
        statement_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        Get account statement PDF.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not statement_id:
            raise ValueError(f"Expected a non-empty value for `statement_id` but received {statement_id!r}")
        extra_headers = {"Accept": "application/pdf", **(extra_headers or {})}
        return self._get(
            f"/fdx/accounts/{account_id}/statements/{statement_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncStatementsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStatementsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncStatementsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStatementsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncStatementsResourceWithStreamingResponse(self)

    async def list(
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
    ) -> StatementListResponse:
        """
        Search for statements

        Args:
          end_time: End time for use in retrieval of statements (ISO 8601).

          limit: The number of items to return (default 100, max 1000)

          offset: The ID of the last item in the previous page of results

          start_time: Start time for use in retrieval of statements (ISO 8601).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            f"/fdx/accounts/{account_id}/statements",
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
                    statement_list_params.StatementListParams,
                ),
            ),
            cast_to=StatementListResponse,
        )

    async def retrieve_pdf(
        self,
        statement_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        Get account statement PDF.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not statement_id:
            raise ValueError(f"Expected a non-empty value for `statement_id` but received {statement_id!r}")
        extra_headers = {"Accept": "application/pdf", **(extra_headers or {})}
        return await self._get(
            f"/fdx/accounts/{account_id}/statements/{statement_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class StatementsResourceWithRawResponse:
    def __init__(self, statements: StatementsResource) -> None:
        self._statements = statements

        self.list = to_raw_response_wrapper(
            statements.list,
        )
        self.retrieve_pdf = to_custom_raw_response_wrapper(
            statements.retrieve_pdf,
            BinaryAPIResponse,
        )


class AsyncStatementsResourceWithRawResponse:
    def __init__(self, statements: AsyncStatementsResource) -> None:
        self._statements = statements

        self.list = async_to_raw_response_wrapper(
            statements.list,
        )
        self.retrieve_pdf = async_to_custom_raw_response_wrapper(
            statements.retrieve_pdf,
            AsyncBinaryAPIResponse,
        )


class StatementsResourceWithStreamingResponse:
    def __init__(self, statements: StatementsResource) -> None:
        self._statements = statements

        self.list = to_streamed_response_wrapper(
            statements.list,
        )
        self.retrieve_pdf = to_custom_streamed_response_wrapper(
            statements.retrieve_pdf,
            StreamedBinaryAPIResponse,
        )


class AsyncStatementsResourceWithStreamingResponse:
    def __init__(self, statements: AsyncStatementsResource) -> None:
        self._statements = statements

        self.list = async_to_streamed_response_wrapper(
            statements.list,
        )
        self.retrieve_pdf = async_to_custom_streamed_response_wrapper(
            statements.retrieve_pdf,
            AsyncStreamedBinaryAPIResponse,
        )
