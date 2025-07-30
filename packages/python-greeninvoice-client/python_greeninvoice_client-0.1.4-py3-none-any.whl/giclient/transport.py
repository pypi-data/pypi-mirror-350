import logging
import httpx
from aiolimiter import AsyncLimiter


class RateLimitedAsyncTransport(httpx.AsyncHTTPTransport):
    """
    A rate limited async httpx TransportLayer.
    """

    _logger_name: str = "greeninvoice.async_greeninvoice_api_transport"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(
        self,
        max_rate: int | None = None,
        time_period: int | None = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
        )
        if max_rate is None or time_period is None:
            from contextlib import nullcontext
            self.rate_limiter = nullcontext()
        else:
            self.rate_limiter = AsyncLimiter(max_rate=max_rate, time_period=time_period)  # aiolimiter.AsyncLimiter(max_rate, time_period)

    async def handle_async_request(self, request):
        async with self.rate_limiter:  # this section is *at most* going to entered "max_rate" times in a "time_period" second period.
            self._logger.debug("handled request.")
            return await super().handle_async_request(request)
