from pydantic import BaseModel, Field
from typing import Literal

from google_a2a.common.types import (
    JSONRPCRequest,
    JSONRPCResponse,
    AgentCard,
)

from .llm import Model


class AgentCapabilities(BaseModel):
    streaming: bool


class AgentSkill(BaseModel):
    id: str
    name: str
    description: str
    tags: list[str]
    examples: list[str]
    inputModes: list[str] = Field(default_factory=list)
    outputModes: list[str] = Field(default_factory=list)


class MCPServerConfig(BaseModel):
    name: str
    url: str
    transport: str


class AgentConfig(BaseModel):
    name: str
    description: str
    version: str
    capabilities: AgentCapabilities
    skills: list[AgentSkill]
    prompt: str
    logoUrl: str = ""
    mcpServers: list[MCPServerConfig] = Field(default_factory=list)
    supported_content_types: list[str] = Field(default_factory=list)
    hiveIds: list[str] = Field(default_factory=list)
    primaryModel: Model | None = None
    fallbackModels: list[Model] = Field(default_factory=list)


class RegisterAgentParams(BaseModel):
    user_id: str
    project_id: str
    conversation_id: str
    url: str


class RegisterAgentRequest(JSONRPCRequest):
    method: Literal["agent/register"] = "agent/register"
    params: RegisterAgentParams


class RegisterAgentResponse(JSONRPCResponse):
    result: AgentCard | None = None
    error: str | None = None


class ListAgentParams(BaseModel):
    user_id: str
    project_id: str
    conversation_id: str


class ListAgentRequest(JSONRPCRequest):
    method: Literal["agent/list"] = "agent/list"
    params: ListAgentParams


class ListAgentResponse(JSONRPCResponse):
    result: list[AgentCard] | None = None


class DeregisterAgentParams(BaseModel):
    user_id: str
    project_id: str
    conversation_id: str
    url: str


class DeregisterAgentRequest(JSONRPCRequest):
    method: Literal["agent/deregister"] = "agent/deregister"
    params: DeregisterAgentParams


class DeregisterAgentResponse(JSONRPCResponse):
    result: bool | None = None
    error: str | None = None


class ApiKeyRecord(BaseModel):
    id: str
    key: str


class HiveInstance(BaseModel):
    id: str
    apiKey: ApiKeyRecord


class AgentInstance(BaseModel):
    id: str
    agentId: str
    agentVersion: str
    spaceId: str
    status: str
    agent: AgentConfig
    hiveInstances: list[HiveInstance] = Field(default_factory=list)
    createdAt: str
    updatedAt: str
