# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import transaction_list_params, transaction_aggregate_params, transaction_update_note_params
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
from ..types.transaction import Transaction
from ..types.transaction_list_response import TransactionListResponse
from ..types.transaction_aggregate_response import TransactionAggregateResponse
from ..types.transaction_update_note_response import TransactionUpdateNoteResponse
from ..types.transaction_retrieve_fee_details_response import TransactionRetrieveFeeDetailsResponse

__all__ = ["TransactionResource", "AsyncTransactionResource"]


class TransactionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TransactionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TransactionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TransactionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return TransactionResourceWithStreamingResponse(self)

    def retrieve(
        self,
        transaction_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Transaction:
        """
        Fetch details for a single transaction by ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transaction_id:
            raise ValueError(f"Expected a non-empty value for `transaction_id` but received {transaction_id!r}")
        return self._get(
            f"/transaction/{transaction_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Transaction,
        )

    def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        cursor: str | NotGiven = NOT_GIVEN,
        filter_account_id: str | NotGiven = NOT_GIVEN,
        filter_card_id: str | NotGiven = NOT_GIVEN,
        filter_detailed_status: Literal[
            "pending", "canceled", "failed", "settled", "declined", "refund", "reversed", "returned", "dispute"
        ]
        | NotGiven = NOT_GIVEN,
        filter_from_authorized_at: str | NotGiven = NOT_GIVEN,
        filter_from_date: str | NotGiven = NOT_GIVEN,
        filter_legal_entity_id: str | NotGiven = NOT_GIVEN,
        filter_status: Literal["pending", "posted", "failed"] | NotGiven = NOT_GIVEN,
        filter_to_authorized_at: str | NotGiven = NOT_GIVEN,
        filter_to_date: str | NotGiven = NOT_GIVEN,
        filter_virtual_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransactionListResponse:
        """
        Get all transactions

        Args:
          account_id: Use filter:accountId to filter by account ID

          cursor: A cursor string to fetch the next page of results

          filter_account_id: Pass in an account ID to filter transactions by account ID. This will return all
              transactions that match the account ID passed in.

          filter_card_id: Filter transactions by cardId

          filter_detailed_status: Filter transactions by detailed status

          filter_from_authorized_at: Pass in a unix timestamp in milliseconds to filter transactions by authorization
              time. This will return all transactions that are authorized on or after the date
              passed in.

          filter_from_date: Pass in a unix timestamp in milliseconds to filter transactions by date. This
              will return all transactions that occurred on or after the date passed in.

          filter_legal_entity_id: Pass in a legal entity ID to filter transactions by accounts under a specific
              legal entity.

          filter_status: Filter transactions by status

          filter_to_authorized_at: Pass in a unix timestamp in milliseconds to filter transactions by authorization
              time. This will return all transactions that are authorized on or before the
              date passed in.

          filter_to_date: Pass in a unix timestamp in milliseconds to filter transactions by date. This
              will return all transactions that occurred on or before the date passed in.

          filter_virtual_account_id: Pass in a virtual account ID to filter transactions by virtual account ID. This
              will return all transactions that match the virtual account ID passed in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/transaction",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "cursor": cursor,
                        "filter_account_id": filter_account_id,
                        "filter_card_id": filter_card_id,
                        "filter_detailed_status": filter_detailed_status,
                        "filter_from_authorized_at": filter_from_authorized_at,
                        "filter_from_date": filter_from_date,
                        "filter_legal_entity_id": filter_legal_entity_id,
                        "filter_status": filter_status,
                        "filter_to_authorized_at": filter_to_authorized_at,
                        "filter_to_date": filter_to_date,
                        "filter_virtual_account_id": filter_virtual_account_id,
                    },
                    transaction_list_params.TransactionListParams,
                ),
            ),
            cast_to=TransactionListResponse,
        )

    def aggregate(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        filter_account_id: str | NotGiven = NOT_GIVEN,
        filter_card_id: str | NotGiven = NOT_GIVEN,
        filter_detailed_status: Literal[
            "pending", "canceled", "failed", "settled", "declined", "refund", "reversed", "returned", "dispute"
        ]
        | NotGiven = NOT_GIVEN,
        filter_from_authorized_at: str | NotGiven = NOT_GIVEN,
        filter_from_date: str | NotGiven = NOT_GIVEN,
        filter_legal_entity_id: str | NotGiven = NOT_GIVEN,
        filter_status: Literal["pending", "posted", "failed"] | NotGiven = NOT_GIVEN,
        filter_to_authorized_at: str | NotGiven = NOT_GIVEN,
        filter_to_date: str | NotGiven = NOT_GIVEN,
        filter_virtual_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransactionAggregateResponse:
        """
        Get transaction aggregations

        Args:
          account_id: Use filter:accountId to filter by account ID

          filter_account_id: Pass in an account ID to filter transactions by account ID. This will return all
              transactions that match the account ID passed in.

          filter_card_id: Filter transactions by cardId

          filter_detailed_status: Filter transactions by detailed status

          filter_from_authorized_at: Pass in a unix timestamp in milliseconds to filter transactions by authorization
              time. This will return all transactions that are authorized on or after the date
              passed in.

          filter_from_date: Pass in a unix timestamp in milliseconds to filter transactions by date. This
              will return all transactions that occurred on or after the date passed in.

          filter_legal_entity_id: Pass in a legal entity ID to filter transactions by accounts under a specific
              legal entity.

          filter_status: Filter transactions by status

          filter_to_authorized_at: Pass in a unix timestamp in milliseconds to filter transactions by authorization
              time. This will return all transactions that are authorized on or before the
              date passed in.

          filter_to_date: Pass in a unix timestamp in milliseconds to filter transactions by date. This
              will return all transactions that occurred on or before the date passed in.

          filter_virtual_account_id: Pass in a virtual account ID to filter transactions by virtual account ID. This
              will return all transactions that match the virtual account ID passed in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/transaction/aggregation",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "filter_account_id": filter_account_id,
                        "filter_card_id": filter_card_id,
                        "filter_detailed_status": filter_detailed_status,
                        "filter_from_authorized_at": filter_from_authorized_at,
                        "filter_from_date": filter_from_date,
                        "filter_legal_entity_id": filter_legal_entity_id,
                        "filter_status": filter_status,
                        "filter_to_authorized_at": filter_to_authorized_at,
                        "filter_to_date": filter_to_date,
                        "filter_virtual_account_id": filter_virtual_account_id,
                    },
                    transaction_aggregate_params.TransactionAggregateParams,
                ),
            ),
            cast_to=TransactionAggregateResponse,
        )

    def retrieve_fee_details(
        self,
        transaction_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransactionRetrieveFeeDetailsResponse:
        """
        Fetch breakdown of a fee transaction

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transaction_id:
            raise ValueError(f"Expected a non-empty value for `transaction_id` but received {transaction_id!r}")
        return self._get(
            f"/transaction/{transaction_id}/fee-details",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransactionRetrieveFeeDetailsResponse,
        )

    def update_note(
        self,
        transaction_id: str,
        *,
        note: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransactionUpdateNoteResponse:
        """
        Update note for a transaction

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transaction_id:
            raise ValueError(f"Expected a non-empty value for `transaction_id` but received {transaction_id!r}")
        return self._patch(
            f"/transaction/{transaction_id}/note",
            body=maybe_transform({"note": note}, transaction_update_note_params.TransactionUpdateNoteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransactionUpdateNoteResponse,
        )


class AsyncTransactionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTransactionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTransactionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTransactionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncTransactionResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        transaction_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Transaction:
        """
        Fetch details for a single transaction by ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transaction_id:
            raise ValueError(f"Expected a non-empty value for `transaction_id` but received {transaction_id!r}")
        return await self._get(
            f"/transaction/{transaction_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Transaction,
        )

    async def list(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        cursor: str | NotGiven = NOT_GIVEN,
        filter_account_id: str | NotGiven = NOT_GIVEN,
        filter_card_id: str | NotGiven = NOT_GIVEN,
        filter_detailed_status: Literal[
            "pending", "canceled", "failed", "settled", "declined", "refund", "reversed", "returned", "dispute"
        ]
        | NotGiven = NOT_GIVEN,
        filter_from_authorized_at: str | NotGiven = NOT_GIVEN,
        filter_from_date: str | NotGiven = NOT_GIVEN,
        filter_legal_entity_id: str | NotGiven = NOT_GIVEN,
        filter_status: Literal["pending", "posted", "failed"] | NotGiven = NOT_GIVEN,
        filter_to_authorized_at: str | NotGiven = NOT_GIVEN,
        filter_to_date: str | NotGiven = NOT_GIVEN,
        filter_virtual_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransactionListResponse:
        """
        Get all transactions

        Args:
          account_id: Use filter:accountId to filter by account ID

          cursor: A cursor string to fetch the next page of results

          filter_account_id: Pass in an account ID to filter transactions by account ID. This will return all
              transactions that match the account ID passed in.

          filter_card_id: Filter transactions by cardId

          filter_detailed_status: Filter transactions by detailed status

          filter_from_authorized_at: Pass in a unix timestamp in milliseconds to filter transactions by authorization
              time. This will return all transactions that are authorized on or after the date
              passed in.

          filter_from_date: Pass in a unix timestamp in milliseconds to filter transactions by date. This
              will return all transactions that occurred on or after the date passed in.

          filter_legal_entity_id: Pass in a legal entity ID to filter transactions by accounts under a specific
              legal entity.

          filter_status: Filter transactions by status

          filter_to_authorized_at: Pass in a unix timestamp in milliseconds to filter transactions by authorization
              time. This will return all transactions that are authorized on or before the
              date passed in.

          filter_to_date: Pass in a unix timestamp in milliseconds to filter transactions by date. This
              will return all transactions that occurred on or before the date passed in.

          filter_virtual_account_id: Pass in a virtual account ID to filter transactions by virtual account ID. This
              will return all transactions that match the virtual account ID passed in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/transaction",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "account_id": account_id,
                        "cursor": cursor,
                        "filter_account_id": filter_account_id,
                        "filter_card_id": filter_card_id,
                        "filter_detailed_status": filter_detailed_status,
                        "filter_from_authorized_at": filter_from_authorized_at,
                        "filter_from_date": filter_from_date,
                        "filter_legal_entity_id": filter_legal_entity_id,
                        "filter_status": filter_status,
                        "filter_to_authorized_at": filter_to_authorized_at,
                        "filter_to_date": filter_to_date,
                        "filter_virtual_account_id": filter_virtual_account_id,
                    },
                    transaction_list_params.TransactionListParams,
                ),
            ),
            cast_to=TransactionListResponse,
        )

    async def aggregate(
        self,
        *,
        account_id: str | NotGiven = NOT_GIVEN,
        filter_account_id: str | NotGiven = NOT_GIVEN,
        filter_card_id: str | NotGiven = NOT_GIVEN,
        filter_detailed_status: Literal[
            "pending", "canceled", "failed", "settled", "declined", "refund", "reversed", "returned", "dispute"
        ]
        | NotGiven = NOT_GIVEN,
        filter_from_authorized_at: str | NotGiven = NOT_GIVEN,
        filter_from_date: str | NotGiven = NOT_GIVEN,
        filter_legal_entity_id: str | NotGiven = NOT_GIVEN,
        filter_status: Literal["pending", "posted", "failed"] | NotGiven = NOT_GIVEN,
        filter_to_authorized_at: str | NotGiven = NOT_GIVEN,
        filter_to_date: str | NotGiven = NOT_GIVEN,
        filter_virtual_account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransactionAggregateResponse:
        """
        Get transaction aggregations

        Args:
          account_id: Use filter:accountId to filter by account ID

          filter_account_id: Pass in an account ID to filter transactions by account ID. This will return all
              transactions that match the account ID passed in.

          filter_card_id: Filter transactions by cardId

          filter_detailed_status: Filter transactions by detailed status

          filter_from_authorized_at: Pass in a unix timestamp in milliseconds to filter transactions by authorization
              time. This will return all transactions that are authorized on or after the date
              passed in.

          filter_from_date: Pass in a unix timestamp in milliseconds to filter transactions by date. This
              will return all transactions that occurred on or after the date passed in.

          filter_legal_entity_id: Pass in a legal entity ID to filter transactions by accounts under a specific
              legal entity.

          filter_status: Filter transactions by status

          filter_to_authorized_at: Pass in a unix timestamp in milliseconds to filter transactions by authorization
              time. This will return all transactions that are authorized on or before the
              date passed in.

          filter_to_date: Pass in a unix timestamp in milliseconds to filter transactions by date. This
              will return all transactions that occurred on or before the date passed in.

          filter_virtual_account_id: Pass in a virtual account ID to filter transactions by virtual account ID. This
              will return all transactions that match the virtual account ID passed in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/transaction/aggregation",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "account_id": account_id,
                        "filter_account_id": filter_account_id,
                        "filter_card_id": filter_card_id,
                        "filter_detailed_status": filter_detailed_status,
                        "filter_from_authorized_at": filter_from_authorized_at,
                        "filter_from_date": filter_from_date,
                        "filter_legal_entity_id": filter_legal_entity_id,
                        "filter_status": filter_status,
                        "filter_to_authorized_at": filter_to_authorized_at,
                        "filter_to_date": filter_to_date,
                        "filter_virtual_account_id": filter_virtual_account_id,
                    },
                    transaction_aggregate_params.TransactionAggregateParams,
                ),
            ),
            cast_to=TransactionAggregateResponse,
        )

    async def retrieve_fee_details(
        self,
        transaction_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransactionRetrieveFeeDetailsResponse:
        """
        Fetch breakdown of a fee transaction

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transaction_id:
            raise ValueError(f"Expected a non-empty value for `transaction_id` but received {transaction_id!r}")
        return await self._get(
            f"/transaction/{transaction_id}/fee-details",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransactionRetrieveFeeDetailsResponse,
        )

    async def update_note(
        self,
        transaction_id: str,
        *,
        note: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransactionUpdateNoteResponse:
        """
        Update note for a transaction

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transaction_id:
            raise ValueError(f"Expected a non-empty value for `transaction_id` but received {transaction_id!r}")
        return await self._patch(
            f"/transaction/{transaction_id}/note",
            body=await async_maybe_transform(
                {"note": note}, transaction_update_note_params.TransactionUpdateNoteParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransactionUpdateNoteResponse,
        )


class TransactionResourceWithRawResponse:
    def __init__(self, transaction: TransactionResource) -> None:
        self._transaction = transaction

        self.retrieve = to_raw_response_wrapper(
            transaction.retrieve,
        )
        self.list = to_raw_response_wrapper(
            transaction.list,
        )
        self.aggregate = to_raw_response_wrapper(
            transaction.aggregate,
        )
        self.retrieve_fee_details = to_raw_response_wrapper(
            transaction.retrieve_fee_details,
        )
        self.update_note = to_raw_response_wrapper(
            transaction.update_note,
        )


class AsyncTransactionResourceWithRawResponse:
    def __init__(self, transaction: AsyncTransactionResource) -> None:
        self._transaction = transaction

        self.retrieve = async_to_raw_response_wrapper(
            transaction.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            transaction.list,
        )
        self.aggregate = async_to_raw_response_wrapper(
            transaction.aggregate,
        )
        self.retrieve_fee_details = async_to_raw_response_wrapper(
            transaction.retrieve_fee_details,
        )
        self.update_note = async_to_raw_response_wrapper(
            transaction.update_note,
        )


class TransactionResourceWithStreamingResponse:
    def __init__(self, transaction: TransactionResource) -> None:
        self._transaction = transaction

        self.retrieve = to_streamed_response_wrapper(
            transaction.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            transaction.list,
        )
        self.aggregate = to_streamed_response_wrapper(
            transaction.aggregate,
        )
        self.retrieve_fee_details = to_streamed_response_wrapper(
            transaction.retrieve_fee_details,
        )
        self.update_note = to_streamed_response_wrapper(
            transaction.update_note,
        )


class AsyncTransactionResourceWithStreamingResponse:
    def __init__(self, transaction: AsyncTransactionResource) -> None:
        self._transaction = transaction

        self.retrieve = async_to_streamed_response_wrapper(
            transaction.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            transaction.list,
        )
        self.aggregate = async_to_streamed_response_wrapper(
            transaction.aggregate,
        )
        self.retrieve_fee_details = async_to_streamed_response_wrapper(
            transaction.retrieve_fee_details,
        )
        self.update_note = async_to_streamed_response_wrapper(
            transaction.update_note,
        )
