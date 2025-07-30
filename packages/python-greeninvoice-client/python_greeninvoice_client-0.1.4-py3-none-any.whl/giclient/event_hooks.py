import logging
import httpx


# Event-Hooks:
# https://www.python-httpx.org/advanced/event-hooks/
## REQUEST:
async def log_request(request: httpx.Request, logger_name: str):
    logger = logging.getLogger(name=logger_name)
    logger.debug(msg=f"Request event hook: {request.method} {request.url} - Waiting for response")


## RESPONSE:
async def log_response(response: httpx.Response, logger_name: str):
    logger = logging.getLogger(name=logger_name)
    request: httpx.Request = response.request
    logger.debug(msg=f"Response event hook: {request.method} {str(request.url)} - Status {response.status_code}")


async def response_raise_for_status(response: httpx.Response, logger_name: str):
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        logger = logging.getLogger(name=logger_name)
        logger.error(msg=f"Response event hook (raised for status): {response.status_code} - {response.reason_phrase}. {response.request.url}, {response.request.headers}, {response.request.content}")
        raise e
