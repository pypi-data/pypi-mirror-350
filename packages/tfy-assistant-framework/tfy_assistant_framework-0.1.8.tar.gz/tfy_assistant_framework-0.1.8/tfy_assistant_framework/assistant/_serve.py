import json
from collections.abc import AsyncIterator, Awaitable
from contextlib import asynccontextmanager
from typing import Any

from fastapi import APIRouter, FastAPI, Response
from nats.aio.client import Client as NATS
from nats.errors import NoRespondersError
from pydantic import BaseModel

from tfy_assistant_framework.assistant._assistant_tasks import (
    AssistantTasks,
    CreateAssistantTaskRunResult,
)
from tfy_assistant_framework.assistant._base_assistant_io import AssistantUpdateSink
from tfy_assistant_framework.assistant._nats_assistant_io import (
    NATSAssistantInput,
    NATSInputResponse,
)


class PostAssistantTaskMessage(BaseModel):
    """Message model for sending data to an assistant task."""

    message: dict[str, Any] | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": {
                        "message": {"message_type": "CHAT", "content": "test message"}
                    }
                }
            ]
        }
    }


class AssistantServe:
    def __init__(
        self,
        path: str = "",
    ) -> None:
        self._assistant_tasks: AssistantTasks | None = None
        self._nc: NATS | None = None
        self._router = APIRouter(prefix=path)
        self._app: FastAPI | None = None

    @asynccontextmanager
    async def init(self, nc: NATS, app: FastAPI) -> AsyncIterator["AssistantServe"]:
        self._nc = nc
        self._assistant_tasks = AssistantTasks(nc=self._nc)
        self._app = app
        self._app.include_router(self._router)
        try:
            yield self
        finally:
            await self._assistant_tasks.cancel_tasks()
            self._assistant_tasks = None

    async def create_assistant_task(
        self,
        task_id: str,
        assistant_awaitable: Awaitable[Any],
        assistant_update_sink: AssistantUpdateSink,
    ) -> CreateAssistantTaskRunResult:
        assert self._assistant_tasks is not None
        return await self._assistant_tasks.create_assistant_task(
            task_id=task_id,
            assistant_awaitable=assistant_awaitable,
            assistant_update_sink=assistant_update_sink,
        )

    async def send_message_to_assistant_task(
        self,
        task_id: str,
        payload: PostAssistantTaskMessage,
    ) -> Response:
        sub = NATSAssistantInput.get_incoming_message_subject(task_id=task_id)
        assert self._nc is not None
        try:
            msg = await self._nc.request(
                sub, json.dumps(payload.message).encode(), timeout=10
            )
        except NoRespondersError:
            return Response(status_code=404, content=f"Task {task_id} does not exist")
        response = NATSInputResponse(**json.loads(msg.data.decode()))
        return Response(
            status_code=response.status_code, content=response.error_details
        )
