import logging
from yarl import URL

from typing import Literal, TypeVar
from types import TracebackType

from giclient.manager import AsyncClientManager
from giclient.services.account import AsyncAccountClient
from giclient.services.businesses import AsyncBusinessesClient
from giclient.services.clients import AsyncClientsClient
from giclient.services.suppliers import AsyncSuppliersClient
from giclient.services.items import AsyncItemsClient
from giclient.services.documents import AsyncDocumentsClient
from giclient.services.expenses import AsyncExpensesClient
from giclient.services.accounting import AsyncAccountingClient
from giclient.services.payments import AsyncPaymentsClient


API_BASE_URL = "https://api.greeninvoice.co.il/api/v1"

TOOLS_BASE_URL = "https://cache.greeninvoice.co.il"


T = TypeVar("T", bound="AsyncClientAPI")


class AsyncClientAPI:
    """ AsyncClientAPI is a class that implements the GreenInvoice API client. """

    _logger_name: str = "greeninvoice.async_client_api"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: URL | Literal["api", "tools"] = "api",
        max_rate: int=3,
        time_period: int=1,
        retries: int=0
    ) -> None:
        """
        A constructor method for AsyncClientAPI class. It initializes the class with the given parameters.

        Parameters
        ----------
        api_key : str
            The API key.
        api_secret : str
            The API secret.
        base_url : yarl.URL | str
            The base URL of the GreenInvoice API (might have a v2 release in the future).
        max_rate : int
            The maximum number of requests allowed in 1 time_period.
        time_period : int
            The time period, in seconds.
        retries : int
            The number of retries allowed for a request.
        """

        # Set the client:
        self.manager = AsyncClientManager(
            api_key=str(api_key),
            api_secret=str(api_secret),
            base_url=URL(API_BASE_URL) if base_url == "api" else URL(TOOLS_BASE_URL),
            max_rate=max_rate,
            time_period=time_period,
            retries=retries)

        self._account = None
        self._businesses = None
        self._clients = None
        self._suppliers = None
        self._items = None
        self._documents = None
        self._expenses = None
        self._accounting = None
        self._payments = None


    # ==========================================================================================
    #                                   Context Manager Methods
    # ==========================================================================================
    async def __aenter__(self: T) -> T:
        self._logger.debug(msg="Entering the context manager.")
        await self.manager.client.__aenter__()
        return self

    async def __aexit__(self,
                exc_type: type[BaseException] | None = None,
                exc_value: BaseException | None = None,
                traceback: TracebackType | None = None) -> None:
        self._logger.debug(msg=f"Exiting the context manager. Exception: {str(exc_type)} - {str(exc_value)} - {str(traceback)}")
        await self.manager.client.__aexit__(exc_type, exc_value, traceback)

    async def aclose(self) -> None:
        self._logger.debug(msg="Closing the client.")
        await self.manager.client.aclose()


    # ==========================================================================================
    #                                   API Properties
    # ==========================================================================================
    @property
    def account(self) -> AsyncAccountClient:
        """ Get the account client. """
        if self._account is None:
            self._account = AsyncAccountClient(manager=self.manager)
        return self._account

    @property
    def businesses(self) -> AsyncBusinessesClient:
        """ Get the businesses client. """
        if self._businesses is None:
            self._businesses = AsyncBusinessesClient(manager=self.manager)
        return self._businesses

    @property
    def clients(self) -> AsyncClientsClient:
        """ Get the clients client. """
        if self._clients is None:
            self._clients = AsyncClientsClient(manager=self.manager)
        return self._clients

    @property
    def suppliers(self) -> AsyncSuppliersClient:
        """ Get the suppliers client. """
        if self._suppliers is None:
            self._suppliers = AsyncSuppliersClient(manager=self.manager)
        return self._suppliers

    @property
    def items(self) -> AsyncItemsClient:
        """ Get the items client. """
        if self._items is None:
            self._items = AsyncItemsClient(manager=self.manager)
        return self._items

    @property
    def documents(self) -> AsyncDocumentsClient:
        """ Get the documents client. """
        if self._documents is None:
            self._documents = AsyncDocumentsClient(manager=self.manager)
        return self._documents

    @property
    def expenses(self) -> AsyncExpensesClient:
        """ Get the expenses client. """
        if self._expenses is None:
            self._expenses = AsyncExpensesClient(manager=self.manager)
        return self._expenses

    @property
    def accounting(self) -> AsyncAccountingClient:
        """ Get the accounting client. """
        if self._accounting is None:
            self._accounting = AsyncAccountingClient(manager=self.manager)
        return self._accounting

    @property
    def payments(self) -> AsyncPaymentsClient:
        """ Get the payments client. """
        if self._payments is None:
            self._payments = AsyncPaymentsClient(manager=self.manager)
        return self._payments
