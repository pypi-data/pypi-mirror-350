import logging
from typing import Any

from giclient.manager import AsyncClientManager
from giclient.services.shared.search import AsyncSearchMixin
from giclient.services.shared.get_update_delete import AsyncGetUpdateDeleteMixin


class AsyncItemsClient(AsyncSearchMixin, AsyncGetUpdateDeleteMixin):
    """ AsyncItemsClient is a class that implements the `/items` endpoint of the GreenInvoice API. """

    _logger_name: str = "greeninvoice.async_items_client"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(
        self,
        manager: AsyncClientManager) -> None:
        super(AsyncItemsClient, self).__init__(manager=manager, endpoint="items")
        self.manager = manager
        self.url = self.manager.base_url.joinpath("items")

    async def add(
        self,
        **kwargs: Any) -> dict[str, Any]:
        """ Add a new item.

        Parameters
        ----------
        kwargs : Any
            The data of the item to add.

        Returns
        -------
        dict[str, Any]
            The added item.
        """
        response = await self.manager.client.post(
            url=str(self.url),
            json=kwargs)
        return response.json()

# ==================================================================================================
#                                      Search-Related Methods
# ==================================================================================================
    # async def search(
    #     self,
    #     get_all: bool=False,
    #     raw: bool=False,
    #     **search_fields: Any) -> dict[str, Any] | list[dict[str, Any]]:
    #     """ Search for items.

    #     Parameters
    #     ----------
    #     get_all : bool
    #         Whether to get all the items.
    #         Default is False, which means only the page specified in the kwargs will be returned.
    #         If True, all the responses will be returned as a list of json dicts.
    #     raw : bool
    #         Whether to return the raw responses (contains additional serverside aggregations and results metadata) or to return a list of the search results.
    #     search_fields : Any
    #         The search parameters.

    #     Returns
    #     -------
    #     dict[str, Any] | list[dict[str, Any]]
    #         The search results.
    #     """
    #     if not get_all:
    #         return await self._search(endpoint="items", search_fields=search_fields, raw=raw, add_linked_ids=False)
    #     return await self._get_all(endpoint="items", search_fields=search_fields, raw=raw, add_linked_ids=False)