import logging
from yarl import URL
from typing import Any

from giclient.event_hooks import *
from giclient.manager import AsyncClientManager
from giclient.services.shared.search import AsyncSearchMixin


class AsyncDocumentsClient(AsyncSearchMixin):
    """
    AsyncDocumentsClient is a class that implements the `/documents` endpoint of the GreenInvoice API.

    The main component of the Green Invoice system is the documents, these documents can be of different types, such as but not only - order, invoice, receipt.
    Documents are business specific, and only the documents of the current used business are visible to you.
    """

    _logger_name: str = "greeninvoice.async_documents_client"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(
        self,
        manager: AsyncClientManager) -> None:
        super(AsyncDocumentsClient, self).__init__(manager=manager, endpoint="documents")
        self.manager = manager
        self.url = self.manager.base_url.joinpath("documents")
        self._types_en = None
        self._types_he = None
        self._statuses_en = None
        self._statuses_he = None

    async def add(
        self,
        **kwargs: Any
        ) -> dict:
        """
        Add a document to the current business.

        The document will be generated based on the default business & document settings, and by any overriding request attributes that we receive in this endpoint.

        Parameters
        ----------
        **kwargs : Any
            The document fields.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/add-document/add-document>`_
            for more information.

        Returns
        -------
        dict
            Contains:
            - id : str
                Document unique ID in the system
            - number : str
                Document serial number
            - signed : bool
                Marks if document was digitally signed
            - lang : Literal["he", "en"]
                The document language
            - url : dict
                Document URL (in origin, he and en)

        Notes
        -----
        - When declaring your vatType there's multiple different declarations. You can define the general vatType of the document, but - you can also define each income row vatType.
        - linkedDocumentIds allows you to state the related / relevant documents, e.g.: when creating a receipt, attach your original invoice document ID as one of the ids in the linkedDocumentIds - this in turn will automatically close the original invoice if needed.
        - linkedPaymentId allows you to define the paymentId that the document is going to be relevant to, this can be attached only to invoice documents (type 305).
        """
        response = await self.manager.client.post(
            url=str(self.url),
            json=kwargs
        )
        return response.json()

    async def preview(
        self,
        **kwargs: Any
        ) -> dict:
        """
        preview gets a Preview Document according to the given parameters.

        Parameters
        ----------
        **kwargs : Any
            The document fields.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/get-a-preview-document/get-a-preview-document>`_
            for more information.

        Returns
        -------
        dict
            Contains:
            - file : str
                The base64 encoded document file
        """
        response = await self.manager.client.post(
            url=str(self.url.joinpath("preview")),
            json=kwargs
        )
        return response.json()

    # ==================================================================================================
    #                                      Document ID Methods
    # ==================================================================================================
    async def _get_with_action(
        self,
        id: str,
        actions: list[str]
        ) -> dict:
        """
        Get a document by ID with a specific action.

        Parameters
        ----------
        id : str
            The document ID.
        actions : list[str]
            The actions to perform.

        Returns
        -------
        dict
            Contains the document data.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/interacting-with-existing-documents>`_
            for more information.
        """
        response = await self.manager.client.get(
            url=str(self.url.joinpath(id, *actions))
        )
        return response.json()

    async def _post_with_action(
        self,
        id: str,
        actions: list[str],
        kwargs: Any
        ) -> dict:
        """
        Post a document by ID with a specific action.

        Parameters
        ----------
        id : str
            The document ID.
        actions : list[str]
            The actions to perform.
        kwargs : Any
            The document fields.

        Returns
        -------
        int | dict
            The status code of the response, or the response body if it's not empty.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/>`_
            for more information.
        """
        response = await self.manager.client.post(
            url=str(self.url.joinpath(id, *actions)),
            json=kwargs
        )
        return response.json()

    async def get(
        self,
        id: str
        ) -> dict:
        """
        Get a document by ID.

        Parameters
        ----------
        id : str
            The document ID.

        Returns
        -------
        dict
            Contains the document data.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/interacting-with-existing-documents/get-document>`_
            for more information.
        """
        return await self._get_with_action(id, [])

    async def close(
        self,
        id: str
        ) -> dict:
        """
        Close a document.

        Parameters
        ----------
        id : str
            The document ID.

        Returns
        -------
        dict
            Contains the document data.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/close-document/close-document>`_
            for more information.
        """
        return await self._get_with_action(id, ["close"])

    async def open(
        self,
        id: str
        ) -> dict:
        """
        Open a document.

        Parameters
        ----------
        id : str
            The document ID.

        Returns
        -------
        dict
            Contains the document data.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/open-document/open-document>`_
            for more information.
        """
        return await self._get_with_action(id, ["open"])

    async def distribute(
        self,
        id: str,
        **document_fields: Any
        ) -> dict:
        """
        distribute sends an already generated document to a customer.

        Parameters
        ----------
        id : str
            The document ID.
        document_fields : Any
            The document fields.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/>`_
            for more information.

        Returns
        -------
        int
            The status code of the response.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/>`_
            for more information.
        """
        return await self._post_with_action(id=id, actions=["distribute"], kwargs=document_fields)

    async def distribution(
        self,
        id: str
        ) -> dict:
        """
        Get the document distribution.

        Parameters
        ----------
        id : str
            The document ID.

        Returns
        -------
        dict
            Contains the document distribution.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/get-document-distribution/get-document-distribution>`_
            for more information.
        """
        return await self._get_with_action(id, ["distribution"])

    async def linked(
        self,
        id: str
        ) -> list:
        """
        Get the linked documents of a document.

        Parameters
        ----------
        id : str
            The document ID.

        Returns
        -------
        list
            Contains the linked documents.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/get-linked-documents/get-linked-documents>`_
            for more information.
        """
        return await self._get_with_action(id, ["linked"])

    async def download_links(
        self,
        id: str
        ) -> dict:
        """
        Get the download links of a document.

        Parameters
        ----------
        id : str
            The document ID.

        Returns
        -------
        dict
            Contains the download links.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/get-document-download-links/get-document-download-links>`_
            for more information.
        """
        return await self._get_with_action(id, ["download", "links"])

    # ==================================================================================================
    #                                      Miscelanious Methods
    # ==================================================================================================
    async def info(
        self,
        document_type: int
        ) -> dict:
        """
        Get the document info.

        Parameters
        ----------
        document_type : int
            The document type.

        Returns
        -------
        dict
            Contains the document info.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/get-document-info/get-document-info>`_
            for more information.
        """
        response = await self.manager.client.get(
            url=str(self.url.joinpath("info").update_query({"type": document_type}))
        )
        return response.json()

    async def templates(
        self
        ) -> dict:
        """
        Retrieves information regarding the available templates and their corresponding colors / skins in the system.

        Returns
        -------
        dict
            Contains the document templates.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/get-document-templates/get-document-templates>`_
            for more information.
        """
        response = await self.manager.client.get(
            url=str(self.url.joinpath("templates"))
        )
        return response.json()

    # ==================================================================================================
    #                                      Types and Statuses Properties
    # ==================================================================================================
    async def _get_types_or_statuses(self, endpoint: str, lang: str) -> dict:
        response = await self.manager.client.get(
            url=str(self.url.joinpath(endpoint).update_query({"lang": lang})),
            auth=None)
        return response.json()

    @property
    async def types_en(self) -> dict:
        """ Retrieve information regarding the available document types that are open for the current business, in english. """
        if self._types_en is None:
            self._types_en = await self._get_types_or_statuses("types", "en")
        return self._types_en

    @property
    async def types_he(self) -> dict:
        """ Retrieve information regarding the available document types that are open for the current business, in hebrew. """
        if self._types_he is None:
            self._types_he = await self._get_types_or_statuses("types", "he")
        return self._types_he

    @property
    async def statuses_en(self) -> dict:
        """ Retrieve information regarding the available document statuses, in english. """
        if self._statuses_en is None:
            self._statuses_en = await self._get_types_or_statuses("statuses", "en")
        return self._statuses_en

    @property
    async def statuses_he(self) -> dict:
        """ Retrieve information regarding the available document statuses, in hebrew. """
        if self._statuses_he is None:
            self._statuses_he = await self._get_types_or_statuses("statuses", "he")
        return self._statuses_he

# ==================================================================================================
#                                      Search-Related Methods
# ==================================================================================================
    async def search(
        self,
        get_all: bool=False,
        raw: bool=False,
        add_linked_ids: bool=False,
        filter_fields: dict[str, list[Any]] | None=None,
        **search_fields: Any
        ) -> dict[str, Any]| list[dict[str, Any]]:
        """
        Search documents.

        Parameters
        ----------
        get_all : bool
            Whether to get all the documents.
            Default is False, which means only the page specified in the kwargs will be returned.
            If True, all the responses will be returned as a list of json dicts.
        raw : bool
            Whether to return the raw responses (contains additional serverside aggregations and results metadata) or to return a list of the search results.
        add_linked_ids : bool
            Whether to add a list of linked document IDs to each document in the search results. Default is False.
        filter_fields : dict[str, list[Any]] | None
            The fields to filter by. The keys are the field names, and the values are the allowed values for each field.
            For example:
            - If you want to add the linked IDs only to the results whose type is in [10, 20, 100], you would pass:
            - - filter_fields = {"type": [10, 20, 100]}
            - If you want to add the linked IDs only to the results whose status is 10, you would pass:
            - - filter_fields = {"status": [10]}
            - If you want to add the linked IDs to all the results in the response, pass a falsey value, like None, false, `{}` and so on.
        **search_fields : Any
            The search fields.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/search-documents/search-documents>`_
            for more information.

        Returns
        -------
        dict[str, Any] | list[dict[str, Any]]
            Contains the search results.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/search-documents/search-documents>`_
            for more information on each result's structure.
        """
        if not get_all:
            return await self._search(endpoint="documents", search_fields=search_fields, raw=raw, add_linked_ids=add_linked_ids, filter_fields=filter_fields)
        return await self._get_all(endpoint="documents", search_fields=search_fields, raw=raw, add_linked_ids=add_linked_ids, filter_fields=filter_fields)

    async def search_payments(
        self,
        get_all: bool=False,
        raw: bool=False,
        **search_fields: Any
        ) -> dict| list[dict]:
        """
        Search payments.

        Parameters
        ----------
        get_all : bool
            Whether to get all the payments. by default False,
            which means only the page specified in the `search_fields` will be returned.
            If True, all the responses will be returned as a list of json dicts.
        raw : bool
            Whether to return the raw responses (contains additional serverside aggregations and results metadata) or to return a list of the search results.
        **search_fields : Any
            The search fields.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/search-payments-in-documents/search-payments-in-documents>`_
            for more information.

        Returns
        -------
        dict | list[dict]
            Contains the search results.
            See the `Morning API Docs<https://www.greeninvoice.co.il/api-docs#/reference/documents/search-payments-in-documents/search-payments-in-documents>`_
            for more information on each result's structure.
        """
        endpoint = str(URL("documents").joinpath("payments"))

        if not get_all:
            return await self._search(endpoint=endpoint, search_fields=search_fields, raw=raw, add_linked_ids=False)
        return await self._get_all(endpoint=endpoint, search_fields=search_fields, raw=raw, add_linked_ids=False)
