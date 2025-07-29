# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import DeveloperApplicationType, developer_account_create_application_params
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
from ..types.developer_application_type import DeveloperApplicationType
from ..types.developer_application_model import DeveloperApplicationModel
from ..types.developer_application_data_param import DeveloperApplicationDataParam

__all__ = ["DeveloperAccountResource", "AsyncDeveloperAccountResource"]


class DeveloperAccountResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DeveloperAccountResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DeveloperAccountResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DeveloperAccountResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return DeveloperAccountResourceWithStreamingResponse(self)

    def create_application(
        self,
        developer_account_id: str,
        *,
        data: DeveloperApplicationDataParam,
        name: str,
        type: DeveloperApplicationType,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeveloperApplicationModel:
        """
        Create a DeveloperApplication

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not developer_account_id:
            raise ValueError(
                f"Expected a non-empty value for `developer_account_id` but received {developer_account_id!r}"
            )
        return self._post(
            f"/developer-account/{developer_account_id}/application",
            body=maybe_transform(
                {
                    "data": data,
                    "name": name,
                    "type": type,
                },
                developer_account_create_application_params.DeveloperAccountCreateApplicationParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeveloperApplicationModel,
        )


class AsyncDeveloperAccountResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDeveloperAccountResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDeveloperAccountResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDeveloperAccountResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncDeveloperAccountResourceWithStreamingResponse(self)

    async def create_application(
        self,
        developer_account_id: str,
        *,
        data: DeveloperApplicationDataParam,
        name: str,
        type: DeveloperApplicationType,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeveloperApplicationModel:
        """
        Create a DeveloperApplication

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not developer_account_id:
            raise ValueError(
                f"Expected a non-empty value for `developer_account_id` but received {developer_account_id!r}"
            )
        return await self._post(
            f"/developer-account/{developer_account_id}/application",
            body=await async_maybe_transform(
                {
                    "data": data,
                    "name": name,
                    "type": type,
                },
                developer_account_create_application_params.DeveloperAccountCreateApplicationParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeveloperApplicationModel,
        )


class DeveloperAccountResourceWithRawResponse:
    def __init__(self, developer_account: DeveloperAccountResource) -> None:
        self._developer_account = developer_account

        self.create_application = to_raw_response_wrapper(
            developer_account.create_application,
        )


class AsyncDeveloperAccountResourceWithRawResponse:
    def __init__(self, developer_account: AsyncDeveloperAccountResource) -> None:
        self._developer_account = developer_account

        self.create_application = async_to_raw_response_wrapper(
            developer_account.create_application,
        )


class DeveloperAccountResourceWithStreamingResponse:
    def __init__(self, developer_account: DeveloperAccountResource) -> None:
        self._developer_account = developer_account

        self.create_application = to_streamed_response_wrapper(
            developer_account.create_application,
        )


class AsyncDeveloperAccountResourceWithStreamingResponse:
    def __init__(self, developer_account: AsyncDeveloperAccountResource) -> None:
        self._developer_account = developer_account

        self.create_application = async_to_streamed_response_wrapper(
            developer_account.create_application,
        )
