import httpx

from tfy_assistant_framework._logger import logger

async_http_client = httpx.AsyncClient()

REQUEST_TIMEOUT = 30


def log_and_raise_for_status(response: httpx.Response) -> None:
    """Log and raise an exception if the response status code is non-2xx."""
    if not response.is_success:
        logger.warning(
            "Request to %s %s failed with status code %d. Response body: %s.",
            response.request.method,
            response.request.url,
            response.status_code,
            response.text,
        )
    response.raise_for_status()
