import logging
from typing import Any
from yarl import URL
from giclient.manager import AsyncClientManager


class AsyncGetUpdateDeleteMixin:
    """ This class is a mixin class that contains the methods `get`, `update` and `delete` for the async client classes. """

    _logger_name: str = "greeninvoice.async_get_update_delete_mixin"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(self, manager: AsyncClientManager, endpoint: str="", *args, **kwargs) -> None:
        self.manager = manager
        self.url = URL(manager.base_url).joinpath(endpoint)

    async def get(
        self,
        id: str="") -> dict[str, Any]:
        """ Get a resource.

        Parameters
        ----------
        endpoint : str
            The id of the resource to get.
            Added directly to the base URL.

        Returns
        -------
        dict[str, Any]
            The resource.
        """
        response = await self.manager.client.get(url=str(self.url.joinpath(id)))
        return response.json()

    async def update(
        self,
        id: str="",
        **kwargs: Any) -> dict[str, Any]:
        """ Update a resource.

        Parameters
        ----------
        id : str
            The id of the resource to update.
            Added directly to the base URL.
        kwargs : Any
            The data to update.
            Fields should be written according to the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference>`_.

        Returns
        -------
        dict[str, Any]
            The updated resource.
        """
        response = await self.manager.client.put(url=str(self.url.joinpath(id)), json=kwargs)
        return response.json()

    async def delete(
        self,
        id: str="") -> dict[str, Any]:
        """ Delete a resource.

        Parameters
        ----------
        id : str
            The id of the resource to delete.
            Added directly to the base URL.

        Returns
        -------
        dict[str, Any]
            The deleted resource.
        """
        response = await self.manager.client.delete(url=str(self.url.joinpath(id)))
        return response.json()