from abc import abstractmethod
from collections.abc import Awaitable, Callable
from types import TracebackType
from typing import Any, Protocol

from pydantic import BaseModel

from tfy_assistant_framework.assistant._types import IncomingMessage, UpdateToUser


class AssistantInput(Protocol):
    _incoming_message_handler: Callable[[IncomingMessage], Awaitable[None]] | None

    @property
    def incoming_message_handler(self) -> Callable[[IncomingMessage], Awaitable[None]]:
        assert self._incoming_message_handler is not None
        return self._incoming_message_handler

    async def __aenter__(self) -> "AssistantInput": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...


class AssistantUpdateSink(Protocol):
    @abstractmethod
    async def send_update(self, update: UpdateToUser[Any, Any]) -> None: ...

    @abstractmethod
    def init_streaming_update(
        self, parent_update: UpdateToUser[Any, Any], title: str
    ) -> UpdateToUser[Any, Any]: ...

    @abstractmethod
    async def send_streaming_update(
        self, update: BaseModel, parent_update: UpdateToUser[Any, Any]
    ) -> None: ...

    async def get_sink_config(self) -> dict[Any, Any] | None:
        return None
