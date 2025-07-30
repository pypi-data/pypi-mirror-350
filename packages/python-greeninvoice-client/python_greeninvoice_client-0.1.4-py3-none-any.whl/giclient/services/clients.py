import logging
from typing import Any

from giclient.manager import AsyncClientManager
from giclient.services.shared.search import AsyncSearchMixin
from giclient.services.shared.get_update_delete import AsyncGetUpdateDeleteMixin


class AsyncClientsClient(AsyncSearchMixin, AsyncGetUpdateDeleteMixin):
    """ AsyncClientsClient is a class that implements the `/clients` endpoint of the GreenInvoice API. """

    _logger_name: str = "greeninvoice.async_clients_client"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(
        self,
        manager: AsyncClientManager) -> None:
        super(AsyncClientsClient, self).__init__(manager=manager, endpoint="clients")
        self.manager = manager
        self.url = self.manager.base_url.joinpath("clients")

    async def add(
        self,
        **kwargs: Any) -> dict[str, Any]:
        """ Add a new client.

        Parameters
        ----------
        kwargs : Any
            The data of the client to add.

        Returns
        -------
        dict[str, Any]
            The added client.
        """
        response = await self.manager.client.post(
            url=str(self.url),
            json=kwargs)
        return response.json()

    async def associate(
        self,
        client_id: str,
        document_ids: list[str]) -> int:
        """ Associate existing documents to a client.

        Parameters
        ----------
        client_id : str
            The ID of the client to associate.
        document_ids : list[str]
            The IDs of the documents to associate.

        Returns
        -------
        int
            The status code of the response.
        """
        response = await self.manager.client.post(
            url=str(self.url.joinpath(str(client_id), "assoc")),
            json={"ids": document_ids})
        return response.status_code

    async def merge(
        self,
        client_id: str,
        merge_with: str) -> int:
        """ Merge a client with another client.

        Parameters
        ----------
        client_id : str
            The ID of the client to merge.
        merge_with : str
            The ID of the client to merge with.

        Returns
        -------
        int
            The status code of the response.

        Notes
        -----
            In-order to merge clients, one of them must be inactive.
            Once merged - the inactive client will be deleted and all his documents will be added to the merged client.
        """
        response = await self.manager.client.post(
            url=str(self.url.joinpath(str(client_id), "merge")),
            json={"mergeId": merge_with})
        return response.status_code

    async def balance(
        self,
        client_id: str,
        new_balance: float) -> int:
        """
        Update the balance of a client.

        This endpoint will recalculate the final payment amount of a client by the given requested balance.

        To reset a client's balance - insert 0 as value.

        Parameters
        ----------
        client_id : str
            The ID of the client to add the payment to.
        new_balance : float
            The amount of the payment.

        Returns
        -------
        int
            The status code of the response.
        """
        response = await self.manager.client.post(
            url=str(self.url.joinpath(str(client_id), "balance")),
            json={"balance": new_balance})
        return response.status_code

# ==================================================================================================
#                                      Search-Related Methods
# ==================================================================================================
    async def search(
        self,
        get_all: bool=False,
        raw: bool=False,
        **search_fields: Any
        ) -> dict[str, Any]| list[dict[str, Any]]:
        """
        Search clients.

        Parameters
        ----------
        get_all : bool
            Whether to get all the clients.
            Default is False, which means only the page specified in the kwargs will be returned.
            If True, all the responses will be returned as a list of json dicts.
        raw : bool
            Whether to return the raw responses (contains additional serverside aggregations and results metadata) or to return a list of the search results.
        **search_fields : Any
            The search fields.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/clients/search-clients/search-clients>`_
            for more information.

        Returns
        -------
        dict[str, Any] | list[dict[str, Any]]
            Contains the search results.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/clients/search-clients/search-clients>`_
            for more information on each result's structure.
        """
        if not get_all:
            return await self._search(endpoint="clients", search_fields=search_fields, raw=raw, add_linked_ids=False)
        return await self._get_all(endpoint="clients", search_fields=search_fields, raw=raw, add_linked_ids=False)
