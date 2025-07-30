from typing import Literal
from google_a2a.common.types import (
    JSONRPCRequest,
)
from pydantic import BaseModel


class SSEConnectionParams(BaseModel):
    user_id: str
    project_id: str
    conversation_id: str
    message_id: str


class SSEConnectionRequest(JSONRPCRequest):
    method: Literal["sse/connect"] = "sse/connect"
    params: SSEConnectionParams


class SSEEvent(BaseModel):
    actor: str
    content: str
