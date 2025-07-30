from collections.abc import Iterable
from datetime import datetime
from typing import cast

from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCallParam,
)
from pydantic import BaseModel, Field, SkipValidation
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

console = Console()


class AgentLogLine(BaseModel):
    agent_name: str
    num_messages: int

    # https://github.com/pydantic/pydantic/issues/9467
    current_message: SkipValidation[ChatCompletionMessageParam]
    timestamp: datetime = Field(default_factory=lambda: datetime.now().astimezone())


def log(log_line: AgentLogLine) -> None:
    timestamp = log_line.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    code_theme = "github-dark"
    role = log_line.current_message["role"]
    message_content = str(log_line.current_message.get("content") or "")
    tool_calls: Iterable[ChatCompletionMessageToolCallParam] = cast(
        list[ChatCompletionMessageToolCallParam],
        log_line.current_message.get("tool_calls", []),
    )

    rendered_content: list[Markdown | Text] = []

    if bool(message_content.strip()):
        rendered_content.append(Markdown(markup=message_content, code_theme=code_theme))

    role_str = (role or "Unknown").upper()

    for call in tool_calls:
        name = call["function"]["name"]
        args = call["function"]["arguments"]

        if name == "RESPONSE":
            rendered_content.append(
                Text.from_markup("[bold green]Response:[/bold green]")
            )
            rendered_content.append(
                Markdown(
                    markup=f"```json\n{args}\n```",
                    code_theme=code_theme,
                )
            )
        else:
            rendered_content.append(
                Text.from_markup("[bold magenta]Tool Calls:[/bold magenta]\n")
            )
            rendered_content.append(
                Markdown(
                    markup=f"```python\n▶ {name}({args})\n```", code_theme=code_theme
                )
            )

    if not rendered_content:
        return

    header = Text()
    header.append("Agent: ", style="bold cyan")
    header.append(log_line.agent_name, style="bold green")
    header.append(" | ", style="bold cyan")
    header.append(role_str, style="bold magenta")
    header.append(" | Total Messages: ", style="bold cyan")
    header.append(str(log_line.num_messages), style="bold yellow")
    header.append(" | Time: ", style="bold cyan")
    header.append(timestamp, style="bold blue")

    panel = Panel(
        Group(*rendered_content),
        title=header,
        border_style="bright_blue",
        padding=(1, 2),
    )

    console.print(panel)
