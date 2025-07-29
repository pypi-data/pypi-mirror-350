# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, cast

import httpx

from ..types import pay_send_params
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
from ..types.slash_handle import SlashHandle
from ..types.pay_send_response import PaySendResponse

__all__ = ["PayResource", "AsyncPayResource"]


class PayResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PayResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return PayResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PayResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return PayResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SlashHandle:
        """Retrieve your pay by slash information."""
        return self._get(
            "/pay",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SlashHandle,
        )

    def send(
        self,
        *,
        amount_cents: float,
        slash_handle: str,
        legal_entity_id: str | NotGiven = NOT_GIVEN,
        source_slash_handle_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaySendResponse:
        """
        Send money to a slash handle

        Args:
          amount_cents: The amount of money to send in cents.

          slash_handle: The username of the SlashHandle to send money to. You can get this by asking
              your recipient for their SlashHandle.

          legal_entity_id: The ID of the LegalEntity to send money from. You can get this by calling
              `GET /legal-entity`. This field or `slashHandleId` is required unless you are
              authenticating via API key.

          source_slash_handle_id: The ID of the SlashHandle to send money from. You can get this by calling
              `GET /slash-handle`. This field or `legalEntityId` is required unless you are
              authenticating via API key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            PaySendResponse,
            self._post(
                "/pay",
                body=maybe_transform(
                    {
                        "amount_cents": amount_cents,
                        "slash_handle": slash_handle,
                        "legal_entity_id": legal_entity_id,
                        "source_slash_handle_id": source_slash_handle_id,
                    },
                    pay_send_params.PaySendParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, PaySendResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncPayResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPayResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPayResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPayResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncPayResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SlashHandle:
        """Retrieve your pay by slash information."""
        return await self._get(
            "/pay",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SlashHandle,
        )

    async def send(
        self,
        *,
        amount_cents: float,
        slash_handle: str,
        legal_entity_id: str | NotGiven = NOT_GIVEN,
        source_slash_handle_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaySendResponse:
        """
        Send money to a slash handle

        Args:
          amount_cents: The amount of money to send in cents.

          slash_handle: The username of the SlashHandle to send money to. You can get this by asking
              your recipient for their SlashHandle.

          legal_entity_id: The ID of the LegalEntity to send money from. You can get this by calling
              `GET /legal-entity`. This field or `slashHandleId` is required unless you are
              authenticating via API key.

          source_slash_handle_id: The ID of the SlashHandle to send money from. You can get this by calling
              `GET /slash-handle`. This field or `legalEntityId` is required unless you are
              authenticating via API key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            PaySendResponse,
            await self._post(
                "/pay",
                body=await async_maybe_transform(
                    {
                        "amount_cents": amount_cents,
                        "slash_handle": slash_handle,
                        "legal_entity_id": legal_entity_id,
                        "source_slash_handle_id": source_slash_handle_id,
                    },
                    pay_send_params.PaySendParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, PaySendResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class PayResourceWithRawResponse:
    def __init__(self, pay: PayResource) -> None:
        self._pay = pay

        self.retrieve = to_raw_response_wrapper(
            pay.retrieve,
        )
        self.send = to_raw_response_wrapper(
            pay.send,
        )


class AsyncPayResourceWithRawResponse:
    def __init__(self, pay: AsyncPayResource) -> None:
        self._pay = pay

        self.retrieve = async_to_raw_response_wrapper(
            pay.retrieve,
        )
        self.send = async_to_raw_response_wrapper(
            pay.send,
        )


class PayResourceWithStreamingResponse:
    def __init__(self, pay: PayResource) -> None:
        self._pay = pay

        self.retrieve = to_streamed_response_wrapper(
            pay.retrieve,
        )
        self.send = to_streamed_response_wrapper(
            pay.send,
        )


class AsyncPayResourceWithStreamingResponse:
    def __init__(self, pay: AsyncPayResource) -> None:
        self._pay = pay

        self.retrieve = async_to_streamed_response_wrapper(
            pay.retrieve,
        )
        self.send = async_to_streamed_response_wrapper(
            pay.send,
        )
