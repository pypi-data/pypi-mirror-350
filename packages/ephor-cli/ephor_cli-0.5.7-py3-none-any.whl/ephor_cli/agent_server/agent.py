import logging
from contextlib import asynccontextmanager
from typing import AsyncIterable, Union

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_aws import ChatBedrock
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessageChunk,
    ToolMessageChunk,
)
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from ephor_cli.types.agent import MCPServerConfig, HiveInstance
from ephor_cli.types.llm import Model, LLMProvider
from ephor_cli.constant import MCP_SERVER_URL

logger = logging.getLogger(__name__)


def _create_llm_instance(model: Model):
    """Create the appropriate LLM instance based on the model provider."""
    print(f"Creating LLM instance for model: {model.name}, provider: {model.provider}")
    if model.provider == LLMProvider.ANTHROPIC:
        return ChatAnthropic(model=model.name, max_tokens=8192)
    elif model.provider == LLMProvider.OPENAI:
        return ChatOpenAI(model=model.name, max_tokens=8192)
    elif model.provider == LLMProvider.GOOGLE:
        return ChatGoogleGenerativeAI(model=model.name, max_output_tokens=8192)
    elif model.provider == LLMProvider.AWS:
        return ChatBedrock(
            model_id=model.name,
            model_kwargs={"max_tokens": 8192},
        )
    else:
        raise ValueError(f"Unsupported model provider: {model.provider}")


@asynccontextmanager
async def get_tools(
    mcpServers: list[MCPServerConfig], hiveInstances: list[HiveInstance]
):
    if not mcpServers and not hiveInstances:
        yield []
        return

    config = {}

    if mcpServers:
        for mcpServer in mcpServers:
            config[mcpServer.name] = {
                "url": mcpServer.url,
                "transport": mcpServer.transport,
            }

    if hiveInstances:
        for hiveInstance in hiveInstances:
            config[hiveInstance.id] = {
                "url": f"{MCP_SERVER_URL}/{hiveInstance.id}/sse?x-api-key={hiveInstance.apiKey.key}",
                "transport": "sse",
            }

    async with MultiServerMCPClient(config) as client:
        logger.info(f"Loaded {len(client.get_tools())} tools")
        yield client.get_tools()


class Agent:
    def __init__(
        self,
        name: str,
        prompt: str = None,
        model: Union[str, Model] = "claude-3-5-sonnet-20240620",
        supported_content_types: list[str] = ["text", "text/plain"],
        initial_state: list[BaseMessage] = None,
        tools: list = None,
    ):
        self.name = name
        self.prompt = prompt

        # Handle both string and Model object inputs for backward compatibility
        if isinstance(model, str):
            # Default to Anthropic for string inputs
            model_obj = Model(name=model, provider=LLMProvider.ANTHROPIC)
        else:
            model_obj = model

        self.model = _create_llm_instance(model_obj)
        self.supported_content_types = supported_content_types
        self.tools = tools if tools is not None else []
        self.graph = None
        self.memory = MemorySaver()
        self.initial_state = initial_state

    def _prompt(self, prompt: str):
        return f"""
        {prompt}

        Remember: 
        - Your job is to complete the given task.
        - You can ask user for additional information if needed to complete the task. Respond with input_required status and provide a message to the user.
        - If task can not be completed even with additional input from user or if you are not supposed to entertain such requests, respond with error status and provide an error message to the user.
        - If task is completed, respond with completed status and provide a final response to the user. Do not ask any follow up question to continue the chat.
        """

    async def initialize_graph(self, sessionId: str):
        if self.graph:
            return

        self.graph = create_react_agent(
            self.model,
            prompt=self.prompt,
            tools=self.tools,
            checkpointer=self.memory,
        )

        if self.initial_state:
            self.graph.update_state(
                self._get_config(sessionId), {"messages": self.initial_state}
            )

    def _get_config(self, session_id: str):
        return {"configurable": {"thread_id": session_id}}

    async def stream(
        self, message: HumanMessage, session_id: str
    ) -> AsyncIterable[Union[AIMessageChunk, ToolMessageChunk]]:
        await self.initialize_graph(session_id)
        inputs = {"messages": [message]}
        config = self._get_config(session_id)

        logger.info(
            f"Streaming agent with query: {message}, sessionId: {session_id}, current state: {self.graph.get_state(config)}"
        )

        async for chunk, _ in self.graph.astream(
            inputs, config, stream_mode="messages"
        ):
            # print(f"Stream event => {chunk}")
            yield chunk

    def get_current_state(self, session_id: str):
        return self.graph.get_state(self._get_config(session_id))
