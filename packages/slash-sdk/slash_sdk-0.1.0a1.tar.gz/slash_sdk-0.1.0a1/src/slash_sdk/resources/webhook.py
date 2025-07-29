# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import webhook_list_params, webhook_create_params, webhook_update_params
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
from ..types.webhook import Webhook
from ..types.webhook_list_response import WebhookListResponse

__all__ = ["WebhookResource", "AsyncWebhookResource"]


class WebhookResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WebhookResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return WebhookResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebhookResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return WebhookResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        url: str,
        legal_entity_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Webhook:
        """
        Create a new webhook endpoint

        Args:
          url: The URL that will receive the webhook payload

          legal_entity_id: The ID of the LegalEntity to create the webhook for. You can get this by calling
              `GET /legal-entity`. This field is required unless you are authenticating via
              API key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/webhook",
            body=maybe_transform(
                {
                    "name": name,
                    "url": url,
                    "legal_entity_id": legal_entity_id,
                },
                webhook_create_params.WebhookCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Webhook,
        )

    def update(
        self,
        webhook_id: str,
        *,
        status: Literal["archived"],
        reason: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Webhook:
        """
        Update a webhook endpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_id:
            raise ValueError(f"Expected a non-empty value for `webhook_id` but received {webhook_id!r}")
        return self._patch(
            f"/webhook/{webhook_id}",
            body=maybe_transform(
                {
                    "status": status,
                    "reason": reason,
                },
                webhook_update_params.WebhookUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Webhook,
        )

    def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        filter_legal_entity_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookListResponse:
        """
        Get all webhooks

        Args:
          cursor: A cursor string to fetch the next page of results

          filter_legal_entity_id: Pass in a legal entity ID to filter for webhooks under a specific legal entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/webhook",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "filter_legal_entity_id": filter_legal_entity_id,
                    },
                    webhook_list_params.WebhookListParams,
                ),
            ),
            cast_to=WebhookListResponse,
        )


class AsyncWebhookResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWebhookResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWebhookResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebhookResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncWebhookResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        url: str,
        legal_entity_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Webhook:
        """
        Create a new webhook endpoint

        Args:
          url: The URL that will receive the webhook payload

          legal_entity_id: The ID of the LegalEntity to create the webhook for. You can get this by calling
              `GET /legal-entity`. This field is required unless you are authenticating via
              API key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/webhook",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "url": url,
                    "legal_entity_id": legal_entity_id,
                },
                webhook_create_params.WebhookCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Webhook,
        )

    async def update(
        self,
        webhook_id: str,
        *,
        status: Literal["archived"],
        reason: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Webhook:
        """
        Update a webhook endpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_id:
            raise ValueError(f"Expected a non-empty value for `webhook_id` but received {webhook_id!r}")
        return await self._patch(
            f"/webhook/{webhook_id}",
            body=await async_maybe_transform(
                {
                    "status": status,
                    "reason": reason,
                },
                webhook_update_params.WebhookUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Webhook,
        )

    async def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        filter_legal_entity_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookListResponse:
        """
        Get all webhooks

        Args:
          cursor: A cursor string to fetch the next page of results

          filter_legal_entity_id: Pass in a legal entity ID to filter for webhooks under a specific legal entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/webhook",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cursor": cursor,
                        "filter_legal_entity_id": filter_legal_entity_id,
                    },
                    webhook_list_params.WebhookListParams,
                ),
            ),
            cast_to=WebhookListResponse,
        )


class WebhookResourceWithRawResponse:
    def __init__(self, webhook: WebhookResource) -> None:
        self._webhook = webhook

        self.create = to_raw_response_wrapper(
            webhook.create,
        )
        self.update = to_raw_response_wrapper(
            webhook.update,
        )
        self.list = to_raw_response_wrapper(
            webhook.list,
        )


class AsyncWebhookResourceWithRawResponse:
    def __init__(self, webhook: AsyncWebhookResource) -> None:
        self._webhook = webhook

        self.create = async_to_raw_response_wrapper(
            webhook.create,
        )
        self.update = async_to_raw_response_wrapper(
            webhook.update,
        )
        self.list = async_to_raw_response_wrapper(
            webhook.list,
        )


class WebhookResourceWithStreamingResponse:
    def __init__(self, webhook: WebhookResource) -> None:
        self._webhook = webhook

        self.create = to_streamed_response_wrapper(
            webhook.create,
        )
        self.update = to_streamed_response_wrapper(
            webhook.update,
        )
        self.list = to_streamed_response_wrapper(
            webhook.list,
        )


class AsyncWebhookResourceWithStreamingResponse:
    def __init__(self, webhook: AsyncWebhookResource) -> None:
        self._webhook = webhook

        self.create = async_to_streamed_response_wrapper(
            webhook.create,
        )
        self.update = async_to_streamed_response_wrapper(
            webhook.update,
        )
        self.list = async_to_streamed_response_wrapper(
            webhook.list,
        )
