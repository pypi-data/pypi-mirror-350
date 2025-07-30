from typing import Any, List, Literal

from google_a2a.common.types import (
    Artifact,
    JSONRPCRequest,
    JSONRPCResponse,
    TaskStatus,
)
from langchain_core.messages import BaseMessage
from pydantic import BaseModel


class TaskMetadata(BaseModel):
    id: str
    agent_name: str
    tool_call_id: str
    conversation_id: str
    project_id: str
    user_id: str
    status: TaskStatus
    metadata: dict[str, Any] | None = None


class Task(TaskMetadata):
    artifacts: List[Artifact] | None = None
    history: List[BaseMessage | dict] | None = None


class ListTaskParams(BaseModel):
    user_id: str
    project_id: str
    conversation_id: str


class ListTaskRequest(JSONRPCRequest):
    method: Literal["task/list"] = "task/list"
    params: ListTaskParams


class ListTaskResponse(JSONRPCResponse):
    result: list[TaskMetadata] | None = None


class GetTaskParams(BaseModel):
    user_id: str
    project_id: str
    conversation_id: str
    agent_name: str
    task_id: str


class GetTaskRequest(JSONRPCRequest):
    method: Literal["task/get"] = "task/get"
    params: GetTaskParams


class GetTaskResponse(JSONRPCResponse):
    result: Task | None = None
