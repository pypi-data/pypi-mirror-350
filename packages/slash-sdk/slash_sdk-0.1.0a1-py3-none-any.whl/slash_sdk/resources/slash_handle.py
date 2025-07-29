# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import slash_handle_list_params
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
from ..types.slash_handle_list_response import SlashHandleListResponse

__all__ = ["SlashHandleResource", "AsyncSlashHandleResource"]


class SlashHandleResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SlashHandleResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SlashHandleResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SlashHandleResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return SlashHandleResourceWithStreamingResponse(self)

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
    ) -> SlashHandleListResponse:
        """
        List all of your Slash Handles

        Args:
          cursor: A cursor string to fetch the next page of results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/slash-handle",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"cursor": cursor}, slash_handle_list_params.SlashHandleListParams),
            ),
            cast_to=SlashHandleListResponse,
        )


class AsyncSlashHandleResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSlashHandleResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSlashHandleResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSlashHandleResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncSlashHandleResourceWithStreamingResponse(self)

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
    ) -> SlashHandleListResponse:
        """
        List all of your Slash Handles

        Args:
          cursor: A cursor string to fetch the next page of results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/slash-handle",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"cursor": cursor}, slash_handle_list_params.SlashHandleListParams),
            ),
            cast_to=SlashHandleListResponse,
        )


class SlashHandleResourceWithRawResponse:
    def __init__(self, slash_handle: SlashHandleResource) -> None:
        self._slash_handle = slash_handle

        self.list = to_raw_response_wrapper(
            slash_handle.list,
        )


class AsyncSlashHandleResourceWithRawResponse:
    def __init__(self, slash_handle: AsyncSlashHandleResource) -> None:
        self._slash_handle = slash_handle

        self.list = async_to_raw_response_wrapper(
            slash_handle.list,
        )


class SlashHandleResourceWithStreamingResponse:
    def __init__(self, slash_handle: SlashHandleResource) -> None:
        self._slash_handle = slash_handle

        self.list = to_streamed_response_wrapper(
            slash_handle.list,
        )


class AsyncSlashHandleResourceWithStreamingResponse:
    def __init__(self, slash_handle: AsyncSlashHandleResource) -> None:
        self._slash_handle = slash_handle

        self.list = async_to_streamed_response_wrapper(
            slash_handle.list,
        )
