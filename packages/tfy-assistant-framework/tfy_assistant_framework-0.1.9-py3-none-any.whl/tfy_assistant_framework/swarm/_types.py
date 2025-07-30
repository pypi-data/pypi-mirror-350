import inspect
import os
import sys
from collections.abc import Callable
from enum import Enum, auto
from itertools import chain
from textwrap import dedent
from typing import Annotated, Any, Generic, Literal, TypeVar, Union

import logfire
from fastapi.concurrency import run_in_threadpool
from openai import NOT_GIVEN, NotGiven
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    create_model,
    model_validator,
)

from tfy_assistant_framework.settings import settings
from tfy_assistant_framework.swarm._logger import AgentLogLine, log

__CTX_VARS_NAME__ = "context_variables"
ContextVarType = dict[str, Any]


def get_obj_type_identity(obj: object) -> str:
    c = obj.__class__
    module: str | None = c.__module__
    if module == "__main__":
        module = sys.modules[module].__file__
        assert module is not None
        module = os.path.splitext(os.path.basename(module))[0]
    return f"{module}:{obj.__class__.__qualname__}"


class Tool(BaseModel):
    name: str
    func: Callable[..., Any]
    model: type[BaseModel]
    openai_function_schema: ChatCompletionToolParam
    pass_ctx: bool

    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def call(
        self, args: dict[Any, Any], context_variables: ContextVarType
    ) -> Union[str, "Agent[Any]", dict[Any, Any], BaseModel]:
        kwargs = {}
        if self.pass_ctx:
            kwargs[__CTX_VARS_NAME__] = context_variables

        args_model = self.model(**args)
        keys = chain(
            self.model.model_fields.keys(), args_model.model_computed_fields.keys()
        )
        for k in keys:
            kwargs[k] = getattr(args_model, k)

        with logfire.span(
            f"Tool: {self.name}",
            attributes={
                "tool.name": self.name,
                "tool.args": kwargs,
                "tool.context_variables": context_variables,
            },
        ) as span:
            if inspect.iscoroutinefunction(self.func):
                result = await self.func(**kwargs)
            else:
                result = await run_in_threadpool(self.func, **kwargs)

            # Add result to span attributes
            span.set_attributes(
                {
                    "tool.result": result,
                }
            )
            return result

    @classmethod
    def from_function(cls, func: Callable[..., Any]) -> "Tool":
        try:
            signature = inspect.signature(func)
        except ValueError as e:
            raise ValueError(
                f"Failed to get signature for function {func.__name__}: {e!s}"
            ) from e

        parameters: dict[str, tuple[type, Any]] = {}
        pass_ctx = False
        for param_name, param in signature.parameters.items():
            # hide context_variables from model
            if param_name == __CTX_VARS_NAME__:
                pass_ctx = True
                continue
            if param.annotation == inspect.Parameter.empty:
                raise ValueError(
                    f"Type annotation required for function: {func.__name__} argument: {param.name}"
                )
            if param.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.KEYWORD_ONLY,
            ):
                raise ValueError(
                    f"{param.kind} not supported for function: {func.__name__} argument: {param.name}"
                )
            parameters[param_name] = (
                param.annotation,
                param.default if param.default != inspect.Parameter.empty else ...,
            )

        model = create_model(func.__qualname__, **parameters)  # type: ignore
        return cls(
            name=func.__name__,
            func=func,
            model=model,
            pass_ctx=pass_ctx,
            openai_function_schema=ChatCompletionToolParam(
                {
                    "type": "function",
                    "function": {
                        "name": func.__name__,
                        "description": func.__doc__ or "",
                        "parameters": model.model_json_schema(),
                    },
                }
            ),
        )


class AgentResponseValidationError(BaseModel):
    error_message: Annotated[
        str,
        Field(min_length=1),
    ]


AgentResponseType = TypeVar("AgentResponseType", bound=BaseModel)


class Agent(BaseModel, Generic[AgentResponseType]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = ""
    model: str = settings.openai_model_name
    instructions: str | Callable[[dict[Any, Any] | None], str]
    functions: list[Callable[..., Any]] = []
    _tools: dict[str, Tool | ChatCompletionToolParam] = {}
    tool_choice: Literal["none", "auto", "required"] | NotGiven = NOT_GIVEN
    parallel_tool_calls: bool | NotGiven = NOT_GIVEN

    response_type: type[AgentResponseType] | None = None
    response_tool_name: Annotated[
        str,
        Field(min_length=1),
    ] = "RESPONSE"
    response_tool_description: Annotated[
        str,
        Field(min_length=1),
    ] = """
Call this tool once you have achieved your goal.
    """

    @model_validator(mode="after")
    def process_response_tool_description(self) -> "Agent[AgentResponseType]":
        self.response_tool_description = dedent(self.response_tool_description)
        return self

    @model_validator(mode="after")
    def set_name(self) -> "Agent[AgentResponseType]":
        self.name = self.name if self.name else get_obj_type_identity(self)
        return self

    @model_validator(mode="after")
    def create_tools(self) -> "Agent[AgentResponseType]":
        if self.tools:
            return self
        for f in self.functions:
            t = Tool.from_function(f)
            if t.name in self._tools:
                raise ValueError(f"Duplicate tool {t.name}")
            self._tools[t.name] = t
        if self.response_type:
            if self.response_tool_name in self._tools:
                raise ValueError(f"Duplicate tool {self.response_tool_name}")
            self._tools[self.response_tool_name] = ChatCompletionToolParam(
                {
                    "type": "function",
                    "function": {
                        "name": self.response_tool_name,
                        "description": self.response_tool_description,
                        "parameters": self.response_type.model_json_schema(),  # type: ignore
                    },
                }
            )
        return self

    @property
    def tools(self) -> dict[str, Tool | ChatCompletionToolParam]:
        return self._tools

    async def validate_response(
        self, response: AgentResponseType, context_variables: ContextVarType
    ) -> AgentResponseValidationError | AgentResponseType:
        return response


def create_structured_agent(
    name: str,
    response_type: type[AgentResponseType],
    instruction_template: str,
    model: str = settings.openai_model_name,
) -> Agent[AgentResponseType]:
    def generate_instructions(context_variables: ContextVarType | None) -> str:
        assert context_variables is not None
        return instruction_template.format(d=context_variables)

    return Agent(
        name=name,
        model=model,
        response_type=response_type,
        instructions=generate_instructions,
        tool_choice="required",
    )


class AgentRunState(Enum):
    EMPTY = auto()
    AI = auto()
    HUMAN = auto()
    AI_IN_TOOL_CALLS = auto()


ALLOWED_AGENT_RUN_STATE_TRANSITION: dict[AgentRunState, set[AgentRunState]] = {
    AgentRunState.EMPTY: {
        AgentRunState.AI,
        AgentRunState.HUMAN,
        AgentRunState.AI_IN_TOOL_CALLS,
    },
    AgentRunState.AI: {
        AgentRunState.HUMAN,
        AgentRunState.AI_IN_TOOL_CALLS,
        AgentRunState.AI,
    },
    AgentRunState.HUMAN: {AgentRunState.AI, AgentRunState.AI_IN_TOOL_CALLS},
    AgentRunState.AI_IN_TOOL_CALLS: {AgentRunState.AI, AgentRunState.AI_IN_TOOL_CALLS},
}


def message_to_state(
    m: ChatCompletionMessageParam, pending_tool_calls: set[str]
) -> AgentRunState:
    match m["role"]:
        case "user":
            return AgentRunState.HUMAN
        case "assistant":
            if m.get("tool_calls"):
                return AgentRunState.AI_IN_TOOL_CALLS
            return AgentRunState.AI
        case "tool":
            if pending_tool_calls:
                return AgentRunState.AI
            return AgentRunState.AI_IN_TOOL_CALLS
        case _:
            raise ValueError(f"Unknown ${m['role']}")


class AgentRun(BaseModel, Generic[AgentResponseType]):
    messages: list[ChatCompletionMessageParam] = []
    last_logged_message_index: int = 0
    agent: Agent[AgentResponseType]
    context_variables: ContextVarType = {}
    response: AgentResponseType | None = None
    state: AgentRunState = AgentRunState.EMPTY
    pending_tool_calls: set[str] = Field(default_factory=set)

    def update(
        self,
        message: ChatCompletionMessageParam,
        context_variables: ContextVarType | None = None,
        agent: Agent[AgentResponseType] | None = None,
    ) -> None:
        if message["role"] == "assistant":
            tool_calls = message.get("tool_calls")
            if tool_calls:
                self.pending_tool_calls = {t["id"] for t in tool_calls}
        if message["role"] == "tool":
            tool_call_id = message.get("tool_call_id")
            if tool_call_id:
                self.pending_tool_calls.discard(tool_call_id)
        transitioning_to_state = message_to_state(message, self.pending_tool_calls)
        if transitioning_to_state not in ALLOWED_AGENT_RUN_STATE_TRANSITION[self.state]:
            raise ValueError(
                f"{self.state!r} to {transitioning_to_state!r} not allowed"
            )

        self.state = transitioning_to_state
        self.messages.append(message)
        if context_variables:
            self.context_variables.update(context_variables)
        if agent:
            self.agent = agent

    def debug_log(self) -> None:
        while self.last_logged_message_index < len(self.messages):
            log(
                AgentLogLine(
                    agent_name=self.agent.name,
                    num_messages=self.last_logged_message_index + 1,
                    current_message=self.messages[self.last_logged_message_index],
                )
            )
            self.last_logged_message_index += 1

    def last_message(self) -> ChatCompletionMessageParam:
        return self.messages[-1]


class AgentFunctionResult(BaseModel):
    """
    Encapsulates the possible return values for an agent function.

    Attributes:
        value (str): The result value as a string.
        agent (Agent): The agent instance, if applicable.
        context_variables (dict): A dictionary of context variables.
    """

    value: str = ""
    agent: Agent[Any] | None = None
    context_variables: dict[Any, Any] = {}
