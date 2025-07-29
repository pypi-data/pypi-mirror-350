# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.well_known_retrieve_openid_configuration_response import WellKnownRetrieveOpenidConfigurationResponse

__all__ = ["WellKnownResource", "AsyncWellKnownResource"]


class WellKnownResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WellKnownResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return WellKnownResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WellKnownResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return WellKnownResourceWithStreamingResponse(self)

    def retrieve_openid_configuration(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WellKnownRetrieveOpenidConfigurationResponse:
        """Get OpenID Configuration"""
        return self._get(
            "/.well-known/openid-configuration",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WellKnownRetrieveOpenidConfigurationResponse,
        )


class AsyncWellKnownResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWellKnownResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWellKnownResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWellKnownResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncWellKnownResourceWithStreamingResponse(self)

    async def retrieve_openid_configuration(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WellKnownRetrieveOpenidConfigurationResponse:
        """Get OpenID Configuration"""
        return await self._get(
            "/.well-known/openid-configuration",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WellKnownRetrieveOpenidConfigurationResponse,
        )


class WellKnownResourceWithRawResponse:
    def __init__(self, well_known: WellKnownResource) -> None:
        self._well_known = well_known

        self.retrieve_openid_configuration = to_raw_response_wrapper(
            well_known.retrieve_openid_configuration,
        )


class AsyncWellKnownResourceWithRawResponse:
    def __init__(self, well_known: AsyncWellKnownResource) -> None:
        self._well_known = well_known

        self.retrieve_openid_configuration = async_to_raw_response_wrapper(
            well_known.retrieve_openid_configuration,
        )


class WellKnownResourceWithStreamingResponse:
    def __init__(self, well_known: WellKnownResource) -> None:
        self._well_known = well_known

        self.retrieve_openid_configuration = to_streamed_response_wrapper(
            well_known.retrieve_openid_configuration,
        )


class AsyncWellKnownResourceWithStreamingResponse:
    def __init__(self, well_known: AsyncWellKnownResource) -> None:
        self._well_known = well_known

        self.retrieve_openid_configuration = async_to_streamed_response_wrapper(
            well_known.retrieve_openid_configuration,
        )
