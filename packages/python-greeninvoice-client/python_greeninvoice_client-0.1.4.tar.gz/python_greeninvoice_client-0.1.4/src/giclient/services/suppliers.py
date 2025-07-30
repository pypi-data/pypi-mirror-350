import logging
from typing import Any

from giclient.manager import AsyncClientManager
from giclient.services.shared.search import AsyncSearchMixin
from giclient.services.shared.get_update_delete import AsyncGetUpdateDeleteMixin


class AsyncSuppliersClient(AsyncSearchMixin, AsyncGetUpdateDeleteMixin):
    """ AsyncSuppliersClient is a class that implements the `/suppliers` endpoint of the GreenInvoice API. """

    _logger_name: str = "greeninvoice.async_suppliers_client"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(
        self,
        manager: AsyncClientManager) -> None:
        super(AsyncSuppliersClient, self).__init__(manager=manager, endpoint="suppliers")
        self.manager = manager
        self.url = self.manager.base_url.joinpath("suppliers")

    async def add(
        self,
        **kwargs: Any) -> dict[str, Any]:
        """ Add a new supplier.

        Parameters
        ----------
        kwargs : Any
            The data of the supplier to add.

        Returns
        -------
        dict[str, Any]
            The added supplier.
        """
        response = await self.manager.client.post(
            url=str(self.url),
            json=kwargs)
        return response.json()

    async def merge(
        self,
        supplier_id: str,
        merge_with: str) -> int:
        """ Merge a supplier with another supplier.

        Parameters
        ----------
        supplier_id : str
            The ID of the supplier to merge.
        merge_with : str
            The ID of the supplier to merge with.

        Returns
        -------
        int
            The status code of the response.

        Notes
        -----
            In-order to merge suppliers, one of them must be inactive.
            Once merged - the inactive supplier will be deleted and all his documents will be added to the merged supplier.
        """
        response = await self.manager.client.post(
            url=str(self.url.joinpath(str(supplier_id), "merge")),
            json={"mergeId": merge_with})
        return response.status_code

# ==================================================================================================
#                                      Search-Related Methods
# ==================================================================================================
    # async def search(
    #     self,
    #     get_all: bool=False,
    #     **search_fields: Any) -> dict[str, Any] | list[dict[str, Any]]:
    #     """ Search for suppliers.

    #     Parameters
    #     ----------
    #     get_all : bool
    #         Whether to get all the suppliers.
    #         Default is False, which means only the page specified in the `search_fields` will be returned.
    #         If True, all the responses will be returned as a list of json dicts.
    #     search_fields : Any
    #         The search fields.

    #     Returns
    #     -------
    #     dict[str, Any] | list[dict[str, Any]]
    #         The search results.
    #     """
    #     if not get_all:
    #         return await self._search(endpoint="suppliers", search_fields=search_fields, add_linked_ids=False)
    #     return await self._get_all(endpoint="suppliers", search_fields=search_fields, add_linked_ids=False)
