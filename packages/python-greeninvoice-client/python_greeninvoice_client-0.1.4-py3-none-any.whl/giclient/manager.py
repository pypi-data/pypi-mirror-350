import logging
import httpx
from yarl import URL
from functools import partial

from giclient.event_hooks import *
from giclient.authentication import JWTAuthenticaion
from giclient.transport import RateLimitedAsyncTransport


type _AsyncClientManager = AsyncClientManager


class AsyncClientManager:
    """
    AsyncClientManager is a class that manages the httpx.AsyncClient instance.

    This class is used when implementing the endpoints of the Green Invoice API,
    and it exposes the httpx.AsyncClient instance through it's ``client`` property.
    It is not advisable to store the httpx.AsyncClient instance outside of this class, using e.g., ``client = manager.client``,
    as the rate limits will not be respected, and also if the client is closed, it will not be re-opened by the manager.
    By using the same instance of this class in all endpoint implementations,
    you can ensure that the rate limits are respected across all endpoints.
    """

    _logger_name: str = "greeninvoice.async_client_manager"
    _logger = logging.getLogger(name=_logger_name)
    _request_hooks: list[partial] = [
        partial(log_request, logger_name=_logger_name)
    ]
    _response_hooks: list[partial] = [
        # partial(log_response, logger_name=_logger_name),
        partial(response_raise_for_status, logger_name=_logger_name)
    ]

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: URL,
        max_rate: int=3,
        time_period: int=1,
        retries: int=0) -> None:

        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.max_rate = max_rate
        self.time_period = time_period
        self.retries = retries
        self.refresh_client(self.max_rate, self.time_period, self.retries)

    def refresh_client(
        self,
        max_rate: int=3,
        time_period: int=1,
        retries: int=0) -> _AsyncClientManager:
        """
        refresh_client recreates the client with the given parameters.

        This method is useful when the client is already created and you want to change the parameters,
        or if you already exited the context manager and want to re-enter it.

        Parameters
        ----------
        max_rate : int
            The maximum number of requests allowed in 1 time_period.
        time_period : int
            The time period, in seconds.
        retries : int
            The number of retries allowed for a request.

        Returns
        -------
        _AsyncClientManager
            The client manager with the refreshed client.
        """
        self._logger.debug(msg="Refreshing the client.")

        self.auth = JWTAuthenticaion(
            api_key=self.api_key,
            api_secret=self.api_secret,
            base_url=str(self.base_url),
            token_endpoint="/account/token"
        )
        self.client_timeout = httpx.Timeout(
            timeout=None
        )
        self.limits = httpx.Limits(
            max_keepalive_connections=None,
            max_connections=None,
            keepalive_expiry=60.0
        )
        self.transport = RateLimitedAsyncTransport(
            limits=self.limits,
            retries=retries,
            max_rate=max_rate,
            time_period=time_period
        )
        self._client = httpx.AsyncClient(
            base_url=str(self.base_url),
            auth=self.auth,
            headers={'Content-Type': 'application/json'},
            timeout=self.client_timeout,
            limits=self.limits,
            transport=self.transport,
            event_hooks={
                'request': self._request_hooks,
                'response': self._response_hooks
            }
        )
        return self

    @property
    def client(self) -> httpx.AsyncClient:
        """
        client returns the httpx.AsyncClient instance.

        If the client is closed, it will refresh the client with the given parameters.

        Returns
        -------
        httpx.AsyncClient
            The httpx.AsyncClient object.
        """
        if not hasattr(self, '_client') or self._client.is_closed:
            self.refresh_client(self.max_rate, self.time_period, self.retries)
        return self._client

    def reset_credentials(
        self,
        api_key: str,
        api_secret: str
    ) -> _AsyncClientManager:
        """
        reset_credentials resets the credentials of the client.

        Parameters
        ----------
        api_key : str
            The API key.
        api_secret : str
            The API secret.

        Returns
        -------
        _AsyncClientManager
            The client manager with the new credentials.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self._client.auth.reset_credentials(
            api_key=self.api_key,
            api_secret=self.api_secret
        )
        return self
