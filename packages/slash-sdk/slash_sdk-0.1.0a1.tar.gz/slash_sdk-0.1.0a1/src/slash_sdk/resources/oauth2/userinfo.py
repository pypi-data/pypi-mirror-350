# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.oauth2.user_info import UserInfo

__all__ = ["UserinfoResource", "AsyncUserinfoResource"]


class UserinfoResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UserinfoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return UserinfoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UserinfoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return UserinfoResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserInfo:
        """Get userinfo"""
        return self._get(
            "/oauth2/userinfo",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserInfo,
        )

    def submit(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserInfo:
        """Get userinfo"""
        return self._post(
            "/oauth2/userinfo",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserInfo,
        )


class AsyncUserinfoResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUserinfoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUserinfoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUserinfoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncUserinfoResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserInfo:
        """Get userinfo"""
        return await self._get(
            "/oauth2/userinfo",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserInfo,
        )

    async def submit(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserInfo:
        """Get userinfo"""
        return await self._post(
            "/oauth2/userinfo",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserInfo,
        )


class UserinfoResourceWithRawResponse:
    def __init__(self, userinfo: UserinfoResource) -> None:
        self._userinfo = userinfo

        self.retrieve = to_raw_response_wrapper(
            userinfo.retrieve,
        )
        self.submit = to_raw_response_wrapper(
            userinfo.submit,
        )


class AsyncUserinfoResourceWithRawResponse:
    def __init__(self, userinfo: AsyncUserinfoResource) -> None:
        self._userinfo = userinfo

        self.retrieve = async_to_raw_response_wrapper(
            userinfo.retrieve,
        )
        self.submit = async_to_raw_response_wrapper(
            userinfo.submit,
        )


class UserinfoResourceWithStreamingResponse:
    def __init__(self, userinfo: UserinfoResource) -> None:
        self._userinfo = userinfo

        self.retrieve = to_streamed_response_wrapper(
            userinfo.retrieve,
        )
        self.submit = to_streamed_response_wrapper(
            userinfo.submit,
        )


class AsyncUserinfoResourceWithStreamingResponse:
    def __init__(self, userinfo: AsyncUserinfoResource) -> None:
        self._userinfo = userinfo

        self.retrieve = async_to_streamed_response_wrapper(
            userinfo.retrieve,
        )
        self.submit = async_to_streamed_response_wrapper(
            userinfo.submit,
        )
