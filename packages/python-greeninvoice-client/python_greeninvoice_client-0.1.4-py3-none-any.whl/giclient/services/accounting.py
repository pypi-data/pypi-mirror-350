import logging
import asyncio
import httpx
from typing import Any

from giclient.manager import AsyncClientManager


class AsyncAccountingClient:
    """ AsyncAccountingClient is a class that implements the `/accounting` endpoint of the GreenInvoice API. """

    _logger_name: str = "greeninvoice.async_accounting_client"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(
        self,
        manager: AsyncClientManager) -> None:
        self.manager = manager
        self.url = self.manager.base_url.joinpath("accounting")

    async def classifications(
        self) -> list[dict[str, Any]]:
        """
        Shows the accounting classifications that were defined for this business.
        The classification can be specified in the accountingClassification field when adding or updating an expense.

        Returns
        -------
        list[dict[str, Any]]
            The classifications.
        """
        response = await self.manager.client.get(
            url=str(self.url.joinpath("classifications", "map")))
        return response.json()