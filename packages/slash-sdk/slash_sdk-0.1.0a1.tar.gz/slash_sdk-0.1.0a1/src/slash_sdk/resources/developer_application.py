# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import developer_application_update_params
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
from ..types.developer_application_model import DeveloperApplicationModel
from ..types.developer_application_data_param import DeveloperApplicationDataParam

__all__ = ["DeveloperApplicationResource", "AsyncDeveloperApplicationResource"]


class DeveloperApplicationResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DeveloperApplicationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DeveloperApplicationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DeveloperApplicationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return DeveloperApplicationResourceWithStreamingResponse(self)

    def retrieve(
        self,
        developer_application_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeveloperApplicationModel:
        """
        Get a DeveloperApplication

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not developer_application_id:
            raise ValueError(
                f"Expected a non-empty value for `developer_application_id` but received {developer_application_id!r}"
            )
        return self._get(
            f"/developer-application/{developer_application_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeveloperApplicationModel,
        )

    def update(
        self,
        developer_application_id: str,
        *,
        data: DeveloperApplicationDataParam | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeveloperApplicationModel:
        """
        Update a DeveloperApplication

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not developer_application_id:
            raise ValueError(
                f"Expected a non-empty value for `developer_application_id` but received {developer_application_id!r}"
            )
        return self._patch(
            f"/developer-application/{developer_application_id}",
            body=maybe_transform(
                {
                    "data": data,
                    "name": name,
                },
                developer_application_update_params.DeveloperApplicationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeveloperApplicationModel,
        )

    def create_or_regenerate_secret(
        self,
        developer_application_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeveloperApplicationModel:
        """
        Create or regenerate a DeveloperApplication's OAuthClientSecret

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not developer_application_id:
            raise ValueError(
                f"Expected a non-empty value for `developer_application_id` but received {developer_application_id!r}"
            )
        return self._post(
            f"/developer-application/{developer_application_id}/secret",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeveloperApplicationModel,
        )


class AsyncDeveloperApplicationResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDeveloperApplicationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDeveloperApplicationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDeveloperApplicationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncDeveloperApplicationResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        developer_application_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeveloperApplicationModel:
        """
        Get a DeveloperApplication

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not developer_application_id:
            raise ValueError(
                f"Expected a non-empty value for `developer_application_id` but received {developer_application_id!r}"
            )
        return await self._get(
            f"/developer-application/{developer_application_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeveloperApplicationModel,
        )

    async def update(
        self,
        developer_application_id: str,
        *,
        data: DeveloperApplicationDataParam | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeveloperApplicationModel:
        """
        Update a DeveloperApplication

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not developer_application_id:
            raise ValueError(
                f"Expected a non-empty value for `developer_application_id` but received {developer_application_id!r}"
            )
        return await self._patch(
            f"/developer-application/{developer_application_id}",
            body=await async_maybe_transform(
                {
                    "data": data,
                    "name": name,
                },
                developer_application_update_params.DeveloperApplicationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeveloperApplicationModel,
        )

    async def create_or_regenerate_secret(
        self,
        developer_application_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeveloperApplicationModel:
        """
        Create or regenerate a DeveloperApplication's OAuthClientSecret

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not developer_application_id:
            raise ValueError(
                f"Expected a non-empty value for `developer_application_id` but received {developer_application_id!r}"
            )
        return await self._post(
            f"/developer-application/{developer_application_id}/secret",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeveloperApplicationModel,
        )


class DeveloperApplicationResourceWithRawResponse:
    def __init__(self, developer_application: DeveloperApplicationResource) -> None:
        self._developer_application = developer_application

        self.retrieve = to_raw_response_wrapper(
            developer_application.retrieve,
        )
        self.update = to_raw_response_wrapper(
            developer_application.update,
        )
        self.create_or_regenerate_secret = to_raw_response_wrapper(
            developer_application.create_or_regenerate_secret,
        )


class AsyncDeveloperApplicationResourceWithRawResponse:
    def __init__(self, developer_application: AsyncDeveloperApplicationResource) -> None:
        self._developer_application = developer_application

        self.retrieve = async_to_raw_response_wrapper(
            developer_application.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            developer_application.update,
        )
        self.create_or_regenerate_secret = async_to_raw_response_wrapper(
            developer_application.create_or_regenerate_secret,
        )


class DeveloperApplicationResourceWithStreamingResponse:
    def __init__(self, developer_application: DeveloperApplicationResource) -> None:
        self._developer_application = developer_application

        self.retrieve = to_streamed_response_wrapper(
            developer_application.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            developer_application.update,
        )
        self.create_or_regenerate_secret = to_streamed_response_wrapper(
            developer_application.create_or_regenerate_secret,
        )


class AsyncDeveloperApplicationResourceWithStreamingResponse:
    def __init__(self, developer_application: AsyncDeveloperApplicationResource) -> None:
        self._developer_application = developer_application

        self.retrieve = async_to_streamed_response_wrapper(
            developer_application.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            developer_application.update,
        )
        self.create_or_regenerate_secret = async_to_streamed_response_wrapper(
            developer_application.create_or_regenerate_secret,
        )
