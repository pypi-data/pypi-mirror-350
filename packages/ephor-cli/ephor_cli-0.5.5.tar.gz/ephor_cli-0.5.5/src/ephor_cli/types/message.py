from pydantic import BaseModel
from typing import Literal, Dict, Any, Optional

from google_a2a.common.types import (
    JSONRPCRequest,
    JSONRPCResponse,
)


class SendMessageParams(BaseModel):
    user_id: str
    project_id: str
    conversation_id: str
    message: dict


class SendMessageRequest(JSONRPCRequest):
    method: Literal["message/send"] = "message/send"
    params: SendMessageParams


class ListMessageParams(BaseModel):
    user_id: str
    project_id: str
    conversation_id: str


class ListMessageRequest(JSONRPCRequest):
    method: Literal["message/list"] = "message/list"
    params: ListMessageParams


class ListMessageResponse(JSONRPCResponse):
    result: list[dict] | None = None


class MessageInfo(BaseModel):
    message_id: str
    conversation_id: str
    project_id: str
    user_id: str


class SendMessageResponse(JSONRPCResponse):
    result: MessageInfo | None = None


class CancelMessageParams(BaseModel):
    """Parameters for cancelling a message."""
    user_id: str
    project_id: str
    conversation_id: str
    message_id: str


class CancelMessageRequest(JSONRPCRequest):
    """Request to cancel message processing."""
    method: Literal["message/cancel"] = "message/cancel"
    params: CancelMessageParams


class CancelMessageResponse(JSONRPCResponse):
    """Response from cancelling a message."""
    result: bool
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
