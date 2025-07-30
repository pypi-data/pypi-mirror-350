import asyncio
import contextvars
from collections.abc import AsyncGenerator, Awaitable, Callable, Iterator
from contextlib import asynccontextmanager, contextmanager
from functools import partial
from typing import (
    Any,
    TypeVar,
)

import logfire
from fastapi import HTTPException
from pydantic import BaseModel

from tfy_assistant_framework._logger import logger
from tfy_assistant_framework.assistant._base_assistant_io import (
    AssistantUpdateSink,
)
from tfy_assistant_framework.assistant._console_assistant_io import (
    _ask_user_from_console,
    _fake_send_streaming_update_to_user,
    _fake_send_update_to_user,
)
from tfy_assistant_framework.assistant._types import (
    AssistantState,
    AssistantUpdateToUser,
    IncomingMessage,
    UpdateToUser,
    UserChatMessage,
    UserMessageTypes,
    UserUpdateToUser,
)
from tfy_assistant_framework.settings import settings

AssistantRequestBody = TypeVar(
    "AssistantRequestBody", bound=BaseModel | None, contravariant=True
)


_send_update_var: contextvars.ContextVar[
    Callable[[UpdateToUser[Any, Any]], Awaitable[None]] | None
] = contextvars.ContextVar("_send_update_var", default=None)


def _set_send_update_var(
    f: Callable[[UpdateToUser[Any, Any]], Awaitable[None]],
) -> None:
    assert _send_update_var.get() is None
    _send_update_var.set(f)


_active_assistant_runner: contextvars.ContextVar["AssistantRunner | None"] = (
    contextvars.ContextVar("_active_assistant_runner", default=None)
)


def _set_active_assistant_runner(
    f: "AssistantRunner",
) -> None:
    assert _active_assistant_runner.get() is None
    _active_assistant_runner.set(f)
    _set_send_update_var(f.send_update)


_streaming_update_ongoing: contextvars.ContextVar[bool | None] = contextvars.ContextVar(
    "_streaming_update_ongoing", default=None
)

_collected_updates_var: contextvars.ContextVar[list[BaseModel] | None] = (
    contextvars.ContextVar("_collected_updates_var", default=None)
)


def _unset_assistant_context_vars() -> None:
    """unset all context variables to their default values."""
    _active_assistant_runner.set(None)
    _send_update_var.set(None)
    _collected_updates_var.set(None)


@contextmanager
def collect_send_update() -> Iterator[list[BaseModel]]:
    try:
        data: list[BaseModel] = []
        _collected_updates_var.set(data)
        yield data
    finally:
        _collected_updates_var.set(None)


async def send_update(update: UpdateToUser[Any, Any]) -> None:
    collection = _collected_updates_var.get()
    if collection is not None:
        collection.append(update)
        return

    func = _send_update_var.get()
    if func is not None:
        await func(update)
        return

    await _fake_send_update_to_user(update.content)


def get_active_task_id() -> str | None:
    r = _active_assistant_runner.get()
    if r is not None:
        return r._task_id
    return None


@asynccontextmanager
async def init_streaming_update(
    assistant_update: AssistantUpdateToUser, right_side_content_title: str
) -> AsyncGenerator[Callable[[BaseModel], Awaitable[None]]]:
    """Initialize a streaming update context for the assistant update."""

    if _streaming_update_ongoing.get() is not None:
        raise RuntimeError(
            "init_streaming_update is already in progress. "
            "Nested init_streaming_update are not allowed. Ensure you are not calling init_streaming_update concurrently."
        )

    _streaming_update_ongoing.set(True)
    try:
        assistant_runner = _active_assistant_runner.get()
        collection = _collected_updates_var.get()
        if collection is not None:

            async def streaming_update_with_collection(content: BaseModel) -> None:
                collection.append(content)

            yield streaming_update_with_collection
        elif assistant_runner is not None:
            _assistant_update_sink = assistant_runner._update_sink
            assistant_update_streaming_content = (
                _assistant_update_sink.init_streaming_update(
                    parent_update=assistant_update,
                    title=right_side_content_title,
                )
            )
            await send_update(assistant_update_streaming_content)
            yield partial(
                _assistant_update_sink.send_streaming_update,
                parent_update=assistant_update,
            )
        elif settings.local:
            yield _fake_send_streaming_update_to_user
        else:
            raise Exception(
                "Please set env `local` to `True` to run the assistant locally."
            )
    finally:
        _streaming_update_ongoing.set(None)


async def get_user_input(prompt: str) -> str:
    assistant_runner = _active_assistant_runner.get()
    if assistant_runner is not None:
        return await assistant_runner.get_user_input(prompt)
    if settings.local:
        return await _ask_user_from_console(prompt)
    raise Exception("Please set env `local` to `True` to run the assistant locally.")


class AssistantRunner:
    def __init__(
        self,
        task_id: str,
        assistant_awaitable: Awaitable[None],
        assistant_update_sink: AssistantUpdateSink,
    ) -> None:
        self._task_id = task_id
        self._waiting_input_messages: list[str] = []
        self._expected_user_message_type: UserMessageTypes = UserMessageTypes.NONE
        self._assistant_awaitable = assistant_awaitable
        self._update_sink = assistant_update_sink
        _set_active_assistant_runner(self)

    async def send_update(self, update: UpdateToUser[Any, Any]) -> None:
        with logfire.span(
            "send_update",
            update=update,
        ):
            self._expected_user_message_type = update.expected_user_message_type
            await self._update_sink.send_update(update)

    async def get_user_input(self, prompt: str) -> str:
        with logfire.span(
            "assistant.get_user_input",
            prompt=prompt,
        ) as span:
            await self.send_update(
                AssistantUpdateToUser(
                    content=prompt,
                    expected_user_message_type=UserMessageTypes.CHAT,
                ),
            )

            while not self._waiting_input_messages:
                await asyncio.sleep(0.5)

            input_message = self._waiting_input_messages.pop()
            span.set_attributes(
                {
                    "user_input": input_message,
                }
            )

            await self.send_update(
                UserUpdateToUser(
                    content=input_message,
                ),
            )
            return input_message

    async def handle_incoming_message(self, body: IncomingMessage) -> None:
        if (
            body is not None
            and isinstance(body.message, UserChatMessage)
            and self._expected_user_message_type == UserMessageTypes.CHAT
        ):
            if len(self._waiting_input_messages) > 1:
                raise HTTPException(
                    status_code=400,
                    detail="Multiple user messages received while waiting for a single message",
                )
            self._waiting_input_messages.append(body.message.content)

    async def run(self) -> None:
        try:
            logger.info("Task %s started", self._task_id)

            await self._assistant_awaitable

            await send_update(
                AssistantUpdateToUser(
                    content="Assistant completed.",
                    state=AssistantState.TERMINATED,
                )
            )
            logger.info("Task %s completed", self._task_id)

        except asyncio.CancelledError:
            await send_update(
                AssistantUpdateToUser(
                    content="Assistant cancelled.",
                    state=AssistantState.TERMINATED,
                )
            )
            logger.info("Task %s cancelled", self._task_id)
        except Exception:
            logger.exception("Task %s failed with exception", self._task_id)
            await send_update(
                AssistantUpdateToUser(
                    content="Assistant failed.",
                    state=AssistantState.TERMINATED,
                )
            )
            raise
        finally:
            # unset all context variables to their defaults
            _unset_assistant_context_vars()
