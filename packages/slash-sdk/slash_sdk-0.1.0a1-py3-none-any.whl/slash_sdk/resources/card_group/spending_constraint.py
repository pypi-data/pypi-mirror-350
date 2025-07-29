# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

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
from ...types.card_group import spending_constraint_update_full_params, spending_constraint_update_partial_params
from ...types.card.spending_constraint import SpendingConstraint

__all__ = ["SpendingConstraintResource", "AsyncSpendingConstraintResource"]


class SpendingConstraintResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SpendingConstraintResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SpendingConstraintResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpendingConstraintResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return SpendingConstraintResourceWithStreamingResponse(self)

    def update_full(
        self,
        card_group_id: str,
        *,
        country_rule: Optional[spending_constraint_update_full_params.CountryRule] | NotGiven = NOT_GIVEN,
        merchant_category_code_rule: Optional[spending_constraint_update_full_params.MerchantCategoryCodeRule]
        | NotGiven = NOT_GIVEN,
        merchant_category_rule: Optional[spending_constraint_update_full_params.MerchantCategoryRule]
        | NotGiven = NOT_GIVEN,
        merchant_rule: Optional[spending_constraint_update_full_params.MerchantRule] | NotGiven = NOT_GIVEN,
        spending_rule: Optional[spending_constraint_update_full_params.SpendingRule] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SpendingConstraint:
        """
        Fully replace a card group's spending constraint.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_group_id:
            raise ValueError(f"Expected a non-empty value for `card_group_id` but received {card_group_id!r}")
        return self._put(
            f"/card-group/{card_group_id}/spending-constraint",
            body=maybe_transform(
                {
                    "country_rule": country_rule,
                    "merchant_category_code_rule": merchant_category_code_rule,
                    "merchant_category_rule": merchant_category_rule,
                    "merchant_rule": merchant_rule,
                    "spending_rule": spending_rule,
                },
                spending_constraint_update_full_params.SpendingConstraintUpdateFullParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpendingConstraint,
        )

    def update_partial(
        self,
        card_group_id: str,
        *,
        country_rule: Optional[spending_constraint_update_partial_params.CountryRule] | NotGiven = NOT_GIVEN,
        merchant_category_code_rule: Optional[spending_constraint_update_partial_params.MerchantCategoryCodeRule]
        | NotGiven = NOT_GIVEN,
        merchant_category_rule: Optional[spending_constraint_update_partial_params.MerchantCategoryRule]
        | NotGiven = NOT_GIVEN,
        merchant_rule: Optional[spending_constraint_update_partial_params.MerchantRule] | NotGiven = NOT_GIVEN,
        spending_rule: Optional[spending_constraint_update_partial_params.SpendingRule] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SpendingConstraint:
        """
        Apply a partial update to a card group's spending constraint while preserving
        current properties applied. Properties set to "null" will be removed from the
        spending constraint.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_group_id:
            raise ValueError(f"Expected a non-empty value for `card_group_id` but received {card_group_id!r}")
        return self._patch(
            f"/card-group/{card_group_id}/spending-constraint",
            body=maybe_transform(
                {
                    "country_rule": country_rule,
                    "merchant_category_code_rule": merchant_category_code_rule,
                    "merchant_category_rule": merchant_category_rule,
                    "merchant_rule": merchant_rule,
                    "spending_rule": spending_rule,
                },
                spending_constraint_update_partial_params.SpendingConstraintUpdatePartialParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpendingConstraint,
        )


class AsyncSpendingConstraintResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSpendingConstraintResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSpendingConstraintResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpendingConstraintResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncSpendingConstraintResourceWithStreamingResponse(self)

    async def update_full(
        self,
        card_group_id: str,
        *,
        country_rule: Optional[spending_constraint_update_full_params.CountryRule] | NotGiven = NOT_GIVEN,
        merchant_category_code_rule: Optional[spending_constraint_update_full_params.MerchantCategoryCodeRule]
        | NotGiven = NOT_GIVEN,
        merchant_category_rule: Optional[spending_constraint_update_full_params.MerchantCategoryRule]
        | NotGiven = NOT_GIVEN,
        merchant_rule: Optional[spending_constraint_update_full_params.MerchantRule] | NotGiven = NOT_GIVEN,
        spending_rule: Optional[spending_constraint_update_full_params.SpendingRule] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SpendingConstraint:
        """
        Fully replace a card group's spending constraint.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_group_id:
            raise ValueError(f"Expected a non-empty value for `card_group_id` but received {card_group_id!r}")
        return await self._put(
            f"/card-group/{card_group_id}/spending-constraint",
            body=await async_maybe_transform(
                {
                    "country_rule": country_rule,
                    "merchant_category_code_rule": merchant_category_code_rule,
                    "merchant_category_rule": merchant_category_rule,
                    "merchant_rule": merchant_rule,
                    "spending_rule": spending_rule,
                },
                spending_constraint_update_full_params.SpendingConstraintUpdateFullParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpendingConstraint,
        )

    async def update_partial(
        self,
        card_group_id: str,
        *,
        country_rule: Optional[spending_constraint_update_partial_params.CountryRule] | NotGiven = NOT_GIVEN,
        merchant_category_code_rule: Optional[spending_constraint_update_partial_params.MerchantCategoryCodeRule]
        | NotGiven = NOT_GIVEN,
        merchant_category_rule: Optional[spending_constraint_update_partial_params.MerchantCategoryRule]
        | NotGiven = NOT_GIVEN,
        merchant_rule: Optional[spending_constraint_update_partial_params.MerchantRule] | NotGiven = NOT_GIVEN,
        spending_rule: Optional[spending_constraint_update_partial_params.SpendingRule] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SpendingConstraint:
        """
        Apply a partial update to a card group's spending constraint while preserving
        current properties applied. Properties set to "null" will be removed from the
        spending constraint.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_group_id:
            raise ValueError(f"Expected a non-empty value for `card_group_id` but received {card_group_id!r}")
        return await self._patch(
            f"/card-group/{card_group_id}/spending-constraint",
            body=await async_maybe_transform(
                {
                    "country_rule": country_rule,
                    "merchant_category_code_rule": merchant_category_code_rule,
                    "merchant_category_rule": merchant_category_rule,
                    "merchant_rule": merchant_rule,
                    "spending_rule": spending_rule,
                },
                spending_constraint_update_partial_params.SpendingConstraintUpdatePartialParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpendingConstraint,
        )


class SpendingConstraintResourceWithRawResponse:
    def __init__(self, spending_constraint: SpendingConstraintResource) -> None:
        self._spending_constraint = spending_constraint

        self.update_full = to_raw_response_wrapper(
            spending_constraint.update_full,
        )
        self.update_partial = to_raw_response_wrapper(
            spending_constraint.update_partial,
        )


class AsyncSpendingConstraintResourceWithRawResponse:
    def __init__(self, spending_constraint: AsyncSpendingConstraintResource) -> None:
        self._spending_constraint = spending_constraint

        self.update_full = async_to_raw_response_wrapper(
            spending_constraint.update_full,
        )
        self.update_partial = async_to_raw_response_wrapper(
            spending_constraint.update_partial,
        )


class SpendingConstraintResourceWithStreamingResponse:
    def __init__(self, spending_constraint: SpendingConstraintResource) -> None:
        self._spending_constraint = spending_constraint

        self.update_full = to_streamed_response_wrapper(
            spending_constraint.update_full,
        )
        self.update_partial = to_streamed_response_wrapper(
            spending_constraint.update_partial,
        )


class AsyncSpendingConstraintResourceWithStreamingResponse:
    def __init__(self, spending_constraint: AsyncSpendingConstraintResource) -> None:
        self._spending_constraint = spending_constraint

        self.update_full = async_to_streamed_response_wrapper(
            spending_constraint.update_full,
        )
        self.update_partial = async_to_streamed_response_wrapper(
            spending_constraint.update_partial,
        )
