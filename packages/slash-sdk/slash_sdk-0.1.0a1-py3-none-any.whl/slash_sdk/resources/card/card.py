# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal

import httpx

from ...types import CardStatus, card_list_params, card_create_params, card_update_params, card_retrieve_params
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
from ...types.card.card import Card
from ...types.card_status import CardStatus
from .spending_constraint import (
    SpendingConstraintResource,
    AsyncSpendingConstraintResource,
    SpendingConstraintResourceWithRawResponse,
    AsyncSpendingConstraintResourceWithRawResponse,
    SpendingConstraintResourceWithStreamingResponse,
    AsyncSpendingConstraintResourceWithStreamingResponse,
)
from ...types.card_list_response import CardListResponse
from ...types.card_group_utilization import CardGroupUtilization
from ...types.card.spending_constraint_param import SpendingConstraintParam

__all__ = ["CardResource", "AsyncCardResource"]


class CardResource(SyncAPIResource):
    @cached_property
    def spending_constraint(self) -> SpendingConstraintResource:
        return SpendingConstraintResource(self._client)

    @cached_property
    def with_raw_response(self) -> CardResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return CardResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CardResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return CardResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        type: Literal["virtual"],
        account_id: str | NotGiven = NOT_GIVEN,
        card_group_id: str | NotGiven = NOT_GIVEN,
        card_product_id: str | NotGiven = NOT_GIVEN,
        is_single_use: bool | NotGiven = NOT_GIVEN,
        spending_constraint: SpendingConstraintParam | NotGiven = NOT_GIVEN,
        user_data: Dict[str, object] | NotGiven = NOT_GIVEN,
        virtual_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Card:
        """Create a card

        Args:
          type: Specify the type of card you'd like to create.

        At the moment, only virtual cards
              are supported.

          account_id: The ID of the account to create the card under. You can get this by calling
              `GET /account`. This field is required unless you are authenticating via API
              key, in which case it will default to your first commercial account. We
              recommend supplying this even if you are authenticating via API key.

          card_product_id: The ID of the card product to use when creating this card, if not specified a
              random card product will be chosen.

          is_single_use: Defaults to false. When set to true, the card will be automatically closed after
              a single authorization attempt. Note that the card will be closed even if the
              authorization declines or drops

          spending_constraint: A constraint that can be applied to a CardGroupSpendingRule

          user_data: Arbitrary information that can be attached to the card. This should be a JSON
              object and cannot exceed 4kb.

          virtual_account_id: The ID of the virtual account to create the card under. Virtual accounts can be
              retrieved by calling `GET /virtual-account`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/card",
            body=maybe_transform(
                {
                    "name": name,
                    "type": type,
                    "account_id": account_id,
                    "card_group_id": card_group_id,
                    "card_product_id": card_product_id,
                    "is_single_use": is_single_use,
                    "spending_constraint": spending_constraint,
                    "user_data": user_data,
                    "virtual_account_id": virtual_account_id,
                },
                card_create_params.CardCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )

    def retrieve(
        self,
        card_id: str,
        *,
        include_cvv: Literal["true", "false"] | NotGiven = NOT_GIVEN,
        include_pan: Literal["true", "false"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Card:
        """
        Fetch details for a single card by card ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_id:
            raise ValueError(f"Expected a non-empty value for `card_id` but received {card_id!r}")
        return self._get(
            f"/card/{card_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_cvv": include_cvv,
                        "include_pan": include_pan,
                    },
                    card_retrieve_params.CardRetrieveParams,
                ),
            ),
            cast_to=Card,
        )

    def update(
        self,
        card_id: str,
        *,
        card_group_id: Optional[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        spending_constraint: Optional[SpendingConstraintParam] | NotGiven = NOT_GIVEN,
        status: CardStatus | NotGiven = NOT_GIVEN,
        user_data: Optional[Dict[str, object]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Card:
        """
        Update a card

        Args:
          card_group_id: Explicitly set this value to null to remove the card from a group. Omitting this
              field entirely will not affect the group the card belongs to.

          spending_constraint: Explicitly set this value to null to remove all card level spending constraints.

          user_data: Arbitrary information that can be attached to the card. This should be a JSON
              object and cannot exceed 4kb.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_id:
            raise ValueError(f"Expected a non-empty value for `card_id` but received {card_id!r}")
        return self._patch(
            f"/card/{card_id}",
            body=maybe_transform(
                {
                    "card_group_id": card_group_id,
                    "name": name,
                    "spending_constraint": spending_constraint,
                    "status": status,
                    "user_data": user_data,
                },
                card_update_params.CardUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )

    def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        filter_account_id: str | NotGiven = NOT_GIVEN,
        filter_card_group_id: str | NotGiven = NOT_GIVEN,
        filter_card_group_name: str | NotGiven = NOT_GIVEN,
        filter_legal_entity_id: str | NotGiven = NOT_GIVEN,
        filter_status: Literal["active", "paused", "closed", "inactive"] | NotGiven = NOT_GIVEN,
        filter_virtual_account_id: str | NotGiven = NOT_GIVEN,
        sort: Literal["createdAt", "name"] | NotGiven = NOT_GIVEN,
        sort_direction: Literal["ASC", "DESC"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardListResponse:
        """
        List all cards you have access to.

        Args:
          cursor: A cursor string to fetch the next page of results

          filter_account_id: Pass in an account ID to filter for cards under a specific account.

          filter_card_group_id: Pass in a card group ID, This will return all cards that belong to the card
              group ID passed in. Cannot be combined with filter:cardGroupName.

          filter_card_group_name: Pass in a card group name, This will return all cards that belong to the card
              group name passed in. Cannot be combined with filter:cardGroupId.

          filter_legal_entity_id: Pass in a legal entity ID to filter for cards in accounts under a specific legal
              entity.

          filter_status: Returns all cards matching the status passed in.

          filter_virtual_account_id: Pass in a virtual account ID to filter for cards under a specific virtual
              account.

          sort: Sorts card by creation date or name.

          sort_direction: The direction to apply the sort filter by. Default ASC.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/card",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "filter_account_id": filter_account_id,
                        "filter_card_group_id": filter_card_group_id,
                        "filter_card_group_name": filter_card_group_name,
                        "filter_legal_entity_id": filter_legal_entity_id,
                        "filter_status": filter_status,
                        "filter_virtual_account_id": filter_virtual_account_id,
                        "sort": sort,
                        "sort_direction": sort_direction,
                    },
                    card_list_params.CardListParams,
                ),
            ),
            cast_to=CardListResponse,
        )

    def get_utilization(
        self,
        card_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroupUtilization:
        """
        Get a card's current utilization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_id:
            raise ValueError(f"Expected a non-empty value for `card_id` but received {card_id!r}")
        return self._get(
            f"/card/{card_id}/utilization",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CardGroupUtilization,
        )


class AsyncCardResource(AsyncAPIResource):
    @cached_property
    def spending_constraint(self) -> AsyncSpendingConstraintResource:
        return AsyncSpendingConstraintResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCardResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCardResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCardResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncCardResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        type: Literal["virtual"],
        account_id: str | NotGiven = NOT_GIVEN,
        card_group_id: str | NotGiven = NOT_GIVEN,
        card_product_id: str | NotGiven = NOT_GIVEN,
        is_single_use: bool | NotGiven = NOT_GIVEN,
        spending_constraint: SpendingConstraintParam | NotGiven = NOT_GIVEN,
        user_data: Dict[str, object] | NotGiven = NOT_GIVEN,
        virtual_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Card:
        """Create a card

        Args:
          type: Specify the type of card you'd like to create.

        At the moment, only virtual cards
              are supported.

          account_id: The ID of the account to create the card under. You can get this by calling
              `GET /account`. This field is required unless you are authenticating via API
              key, in which case it will default to your first commercial account. We
              recommend supplying this even if you are authenticating via API key.

          card_product_id: The ID of the card product to use when creating this card, if not specified a
              random card product will be chosen.

          is_single_use: Defaults to false. When set to true, the card will be automatically closed after
              a single authorization attempt. Note that the card will be closed even if the
              authorization declines or drops

          spending_constraint: A constraint that can be applied to a CardGroupSpendingRule

          user_data: Arbitrary information that can be attached to the card. This should be a JSON
              object and cannot exceed 4kb.

          virtual_account_id: The ID of the virtual account to create the card under. Virtual accounts can be
              retrieved by calling `GET /virtual-account`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/card",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "type": type,
                    "account_id": account_id,
                    "card_group_id": card_group_id,
                    "card_product_id": card_product_id,
                    "is_single_use": is_single_use,
                    "spending_constraint": spending_constraint,
                    "user_data": user_data,
                    "virtual_account_id": virtual_account_id,
                },
                card_create_params.CardCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )

    async def retrieve(
        self,
        card_id: str,
        *,
        include_cvv: Literal["true", "false"] | NotGiven = NOT_GIVEN,
        include_pan: Literal["true", "false"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Card:
        """
        Fetch details for a single card by card ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_id:
            raise ValueError(f"Expected a non-empty value for `card_id` but received {card_id!r}")
        return await self._get(
            f"/card/{card_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "include_cvv": include_cvv,
                        "include_pan": include_pan,
                    },
                    card_retrieve_params.CardRetrieveParams,
                ),
            ),
            cast_to=Card,
        )

    async def update(
        self,
        card_id: str,
        *,
        card_group_id: Optional[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        spending_constraint: Optional[SpendingConstraintParam] | NotGiven = NOT_GIVEN,
        status: CardStatus | NotGiven = NOT_GIVEN,
        user_data: Optional[Dict[str, object]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Card:
        """
        Update a card

        Args:
          card_group_id: Explicitly set this value to null to remove the card from a group. Omitting this
              field entirely will not affect the group the card belongs to.

          spending_constraint: Explicitly set this value to null to remove all card level spending constraints.

          user_data: Arbitrary information that can be attached to the card. This should be a JSON
              object and cannot exceed 4kb.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_id:
            raise ValueError(f"Expected a non-empty value for `card_id` but received {card_id!r}")
        return await self._patch(
            f"/card/{card_id}",
            body=await async_maybe_transform(
                {
                    "card_group_id": card_group_id,
                    "name": name,
                    "spending_constraint": spending_constraint,
                    "status": status,
                    "user_data": user_data,
                },
                card_update_params.CardUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )

    async def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        filter_account_id: str | NotGiven = NOT_GIVEN,
        filter_card_group_id: str | NotGiven = NOT_GIVEN,
        filter_card_group_name: str | NotGiven = NOT_GIVEN,
        filter_legal_entity_id: str | NotGiven = NOT_GIVEN,
        filter_status: Literal["active", "paused", "closed", "inactive"] | NotGiven = NOT_GIVEN,
        filter_virtual_account_id: str | NotGiven = NOT_GIVEN,
        sort: Literal["createdAt", "name"] | NotGiven = NOT_GIVEN,
        sort_direction: Literal["ASC", "DESC"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardListResponse:
        """
        List all cards you have access to.

        Args:
          cursor: A cursor string to fetch the next page of results

          filter_account_id: Pass in an account ID to filter for cards under a specific account.

          filter_card_group_id: Pass in a card group ID, This will return all cards that belong to the card
              group ID passed in. Cannot be combined with filter:cardGroupName.

          filter_card_group_name: Pass in a card group name, This will return all cards that belong to the card
              group name passed in. Cannot be combined with filter:cardGroupId.

          filter_legal_entity_id: Pass in a legal entity ID to filter for cards in accounts under a specific legal
              entity.

          filter_status: Returns all cards matching the status passed in.

          filter_virtual_account_id: Pass in a virtual account ID to filter for cards under a specific virtual
              account.

          sort: Sorts card by creation date or name.

          sort_direction: The direction to apply the sort filter by. Default ASC.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/card",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cursor": cursor,
                        "filter_account_id": filter_account_id,
                        "filter_card_group_id": filter_card_group_id,
                        "filter_card_group_name": filter_card_group_name,
                        "filter_legal_entity_id": filter_legal_entity_id,
                        "filter_status": filter_status,
                        "filter_virtual_account_id": filter_virtual_account_id,
                        "sort": sort,
                        "sort_direction": sort_direction,
                    },
                    card_list_params.CardListParams,
                ),
            ),
            cast_to=CardListResponse,
        )

    async def get_utilization(
        self,
        card_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CardGroupUtilization:
        """
        Get a card's current utilization

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_id:
            raise ValueError(f"Expected a non-empty value for `card_id` but received {card_id!r}")
        return await self._get(
            f"/card/{card_id}/utilization",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CardGroupUtilization,
        )


class CardResourceWithRawResponse:
    def __init__(self, card: CardResource) -> None:
        self._card = card

        self.create = to_raw_response_wrapper(
            card.create,
        )
        self.retrieve = to_raw_response_wrapper(
            card.retrieve,
        )
        self.update = to_raw_response_wrapper(
            card.update,
        )
        self.list = to_raw_response_wrapper(
            card.list,
        )
        self.get_utilization = to_raw_response_wrapper(
            card.get_utilization,
        )

    @cached_property
    def spending_constraint(self) -> SpendingConstraintResourceWithRawResponse:
        return SpendingConstraintResourceWithRawResponse(self._card.spending_constraint)


class AsyncCardResourceWithRawResponse:
    def __init__(self, card: AsyncCardResource) -> None:
        self._card = card

        self.create = async_to_raw_response_wrapper(
            card.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            card.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            card.update,
        )
        self.list = async_to_raw_response_wrapper(
            card.list,
        )
        self.get_utilization = async_to_raw_response_wrapper(
            card.get_utilization,
        )

    @cached_property
    def spending_constraint(self) -> AsyncSpendingConstraintResourceWithRawResponse:
        return AsyncSpendingConstraintResourceWithRawResponse(self._card.spending_constraint)


class CardResourceWithStreamingResponse:
    def __init__(self, card: CardResource) -> None:
        self._card = card

        self.create = to_streamed_response_wrapper(
            card.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            card.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            card.update,
        )
        self.list = to_streamed_response_wrapper(
            card.list,
        )
        self.get_utilization = to_streamed_response_wrapper(
            card.get_utilization,
        )

    @cached_property
    def spending_constraint(self) -> SpendingConstraintResourceWithStreamingResponse:
        return SpendingConstraintResourceWithStreamingResponse(self._card.spending_constraint)


class AsyncCardResourceWithStreamingResponse:
    def __init__(self, card: AsyncCardResource) -> None:
        self._card = card

        self.create = async_to_streamed_response_wrapper(
            card.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            card.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            card.update,
        )
        self.list = async_to_streamed_response_wrapper(
            card.list,
        )
        self.get_utilization = async_to_streamed_response_wrapper(
            card.get_utilization,
        )

    @cached_property
    def spending_constraint(self) -> AsyncSpendingConstraintResourceWithStreamingResponse:
        return AsyncSpendingConstraintResourceWithStreamingResponse(self._card.spending_constraint)
