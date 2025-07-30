from pydantic import BaseModel, Field
from typing import Literal, Union

from google_a2a.common.types import (
    JSONRPCRequest,
    JSONRPCResponse,
    AgentCard,
)
from langchain_core.messages import BaseMessage
from ephor_cli.types.event import Event
from ephor_cli.types.task import Task, TaskMetadata


class ConversationMetadata(BaseModel):
    conversation_id: str
    user_id: str
    project_id: str
    name: str = ""
    created_at: str = ""
    updated_at: str = ""
    task_map: dict[str, str] = Field(default_factory=dict)
    trace_map: dict[str, str] = Field(default_factory=dict)


class Conversation(ConversationMetadata):
    agents: list[AgentCard] = Field(default_factory=list)
    messages: list[Union[BaseMessage, dict]] = Field(default_factory=list)
    tasks: list[Union[Task, TaskMetadata]] = Field(default_factory=list)
    events: list[Event] = Field(default_factory=list)


class CreateConversationParams(BaseModel):
    user_id: str
    project_id: str


class CreateConversationRequest(JSONRPCRequest):
    method: Literal["conversation/create"] = "conversation/create"
    params: CreateConversationParams


class CreateConversationResponse(JSONRPCResponse):
    result: ConversationMetadata | None = None


class GetConversationParams(BaseModel):
    user_id: str
    project_id: str
    conversation_id: str


class GetConversationRequest(JSONRPCRequest):
    method: Literal["conversation/get"] = "conversation/get"
    params: GetConversationParams


class GetConversationResponse(JSONRPCResponse):
    result: Conversation | None = None


class ListConversationParams(BaseModel):
    user_id: str
    project_id: str


class ListConversationRequest(JSONRPCRequest):
    method: Literal["conversation/list"] = "conversation/list"
    params: ListConversationParams


class ListConversationResponse(JSONRPCResponse):
    result: list[ConversationMetadata] | None = None


class DeleteConversationParams(BaseModel):
    user_id: str
    project_id: str
    conversation_id: str


class DeleteConversationRequest(JSONRPCRequest):
    method: Literal["conversation/delete"] = "conversation/delete"
    params: DeleteConversationParams


class DeleteConversationResponse(JSONRPCResponse):
    result: bool | None = None
    error: str | None = None
