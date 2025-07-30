import copy
import json
import logging
import uuid
from collections.abc import AsyncIterable
from typing import Any

import logfire
from openai import NOT_GIVEN, AsyncOpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCall,
    ChatCompletionMessageToolCallParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_message_tool_call_param import Function
from pydantic import BaseModel, ValidationError

from tfy_assistant_framework.assistant._assistant_runner import (
    get_active_task_id,
    get_user_input,
)
from tfy_assistant_framework.settings import settings
from tfy_assistant_framework.swarm._types import (
    Agent,
    AgentFunctionResult,
    AgentResponseType,
    AgentResponseValidationError,
    AgentRun,
    AgentRunState,
    ContextVarType,
    Tool,
)

logger = logging.getLogger(__name__)
__CTX_VARS_NAME__ = "context_variables"


class Swarm:
    def __init__(
        self,
        client: AsyncOpenAI | None = None,
    ) -> None:
        if not client:
            client = AsyncOpenAI()
        self.client = client
        logfire.instrument_openai(client)

    async def get_chat_completion(
        self,
        agent: Agent[Any],
        history: list[ChatCompletionMessageParam],
        context_variables: dict[Any, Any],
        model_override: str | None,
        tracking_session_id: str | None,
        max_tokens: int | None = None,
    ) -> ChatCompletion:
        instructions = (
            agent.instructions(context_variables)
            if callable(agent.instructions)
            else agent.instructions
        )
        system_prompt = ChatCompletionSystemMessageParam(
            content=instructions, role="system"
        )
        # how do we log the system prompt?
        messages = [system_prompt, *history]

        tools = [
            t.openai_function_schema if isinstance(t, Tool) else t
            for t in agent.tools.values()
        ]

        tfy_metadata = {
            "tfy_log_request": "true" if settings.tfy_log_to_gateway else "false",
        }
        if tracking_session_id:
            tfy_metadata["session_id"] = tracking_session_id
        tfy_metadata["agent_name"] = agent.name

        return await self.client.chat.completions.create(
            model=model_override or agent.model,
            messages=messages,
            tools=tools or NOT_GIVEN,
            tool_choice=agent.tool_choice,
            parallel_tool_calls=agent.parallel_tool_calls if tools else NOT_GIVEN,
            extra_headers={"X-TFY-METADATA": json.dumps(tfy_metadata)},
            max_completion_tokens=max_tokens,
        )

    def handle_function_result(
        self, result: str | Agent[Any] | dict[Any, Any] | BaseModel
    ) -> AgentFunctionResult:
        # Disable multi-agent for now.
        match result:
            case AgentFunctionResult() as result:
                assert result.agent is None, "multi-agent is unsupported"
                return result

            case Agent():
                raise AssertionError("multi-agent is unsupported")
                # return AgentFunctionResult(
                #     value=json.dumps({"assistant": agent.name}),
                #     agent=agent,
                # )
            case _:
                try:
                    return AgentFunctionResult(value=str(result))
                except Exception as e:
                    error_message = f"Failed to cast response to string: {result}. Make sure agent functions return a string or Result object. Error: {e!s}"

                    raise TypeError(error_message) from e

    async def handle_tool_calls(
        self,
        agent: Agent[Any],
        tool_calls: list[ChatCompletionMessageToolCall],
        agent_run: AgentRun[Any],
    ) -> AsyncIterable[None]:
        for tool_call in tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            if agent.response_type and name == agent.response_tool_name:
                if len(tool_calls) > 1:
                    agent_run.update(
                        message=ChatCompletionToolMessageParam(
                            content=f"Error: Tool {name} cannot be used with other tool calls.",
                            role="tool",
                            tool_call_id=tool_call.id,
                        )
                    )
                    yield
                    continue

                try:
                    r = agent.response_type(**args)
                except ValidationError as ex:
                    agent_run.update(
                        message=ChatCompletionToolMessageParam(
                            content=f"Fix the arguments to resolve the validation error in the tool call.\nError: {ex}",
                            role="tool",
                            tool_call_id=tool_call.id,
                        )
                    )
                    yield
                    continue

                validation_result = await agent.validate_response(
                    r, agent_run.context_variables
                )
                match validation_result:
                    case agent.response_type() as validation_result:  # type: ignore
                        agent_run.response = validation_result
                        return
                    case AgentResponseValidationError() as validation_result:
                        agent_run.update(
                            message=ChatCompletionToolMessageParam(
                                content=validation_result.error_message,
                                role="tool",
                                tool_call_id=tool_call.id,
                            )
                        )
                        yield
                        continue
                    case _:
                        raise TypeError(f"Unknown type {type(validation_result)}")

            # handle missing tool case, skip to next tool
            if name not in agent.tools:
                agent_run.update(
                    message=ChatCompletionToolMessageParam(
                        content=f"Error: Tool {name} not found.",
                        role="tool",
                        tool_call_id=tool_call.id,
                    )
                )
                yield
                continue

            tool = agent.tools[name]
            raw_result = None
            try:
                assert isinstance(tool, Tool)
                raw_result = await tool.call(args, agent_run.context_variables)
            except ValidationError as ex:
                agent_run.update(
                    message=ChatCompletionToolMessageParam(
                        content=f"Fix the arguments to resolve the validation error in the tool call.\nError: {ex}",
                        role="tool",
                        tool_call_id=tool_call.id,
                    )
                )
                yield
                continue
            except Exception as ex:
                logger.warning("Error calling tool %s: %s", name, ex, exc_info=True)
                agent_run.update(
                    message=ChatCompletionToolMessageParam(
                        content=f"Error: {ex}",
                        role="tool",
                        tool_call_id=tool_call.id,
                    )
                )
                yield
                continue

            result: AgentFunctionResult = self.handle_function_result(raw_result)
            agent_run.update(
                message=ChatCompletionToolMessageParam(
                    content=result.value,
                    role="tool",
                    tool_call_id=tool_call.id,
                ),
                context_variables=result.context_variables,
                agent=result.agent,
            )
            yield

    async def run(
        self,
        agent: Agent[Any],
        messages: list[ChatCompletionMessageParam],
        context_variables: ContextVarType | None = None,
        model_override: str | None = None,
        # no int inf in python
        max_turns: float | int = float("inf"),
        tracking_session_id: str | None = None,
        interactive: bool = False,
        max_tokens: int | None = None,
    ) -> AsyncIterable[AgentRun[Any]]:
        with logfire.span(
            f"Agent: {agent.name}",
            agent=agent,
            context_variables=context_variables,
            max_turns=max_turns,
            interactive=interactive,
            messages=messages,
        ) as span:
            context_variables = context_variables or {}
            messages = copy.deepcopy(messages)
            agent_run: AgentRun[Any] = AgentRun(agent=agent)
            span.set_attributes(
                {
                    "agent.name": agent.name,
                    "max_turns": max_turns,
                    "interactive": interactive,
                    "context_variables": context_variables,
                }
            )
            yield agent_run
            for m in messages:
                agent_run.update(
                    message=m,
                    context_variables=context_variables,
                    agent=agent,
                )
                yield agent_run

            init_len = len(messages)
            tracking_session_id = (
                tracking_session_id or get_active_task_id() or uuid.uuid4().hex
            )

            iteration_count = 0  # Track number of iterations

            while len(agent_run.messages) - init_len < max_turns:
                iteration_count += 1  # Increment iteration count

                # get completion with current history, agent
                completion = await self.get_chat_completion(
                    agent=agent_run.agent,
                    history=agent_run.messages,
                    context_variables=context_variables,
                    model_override=model_override,
                    tracking_session_id=tracking_session_id,
                    max_tokens=max_tokens,
                )
                choice_message = completion.choices[0].message
                message = ChatCompletionAssistantMessageParam(
                    role=choice_message.role,
                    content=choice_message.content,
                    refusal=choice_message.refusal,
                )
                if choice_message.tool_calls:
                    message["tool_calls"] = [
                        ChatCompletionMessageToolCallParam(
                            id=tc.id,
                            type=tc.type,
                            function=Function(
                                name=tc.function.name,
                                arguments=tc.function.arguments,
                            ),
                        )
                        for tc in choice_message.tool_calls
                    ]
                agent_run.update(
                    message=message,
                    context_variables=context_variables,
                    agent=agent,
                )
                yield agent_run
                # handle function calls, updating context_variables, and switching agents
                async for _ in self.handle_tool_calls(
                    agent,
                    choice_message.tool_calls or [],
                    agent_run=agent_run,
                ):
                    yield agent_run
                if agent_run.response:
                    span.set_attributes(
                        {
                            "agent.response": agent_run.response,
                            "iteration_count": iteration_count,
                        }
                    )
                    yield agent_run
                    return

                if (
                    agent_run.state == AgentRunState.AI
                ):  # if llm responds without a tool call or response model it will get stuck
                    if interactive:  # If fetch_input_from_user is provided, then we assume that user input is required to proceed
                        assert "content" in agent_run.messages[-1]
                        message_content = agent_run.messages[-1]["content"]
                        prompt = (
                            str(message_content) if message_content is not None else ""
                        )
                        user_input = await get_user_input(prompt)
                        init_len = len(agent_run.messages)
                        agent_run.update(
                            message=ChatCompletionUserMessageParam(
                                content=user_input, role="user"
                            ),
                            context_variables=context_variables,
                            agent=agent,
                        )
                        yield agent_run
                    elif (
                        agent_run.agent.response_type is not None
                    ):  # If fetch_input_from_user is not provided and response_type is not None, then we force the agent to use only the tools available to it instead of responding to user
                        logger.warning(
                            "User input method not provided and agent is expected to return a response model, forcing agent to use only the tools available to it instead of responding to user"
                        )
                        agent_run.update(
                            message=ChatCompletionUserMessageParam(
                                content="YOU ARE ONLY ALLOWED TO USE THE TOOLS AVAILABLE TO YOU AND RESPOND WITH THE TOOL CALLS",
                                role="user",
                            ),
                            context_variables=context_variables,
                            agent=agent,
                        )
                        yield agent_run


client = Swarm()


class MaxTurnsExceeded(Exception): ...


async def get_response_from_structured_agent(
    agent: Agent[AgentResponseType],
    context_variables: ContextVarType | None = None,
    tracking_session_id: str | None = None,
    messages: list[ChatCompletionMessageParam] | None = None,
    interactive: bool = False,
    max_turns: int = 20,
    max_tokens: int | None = None,
) -> AgentResponseType:
    agent_run = None
    async for agent_run in client.run(
        agent=agent,
        messages=messages or [],
        interactive=interactive,
        context_variables=context_variables,
        tracking_session_id=tracking_session_id,
        max_turns=max_turns,
        max_tokens=max_tokens,
    ):
        agent_run.debug_log()
    assert agent_run is not None

    if agent_run.response is None:
        raise MaxTurnsExceeded()

    return agent_run.response
