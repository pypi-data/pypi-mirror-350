import asyncio
from collections.abc import Awaitable
from dataclasses import dataclass
from typing import Any

from nats.aio.client import Client as NATS

from tfy_assistant_framework._logger import logger
from tfy_assistant_framework.assistant._assistant_runner import (
    AssistantRunner,
)
from tfy_assistant_framework.assistant._base_assistant_io import (
    AssistantInput,
    AssistantUpdateSink,
)
from tfy_assistant_framework.assistant._nats_assistant_io import NATSAssistantInput


@dataclass
class CreateAssistantTaskRunResult:
    task_id: str
    sink_config: dict[Any, Any]


_TASK_PRUNE_TIMEOUT_SECONDS = 30 * 60  # 30 minutes


class AssistantTasks:
    def __init__(self, nc: NATS) -> None:
        self._tasks: dict[str, tuple[asyncio.Task[None], AssistantRunner]] = {}
        self._nc = nc

    async def _run_task(
        self,
        assistant_runner: AssistantRunner,
        assistant_input: AssistantInput,
    ) -> None:
        async with assistant_input:
            await assistant_runner.run()

    async def create_assistant_task(
        self,
        task_id: str,
        assistant_awaitable: Awaitable[Any],
        assistant_update_sink: AssistantUpdateSink,
    ) -> CreateAssistantTaskRunResult:
        assistant_runner = AssistantRunner(
            task_id=task_id,
            assistant_awaitable=assistant_awaitable,
            assistant_update_sink=assistant_update_sink,
        )
        assistant_input = NATSAssistantInput(
            task_id=task_id,
            nc=self._nc,
            incoming_message_handler=assistant_runner.handle_incoming_message,
        )
        loop = asyncio.get_running_loop()
        task = loop.create_task(self._run_task(assistant_runner, assistant_input))
        self._tasks[task_id] = (task, assistant_runner)
        task.add_done_callback(lambda _: self._handle_task_completion(task_id=task_id))
        loop.call_later(_TASK_PRUNE_TIMEOUT_SECONDS, self._handle_task_timeout, task_id)
        sink_config = await assistant_update_sink.get_sink_config()
        if sink_config is None:
            raise ValueError("Sink config is required to create a task")
        return CreateAssistantTaskRunResult(
            task_id=task_id,
            sink_config=sink_config,
        )

    def _handle_task_timeout(self, task_id: str) -> None:
        task_tuple = self._tasks.get(task_id)
        if not task_tuple:
            logger.warning("Task %s not found for timeout", task_id)
            return
        task, _ = task_tuple
        task.cancel()
        logger.warning("Task %s was timed out", task_id)

    def _handle_task_completion(self, task_id: str) -> None:
        if task_id not in self._tasks:
            logger.warning("Task %s not found", task_id)
            return

        task_run, _ = self._tasks.pop(task_id)
        if task_run.cancelled():
            logger.info("Task %s was cancelled", task_id)
            return

        exception = task_run.exception()
        if exception:
            logger.error("Task %s failed with exception", task_id, exc_info=exception)
        else:
            logger.info("Task %s was successfully completed", task_id)

    async def cancel_tasks(self) -> None:
        # Create a list of tasks to avoid modifying dict during iteration
        tasks_to_cancel = list(self._tasks.items())

        for task_id, (task, _) in tasks_to_cancel:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                logger.info("Task %s cancelled during shutdown", task_id)
            except Exception:
                logger.exception("Task %s failed during shutdown", task_id)
        self._tasks.clear()
