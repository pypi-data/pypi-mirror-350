import logging
import asyncio
import httpx
import base64
from typing import Any, Literal

from giclient.manager import AsyncClientManager

class AsyncBusinessesClient:
    """
    AsyncBusinessesClient is a class that implements the `/businesses` endpoint of the GreenInvoice API.

    Businesses are a main component of Green Invoice system.
    Each business contains it's own documents, clients, items & settings.
    """

    _logger_name: str = "greeninvoice.async_documents_client"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(
        self,
        manager: AsyncClientManager) -> None:
        self.manager = manager
        self.url = self.manager.base_url.joinpath("businesses")
        self._types_en = None
        self._types_he = None

    async def add(
        self,
        **business_fields: Any) -> dict[str, Any]:
        """
        Add a new business.

        Parameters
        ----------
        business_fields : Any
            The data of the business to add.

        Returns
        -------
        dict[str, Any]
            The added business.

        Notes
        -----
        - Creating a new business is limited.
        The limitation depends on the user subscription package as shown in the `paying section<https://www.greeninvoice.co.il/pricing>`_.
        The business limitation and the current account subscription can also be found in the `account` section of the Green Invoice application.
        """
        response = await self.manager.client.post(
            url=str(self.url),
            json=business_fields)
        return response.json()

    async def get_all(
        self) -> dict[str, Any]:
        """
        Get all the businesses for the current user.

        Returns
        -------
        dict[str, Any]
            The businesses.
        """
        response = await self.manager.client.get(url=str(self.url))
        return response.json()

    async def update(
        self,
        business_id: str,
        **business_fields: Any) -> dict[str, Any]:
        """
        Update a business.

        Parameters
        ----------
        business_id : str
            The ID of the business to update.
        business_fields : Any
            The data of the business to update.

        Returns
        -------
        dict[str, Any]
            The updated business.
        """
        response = await self.manager.client.put(
            url=str(self.url.joinpath(business_id)),
            json=business_fields)
        return response.json()

    async def current(
        self) -> dict[str, Any]:
        """
        Get the current business.

        Returns
        -------
        dict[str, Any]
            The current business.
        """
        response = await self.manager.client.get(url=str(self.url.joinpath("me")))
        return response.json()

    async def get(
        self,
        business_id: str) -> dict[str, Any]:
        """
        Get a business by ID.

        Parameters
        ----------
        business_id : str
            The ID of the business to get.

        Returns
        -------
        dict[str, Any]
            The business.
        """
        response = await self.manager.client.get(url=str(self.url.joinpath(business_id)))
        return response.json()

    # ==================================================================================================
    #                                      Business Related Files
    # ==================================================================================================
    async def upload(
        self,
        file_type: Literal["logo", "signature", "bookkeeping", "deduction"],
        file_path: str) -> dict[str, Any]:
        """
        Upload business logo, signature, bookkeeping document or deduction document.

        Parameters
        ----------
        file_path : str
            The path of the file to upload.

        Returns
        -------
        dict[str, Any]
            The file type along with a url to the uploaded file.

        Notes
        -----
        - The current allowed file types are: GIF, PNG, JPG, SVG, PDF.
        """
        # Open the file in binary mode:
        with open(file_path, "rb") as file:
            # Encode the file in base64:
            base64_file = base64.b64encode(file.read())
            # Send the file to the API:
            response = await self.manager.client.post(
                url=str(self.url.joinpath("file")),
                json={"type": file_type, "file": base64_file})
            return response.json()

    async def delete(
        self,
        file_type: Literal["logo", "signature", "bookkeeping", "deduction"]) -> dict[str, Any]:
        """
        Delete business logo, signature, bookkeeping document or deduction document.

        Parameters
        ----------
        file_type : Literal["logo", "signature", "bookkeeping", "deduction"]
            The type of the file to delete.

        Returns
        -------
        int
            The status code of the response.
        """
        response = await self.manager.client.request(
            method="DELETE",
            url=str(self.url.joinpath("file")),
            json={"type": file_type})
        return response.status_code

    # ==================================================================================================
    #                                      Handling Documents Numbering
    # ==================================================================================================
    # TODO: Use this method to get the last document date in the `documents` subclient.
    async def all_numberings(
        self) -> list[dict[str, Any]]:
        """
        Get all the document numberings.

        Returns
        -------
        list[dict[str, Any]]
            The document numbering for each document type. Each numbering includes the following fields:
            - type: int
                The document type.
            - number: int
                The first number in the numbering of the document type.
            - nextNumber: int
                The number of the next generated document that will be used.
            - lastDocumentDate: str
                The last time a document of this type was generated. The format is `YYYY-MM-DD`.
            - used: bool
                Was a document of this type generated or not.
            - active: bool
                Is this document type active or not.
        """
        response = await self.manager.client.get(url=str(self.url.joinpath("numbering")))
        return response.json()

    async def modify(
        self,
        type_to_numbering_mapping: Any) -> dict[str, Any]:
        """
        This endpoint allows you to modify a document type's initial numbering.
        Once modified and a first document of that type was generated - the document number will be locked for the specific type.

        Parameters
        ----------
        type_to_numbering_mapping : dict[int, int]
            A mapping between the document type and the new numbering.

        Returns
        -------
        int
            The status code of the response.
        """
        response = await self.manager.client.put(
            url=str(self.url.joinpath("numbering")),
            json=type_to_numbering_mapping)
        return response.status_code

    async def footer(self) -> dict[str, str]:
        """
        Get Business Documents Footer.

        Returns
        -------
        dict[str, str]
            The footer of the business documents. In the format of:
            - he: str
                The footer in Hebrew.
            - en: str
                The footer in English.
        """
        response = await self.manager.client.get(url=str(self.url.joinpath("footer")))
        return response.json()

    # ==================================================================================================
    #                                      Business Types
    # ==================================================================================================
    async def _get_types(
        self,
        lang: Literal["he", "en"] = "en") -> dict[str, str]:
        """
        Get the business types.

        Parameters
        ----------
        lang : str
            The language of the business types.
            Default is English.

        Returns
        -------
        dict[str, int | str]
            The business types, in the specified language. Each type includes the `id` (int) and the `name` (str).
        """
        response = await self.manager.client.get(
            url=self.url.joinpath("types").update_query({"lang": lang}),
            auth=None)
        return response.json()

    @property
    async def types_en(self) -> dict[str, str]:
        """
        Get the business types, in English.

        Returns
        -------
        dict[str, str]
            The business types, in English. Each type includes the `id` and the `name`.
        """
        if self._types_en is None:
            self._types_en = await self._get_types(lang="en")
        return self._types_en

    @property
    async def types_he(self) -> dict[str, str]:
        """
        Get the business types, in Hebrew.

        Returns
        -------
        dict[str, str]
            The business types, in Hebrew. Each type includes the `id` and the `name`.
        """
        if self._types_he is None:
            self._types_he = await self._get_types(lang="he")
        return self._types_he
