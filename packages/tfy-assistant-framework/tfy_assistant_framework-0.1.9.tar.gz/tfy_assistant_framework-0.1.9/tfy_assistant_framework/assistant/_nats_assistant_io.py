import json
from collections.abc import Awaitable, Callable
from types import TracebackType
from typing import Any, Literal

from fastapi import HTTPException
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
from nats.aio.subscription import Subscription
from nats.js import JetStreamContext
from pydantic import BaseModel

from tfy_assistant_framework._logger import logger
from tfy_assistant_framework.assistant._base_assistant_io import (
    AssistantInput,
    AssistantUpdateSink,
)
from tfy_assistant_framework.assistant._types import (
    AssistantUpdateToUser,
    IncomingMessage,
    UpdateToUser,
    UserMessageTypes,
)
from tfy_assistant_framework.nats_client import JS_PUBLISH_TIMEOUT

_OUTGOING_MESSAGE_STREAM_NAME = "llm-agent-task-state"
_INCOMING_MESSAGE_SUBJECT_NAME = "llm-agent-task-input"


class NATSInputResponse(BaseModel):
    status_code: int
    error_details: str | None = None


class RightSideStreamingUpdate(BaseModel):
    type: Literal["nats-js"] = "nats-js"
    title: str
    stream: str
    subject: str


class NATSAssistantInput(AssistantInput):
    def __init__(
        self,
        task_id: str,
        nc: NATS,
        incoming_message_handler: Callable[[IncomingMessage], Awaitable[None]],
    ) -> None:
        self._task_id = task_id
        self._nc = nc
        self._sub: Subscription | None = None
        self._incoming_message_handler = incoming_message_handler

    @staticmethod
    def get_incoming_message_subject(
        task_id: str,
    ) -> str:
        return f"{_INCOMING_MESSAGE_SUBJECT_NAME}.{task_id}"

    async def _handle_msg(self, msg: Msg) -> None:
        try:
            data = json.loads(msg.data)
            incoming_message = IncomingMessage(**data)
            await self.incoming_message_handler(incoming_message)
            response = NATSInputResponse(status_code=200)
        except HTTPException as ex:
            response = NATSInputResponse(
                status_code=ex.status_code, error_details=ex.detail
            )
        except Exception as ex:
            logger.exception(
                "Task %s failed to process incoming message", self._task_id
            )
            response = NATSInputResponse(status_code=500, error_details=str(ex))

        await self._nc.publish(msg.reply, response.model_dump_json().encode())

    async def __aenter__(self) -> "AssistantInput":
        subject = self.get_incoming_message_subject(task_id=self._task_id)
        logger.info("subscribing to %s for inputs", subject)
        self._sub = await self._nc.subscribe(
            subject=subject,
            cb=self._handle_msg,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._sub:
            try:
                await self._sub.unsubscribe()
            except Exception:
                logger.exception("Task %s failed unsubscribe IO", self._task_id)
        self._sub = None


class NATSAssistantUpdateSink(AssistantUpdateSink):
    def __init__(self, task_id: str, js: JetStreamContext) -> None:
        self._task_id = task_id
        self._js = js

    def _get_outgoing_update_subject(self) -> str:
        return f"{_OUTGOING_MESSAGE_STREAM_NAME}.{self._task_id}"

    def _get_streaming_update_subject(
        self,
        parent_update_id: str,
    ) -> str:
        return f"{_OUTGOING_MESSAGE_STREAM_NAME}.{self._task_id}.{parent_update_id}"

    async def send_update(self, update: UpdateToUser[Any, Any]) -> None:
        payload_json = update.model_dump(mode="json")
        await self._js.publish(
            subject=self._get_outgoing_update_subject(),
            payload=json.dumps(payload_json).encode("utf-8"),
            stream=_OUTGOING_MESSAGE_STREAM_NAME,
            timeout=JS_PUBLISH_TIMEOUT,
        )

    async def get_sink_config(self) -> dict[Any, Any] | None:
        return {
            "type": "nats-js",
            "subject": self._get_outgoing_update_subject(),
            "stream": _OUTGOING_MESSAGE_STREAM_NAME,
        }

    def init_streaming_update(
        self, parent_update: UpdateToUser[Any, Any], title: str
    ) -> AssistantUpdateToUser:
        assert isinstance(parent_update, AssistantUpdateToUser)
        assert parent_update.expected_user_message_type is UserMessageTypes.NONE
        parent_update.right_side_streaming_content = RightSideStreamingUpdate(
            title=title,
            stream=_OUTGOING_MESSAGE_STREAM_NAME,
            subject=self._get_streaming_update_subject(
                parent_update_id=parent_update.message_id,
            ),
        )
        return parent_update

    async def send_streaming_update(
        self,
        update: BaseModel,
        parent_update: UpdateToUser[Any, Any],
    ) -> None:
        payload_json = update.model_dump(mode="json")
        await self._js.publish(
            subject=self._get_streaming_update_subject(
                parent_update_id=parent_update.message_id,
            ),
            payload=json.dumps(payload_json).encode("utf-8"),
            stream=_OUTGOING_MESSAGE_STREAM_NAME,
            timeout=JS_PUBLISH_TIMEOUT,
        )


class TruefoundryNATSAssistantUpdateSink(NATSAssistantUpdateSink):
    def __init__(self, task_id: str, js: JetStreamContext, tenant_name: str) -> None:
        super().__init__(task_id, js)
        self._tenant_name = tenant_name

    def _get_outgoing_update_subject(self) -> str:
        return f"{_OUTGOING_MESSAGE_STREAM_NAME}.{self._tenant_name}.{self._task_id}"

    def _get_streaming_update_subject(
        self,
        parent_update_id: str,
    ) -> str:
        return f"{_OUTGOING_MESSAGE_STREAM_NAME}.{self._tenant_name}.{self._task_id}.{parent_update_id}"
