# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ...types import card_group_list_params, card_group_create_params, card_group_update_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from .spending_constraint import (
    SpendingConstraintResource,
    AsyncSpendingConstraintResource,
    SpendingConstraintResourceWithRawResponse,
    AsyncSpendingConstraintResourceWithRawResponse,
    SpendingConstraintResourceWithStreamingResponse,
    AsyncSpendingConstraintResourceWithStreamingResponse,
)
from ...types.card_group.card_group import CardGroup
from ...types.card_group_utilization import CardGroupUtilization
from ...types.card_group_list_response import CardGroupListResponse
from ...types.card.spending_constraint_param import SpendingConstraintParam

__all__ = ["CardGroupResource", "AsyncCardGroupResource"]


class CardGroupResource(SyncAPIResource):
    @cached_property
    def spending_constraint(self) -> SpendingConstraintResource:
        return SpendingConstraintResource(self._client)

    @cached_property
    def with_raw_response(self) -> CardGroupResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return CardGroupResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CardGroupResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return CardGroupResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        spending_constraint: SpendingConstraintParam | NotGiven = NOT_GIVEN,
        virtual_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroup:
        """
        Create a card group.

        Args:
          spending_constraint: A constraint that can be applied to a CardGroupSpendingRule

          virtual_account_id: The ID of the virtual account to associate with the card group. If not provided,
              the primary virtual account will be used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/card-group",
            body=maybe_transform(
                {
                    "name": name,
                    "spending_constraint": spending_constraint,
                    "virtual_account_id": virtual_account_id,
                },
                card_group_create_params.CardGroupCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CardGroup,
        )

    def retrieve(
        self,
        card_group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroup:
        """
        Fetch details for a single card group by card group ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_group_id:
            raise ValueError(f"Expected a non-empty value for `card_group_id` but received {card_group_id!r}")
        return self._get(
            f"/card-group/{card_group_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CardGroup,
        )

    def update(
        self,
        card_group_id: str,
        *,
        name: str | NotGiven = NOT_GIVEN,
        spending_constraint: Optional[SpendingConstraintParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroup:
        """
        Update a card group

        Args:
          spending_constraint: Explicitly set this value to null to remove all card group level spending
              constraints.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_group_id:
            raise ValueError(f"Expected a non-empty value for `card_group_id` but received {card_group_id!r}")
        return self._patch(
            f"/card-group/{card_group_id}",
            body=maybe_transform(
                {
                    "name": name,
                    "spending_constraint": spending_constraint,
                },
                card_group_update_params.CardGroupUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CardGroup,
        )

    def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        filter_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroupListResponse:
        """
        Retrieve the list of card groups that the user owns.

        Args:
          cursor: A cursor string to fetch the next page of results

          filter_name: Pass in a name to filter for card groups with a matching name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/card-group",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "filter_name": filter_name,
                    },
                    card_group_list_params.CardGroupListParams,
                ),
            ),
            cast_to=CardGroupListResponse,
        )

    def get_utilization(
        self,
        card_group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroupUtilization:
        """
        Get a card group's current utilization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_group_id:
            raise ValueError(f"Expected a non-empty value for `card_group_id` but received {card_group_id!r}")
        return self._get(
            f"/card-group/{card_group_id}/utilization",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CardGroupUtilization,
        )


class AsyncCardGroupResource(AsyncAPIResource):
    @cached_property
    def spending_constraint(self) -> AsyncSpendingConstraintResource:
        return AsyncSpendingConstraintResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCardGroupResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCardGroupResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCardGroupResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncCardGroupResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        spending_constraint: SpendingConstraintParam | NotGiven = NOT_GIVEN,
        virtual_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroup:
        """
        Create a card group.

        Args:
          spending_constraint: A constraint that can be applied to a CardGroupSpendingRule

          virtual_account_id: The ID of the virtual account to associate with the card group. If not provided,
              the primary virtual account will be used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/card-group",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "spending_constraint": spending_constraint,
                    "virtual_account_id": virtual_account_id,
                },
                card_group_create_params.CardGroupCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CardGroup,
        )

    async def retrieve(
        self,
        card_group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroup:
        """
        Fetch details for a single card group by card group ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_group_id:
            raise ValueError(f"Expected a non-empty value for `card_group_id` but received {card_group_id!r}")
        return await self._get(
            f"/card-group/{card_group_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CardGroup,
        )

    async def update(
        self,
        card_group_id: str,
        *,
        name: str | NotGiven = NOT_GIVEN,
        spending_constraint: Optional[SpendingConstraintParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroup:
        """
        Update a card group

        Args:
          spending_constraint: Explicitly set this value to null to remove all card group level spending
              constraints.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_group_id:
            raise ValueError(f"Expected a non-empty value for `card_group_id` but received {card_group_id!r}")
        return await self._patch(
            f"/card-group/{card_group_id}",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "spending_constraint": spending_constraint,
                },
                card_group_update_params.CardGroupUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CardGroup,
        )

    async def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        filter_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroupListResponse:
        """
        Retrieve the list of card groups that the user owns.

        Args:
          cursor: A cursor string to fetch the next page of results

          filter_name: Pass in a name to filter for card groups with a matching name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/card-group",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cursor": cursor,
                        "filter_name": filter_name,
                    },
                    card_group_list_params.CardGroupListParams,
                ),
            ),
            cast_to=CardGroupListResponse,
        )

    async def get_utilization(
        self,
        card_group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroupUtilization:
        """
        Get a card group's current utilization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_group_id:
            raise ValueError(f"Expected a non-empty value for `card_group_id` but received {card_group_id!r}")
        return await self._get(
            f"/card-group/{card_group_id}/utilization",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CardGroupUtilization,
        )


class CardGroupResourceWithRawResponse:
    def __init__(self, card_group: CardGroupResource) -> None:
        self._card_group = card_group

        self.create = to_raw_response_wrapper(
            card_group.create,
        )
        self.retrieve = to_raw_response_wrapper(
            card_group.retrieve,
        )
        self.update = to_raw_response_wrapper(
            card_group.update,
        )
        self.list = to_raw_response_wrapper(
            card_group.list,
        )
        self.get_utilization = to_raw_response_wrapper(
            card_group.get_utilization,
        )

    @cached_property
    def spending_constraint(self) -> SpendingConstraintResourceWithRawResponse:
        return SpendingConstraintResourceWithRawResponse(self._card_group.spending_constraint)


class AsyncCardGroupResourceWithRawResponse:
    def __init__(self, card_group: AsyncCardGroupResource) -> None:
        self._card_group = card_group

        self.create = async_to_raw_response_wrapper(
            card_group.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            card_group.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            card_group.update,
        )
        self.list = async_to_raw_response_wrapper(
            card_group.list,
        )
        self.get_utilization = async_to_raw_response_wrapper(
            card_group.get_utilization,
        )

    @cached_property
    def spending_constraint(self) -> AsyncSpendingConstraintResourceWithRawResponse:
        return AsyncSpendingConstraintResourceWithRawResponse(self._card_group.spending_constraint)


class CardGroupResourceWithStreamingResponse:
    def __init__(self, card_group: CardGroupResource) -> None:
        self._card_group = card_group

        self.create = to_streamed_response_wrapper(
            card_group.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            card_group.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            card_group.update,
        )
        self.list = to_streamed_response_wrapper(
            card_group.list,
        )
        self.get_utilization = to_streamed_response_wrapper(
            card_group.get_utilization,
        )

    @cached_property
    def spending_constraint(self) -> SpendingConstraintResourceWithStreamingResponse:
        return SpendingConstraintResourceWithStreamingResponse(self._card_group.spending_constraint)


class AsyncCardGroupResourceWithStreamingResponse:
    def __init__(self, card_group: AsyncCardGroupResource) -> None:
        self._card_group = card_group

        self.create = async_to_streamed_response_wrapper(
            card_group.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            card_group.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            card_group.update,
        )
        self.list = async_to_streamed_response_wrapper(
            card_group.list,
        )
        self.get_utilization = async_to_streamed_response_wrapper(
            card_group.get_utilization,
        )

    @cached_property
    def spending_constraint(self) -> AsyncSpendingConstraintResourceWithStreamingResponse:
        return AsyncSpendingConstraintResourceWithStreamingResponse(self._card_group.spending_constraint)
