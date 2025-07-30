from pydantic import BaseModel
from typing import Literal

from google_a2a.common.types import (
    JSONRPCRequest,
    JSONRPCResponse,
)
from langchain_core.messages import BaseMessage


class Event(BaseModel):
    id: str
    actor: str = ""
    content: BaseMessage
    timestamp: float


class ListEventParams(BaseModel):
    user_id: str
    project_id: str
    conversation_id: str


class ListEventRequest(JSONRPCRequest):
    method: Literal["event/list"] = "event/list"
    params: ListEventParams


class ListEventResponse(JSONRPCResponse):
    result: list[Event] | None = None
