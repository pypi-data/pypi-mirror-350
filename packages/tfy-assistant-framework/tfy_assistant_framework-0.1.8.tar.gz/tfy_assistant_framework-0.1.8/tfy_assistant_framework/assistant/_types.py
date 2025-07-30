import time
import uuid
from abc import ABC
from datetime import UTC, datetime
from enum import Enum, unique
from typing import Generic, Literal, TypeVar

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    SerializeAsAny,
    computed_field,
)


@unique
class UserMessageTypes(str, Enum):
    NONE = "NONE"
    CHAT = "CHAT"


@unique
class AssistantState(str, Enum):
    WAITING_FOR_USER_INPUT = "WAITING_FOR_USER_INPUT"
    BUSY = "BUSY"
    TERMINATED = "TERMINATED"


class UserChatMessage(BaseModel):
    message_type: Literal[UserMessageTypes.CHAT]
    content: str


class IncomingMessage(BaseModel):
    message: UserChatMessage


RoleT = TypeVar("RoleT", bound=Literal["assistant", "user"])
RightSideContentT = TypeVar("RightSideContentT", bound=Literal["markdown"])
MessageTypeT = TypeVar("MessageTypeT", bound=UserMessageTypes)


class UpdateToUser(BaseModel, Generic[RoleT, MessageTypeT], ABC):
    model_config = ConfigDict(extra="allow")
    message_id: str = Field(default_factory=lambda: uuid.uuid1().hex)
    timestamp: AwareDatetime = Field(default_factory=lambda: datetime.now(UTC))
    content: str
    role: RoleT
    expected_user_message_type: MessageTypeT
    state_: AssistantState | None = Field(default=None, alias="state", exclude=True)

    # TODO: this is kept for compatibility with Frontend, remove it later, and use the content field directly
    @computed_field
    def display_message(self) -> str:
        return self.content

    @computed_field
    def state(self) -> AssistantState:
        if self.state_ is not None:
            return self.state_
        if (
            self.role == "assistant"
            and self.expected_user_message_type == UserMessageTypes.CHAT
        ):
            return AssistantState.WAITING_FOR_USER_INPUT
        return AssistantState.BUSY


class RightSideContent(BaseModel, Generic[RightSideContentT], ABC):
    type: RightSideContentT


class RightSideMarkdownContent(RightSideContent[Literal["markdown"]]):
    type: Literal["markdown"] = "markdown"
    title: str
    content: str


class AssistantUpdateToUser(UpdateToUser[Literal["assistant"], UserMessageTypes]):
    """
    Represents an update sent to the user from the assistant.

    This class extends `UpdateToUser` with specific attributes to define the role, expected user response type, and additional content elements.

    Attributes:
        role (Literal["assistant"]): Specifies the role of the sender as "assistant".
        expected_user_message_type (UserMessageTypes): Defines the expected type of user response.
            Defaults to `UserMessageTypes.NONE`, indicating no response is required.
        right_side_content (list[BaseModel] | None): Optional content displayed on the right side of the user interface.
        right_side_streaming_content (BaseModel | None): Optional streaming content displayed on the right side of the user interface.
    """

    role: Literal["assistant"] = "assistant"
    expected_user_message_type: UserMessageTypes = UserMessageTypes.NONE
    right_side_content: SerializeAsAny[list[BaseModel]] | None = None
    right_side_streaming_content: SerializeAsAny[BaseModel] | None = None


class UserUpdateToUser(UpdateToUser[Literal["user"], Literal[UserMessageTypes.NONE]]):
    role: Literal["user"] = "user"
    expected_user_message_type: Literal[UserMessageTypes.NONE] = UserMessageTypes.NONE


class Log(BaseModel):
    # This follows Loki's log format
    type: Literal["log"] = "log"
    log: str
    stream: str
    time: int = Field(default_factory=lambda: int(time.time_ns()))  # in nanoseconds
