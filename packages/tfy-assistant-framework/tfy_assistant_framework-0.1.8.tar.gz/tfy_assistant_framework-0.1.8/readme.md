# Tfy Assistant Framework

## Overview

The Tfy Assistant Framework is a framework for building AI assistants with streaming updates and user interactions.

## Installation

```bash
pip install tfy-assistant-framework
```

## Usage

### Prerequisites
1. Create a `.env` file following the `.env.example` template
2. Configure `TFY_*` environment variables if using Truefoundry's NATS service
   - Skip this if using your own NATS connection and JetStream context

### Basic Chat Assistant
Here's a minimal example of a chat assistant:
```python
from tfy_assistant_framework.swarm import Agent, client
from typing import Any

# Custom chat agent that inherits from the base Agent class
class ChatAssistant(Agent[Any]): ...

# Initialize the chat agent
chat_agent = ChatAssistant(instructions="You are a helpful AI assistant")

async def run_chat_assistant() -> None:
    # Start interactive chat session
    async for agent_run in client.run(
        agent=chat_agent,
        messages=[],  # Initial messages (if any)
        interactive=True
    ):
        agent_run.debug_log()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_chat_assistant())
```


### FastAPI Integration
To serve the assistant via a REST API:

```python
from fastapi import FastAPI, Response
from nats.js import JetStreamContext
from contextlib import asynccontextmanager
from typing import AsyncIterator
import uuid

from tfy_assistant_framework.assistant import (
    AssistantServe,
    CreateAssistantTaskRunResult,
    NATSAssistantUpdateSink,
    PostAssistantTaskMessage,
)
from tfy_assistant_framework.nats_client import nats_connection

# Initialize global variables
js: JetStreamContext
assistant_serve = AssistantServe()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global js
    async with nats_connection() as (nc, js_):
        js = js_
        async with assistant_serve.init(nc=nc, app=app):
            yield

# Create FastAPI app
app = FastAPI(lifespan=lifespan)

@app.post("/assistants/chat/task")
async def create_chat_task() -> CreateAssistantTaskRunResult:
    """Create a new chat assistant task"""
    task_id = uuid.uuid4().hex
    return await assistant_serve.create_assistant_task(
        task_id=task_id,
        assistant_awaitable=run_chat_assistant(),
        assistant_update_sink=NATSAssistantUpdateSink(task_id=task_id, js=js),
    )

@app.post("/tasks/{task_id}/message")
async def send_message(
    task_id: str,
    message: PostAssistantTaskMessage,
) -> Response:
    """Send a message to an existing assistant task"""
    return await assistant_serve.send_message_to_assistant_task(task_id, message)
```

For an end-to-end example, see [examples](https://github.com/truefoundry/tfy_assistant_framework/tree/main/examples/readme.md).
