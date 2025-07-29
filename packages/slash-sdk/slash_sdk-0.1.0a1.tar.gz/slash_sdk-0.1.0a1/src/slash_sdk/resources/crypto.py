# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import crypto_create_offramp_params
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
from ..types.crypto_create_offramp_response import CryptoCreateOfframpResponse

__all__ = ["CryptoResource", "AsyncCryptoResource"]


class CryptoResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CryptoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return CryptoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CryptoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return CryptoResourceWithStreamingResponse(self)

    def create_offramp(
        self,
        *,
        currency: Literal["usdt", "usdc"],
        payment_rail: Literal["ach", "wire"],
        virtual_account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CryptoCreateOfframpResponse:
        """
        Retrieve a list of crypto offramp options

        Args:
          virtual_account_id: The id of the virtual account to offramp funds to.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/crypto/offramp",
            body=maybe_transform(
                {
                    "currency": currency,
                    "payment_rail": payment_rail,
                    "virtual_account_id": virtual_account_id,
                },
                crypto_create_offramp_params.CryptoCreateOfframpParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CryptoCreateOfframpResponse,
        )


class AsyncCryptoResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCryptoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCryptoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCryptoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncCryptoResourceWithStreamingResponse(self)

    async def create_offramp(
        self,
        *,
        currency: Literal["usdt", "usdc"],
        payment_rail: Literal["ach", "wire"],
        virtual_account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CryptoCreateOfframpResponse:
        """
        Retrieve a list of crypto offramp options

        Args:
          virtual_account_id: The id of the virtual account to offramp funds to.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/crypto/offramp",
            body=await async_maybe_transform(
                {
                    "currency": currency,
                    "payment_rail": payment_rail,
                    "virtual_account_id": virtual_account_id,
                },
                crypto_create_offramp_params.CryptoCreateOfframpParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CryptoCreateOfframpResponse,
        )


class CryptoResourceWithRawResponse:
    def __init__(self, crypto: CryptoResource) -> None:
        self._crypto = crypto

        self.create_offramp = to_raw_response_wrapper(
            crypto.create_offramp,
        )


class AsyncCryptoResourceWithRawResponse:
    def __init__(self, crypto: AsyncCryptoResource) -> None:
        self._crypto = crypto

        self.create_offramp = async_to_raw_response_wrapper(
            crypto.create_offramp,
        )


class CryptoResourceWithStreamingResponse:
    def __init__(self, crypto: CryptoResource) -> None:
        self._crypto = crypto

        self.create_offramp = to_streamed_response_wrapper(
            crypto.create_offramp,
        )


class AsyncCryptoResourceWithStreamingResponse:
    def __init__(self, crypto: AsyncCryptoResource) -> None:
        self._crypto = crypto

        self.create_offramp = async_to_streamed_response_wrapper(
            crypto.create_offramp,
        )
