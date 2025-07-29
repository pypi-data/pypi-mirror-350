# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, overload

import httpx

from ...types import oauth2_get_token_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import required_args, maybe_transform, async_maybe_transform
from .userinfo import (
    UserinfoResource,
    AsyncUserinfoResource,
    UserinfoResourceWithRawResponse,
    AsyncUserinfoResourceWithRawResponse,
    UserinfoResourceWithStreamingResponse,
    AsyncUserinfoResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.oauth2_get_token_response import Oauth2GetTokenResponse

__all__ = ["Oauth2Resource", "AsyncOauth2Resource"]


class Oauth2Resource(SyncAPIResource):
    @cached_property
    def userinfo(self) -> UserinfoResource:
        return UserinfoResource(self._client)

    @cached_property
    def with_raw_response(self) -> Oauth2ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return Oauth2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> Oauth2ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return Oauth2ResourceWithStreamingResponse(self)

    @overload
    def get_token(
        self,
        *,
        code: str,
        grant_type: Literal["authorization_code"],
        redirect_uri: str,
        code_verifier: str | NotGiven = NOT_GIVEN,
        prompt: str | NotGiven = NOT_GIVEN,
        scope: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Oauth2GetTokenResponse:
        """
        Get or refresh an access token

        Args:
          code_verifier: Unused by Slash, but required in the OAuth spec.

          prompt: Unused by Slash, but required in the OAuth spec.

          scope: Unused by Slash, but required in the OAuth spec.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def get_token(
        self,
        *,
        grant_type: Literal["refresh_token"],
        refresh_token: str,
        code: str | NotGiven = NOT_GIVEN,
        code_verifier: str | NotGiven = NOT_GIVEN,
        prompt: str | NotGiven = NOT_GIVEN,
        redirect_uri: str | NotGiven = NOT_GIVEN,
        scope: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Oauth2GetTokenResponse:
        """
        Get or refresh an access token

        Args:
          code: Unused by Slash, but required in the OAuth spec.

          code_verifier: Unused by Slash, but required in the OAuth spec.

          prompt: Unused by Slash, but required in the OAuth spec.

          redirect_uri: Unused by Slash, but required in the OAuth spec.

          scope: Unused by Slash, but required in the OAuth spec.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["code", "grant_type", "redirect_uri"], ["grant_type", "refresh_token"])
    def get_token(
        self,
        *,
        code: str | NotGiven = NOT_GIVEN,
        grant_type: Literal["authorization_code"] | Literal["refresh_token"],
        redirect_uri: str | NotGiven = NOT_GIVEN,
        code_verifier: str | NotGiven = NOT_GIVEN,
        prompt: str | NotGiven = NOT_GIVEN,
        scope: str | NotGiven = NOT_GIVEN,
        refresh_token: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Oauth2GetTokenResponse:
        return self._post(
            "/oauth2/token",
            body=maybe_transform(
                {
                    "code": code,
                    "grant_type": grant_type,
                    "redirect_uri": redirect_uri,
                    "code_verifier": code_verifier,
                    "prompt": prompt,
                    "scope": scope,
                    "refresh_token": refresh_token,
                },
                oauth2_get_token_params.Oauth2GetTokenParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Oauth2GetTokenResponse,
        )


class AsyncOauth2Resource(AsyncAPIResource):
    @cached_property
    def userinfo(self) -> AsyncUserinfoResource:
        return AsyncUserinfoResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncOauth2ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOauth2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOauth2ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/slashfi/slash-sdk-python#with_streaming_response
        """
        return AsyncOauth2ResourceWithStreamingResponse(self)

    @overload
    async def get_token(
        self,
        *,
        code: str,
        grant_type: Literal["authorization_code"],
        redirect_uri: str,
        code_verifier: str | NotGiven = NOT_GIVEN,
        prompt: str | NotGiven = NOT_GIVEN,
        scope: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Oauth2GetTokenResponse:
        """
        Get or refresh an access token

        Args:
          code_verifier: Unused by Slash, but required in the OAuth spec.

          prompt: Unused by Slash, but required in the OAuth spec.

          scope: Unused by Slash, but required in the OAuth spec.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def get_token(
        self,
        *,
        grant_type: Literal["refresh_token"],
        refresh_token: str,
        code: str | NotGiven = NOT_GIVEN,
        code_verifier: str | NotGiven = NOT_GIVEN,
        prompt: str | NotGiven = NOT_GIVEN,
        redirect_uri: str | NotGiven = NOT_GIVEN,
        scope: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Oauth2GetTokenResponse:
        """
        Get or refresh an access token

        Args:
          code: Unused by Slash, but required in the OAuth spec.

          code_verifier: Unused by Slash, but required in the OAuth spec.

          prompt: Unused by Slash, but required in the OAuth spec.

          redirect_uri: Unused by Slash, but required in the OAuth spec.

          scope: Unused by Slash, but required in the OAuth spec.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["code", "grant_type", "redirect_uri"], ["grant_type", "refresh_token"])
    async def get_token(
        self,
        *,
        code: str | NotGiven = NOT_GIVEN,
        grant_type: Literal["authorization_code"] | Literal["refresh_token"],
        redirect_uri: str | NotGiven = NOT_GIVEN,
        code_verifier: str | NotGiven = NOT_GIVEN,
        prompt: str | NotGiven = NOT_GIVEN,
        scope: str | NotGiven = NOT_GIVEN,
        refresh_token: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Oauth2GetTokenResponse:
        return await self._post(
            "/oauth2/token",
            body=await async_maybe_transform(
                {
                    "code": code,
                    "grant_type": grant_type,
                    "redirect_uri": redirect_uri,
                    "code_verifier": code_verifier,
                    "prompt": prompt,
                    "scope": scope,
                    "refresh_token": refresh_token,
                },
                oauth2_get_token_params.Oauth2GetTokenParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Oauth2GetTokenResponse,
        )


class Oauth2ResourceWithRawResponse:
    def __init__(self, oauth2: Oauth2Resource) -> None:
        self._oauth2 = oauth2

        self.get_token = to_raw_response_wrapper(
            oauth2.get_token,
        )

    @cached_property
    def userinfo(self) -> UserinfoResourceWithRawResponse:
        return UserinfoResourceWithRawResponse(self._oauth2.userinfo)


class AsyncOauth2ResourceWithRawResponse:
    def __init__(self, oauth2: AsyncOauth2Resource) -> None:
        self._oauth2 = oauth2

        self.get_token = async_to_raw_response_wrapper(
            oauth2.get_token,
        )

    @cached_property
    def userinfo(self) -> AsyncUserinfoResourceWithRawResponse:
        return AsyncUserinfoResourceWithRawResponse(self._oauth2.userinfo)


class Oauth2ResourceWithStreamingResponse:
    def __init__(self, oauth2: Oauth2Resource) -> None:
        self._oauth2 = oauth2

        self.get_token = to_streamed_response_wrapper(
            oauth2.get_token,
        )

    @cached_property
    def userinfo(self) -> UserinfoResourceWithStreamingResponse:
        return UserinfoResourceWithStreamingResponse(self._oauth2.userinfo)


class AsyncOauth2ResourceWithStreamingResponse:
    def __init__(self, oauth2: AsyncOauth2Resource) -> None:
        self._oauth2 = oauth2

        self.get_token = async_to_streamed_response_wrapper(
            oauth2.get_token,
        )

    @cached_property
    def userinfo(self) -> AsyncUserinfoResourceWithStreamingResponse:
        return AsyncUserinfoResourceWithStreamingResponse(self._oauth2.userinfo)
