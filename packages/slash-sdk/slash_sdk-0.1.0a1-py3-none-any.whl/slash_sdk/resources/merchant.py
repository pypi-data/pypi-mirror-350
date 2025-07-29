# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import merchant_list_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.merchant import Merchant
from ..types.merchant_list_response import MerchantListResponse

__all__ = ["MerchantResource", "AsyncMerchantResource"]


class MerchantResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MerchantResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return MerchantResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MerchantResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return MerchantResourceWithStreamingResponse(self)

    def retrieve(
        self,
        merchant_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Merchant:
        """
        Fetch details for a single merchant by ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not merchant_id:
            raise ValueError(f"Expected a non-empty value for `merchant_id` but received {merchant_id!r}")
        return self._get(
            f"/merchant/{merchant_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Merchant,
        )

    def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        search_merchant_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MerchantListResponse:
        """
        Retrieve the list of available merchant ids

        Args:
          cursor: A cursor string to fetch the next page of results

          search_merchant_name: Pass in a merchant name to filter merchants by name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/merchant",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "search_merchant_name": search_merchant_name,
                    },
                    merchant_list_params.MerchantListParams,
                ),
            ),
            cast_to=MerchantListResponse,
        )


class AsyncMerchantResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMerchantResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMerchantResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMerchantResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncMerchantResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        merchant_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Merchant:
        """
        Fetch details for a single merchant by ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not merchant_id:
            raise ValueError(f"Expected a non-empty value for `merchant_id` but received {merchant_id!r}")
        return await self._get(
            f"/merchant/{merchant_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Merchant,
        )

    async def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        search_merchant_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MerchantListResponse:
        """
        Retrieve the list of available merchant ids

        Args:
          cursor: A cursor string to fetch the next page of results

          search_merchant_name: Pass in a merchant name to filter merchants by name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/merchant",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cursor": cursor,
                        "search_merchant_name": search_merchant_name,
                    },
                    merchant_list_params.MerchantListParams,
                ),
            ),
            cast_to=MerchantListResponse,
        )


class MerchantResourceWithRawResponse:
    def __init__(self, merchant: MerchantResource) -> None:
        self._merchant = merchant

        self.retrieve = to_raw_response_wrapper(
            merchant.retrieve,
        )
        self.list = to_raw_response_wrapper(
            merchant.list,
        )


class AsyncMerchantResourceWithRawResponse:
    def __init__(self, merchant: AsyncMerchantResource) -> None:
        self._merchant = merchant

        self.retrieve = async_to_raw_response_wrapper(
            merchant.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            merchant.list,
        )


class MerchantResourceWithStreamingResponse:
    def __init__(self, merchant: MerchantResource) -> None:
        self._merchant = merchant

        self.retrieve = to_streamed_response_wrapper(
            merchant.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            merchant.list,
        )


class AsyncMerchantResourceWithStreamingResponse:
    def __init__(self, merchant: AsyncMerchantResource) -> None:
        self._merchant = merchant

        self.retrieve = async_to_streamed_response_wrapper(
            merchant.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            merchant.list,
        )
