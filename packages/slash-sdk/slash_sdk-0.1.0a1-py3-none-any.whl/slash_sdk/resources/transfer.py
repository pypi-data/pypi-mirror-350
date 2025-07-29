# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import transfer_create_virtual_account_transfer_params
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
from ..types.transfer_create_virtual_account_transfer_response import TransferCreateVirtualAccountTransferResponse

__all__ = ["TransferResource", "AsyncTransferResource"]


class TransferResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TransferResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TransferResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TransferResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return TransferResourceWithStreamingResponse(self)

    def create_virtual_account_transfer(
        self,
        *,
        amount_cents: float,
        destination: str,
        source: str,
        x_idempotency_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransferCreateVirtualAccountTransferResponse:
        """
        Transfer money between Virtual Accounts or fund a Virtual Account from a Primary
        Account

        Args:
          amount_cents: The amount of money to send in cents.

          destination: The ID of the virtual account to transfer money to.

          source: The ID of the virtual account to transfer money from. Can also be the virtual
              account linked to a primary Slash account to fund a new virtual account (Virtual
              account with the name 'Primary account').

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"X-Idempotency-Key": x_idempotency_key, **(extra_headers or {})}
        return self._post(
            "/transfer/virtual-account",
            body=maybe_transform(
                {
                    "amount_cents": amount_cents,
                    "destination": destination,
                    "source": source,
                },
                transfer_create_virtual_account_transfer_params.TransferCreateVirtualAccountTransferParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransferCreateVirtualAccountTransferResponse,
        )


class AsyncTransferResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTransferResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTransferResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTransferResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncTransferResourceWithStreamingResponse(self)

    async def create_virtual_account_transfer(
        self,
        *,
        amount_cents: float,
        destination: str,
        source: str,
        x_idempotency_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransferCreateVirtualAccountTransferResponse:
        """
        Transfer money between Virtual Accounts or fund a Virtual Account from a Primary
        Account

        Args:
          amount_cents: The amount of money to send in cents.

          destination: The ID of the virtual account to transfer money to.

          source: The ID of the virtual account to transfer money from. Can also be the virtual
              account linked to a primary Slash account to fund a new virtual account (Virtual
              account with the name 'Primary account').

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"X-Idempotency-Key": x_idempotency_key, **(extra_headers or {})}
        return await self._post(
            "/transfer/virtual-account",
            body=await async_maybe_transform(
                {
                    "amount_cents": amount_cents,
                    "destination": destination,
                    "source": source,
                },
                transfer_create_virtual_account_transfer_params.TransferCreateVirtualAccountTransferParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransferCreateVirtualAccountTransferResponse,
        )


class TransferResourceWithRawResponse:
    def __init__(self, transfer: TransferResource) -> None:
        self._transfer = transfer

        self.create_virtual_account_transfer = to_raw_response_wrapper(
            transfer.create_virtual_account_transfer,
        )


class AsyncTransferResourceWithRawResponse:
    def __init__(self, transfer: AsyncTransferResource) -> None:
        self._transfer = transfer

        self.create_virtual_account_transfer = async_to_raw_response_wrapper(
            transfer.create_virtual_account_transfer,
        )


class TransferResourceWithStreamingResponse:
    def __init__(self, transfer: TransferResource) -> None:
        self._transfer = transfer

        self.create_virtual_account_transfer = to_streamed_response_wrapper(
            transfer.create_virtual_account_transfer,
        )


class AsyncTransferResourceWithStreamingResponse:
    def __init__(self, transfer: AsyncTransferResource) -> None:
        self._transfer = transfer

        self.create_virtual_account_transfer = async_to_streamed_response_wrapper(
            transfer.create_virtual_account_transfer,
        )
