# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import merchant_category_list_params
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
from ..types.merchant_category_list_response import MerchantCategoryListResponse

__all__ = ["MerchantCategoryResource", "AsyncMerchantCategoryResource"]


class MerchantCategoryResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MerchantCategoryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return MerchantCategoryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MerchantCategoryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return MerchantCategoryResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MerchantCategoryListResponse:
        """
        Retrieve the list of available merchant category ids

        Args:
          cursor: A cursor string to fetch the next page of results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/merchant-category",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"cursor": cursor}, merchant_category_list_params.MerchantCategoryListParams),
            ),
            cast_to=MerchantCategoryListResponse,
        )


class AsyncMerchantCategoryResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMerchantCategoryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMerchantCategoryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMerchantCategoryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncMerchantCategoryResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MerchantCategoryListResponse:
        """
        Retrieve the list of available merchant category ids

        Args:
          cursor: A cursor string to fetch the next page of results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/merchant-category",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"cursor": cursor}, merchant_category_list_params.MerchantCategoryListParams
                ),
            ),
            cast_to=MerchantCategoryListResponse,
        )


class MerchantCategoryResourceWithRawResponse:
    def __init__(self, merchant_category: MerchantCategoryResource) -> None:
        self._merchant_category = merchant_category

        self.list = to_raw_response_wrapper(
            merchant_category.list,
        )


class AsyncMerchantCategoryResourceWithRawResponse:
    def __init__(self, merchant_category: AsyncMerchantCategoryResource) -> None:
        self._merchant_category = merchant_category

        self.list = async_to_raw_response_wrapper(
            merchant_category.list,
        )


class MerchantCategoryResourceWithStreamingResponse:
    def __init__(self, merchant_category: MerchantCategoryResource) -> None:
        self._merchant_category = merchant_category

        self.list = to_streamed_response_wrapper(
            merchant_category.list,
        )


class AsyncMerchantCategoryResourceWithStreamingResponse:
    def __init__(self, merchant_category: AsyncMerchantCategoryResource) -> None:
        self._merchant_category = merchant_category

        self.list = async_to_streamed_response_wrapper(
            merchant_category.list,
        )
