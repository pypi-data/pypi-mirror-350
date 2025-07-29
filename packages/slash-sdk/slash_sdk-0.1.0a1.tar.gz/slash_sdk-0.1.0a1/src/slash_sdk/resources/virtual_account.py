# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, overload

import httpx

from ..types import (
    virtual_account_list_params,
    virtual_account_create_params,
    virtual_account_update_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import required_args, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.virtual_account import VirtualAccount
from ..types.commission_details_param import CommissionDetailsParam
from ..types.virtual_account_list_response import VirtualAccountListResponse
from ..types.virtual_account_create_response import VirtualAccountCreateResponse
from ..types.virtual_account_update_response import VirtualAccountUpdateResponse

__all__ = ["VirtualAccountResource", "AsyncVirtualAccountResource"]


class VirtualAccountResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VirtualAccountResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return VirtualAccountResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VirtualAccountResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return VirtualAccountResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        name: str,
        commission_details: CommissionDetailsParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccountCreateResponse:
        """
        Create a virtual account

        Args:
          account_id: The account ID the virtual account should be created under.

          name: The name of the virtual account

          commission_details: Specifies how much of the virtual account's incoming funds should be diverted to
              the primary account

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/virtual-account",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "name": name,
                    "commission_details": commission_details,
                },
                virtual_account_create_params.VirtualAccountCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VirtualAccountCreateResponse,
        )

    def retrieve(
        self,
        virtual_account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccount:
        """
        Retrieve a single virtual account by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not virtual_account_id:
            raise ValueError(f"Expected a non-empty value for `virtual_account_id` but received {virtual_account_id!r}")
        return self._get(
            f"/virtual-account/{virtual_account_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VirtualAccount,
        )

    @overload
    def update(
        self,
        virtual_account_id: str,
        *,
        action: Literal["update"],
        commission_details: CommissionDetailsParam | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccountUpdateResponse:
        """Update an existing virtual account

        Args:
          action: The type of action to take.

        An action of type "update" will update the virtual
              account with the specified properties.

          name: The name to update the virtual account with.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def update(
        self,
        virtual_account_id: str,
        *,
        action: Literal["close"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccountUpdateResponse:
        """Update an existing virtual account

        Args:
          action: The type of action to take.

        An action of type "close" will close the virtual
              account.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["action"])
    def update(
        self,
        virtual_account_id: str,
        *,
        action: Literal["update"] | Literal["close"],
        commission_details: CommissionDetailsParam | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccountUpdateResponse:
        if not virtual_account_id:
            raise ValueError(f"Expected a non-empty value for `virtual_account_id` but received {virtual_account_id!r}")
        return self._patch(
            f"/virtual-account/{virtual_account_id}",
            body=maybe_transform(
                {
                    "action": action,
                    "commission_details": commission_details,
                    "name": name,
                },
                virtual_account_update_params.VirtualAccountUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VirtualAccountUpdateResponse,
        )

    def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        filter_account_id: str | NotGiven = NOT_GIVEN,
        filter_include_closed_accounts: Literal["true", "false"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccountListResponse:
        """Retrieve a list of virtual accounts under an account.

        The virtual accounts are
        returned in an array, with each item representing a virtual account under that
        account.

        The primary account will also be returned as a virtual account, with an account
        type of 'primary' while actual subaccounts under the primary account will have
        an account type of 'default'.

        Args:
          cursor: A cursor string to fetch the next page of results

          filter_account_id: Pass in an account ID to filter virtual accounts by account ID. This will return
              all virtual accounts that match the account ID passed in.

          filter_include_closed_accounts: Include virtual accounts that have been closed in the query results. By default,
              they will not be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/virtual-account",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "filter_account_id": filter_account_id,
                        "filter_include_closed_accounts": filter_include_closed_accounts,
                    },
                    virtual_account_list_params.VirtualAccountListParams,
                ),
            ),
            cast_to=VirtualAccountListResponse,
        )


class AsyncVirtualAccountResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVirtualAccountResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVirtualAccountResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVirtualAccountResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncVirtualAccountResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        name: str,
        commission_details: CommissionDetailsParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccountCreateResponse:
        """
        Create a virtual account

        Args:
          account_id: The account ID the virtual account should be created under.

          name: The name of the virtual account

          commission_details: Specifies how much of the virtual account's incoming funds should be diverted to
              the primary account

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/virtual-account",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "name": name,
                    "commission_details": commission_details,
                },
                virtual_account_create_params.VirtualAccountCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VirtualAccountCreateResponse,
        )

    async def retrieve(
        self,
        virtual_account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccount:
        """
        Retrieve a single virtual account by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not virtual_account_id:
            raise ValueError(f"Expected a non-empty value for `virtual_account_id` but received {virtual_account_id!r}")
        return await self._get(
            f"/virtual-account/{virtual_account_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VirtualAccount,
        )

    @overload
    async def update(
        self,
        virtual_account_id: str,
        *,
        action: Literal["update"],
        commission_details: CommissionDetailsParam | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccountUpdateResponse:
        """Update an existing virtual account

        Args:
          action: The type of action to take.

        An action of type "update" will update the virtual
              account with the specified properties.

          name: The name to update the virtual account with.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def update(
        self,
        virtual_account_id: str,
        *,
        action: Literal["close"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccountUpdateResponse:
        """Update an existing virtual account

        Args:
          action: The type of action to take.

        An action of type "close" will close the virtual
              account.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["action"])
    async def update(
        self,
        virtual_account_id: str,
        *,
        action: Literal["update"] | Literal["close"],
        commission_details: CommissionDetailsParam | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccountUpdateResponse:
        if not virtual_account_id:
            raise ValueError(f"Expected a non-empty value for `virtual_account_id` but received {virtual_account_id!r}")
        return await self._patch(
            f"/virtual-account/{virtual_account_id}",
            body=await async_maybe_transform(
                {
                    "action": action,
                    "commission_details": commission_details,
                    "name": name,
                },
                virtual_account_update_params.VirtualAccountUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VirtualAccountUpdateResponse,
        )

    async def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        filter_account_id: str | NotGiven = NOT_GIVEN,
        filter_include_closed_accounts: Literal["true", "false"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VirtualAccountListResponse:
        """Retrieve a list of virtual accounts under an account.

        The virtual accounts are
        returned in an array, with each item representing a virtual account under that
        account.

        The primary account will also be returned as a virtual account, with an account
        type of 'primary' while actual subaccounts under the primary account will have
        an account type of 'default'.

        Args:
          cursor: A cursor string to fetch the next page of results

          filter_account_id: Pass in an account ID to filter virtual accounts by account ID. This will return
              all virtual accounts that match the account ID passed in.

          filter_include_closed_accounts: Include virtual accounts that have been closed in the query results. By default,
              they will not be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/virtual-account",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cursor": cursor,
                        "filter_account_id": filter_account_id,
                        "filter_include_closed_accounts": filter_include_closed_accounts,
                    },
                    virtual_account_list_params.VirtualAccountListParams,
                ),
            ),
            cast_to=VirtualAccountListResponse,
        )


class VirtualAccountResourceWithRawResponse:
    def __init__(self, virtual_account: VirtualAccountResource) -> None:
        self._virtual_account = virtual_account

        self.create = to_raw_response_wrapper(
            virtual_account.create,
        )
        self.retrieve = to_raw_response_wrapper(
            virtual_account.retrieve,
        )
        self.update = to_raw_response_wrapper(
            virtual_account.update,
        )
        self.list = to_raw_response_wrapper(
            virtual_account.list,
        )


class AsyncVirtualAccountResourceWithRawResponse:
    def __init__(self, virtual_account: AsyncVirtualAccountResource) -> None:
        self._virtual_account = virtual_account

        self.create = async_to_raw_response_wrapper(
            virtual_account.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            virtual_account.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            virtual_account.update,
        )
        self.list = async_to_raw_response_wrapper(
            virtual_account.list,
        )


class VirtualAccountResourceWithStreamingResponse:
    def __init__(self, virtual_account: VirtualAccountResource) -> None:
        self._virtual_account = virtual_account

        self.create = to_streamed_response_wrapper(
            virtual_account.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            virtual_account.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            virtual_account.update,
        )
        self.list = to_streamed_response_wrapper(
            virtual_account.list,
        )


class AsyncVirtualAccountResourceWithStreamingResponse:
    def __init__(self, virtual_account: AsyncVirtualAccountResource) -> None:
        self._virtual_account = virtual_account

        self.create = async_to_streamed_response_wrapper(
            virtual_account.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            virtual_account.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            virtual_account.update,
        )
        self.list = async_to_streamed_response_wrapper(
            virtual_account.list,
        )
