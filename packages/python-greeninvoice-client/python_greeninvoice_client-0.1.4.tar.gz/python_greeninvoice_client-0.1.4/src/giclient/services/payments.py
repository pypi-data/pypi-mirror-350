import logging
import asyncio
import httpx
from yarl import URL
from typing import Any

from giclient.manager import AsyncClientManager
from giclient.services.shared.search import AsyncSearchMixin


class AsyncPaymentsClient(AsyncSearchMixin):
    """
    AsyncPaymentsClient is a class that implements the `/payments` endpoint of the GreenInvoice API.

    The `/payments` endpoint provides interaction with Morning's online invoice payments system.
    It exposes the the ability to get a payment form.
    This form can be used in an IFrame in your website to provide payment request abilities for invoices within websites.
    After the payment was made - the system will automatically generate a document for you.

    Notes
    -----
    - Access to this endpoint is given to accounts that have purchased Cardcom clearing plugin and on the E-COMMERCE terminal type or the Isracard clearing plugin.
    - If you do not require the automatic creation of a document in our system - there is no need to use our payment system on your website,
    just use your favorite clearing company API directly.
    """

    def __init__(
        self,
        manager: AsyncClientManager) -> None:
        super(AsyncPaymentsClient, self).__init__(manager=manager, endpoint="payments")
        self.manager = manager
        self.url = self.manager.base_url.joinpath("payments")

    async def form(
        self,
        **payment_document_fields: Any) -> dict[str, str]:
        """
        Get a payment form url to embed in an iframe.

        Parameters
        ----------
        payment_document_fields : Any
            The fields of the payment document that will be created once the payment is made.

        Returns
        -------
        dict[str, str]
            The payment form url, along with an errorCode to indicate if the request was successful (errorCode=0 means OK).
        """
        response = await self.manager.client.post(
            url=str(self.url.joinpath("form")),
            json=payment_document_fields)
        return response.json()

    # ==================================================================================================
    #                                  Credit-Card-Token-Related Methods
    # ==================================================================================================
    # async def search(
    #     self,
    #     get_all: bool=False,
    #     **kwargs: Any) -> dict[str, Any] | list[dict[str, Any]]:
    #     """ Search saved credit card tokens.

    #     Parameters
    #     ----------
    #     get_all : bool
    #         Whether to get all the credit card tokens.
    #         Default is False, which means only the page specified in the kwargs will be returned.
    #         If True, all the responses will be returned as a list of json dicts.
    #     kwargs : Any
    #         The search parameters.

    #     Returns
    #     -------
    #     dict[str, Any] | list[dict[str, Any]]
    #         The search results.
    #     """
    #     endpoint = str(URL("payments").joinpath("tokens"))

    #     if not get_all:
    #         return await self._search(endpoint=endpoint, search_fields=kwargs, add_linked_ids=False)
    #     return await self._get_all(endpoint=endpoint, search_fields=kwargs, add_linked_ids=False)

    async def charge(
        self,
        token_id: str) -> dict[str, Any]:
        """
        Charge a credit card token.

        Parameters
        ----------
        token_id : str
            The ID of the credit card token to charge.

        Returns
        -------
        dict[str, Any]
            Document created data is returned.
        """
        response = await self.manager.client.post(
            url=str(self.url.joinpath("tokens", token_id, "charge")))
        return response.json()