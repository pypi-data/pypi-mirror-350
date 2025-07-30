import logging
import asyncio
from typing import Any
from itertools import repeat, chain

from giclient.manager import AsyncClientManager


# Constants:
MAXIMUM_PAGE_SIZE: int = 500  # Inclusive


class AsyncSearchMixin:
    """ AsyncSearchMixin is a mixin class that adds search functionality to any async client class. """

    _logger_name: str = "greeninvoice.async_search_mixin"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(self, manager: AsyncClientManager, endpoint: str=None, *args, **kwargs) -> None:
        """ Initializes the AsyncSearchMixin class with the given parameters. """
        self.manager = manager
        self.endpoint = endpoint

    async def _add_linked_ids_to_response_results(
        self,
        response: dict,
        filter_fields: dict[str, list[Any]] | None=None
        ) -> dict:
        """
        _add_linked_ids_to_response_results is a helper method that adds the linked IDs to the results in the response.

        To improve the performance, this operation can be filtered to only add the linked IDs to the results
        whose fields' values are in the filter_fields allowed values dictionary.

        Parameters
        ----------
        response : dict
            The response from the search.
        filter_fields : dict[str, list[Any]]
            The fields to filter by. The keys are the field names, and the values are the allowed values for each field.
            For example:
            - If you want to add the linked IDs only to the results whose type is in [10, 20, 100], you would pass:
            - - filter_fields = {"type": [10, 20, 100]}
            - If you want to add the linked IDs only to the results whose status is 10, you would pass:
            - - filter_fields = {"status": [10]}
            - If you want to add the linked IDs to all the results in the response, pass a falsey value, like None, false, `{}` and so on.

        Returns
        -------
        dict
            The response with the linked IDs added to the `items` list.
        """

        # create helper function to add empty list to linked if the result doesn't satisfy filter_fields:
        async def _return_empty_list() -> list[str]:
            await asyncio.sleep(0) # pass control to the event loop to give other tasks higher priority
            return []

        # Create the async tasks:
        tasks = []
        # If filter_fields is falsey, add the linked IDs to all the results:
        if not filter_fields:
            for result in response["items"]:
                coro = self.linked(result["id"])
                tasks.append(asyncio.create_task(coro=coro))

        # If filter_fields is truthy, add the linked IDs only to the results that satisfy filter_fields:
        else:
            for result in response["items"]:
                # Check if the result satisfies filter_fields, and if so, add the linked IDs to it. else, add an empty list.
                valid_per_field = [
                    result[field] in allowed_values or (result[field] == allowed_values and allowed_values != [])
                    for field, allowed_values in filter_fields.items()
                ]
                if any(valid_per_field):
                    coro = self.linked(result["id"])
                else:
                    coro = _return_empty_list()
                tasks.append(asyncio.create_task(coro=coro))

        # Get the linked IDs for each result:
        linked_ids = await asyncio.gather(*tasks)

        # Add them to the response:
        for result, item_linked_ids in zip(response["items"], linked_ids):
            result["linked"] = item_linked_ids

        return response

    async def _search(
        self,
        endpoint: str,
        search_fields: dict,
        raw: bool=False,
        add_linked_ids: bool=False,
        filter_fields: dict[str, list[Any]] | None=None
        ) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Search a given endpoint's resources according to the specified search fields.

        Parameters
        ----------
        endpoint : str
            The endpoint to search in.
        search_fields : dict
            The search fields. Each endpoint's fields are slightly different.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference>`_
            for more information.
        raw : bool
            Whether to return the raw response (contains additional serverside aggregations and results metadata) or to return a list of the search results.
        add_linked_ids : bool
            If the endpoint supports the `/linked` route (e.g., the `/documents` endpoint), or simply implements a `self.linked()` method that returns a list of linked IDs,
            this argument specifies whether to add a list of linked result IDs to each result in the search results.
            Default is False.
        filter_fields : dict[str, list[Any]] | None
            The fields to filter by. The keys are the field names, and the values are the allowed values for each field.
            For example:
            - If you want to add the linked IDs only to the results whose type is in [10, 20, 100], you would pass:
            - - filter_fields = {"type": [10, 20, 100]}
            - If you want to add the linked IDs only to the results whose status is 10, you would pass:
            - - filter_fields = {"status": [10]}
            - If you want to add the linked IDs to all the results in the response, pass a falsey value, like None, false, `{}` and so on.

        Returns
        -------
        dict[str, Any] | list[dict[str, Any]]
            Contains the search results.
        """
        # Send the search query:
        response = await self.manager.client.post(
            url=str(self.manager.base_url.joinpath(endpoint, "search")),
            json=search_fields)

        # Parse the response:
        response_dict = response.json()

        # Add the linked IDs to the response:
        if add_linked_ids:
            if not hasattr(self, "linked"):
                raise AttributeError(f"Endpoint implementation for '{endpoint}' does not implement the 'self.linked()' method.")
            response_dict = await self._add_linked_ids_to_response_results(response_dict, filter_fields)

        # Return the raw response if requested:
        if raw:
            return response_dict

        # Return the search results:
        return response_dict["items"]

    def _create_search_task(
        self,
        page_number: int,
        page_size: int,
        endpoint: str,
        search_fields: dict,
        raw: bool,
        add_linked_ids: bool,
        filter_fields: dict[str, list[Any]] | None) -> asyncio.Task:

        # Set the page number and page size in the search fields:
        search_fields["page"] = page_number
        search_fields["pageSize"] = page_size

        # Create the async task:
        task = asyncio.create_task(
            coro=self._search(
                endpoint=endpoint,
                search_fields=search_fields,
                raw=raw,
                add_linked_ids=add_linked_ids,
                filter_fields=filter_fields)
        )

        # Return the task:
        return task

    async def _get_all(
        self,
        endpoint: int,
        search_fields: dict,
        raw: bool=False,
        add_linked_ids: bool=False,
        filter_fields: dict[str, list[Any]] | None=None
        ) -> list[dict[str, Any]]:
        """
        _get_all is a helper method that asynchronously gets all the results from a search as a list of responses, one for each page.

        Parameters
        ----------
        endpoint : int
            The endpoint to search in.
        search_fields : dict
            The search fields.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference>`_
            for more information.
        raw : bool
            Whether to return the raw responses for each page (contains additional serverside aggregations and results metadata) or to return a list of the search results.
        add_linked_ids : bool, optional
            Whether to add a list of linked IDs to each result in the search results. by default False
        filter_fields : dict[str, list[Any]] | None
            The fields to filter by. The keys are the field names, and the values are the allowed values for each field.
            For example:
            - If you want to add the linked IDs only to the results whose type is in [10, 20, 100], you would pass:
            - - filter_fields = {"type": [10, 20, 100]}
            - If you want to add the linked IDs only to the results whose status is 10, you would pass:
            - - filter_fields = {"status": [10]}
            - If you want to add the linked IDs to all the results in the response, pass a falsey value, like None, false, `{}` and so on.

        Returns
        -------
        list[dict[str, Any]]
            Contains the search results.
            If `raw` is set to True then each item in the list is a response that contains the search results for a specific page.
            Otherwise, each item in the list is a search result.
        """
        # Create a shallow copy of the search fields to avoid modifying the original:
        search_fields = search_fields.copy()

        # Get the first page:
        search_fields["page"] = 1
        search_fields["pageSize"] = MAXIMUM_PAGE_SIZE
        first_page = await self._search(
            endpoint=endpoint,
            search_fields=search_fields,
            raw=True,  # Always get the raw response for the first page, as it contains the total number of resources.
            add_linked_ids=add_linked_ids,
            filter_fields=filter_fields)

        # Get the total number of resources:
        total_resources = first_page["total"]

        # Calculate the total number of full pages (including the first page, and excluding the last page if it's not a full page)
        # and the size of the last page (if it's not a full page):
        total_full_pages, last_page_size = divmod(total_resources, MAXIMUM_PAGE_SIZE)

        if last_page_size:
            # If the last page is not a full page, add it to the total number of pages:
            total_pages = total_full_pages + 1

            # Create an iterator for the page sizes that skips the first page (because we already got it):
            page_sizes_iterator = chain(
                repeat(MAXIMUM_PAGE_SIZE, total_full_pages - 1),
                [last_page_size])
        else:
            # If the last page is a full page, the total number of pages is the same as the number of full pages:
            total_pages = total_full_pages

            # Create an iterator for the page sizes that skips the first page (because we already got it):
            page_sizes_iterator = repeat(MAXIMUM_PAGE_SIZE, total_pages - 1)

        # Create page numbers iterator that skips the first page (because we already got it):
        page_numbers_iterator = range(2, total_pages + 1)

        # Get the number of tasks:
        n_tasks = len(page_numbers_iterator)

        # Create the async tasks:
        tasks = list(
            map(self._create_search_task,
                page_numbers_iterator, # page numbers
                page_sizes_iterator,  # page sizes
                repeat(endpoint, n_tasks),  # endpoint
                [search_fields.copy() for _ in range(n_tasks)],  # search_fields (copied because of shared memory between tasks)
                repeat(raw, n_tasks),  # raw
                repeat(add_linked_ids, n_tasks),  # add_linked_ids
                repeat(filter_fields, n_tasks)  # filter_fields (doesn't need to be copied because it's not modified for each task)
            )
        )

        # Get the results for the rest of the pages:
        later_pages: list[dict[str, Any] | list[dict[str, Any]]] = await asyncio.gather(*tasks)

        # Combine the results:
        if not raw:
            # If raw is False, combine the results into a single list:
            resources = first_page["items"]
            for page_results in later_pages:
                resources.extend(page_results)
            return resources
        else:
            # If raw is True, return a list of the raw responses:
            return list(chain([first_page], later_pages))

    # ==================================================================================================
    #                                      Common Search Method
    # =================================================================================================
    async def search(
        self,
        get_all: bool=False,
        raw: bool=False,
        **search_fields: Any) -> dict[str, Any] | list[dict[str, Any]]:
        """ Search for resources in this endpoint.

        Parameters
        ----------
        get_all : bool
            Whether to get all the resources.
            Default is False, which means only the page specified in the `search_fields` will be returned.
            If True, all the results will be returned as a list of json dicts.
        raw : bool
            Whether to return the raw responses (contains additional serverside aggregations and results metadata) or to return a list of the search results.
        search_fields : Any
            The search fields.

        Returns
        -------
        dict[str, Any] | list[dict[str, Any]]
            The search results.
        """
        if not get_all:
            return await self._search(endpoint=self.endpoint, search_fields=search_fields, raw=raw, add_linked_ids=False)
        return await self._get_all(endpoint=self.endpoint, search_fields=search_fields, raw=raw, add_linked_ids=False)
