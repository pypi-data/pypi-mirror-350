import json
import uuid
from typing import Any, Callable

from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.messages.base import message_to_dict

from ephor_cli.conversation_server.host_agent import HostAgent
from ephor_cli.services import (
    agent_service,
    message_service,
)
from ephor_cli.utils.chunk_streamer import ChunkStreamer
from ephor_cli.utils.sanitize_message import sanitize_message
from ephor_cli.types.sse import SSEEvent


class ADKHostManager:
    """An implementation of memory based management with fake agent actions

    This implements the interface of the ApplicationManager to plug into
    the AgentServer. This acts as the service contract that the Mesop app
    uses to send messages to the agent and provide information for the frontend.
    """

    def __init__(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        enqueue_event_for_sse: Callable[[Any], None],
    ):
        self.user_id = user_id
        self.project_id = project_id
        self.conversation_id = conversation_id
        self.enqueue_event_for_sse = enqueue_event_for_sse
        self.chunk_streamer = ChunkStreamer()
        self.host_agent = self._create_host_agent()

    def _create_host_agent(self) -> HostAgent:
        """Get or create a host agent for a specific conversation."""
        agents = agent_service.list_agents(
            self.user_id, self.project_id, self.conversation_id
        )
        messages = message_service.list_messages(
            self.user_id, self.project_id, self.conversation_id
        )

        messages = sanitize_message(messages)

        return HostAgent(
            conversation_id=self.conversation_id,
            project_id=self.project_id,
            user_id=self.user_id,
            remote_agent_addresses=[agent.url for agent in agents],
            initial_state=messages,
            enqueue_event_for_sse=self.enqueue_event_for_sse,
        )

    def sanitize_message(self, message: BaseMessage) -> BaseMessage:
        messages = message_service.list_messages(
            self.user_id, self.project_id, self.conversation_id
        )
        if messages:
            message.additional_kwargs.update({"last_message_id": messages[-1].id})
        return message

    def _add_new_messages(self, message: BaseMessage, new_messages: list[BaseMessage]):
        last_message_id = message.id
        for new_message in new_messages:
            new_message.id = str(uuid.uuid4())
            new_message.additional_kwargs.update({"last_message_id": last_message_id})
            if isinstance(new_message, AIMessage):
                new_message.additional_kwargs["agent"] = "host_agent"
            message_service.add_message(
                self.user_id, self.project_id, self.conversation_id, new_message
            )
            last_message_id = new_message.id

    async def cancel(self, message_id: str = None):
        """Cancel current message processing and all active remote agent tasks."""
        print(f"[HostManager] Cancelling message {message_id}")
        await self.host_agent.cancel_all_tasks()
        self.chunk_streamer.cancel()

    async def process_message(self, message: BaseMessage):
        print(f"Processing message: {message.model_dump_json(exclude_none=True)}")

        self.chunk_streamer.reset()
        async for chunk in self.chunk_streamer.process(
            self.host_agent.astream(message)
        ):
            sse_event = SSEEvent(
                actor="host_agent",
                content=json.dumps(message_to_dict(chunk)),
            )

            await self.enqueue_event_for_sse(sse_event)
            print("[HostManager] Successfully put event in the queue")

        messages = self.chunk_streamer.messages
        self._add_new_messages(message, messages)
