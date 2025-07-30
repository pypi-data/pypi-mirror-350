import time
import logging
import httpx

from typing import Any, Coroutine, Callable
from functools import partial
from giclient.event_hooks import *


class JWTAuthenticaion(httpx.Auth):
    """ JWTAuthenticaion is a class that implements the httpx.Auth interface for JWT authentication. """
    requires_response_body: bool = True

    _logger_name: str = "greeninvoice.async_greeninvoice_api_authenticator"
    _logger = logging.getLogger(name=_logger_name)
    _request_hooks: list[Callable[[httpx.Request], Any]] = [
        # partial(log_request, logger_name=_logger_name)
    ]
    _response_hooks: list[Callable[[httpx.Response], Any]] = [
        # partial(log_response, logger_name=_logger_name),
        partial(response_raise_for_status, logger_name=_logger_name)
    ]

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: httpx.URL | str = "https://api.greeninvoice.co.il/api/v1",
        token_endpoint: str = "/account/token",
        client: httpx.AsyncClient | httpx.Client | None = None):
        """
        A constructor method for JWTAuthenticaion class. It initializes the class with the given parameters.

        The token is fetched from the token_url using the api_key and api_secret only when the first request is made or when the token has expired.

        Args:
            api_key (str): The API key.
            api_secret (str): The API secret.
            token_endpoint (str): The URL endpoint to fetch the JWT token from.
            client (httpx.AsyncClient): The HTTP client to use for fetching the token.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.token_endpoint = token_endpoint
        self._token = None
        self._token_expiration = 0
        self._client = self._set_client(client)

    def _set_client(self, client: httpx.AsyncClient | httpx.Client | None) -> httpx.AsyncClient | httpx.Client:
        if client is not None:
            return client
        # Set the authentication client:
        self.auth_timeout = httpx.Timeout(
            timeout=None
        )
        self.auth_limits = httpx.Limits(
            max_keepalive_connections=None,
            max_connections=None,
            keepalive_expiry=None
        )
        self.auth_transport = httpx.AsyncHTTPTransport(
            limits=self.auth_limits,
            retries=5
        )
        return httpx.AsyncClient(
            base_url=self.base_url,
            headers={'Content-Type': 'application/json'},
            timeout=self.auth_timeout,
            limits=self.auth_limits,
            transport=self.auth_transport,
            event_hooks={
                'request': self._request_hooks,
                'response': self._response_hooks
            }
        )

    def sync_auth_flow(self, request: httpx.Request):
        self._logger.debug(msg="sync_auth_flow")
        # First request:
        if self._token is None or time.time() >= self._token_expiration:
            self._sync_refresh_token()

        # Fetch the resource, if the token is expired or invalid
        # then the retry will fetch a new token and retry the request
        request.headers["Authorization"] = f"Bearer {self._token}"
        yield request

    def _sync_refresh_token(self):
        self._logger.debug("_sync_refresh_token")
        response = self._client.request(
            method="POST",
            url=self.token_endpoint,
            json={
            'id': self.api_key,
            'secret': self.api_secret,
            })
        try:
            token_data = response.json()
            self._token = token_data['token']
            self._token_expiration = token_data['expires']
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                message="Failed to get JWT token.",
                request=response.request,
                response=response
            ) from e

    async def async_auth_flow(self, request: httpx.Request):
        self._logger.debug(msg="async_auth_flow")
        # First request:
        if self._token is None or time.time() >= self._token_expiration:
            await self._async_refresh_token()

        # Fetch the resource, if the token is expired or invalid
        # then the retry will fetch a new token and retry the request
        request.headers["Authorization"] = f"Bearer {self._token}"
        yield request

    async def _async_refresh_token(self):
        self._logger.debug("_async_refresh_token")
        response = self._client.request(
            method="POST",
            url=self.token_endpoint,
            json={
                'id': self.api_key,
                'secret': self.api_secret
            }
        )
        if isinstance(response, Coroutine):
            response = await response
        try:
            token_data = response.json()
            self._token = token_data['token']
            self._token_expiration = token_data['expires']
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                message="Failed to get JWT token.",
                request=response.request,
                response=response
            ) from e

    def reset_credentials(self, api_key: str, api_secret: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self._token = None
        self._token_expiration = 0
