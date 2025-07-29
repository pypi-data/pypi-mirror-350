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
from ..types.legal_entity_list_response import LegalEntityListResponse

__all__ = ["LegalEntityResource", "AsyncLegalEntityResource"]


class LegalEntityResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LegalEntityResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return LegalEntityResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LegalEntityResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return LegalEntityResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LegalEntityListResponse:
        """List all legal entities you have access to"""
        return self._get(
            "/legal-entity",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LegalEntityListResponse,
        )


class AsyncLegalEntityResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLegalEntityResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncLegalEntityResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLegalEntityResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncLegalEntityResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LegalEntityListResponse:
        """List all legal entities you have access to"""
        return await self._get(
            "/legal-entity",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LegalEntityListResponse,
        )


class LegalEntityResourceWithRawResponse:
    def __init__(self, legal_entity: LegalEntityResource) -> None:
        self._legal_entity = legal_entity

        self.list = to_raw_response_wrapper(
            legal_entity.list,
        )


class AsyncLegalEntityResourceWithRawResponse:
    def __init__(self, legal_entity: AsyncLegalEntityResource) -> None:
        self._legal_entity = legal_entity

        self.list = async_to_raw_response_wrapper(
            legal_entity.list,
        )


class LegalEntityResourceWithStreamingResponse:
    def __init__(self, legal_entity: LegalEntityResource) -> None:
        self._legal_entity = legal_entity

        self.list = to_streamed_response_wrapper(
            legal_entity.list,
        )


class AsyncLegalEntityResourceWithStreamingResponse:
    def __init__(self, legal_entity: AsyncLegalEntityResource) -> None:
        self._legal_entity = legal_entity

        self.list = async_to_streamed_response_wrapper(
            legal_entity.list,
        )
