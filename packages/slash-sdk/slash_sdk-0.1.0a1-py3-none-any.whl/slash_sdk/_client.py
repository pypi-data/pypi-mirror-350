# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
import base64
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import (
    pay,
    crypto,
    account,
    webhook,
    merchant,
    transfer,
    well_known,
    transaction,
    card_product,
    legal_entity,
    slash_handle,
    virtual_account,
    developer_account,
    merchant_category,
    developer_application,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.fdx import fdx
from .resources.card import card
from .resources.oauth2 import oauth2
from .resources.card_group import card_group

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "SlashSDK",
    "AsyncSlashSDK",
    "Client",
    "AsyncClient",
]


class SlashSDK(SyncAPIClient):
    legal_entity: legal_entity.LegalEntityResource
    account: account.AccountResource
    virtual_account: virtual_account.VirtualAccountResource
    transaction: transaction.TransactionResource
    transfer: transfer.TransferResource
    card: card.CardResource
    card_group: card_group.CardGroupResource
    card_product: card_product.CardProductResource
    slash_handle: slash_handle.SlashHandleResource
    pay: pay.PayResource
    webhook: webhook.WebhookResource
    merchant: merchant.MerchantResource
    merchant_category: merchant_category.MerchantCategoryResource
    developer_account: developer_account.DeveloperAccountResource
    developer_application: developer_application.DeveloperApplicationResource
    well_known: well_known.WellKnownResource
    oauth2: oauth2.Oauth2Resource
    fdx: fdx.FdxResource
    crypto: crypto.CryptoResource
    with_raw_response: SlashSDKWithRawResponse
    with_streaming_response: SlashSDKWithStreamedResponse

    # client options
    api_key: str | None
    bearer_token: str | None
    username: str | None
    password: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous SlashSDK client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `SLASH_SDK_API_KEY`
        - `bearer_token` from `SLASH_SDK_BEARER_TOKEN`
        - `username` from `SLASH_SDK_USERNAME`
        - `password` from `SLASH_SDK_PASSWORD`
        """
        if api_key is None:
            api_key = os.environ.get("SLASH_SDK_API_KEY")
        self.api_key = api_key

        if bearer_token is None:
            bearer_token = os.environ.get("SLASH_SDK_BEARER_TOKEN")
        self.bearer_token = bearer_token

        if username is None:
            username = os.environ.get("SLASH_SDK_USERNAME")
        self.username = username

        if password is None:
            password = os.environ.get("SLASH_SDK_PASSWORD")
        self.password = password

        if base_url is None:
            base_url = os.environ.get("SLASH_SDK_BASE_URL")
        if base_url is None:
            base_url = f"https://api.joinslash.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.legal_entity = legal_entity.LegalEntityResource(self)
        self.account = account.AccountResource(self)
        self.virtual_account = virtual_account.VirtualAccountResource(self)
        self.transaction = transaction.TransactionResource(self)
        self.transfer = transfer.TransferResource(self)
        self.card = card.CardResource(self)
        self.card_group = card_group.CardGroupResource(self)
        self.card_product = card_product.CardProductResource(self)
        self.slash_handle = slash_handle.SlashHandleResource(self)
        self.pay = pay.PayResource(self)
        self.webhook = webhook.WebhookResource(self)
        self.merchant = merchant.MerchantResource(self)
        self.merchant_category = merchant_category.MerchantCategoryResource(self)
        self.developer_account = developer_account.DeveloperAccountResource(self)
        self.developer_application = developer_application.DeveloperApplicationResource(self)
        self.well_known = well_known.WellKnownResource(self)
        self.oauth2 = oauth2.Oauth2Resource(self)
        self.fdx = fdx.FdxResource(self)
        self.crypto = crypto.CryptoResource(self)
        self.with_raw_response = SlashSDKWithRawResponse(self)
        self.with_streaming_response = SlashSDKWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._api_key, **self._bearer, **self._developer_application}

    @property
    def _api_key(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"X-API-Key": api_key}

    @property
    def _bearer(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        if bearer_token is None:
            return {}
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    def _developer_application(self) -> dict[str, str]:
        if self.username is None:
            return {}
        if self.password is None:
            return {}
        credentials = f"{self.username}:{self.password}".encode("ascii")
        header = f"Basic {base64.b64encode(credentials).decode('ascii')}"
        return {"Authorization": header}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("X-API-Key"):
            return
        if isinstance(custom_headers.get("X-API-Key"), Omit):
            return

        if self.bearer_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        if self.username and self.password and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected one of api_key, bearer_token, username or password to be set. Or for one of the `X-API-Key`, `Authorization` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            bearer_token=bearer_token or self.bearer_token,
            username=username or self.username,
            password=password or self.password,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncSlashSDK(AsyncAPIClient):
    legal_entity: legal_entity.AsyncLegalEntityResource
    account: account.AsyncAccountResource
    virtual_account: virtual_account.AsyncVirtualAccountResource
    transaction: transaction.AsyncTransactionResource
    transfer: transfer.AsyncTransferResource
    card: card.AsyncCardResource
    card_group: card_group.AsyncCardGroupResource
    card_product: card_product.AsyncCardProductResource
    slash_handle: slash_handle.AsyncSlashHandleResource
    pay: pay.AsyncPayResource
    webhook: webhook.AsyncWebhookResource
    merchant: merchant.AsyncMerchantResource
    merchant_category: merchant_category.AsyncMerchantCategoryResource
    developer_account: developer_account.AsyncDeveloperAccountResource
    developer_application: developer_application.AsyncDeveloperApplicationResource
    well_known: well_known.AsyncWellKnownResource
    oauth2: oauth2.AsyncOauth2Resource
    fdx: fdx.AsyncFdxResource
    crypto: crypto.AsyncCryptoResource
    with_raw_response: AsyncSlashSDKWithRawResponse
    with_streaming_response: AsyncSlashSDKWithStreamedResponse

    # client options
    api_key: str | None
    bearer_token: str | None
    username: str | None
    password: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncSlashSDK client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `SLASH_SDK_API_KEY`
        - `bearer_token` from `SLASH_SDK_BEARER_TOKEN`
        - `username` from `SLASH_SDK_USERNAME`
        - `password` from `SLASH_SDK_PASSWORD`
        """
        if api_key is None:
            api_key = os.environ.get("SLASH_SDK_API_KEY")
        self.api_key = api_key

        if bearer_token is None:
            bearer_token = os.environ.get("SLASH_SDK_BEARER_TOKEN")
        self.bearer_token = bearer_token

        if username is None:
            username = os.environ.get("SLASH_SDK_USERNAME")
        self.username = username

        if password is None:
            password = os.environ.get("SLASH_SDK_PASSWORD")
        self.password = password

        if base_url is None:
            base_url = os.environ.get("SLASH_SDK_BASE_URL")
        if base_url is None:
            base_url = f"https://api.joinslash.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.legal_entity = legal_entity.AsyncLegalEntityResource(self)
        self.account = account.AsyncAccountResource(self)
        self.virtual_account = virtual_account.AsyncVirtualAccountResource(self)
        self.transaction = transaction.AsyncTransactionResource(self)
        self.transfer = transfer.AsyncTransferResource(self)
        self.card = card.AsyncCardResource(self)
        self.card_group = card_group.AsyncCardGroupResource(self)
        self.card_product = card_product.AsyncCardProductResource(self)
        self.slash_handle = slash_handle.AsyncSlashHandleResource(self)
        self.pay = pay.AsyncPayResource(self)
        self.webhook = webhook.AsyncWebhookResource(self)
        self.merchant = merchant.AsyncMerchantResource(self)
        self.merchant_category = merchant_category.AsyncMerchantCategoryResource(self)
        self.developer_account = developer_account.AsyncDeveloperAccountResource(self)
        self.developer_application = developer_application.AsyncDeveloperApplicationResource(self)
        self.well_known = well_known.AsyncWellKnownResource(self)
        self.oauth2 = oauth2.AsyncOauth2Resource(self)
        self.fdx = fdx.AsyncFdxResource(self)
        self.crypto = crypto.AsyncCryptoResource(self)
        self.with_raw_response = AsyncSlashSDKWithRawResponse(self)
        self.with_streaming_response = AsyncSlashSDKWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._api_key, **self._bearer, **self._developer_application}

    @property
    def _api_key(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"X-API-Key": api_key}

    @property
    def _bearer(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        if bearer_token is None:
            return {}
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    def _developer_application(self) -> dict[str, str]:
        if self.username is None:
            return {}
        if self.password is None:
            return {}
        credentials = f"{self.username}:{self.password}".encode("ascii")
        header = f"Basic {base64.b64encode(credentials).decode('ascii')}"
        return {"Authorization": header}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("X-API-Key"):
            return
        if isinstance(custom_headers.get("X-API-Key"), Omit):
            return

        if self.bearer_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        if self.username and self.password and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected one of api_key, bearer_token, username or password to be set. Or for one of the `X-API-Key`, `Authorization` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            bearer_token=bearer_token or self.bearer_token,
            username=username or self.username,
            password=password or self.password,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class SlashSDKWithRawResponse:
    def __init__(self, client: SlashSDK) -> None:
        self.legal_entity = legal_entity.LegalEntityResourceWithRawResponse(client.legal_entity)
        self.account = account.AccountResourceWithRawResponse(client.account)
        self.virtual_account = virtual_account.VirtualAccountResourceWithRawResponse(client.virtual_account)
        self.transaction = transaction.TransactionResourceWithRawResponse(client.transaction)
        self.transfer = transfer.TransferResourceWithRawResponse(client.transfer)
        self.card = card.CardResourceWithRawResponse(client.card)
        self.card_group = card_group.CardGroupResourceWithRawResponse(client.card_group)
        self.card_product = card_product.CardProductResourceWithRawResponse(client.card_product)
        self.slash_handle = slash_handle.SlashHandleResourceWithRawResponse(client.slash_handle)
        self.pay = pay.PayResourceWithRawResponse(client.pay)
        self.webhook = webhook.WebhookResourceWithRawResponse(client.webhook)
        self.merchant = merchant.MerchantResourceWithRawResponse(client.merchant)
        self.merchant_category = merchant_category.MerchantCategoryResourceWithRawResponse(client.merchant_category)
        self.developer_account = developer_account.DeveloperAccountResourceWithRawResponse(client.developer_account)
        self.developer_application = developer_application.DeveloperApplicationResourceWithRawResponse(
            client.developer_application
        )
        self.well_known = well_known.WellKnownResourceWithRawResponse(client.well_known)
        self.oauth2 = oauth2.Oauth2ResourceWithRawResponse(client.oauth2)
        self.fdx = fdx.FdxResourceWithRawResponse(client.fdx)
        self.crypto = crypto.CryptoResourceWithRawResponse(client.crypto)


class AsyncSlashSDKWithRawResponse:
    def __init__(self, client: AsyncSlashSDK) -> None:
        self.legal_entity = legal_entity.AsyncLegalEntityResourceWithRawResponse(client.legal_entity)
        self.account = account.AsyncAccountResourceWithRawResponse(client.account)
        self.virtual_account = virtual_account.AsyncVirtualAccountResourceWithRawResponse(client.virtual_account)
        self.transaction = transaction.AsyncTransactionResourceWithRawResponse(client.transaction)
        self.transfer = transfer.AsyncTransferResourceWithRawResponse(client.transfer)
        self.card = card.AsyncCardResourceWithRawResponse(client.card)
        self.card_group = card_group.AsyncCardGroupResourceWithRawResponse(client.card_group)
        self.card_product = card_product.AsyncCardProductResourceWithRawResponse(client.card_product)
        self.slash_handle = slash_handle.AsyncSlashHandleResourceWithRawResponse(client.slash_handle)
        self.pay = pay.AsyncPayResourceWithRawResponse(client.pay)
        self.webhook = webhook.AsyncWebhookResourceWithRawResponse(client.webhook)
        self.merchant = merchant.AsyncMerchantResourceWithRawResponse(client.merchant)
        self.merchant_category = merchant_category.AsyncMerchantCategoryResourceWithRawResponse(
            client.merchant_category
        )
        self.developer_account = developer_account.AsyncDeveloperAccountResourceWithRawResponse(
            client.developer_account
        )
        self.developer_application = developer_application.AsyncDeveloperApplicationResourceWithRawResponse(
            client.developer_application
        )
        self.well_known = well_known.AsyncWellKnownResourceWithRawResponse(client.well_known)
        self.oauth2 = oauth2.AsyncOauth2ResourceWithRawResponse(client.oauth2)
        self.fdx = fdx.AsyncFdxResourceWithRawResponse(client.fdx)
        self.crypto = crypto.AsyncCryptoResourceWithRawResponse(client.crypto)


class SlashSDKWithStreamedResponse:
    def __init__(self, client: SlashSDK) -> None:
        self.legal_entity = legal_entity.LegalEntityResourceWithStreamingResponse(client.legal_entity)
        self.account = account.AccountResourceWithStreamingResponse(client.account)
        self.virtual_account = virtual_account.VirtualAccountResourceWithStreamingResponse(client.virtual_account)
        self.transaction = transaction.TransactionResourceWithStreamingResponse(client.transaction)
        self.transfer = transfer.TransferResourceWithStreamingResponse(client.transfer)
        self.card = card.CardResourceWithStreamingResponse(client.card)
        self.card_group = card_group.CardGroupResourceWithStreamingResponse(client.card_group)
        self.card_product = card_product.CardProductResourceWithStreamingResponse(client.card_product)
        self.slash_handle = slash_handle.SlashHandleResourceWithStreamingResponse(client.slash_handle)
        self.pay = pay.PayResourceWithStreamingResponse(client.pay)
        self.webhook = webhook.WebhookResourceWithStreamingResponse(client.webhook)
        self.merchant = merchant.MerchantResourceWithStreamingResponse(client.merchant)
        self.merchant_category = merchant_category.MerchantCategoryResourceWithStreamingResponse(
            client.merchant_category
        )
        self.developer_account = developer_account.DeveloperAccountResourceWithStreamingResponse(
            client.developer_account
        )
        self.developer_application = developer_application.DeveloperApplicationResourceWithStreamingResponse(
            client.developer_application
        )
        self.well_known = well_known.WellKnownResourceWithStreamingResponse(client.well_known)
        self.oauth2 = oauth2.Oauth2ResourceWithStreamingResponse(client.oauth2)
        self.fdx = fdx.FdxResourceWithStreamingResponse(client.fdx)
        self.crypto = crypto.CryptoResourceWithStreamingResponse(client.crypto)


class AsyncSlashSDKWithStreamedResponse:
    def __init__(self, client: AsyncSlashSDK) -> None:
        self.legal_entity = legal_entity.AsyncLegalEntityResourceWithStreamingResponse(client.legal_entity)
        self.account = account.AsyncAccountResourceWithStreamingResponse(client.account)
        self.virtual_account = virtual_account.AsyncVirtualAccountResourceWithStreamingResponse(client.virtual_account)
        self.transaction = transaction.AsyncTransactionResourceWithStreamingResponse(client.transaction)
        self.transfer = transfer.AsyncTransferResourceWithStreamingResponse(client.transfer)
        self.card = card.AsyncCardResourceWithStreamingResponse(client.card)
        self.card_group = card_group.AsyncCardGroupResourceWithStreamingResponse(client.card_group)
        self.card_product = card_product.AsyncCardProductResourceWithStreamingResponse(client.card_product)
        self.slash_handle = slash_handle.AsyncSlashHandleResourceWithStreamingResponse(client.slash_handle)
        self.pay = pay.AsyncPayResourceWithStreamingResponse(client.pay)
        self.webhook = webhook.AsyncWebhookResourceWithStreamingResponse(client.webhook)
        self.merchant = merchant.AsyncMerchantResourceWithStreamingResponse(client.merchant)
        self.merchant_category = merchant_category.AsyncMerchantCategoryResourceWithStreamingResponse(
            client.merchant_category
        )
        self.developer_account = developer_account.AsyncDeveloperAccountResourceWithStreamingResponse(
            client.developer_account
        )
        self.developer_application = developer_application.AsyncDeveloperApplicationResourceWithStreamingResponse(
            client.developer_application
        )
        self.well_known = well_known.AsyncWellKnownResourceWithStreamingResponse(client.well_known)
        self.oauth2 = oauth2.AsyncOauth2ResourceWithStreamingResponse(client.oauth2)
        self.fdx = fdx.AsyncFdxResourceWithStreamingResponse(client.fdx)
        self.crypto = crypto.AsyncCryptoResourceWithStreamingResponse(client.crypto)


Client = SlashSDK

AsyncClient = AsyncSlashSDK
