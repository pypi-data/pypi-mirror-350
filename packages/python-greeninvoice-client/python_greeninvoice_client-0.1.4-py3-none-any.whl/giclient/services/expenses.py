import logging
from typing import Any
from yarl import URL

from giclient.manager import AsyncClientManager
from giclient.services.shared.search import AsyncSearchMixin
from giclient.services.shared.get_update_delete import AsyncGetUpdateDeleteMixin


class AsyncExpensesClient(AsyncSearchMixin, AsyncGetUpdateDeleteMixin):
    """ AsyncExpensesClient is a class that implements the `/expenses` endpoint of the GreenInvoice API. """

    _logger_name: str = "greeninvoice.async_expenses_client"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(
        self,
        manager: AsyncClientManager) -> None:
        super(AsyncExpensesClient, self).__init__(manager=manager, endpoint="expenses")
        self.manager = manager
        self.url = self.manager.base_url.joinpath("expenses")
        self._statuses_en = None
        self._statuses_he = None

    async def add(
        self,
        **kwargs: Any) -> dict[str, Any]:
        """ Add a new expense.

        Parameters
        ----------
        kwargs : Any
            The data of the expense to add.

        Returns
        -------
        dict[str, Any]
            The added expense.
        """
        response = await self.manager.client.post(
            url=str(self.url),
            json=kwargs)
        return response.json()

    async def _get_with_action(
        self,
        expense_id: str,
        action: str
        ) -> dict:
        """
        Get an expense by ID with a specific action.

        Parameters
        ----------
        expense_id : str
            The expense ID.
        action : str
            The action to perform.

        Returns
        -------
        dict
            Contains the expense data.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/expenses/interacting-with-existing-expenses/get-expense>`_
            for more information.
        """
        response = await self.manager.client.get(
            url=str(self.url.joinpath(expense_id, action))
        )
        return response.json()

    async def open(
        self,
        expense_id: str
        ) -> dict:
        """
        Open an expense.

        Parameters
        ----------
        expense_id : str
            The expense ID.

        Returns
        -------
        dict
            Contains the expense data.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/expenses/open-expense/open-expense>`_
            for more information.
        """
        return await self._get_with_action(expense_id, "open")

    async def close(
        self,
        expense_id: str
        ) -> dict:
        """
        Close a expense.

        Parameters
        ----------
        expense_id : str
            The expense ID.

        Returns
        -------
        dict
            Contains the expense data.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/expenses/close-expense/close-expense>`_
            for more information.
        """
        return await self._get_with_action(expense_id, "close")

# ==================================================================================================
#                                      Search-Related Methods
# ==================================================================================================
    # async def search(
    #     self,
    #     get_all: bool=False,
    #     raw: bool=False,
    #     **search_fields: Any) -> dict[str, Any] | list[dict[str, Any]]:
    #     """ Search for expenses.

    #     Parameters
    #     ----------
    #     get_all : bool
    #         Whether to get all the expenses.
    #         Default is False, which means only the page specified in the kwargs will be returned.
    #         If True, all the responses will be returned as a list of json dicts.
    #     raw : bool
    #         Whether to return the raw responses (contains additional serverside aggregations and results metadata) or to return a list of the search results.
    #     search_fields : Any
    #         The search fields.
    #         See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/expenses/search-expenses/search-expenses>`_
    #         for more information.

    #     Returns
    #     -------
    #     dict[str, Any] | list[dict[str, Any]]
    #         The search results.
    #     """
    #     if not get_all:
    #         return await self._search(endpoint="expenses", search_fields=search_fields, raw=raw, add_linked_ids=False)
    #     return await self._get_all(endpoint="expenses", search_fields=search_fields, raw=raw, add_linked_ids=False)

    async def search_drafts(
        self,
        get_all: bool=False,
        raw: bool=False,
        **search_fields: Any
        ) -> dict| list[dict]:
        """
        Search all generated expense drafts (with possibility to filters).

        Parameters
        ----------
        get_all : bool
            Whether to get all the drafts. by default False,
            which means only the page specified in the kwargs will be returned.
            If True, all the responses will be returned as a list of json dicts.
        raw : bool
            Whether to return the raw responses (contains additional serverside aggregations and results metadata) or to return a list of the search results.
        **kwargs : Any
            The search fields.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/expenses/code-example/search-expense-drafts>`_
            for more information.

        Returns
        -------
        dict | list[dict]
            Contains the search results.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/expenses/code-example/search-expense-drafts>`_
            for more information on each result's structure.
        """
        if not get_all:
            return await self._search(endpoint=str(URL("expenses").joinpath("drafts")), search_fields=search_fields, raw=raw, add_linked_ids=False)
        return await self._get_all(endpoint=str(URL("expenses").joinpath("drafts")), search_fields=search_fields, raw=raw, add_linked_ids=False)

    # ==================================================================================================
    #                                          Statuses Property
    # ==================================================================================================
    def _get_statuses(self, lang: str) -> dict:
        response = self.manager.client.get(
            url=self.url.joinpath("statuses").update_query({"lang": lang}),
            auth=None)
        return response.json()

    @property
    async def statuses_en(self) -> dict:
        """ Get the expense statuses, in english. """
        if self._statuses_en is None:
            self._statuses_en = self._ge_statuses("en")
        return self._statuses_en

    @property
    async def statuses_he(self) -> dict:
        """ Get the expense statuses, in hebrew. """
        if self._statuses_he is None:
            self._statuses_he = self._ge_statuses("he")
        return self._statuses_he

    # ==================================================================================================
    #                                       Expense Drafts
    # ==================================================================================================
    # async def file_upload_url(self) -> str:
    #     """
    #     Get the URL to upload a file for an expense draft.

    #     Returns
    #     -------
    #     str
    #         The URL to upload a file for an expense draft.
    #     """
    #     response = await self.manager.client.get(
    #         url=self.url.joinpath("file")
    #     )
    #     return response.json()
