from datetime import datetime
from typing import (
    Any,
    ClassVar,
    Generic,
    Literal,
    Protocol,
    Sequence,
    TypeVar,
    runtime_checkable,
)
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, SecretStr

from moxn_types.blocks.content_block import ContentBlockModel
from moxn_types.content import Author, MessageRole
from moxn_types.schema import MoxnMessageMetadata

T = TypeVar("T")


@runtime_checkable
class RenderableModel(Protocol):
    moxn_version_config: ClassVar[MoxnMessageMetadata]

    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: Any = None,
        exclude: Any = None,
        context: dict[str, Any] | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        serialize_as_any: bool = False,
    ) -> Any: ...

    def render(self, **kwargs: Any) -> Any: ...


class BaseHeaders(BaseModel):
    user_id: str
    org_id: str | None = None
    api_key: SecretStr

    def to_headers(self) -> dict[str, str]:
        return {
            "user_id": self.user_id,
            "org_id": self.org_id or "",
            "api_key": self.api_key.get_secret_value(),
        }


class MessageBase(BaseModel, Generic[T]):
    id: UUID = Field(default_factory=uuid4)
    version_id: UUID | None = Field(None, alias="versionId")
    name: str
    description: str
    author: Author
    role: MessageRole
    blocks: Sequence[Sequence[T]] = Field(repr=False)

    model_config = ConfigDict(populate_by_name=True)


class Message(MessageBase[ContentBlockModel]):
    blocks: Sequence[Sequence[ContentBlockModel]] = Field(repr=False)


class BasePrompt(BaseModel, Generic[T]):
    id: UUID
    version_id: UUID = Field(..., alias="versionId")
    user_id: UUID = Field(..., alias="userId")
    org_id: UUID | None = Field(None, alias="orgId")
    name: str
    description: str
    task_id: UUID = Field(..., alias="taskId")
    created_at: datetime = Field(..., alias="createdAt")
    messages: Sequence[T]
    message_order: Sequence[UUID] = Field(default_factory=list, alias="messageOrder")

    model_config = ConfigDict(populate_by_name=True)


class Prompt(BasePrompt[Message]):
    messages: Sequence[Message]


class BaseTask(BaseModel, Generic[T]):
    id: UUID
    version_id: UUID = Field(..., alias="versionId")
    user_id: UUID = Field(..., alias="userId")
    org_id: UUID | None = Field(None, alias="orgId")
    name: str
    description: str
    created_at: datetime = Field(..., alias="createdAt")
    prompts: Sequence[T]

    model_config = ConfigDict(populate_by_name=True)


class Task(BaseTask[Prompt]):
    prompts: Sequence[Prompt]
