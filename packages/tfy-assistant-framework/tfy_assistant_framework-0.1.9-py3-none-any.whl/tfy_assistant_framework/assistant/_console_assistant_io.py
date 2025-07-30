from pydantic import BaseModel
from rich.console import Console
from rich.pretty import pprint

console = Console(soft_wrap=True)


async def _ask_user_from_console(question: str) -> str:
    """
    Ask user for input form console and return the response
    Args:
        question: Question to ask the user

    Returns:
        User input as string
    """
    return console.input(f"\n[bold cyan] ({question})[/]: ")


async def _fake_send_update_to_user(message: str) -> None:
    pprint(message)


async def _fake_send_streaming_update_to_user(update: BaseModel) -> None:
    pprint(update.model_dump_json())
