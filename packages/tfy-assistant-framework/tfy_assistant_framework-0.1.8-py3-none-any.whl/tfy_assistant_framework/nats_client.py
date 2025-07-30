from collections import UserString
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from functools import partial
from typing import Any

import nats
from nats.aio.client import Client as NATS
from nats.js import JetStreamContext

from tfy_assistant_framework._http_client import (
    REQUEST_TIMEOUT,
    async_http_client,
    log_and_raise_for_status,
)
from tfy_assistant_framework._logger import logger
from tfy_assistant_framework.settings import settings

_PING_INTERVAL: int = 6
_MAX_OUTSTANDING_PINGS: int = 5
_MAX_RECONNECT_ATTEMPTS: int = -1
_CONNECTION_TIMEOUT: int = 10

JS_PUBLISH_TIMEOUT: int = 10
JS_TIMEOUT: int = 10


async def _get_nats_credentials() -> str:
    """
    Fetch the NATS user credentials from the TrueFoundry API.
    Returns:
        str: The NATS user credentials.
    """
    if any(
        [
            settings.tfy_base_url is None,
            settings.tfy_api_key is None,
            settings.tfy_assumed_user is None,
        ]
    ):
        raise ValueError("TFY credentials are not set, cannot fetch NATS credentials")
    url = f"{settings.tfy_base_url}/v1/x/llm-agent/nats-creds"
    headers = {
        "Authorization": f"Bearer {settings.tfy_api_key}",
    }
    response = await async_http_client.get(
        url, headers=headers, timeout=REQUEST_TIMEOUT
    )
    log_and_raise_for_status(response)
    data = response.json()
    creds = f"""
-----BEGIN NATS USER JWT-----
{data["jwt"]}
------END NATS USER JWT------
************************* IMPORTANT *************************
Private NKEYs are sensitive and should be treated as secrets.
-----BEGIN USER NKEY SEED-----
{data["seed"]}
------END USER NKEY SEED------
*************************************************************
"""
    return creds


async def _log_nats_connection_event(event: str) -> None:
    logger.warning("NATS connection event: %s", event)


async def _log_nats_error(ex: Exception) -> None:
    logger.error("NATS error", exc_info=ex)


# Define callback functions at module level
_DEFAULT_RECONNECTED_CB = partial(_log_nats_connection_event, event="reconnected")
_DEFAULT_DISCONNECTED_CB = partial(_log_nats_connection_event, event="disconnected")
_DEFAULT_CLOSED_CB = partial(_log_nats_connection_event, event="closed")


async def aget_nats_connect(
    servers: str | None = None,
    creds: str | None = None,
    connect_timeout: int = _CONNECTION_TIMEOUT,
    max_reconnect_attempts: int = _MAX_RECONNECT_ATTEMPTS,
    ping_interval: int = _PING_INTERVAL,
    max_outstanding_pings: int = _MAX_OUTSTANDING_PINGS,
    error_cb: Callable[[Exception], Awaitable[Any]] = _log_nats_error,
    reconnected_cb: Callable[[], Awaitable[Any]] = _DEFAULT_RECONNECTED_CB,
    disconnected_cb: Callable[[], Awaitable[Any]] = _DEFAULT_DISCONNECTED_CB,
    closed_cb: Callable[[], Awaitable[Any]] = _DEFAULT_CLOSED_CB,
) -> NATS:
    servers = servers or settings.nats_url
    assert servers is not None, "nats servers or settings.tfy_base_url is not set"
    if not creds:
        logger.info("Getting NATS credentials...")
        creds = await _get_nats_credentials()
    logger.info("Connecting to NATS...")
    nc = await nats.connect(
        servers=servers,
        user_credentials=UserString(creds),
        connect_timeout=connect_timeout,
        max_reconnect_attempts=max_reconnect_attempts,
        ping_interval=ping_interval,
        max_outstanding_pings=max_outstanding_pings,
        error_cb=error_cb,
        reconnected_cb=reconnected_cb,
        disconnected_cb=disconnected_cb,
        closed_cb=closed_cb,
    )
    logger.info("Connected to NATS")
    return nc


@asynccontextmanager
async def nats_connection() -> AsyncIterator[tuple[NATS, JetStreamContext]]:
    nc = await aget_nats_connect()
    js = JetStreamContext(conn=nc, timeout=JS_TIMEOUT)
    try:
        yield nc, js
    finally:
        await nc.drain()
        await nc.close()
