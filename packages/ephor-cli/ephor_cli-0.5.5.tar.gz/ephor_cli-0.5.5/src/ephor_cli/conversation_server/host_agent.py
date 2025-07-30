import asyncio
import json
import uuid
from typing import Any, AsyncIterable, Callable, List, Union, Tuple

from ephor_cli.types.sse import SSEEvent
from google_a2a.common.client import A2ACardResolver, A2AClient
from google_a2a.common.types import (
    AgentCard,
    Message,
    TaskSendParams,
    TaskIdParams,
    TextPart,
    TaskState,
)
from langchain.tools.base import StructuredTool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    ToolMessageChunk,
)
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.utils import messages_from_dict
from langchain_core.messages.base import message_to_dict

from ephor_cli.services import task_service


class HostAgent:
    """The host agent.

    This is the agent responsible for choosing which remote agents to send
    tasks to and coordinate their work.
    """

    conversation_id: str
    user_id: str
    project_id: str
    remote_agent_addresses: List[str]
    initial_state: list[BaseMessage]
    callback: Callable[[Any], None]
    active_tasks: dict[str, dict[str, Any]]

    def __init__(
        self,
        conversation_id: str,
        user_id: str,
        project_id: str,
        remote_agent_addresses: List[str],
        initial_state: list[BaseMessage] = None,
        enqueue_event_for_sse: Callable[[Any], None] = None,
    ):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.project_id = project_id
        self.agent_clients: dict[str, A2AClient] = {}
        self.agent_cards: dict[str, AgentCard] = {}
        self.enqueue_event_for_sse = enqueue_event_for_sse
        for address in remote_agent_addresses:
            self._create_agent_client(address)
        agent_info = []
        for ra in self._list_remote_agents():
            agent_info.append(json.dumps(ra))
        self.agents = "\n".join(agent_info)
        self.memory = MemorySaver()
        self._agent: CompiledGraph = self._create_agent(initial_state)
        self.active_tasks = {}  # task_id -> {"client": client, "request": request}

    def _create_agent_client(
        self, remote_agent_address: str
    ) -> Tuple[A2AClient, AgentCard]:
        print(f"Creating agent client for {remote_agent_address}")
        card_resolver = A2ACardResolver(remote_agent_address)
        card = card_resolver.get_agent_card()
        client = A2AClient(card)
        self.agent_clients[card.name] = client
        self.agent_cards[card.name] = card

    def _create_agent(self, initial_state: list[BaseMessage] = None) -> CompiledGraph:
        model = ChatAnthropic(model="claude-3-5-sonnet-20240620", max_tokens=8192)
        config = self._get_config()
        agent = create_react_agent(
            model,
            prompt=self.root_instruction(),
            tools=[
                StructuredTool.from_function(self.list_remote_agents),
                StructuredTool.from_function(self.send_task),
            ],
            checkpointer=self.memory,
        )
        if initial_state:
            agent.update_state(config, {"messages": initial_state})
        return agent

    def root_instruction(self) -> str:
        return f"""You are an expert delegator that can delegate the user request to the appropriate remote agents.

Discovery:
- You can use `list_remote_agents` to list the available remote agents you can use to delegate the task.

Execution:
- For actionable tasks, you can use `send_task` to assign tasks to remote agents to perform.
- `send_task` should always be passed the agent name and the message to send to the agent.

Please rely on agents to address the request, and don't make up the response. If you are not sure, please ask the user for more details.
Focus on the most recent parts of the conversation primarily.

RESPONSE FORMAT:
- Your responses must ALWAYS be one line only
- When a remote agent completes a task, simply acknowledge and ask "What else can I help you with?"
- Never repeat or summarize responses from remote agents - users see those directly
- If an agent's response contains questions or needs more input, relay those questions to the user and ask them to provide the needed information

Example responses:
- "Task delegated to CodeAgent, waiting for completion."
- "Task completed successfully. What else can I help you with?"
- "Could you please provide more details about your request?"
- "The agent needs to know: 1) What programming language to use? 2) Should it include tests?"

Agents:
{self.agents}"""

    def _list_remote_agents(self):
        """List the available remote agents you can use to delegate the task."""
        if not self.agent_clients:
            return []

        remote_agent_info = []
        for card in self.agent_cards.values():
            remote_agent_info.append(
                {"name": card.name, "description": card.description}
            )
        return remote_agent_info

    def list_remote_agents(self):
        """List the available remote agents you can use to delegate the task."""
        return self._list_remote_agents()

    def send_task(self, agent_name: str, message: str):
        """Sends a task either streaming (if supported) or non-streaming.

        This will send a message to the remote agent named agent_name.

        Args:
          agent_name: The name of the agent to send the task to.
          message: The message to send to the agent for the task.
          tool_context: The tool context this method runs in.

        Yields:
          A dictionary of JSON data.
        """
        # Create a new event loop to run the async function
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self._send_task(agent_name, message))
        finally:
            loop.close()

    def _get_config(self):
        return {"configurable": {"thread_id": self.conversation_id}}

    def _get_tool_call_id(self, agent_name: str, query: str):
        """Get the tool call id for the given message."""
        state = self.get_current_state()
        messages = state.values.get("messages", [])
        for message in messages[::-1]:
            if isinstance(message, AIMessage) and message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_call_name = tool_call["name"]
                    tool_call_args = tool_call["args"]
                    if (
                        tool_call_name == "send_task"
                        and tool_call_args.get("agent_name") == agent_name
                        and tool_call_args.get("message") == query
                    ):
                        return tool_call["id"]
        return None

    async def _send_task(self, agent_name: str, message: str):
        """Sends a task either streaming (if supported) or non-streaming.

        This will send a message to the remote agent named agent_name.

        Args:
          agent_name: The name of the agent to send the task to.
          message: The message to send to the agent for the task.
          tool_context: The tool context this method runs in.

        Yields:
          A dictionary of JSON data.
        """
        print(f"Sending task to {agent_name} with message: {message}")
        if agent_name not in self.agent_clients:
            raise ValueError(f"Agent {agent_name} not found")
        client = self.agent_clients[agent_name]
        if not client:
            raise ValueError(f"Client not available for {agent_name}")
        tool_call_id = self._get_tool_call_id(agent_name, message)
        if not tool_call_id:
            raise ValueError(f"Tool call id not found for {agent_name}")
        task_id = str(uuid.uuid4())
        metadata = {
            "task_id": task_id,
            "tool_call_id": tool_call_id,
            "conversation_id": self.conversation_id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "agent_name": agent_name,
        }
        request: TaskSendParams = TaskSendParams(
            id=task_id,
            sessionId=self.conversation_id,
            message=Message(
                role="user",
                parts=[TextPart(text=message)],
                metadata=metadata,
            ),
            acceptedOutputModes=["text", "text/plain", "image/png"],
            metadata=metadata,
        )

        # Store task reference before sending
        self.active_tasks[task_id] = {
            "client": client,
            "request": request
        }

        stream = client.send_task_streaming(request)
        try:
            async for response in stream:
                event = response.result
                if (
                    hasattr(event, "status")
                    and hasattr(event.status, "message")
                    and event.status.message
                ):
                    if event.status.state in [
                        TaskState.COMPLETED,
                        TaskState.FAILED,
                        TaskState.CANCELED,
                    ]:
                        print(f"Task status update: {event}")
                        break

                    status_message = event.status.message
                    if hasattr(status_message, "parts") and status_message.parts:
                        content = status_message.parts[0].text
                        content = json.loads(content)
                        chunk = messages_from_dict([content])[0]
                        sse_event = SSEEvent(
                            actor=agent_name,
                            content=json.dumps(message_to_dict(chunk)),
                            # content=content,
                        )
                    await self.enqueue_event_for_sse(sse_event)
                    print("[HostAgent] Successfully put event in the queue")
                if hasattr(event, "final") and event.final:
                    break
        except Exception as e:
            print(f"Error streaming task response: {e}")
        finally:
            await stream.aclose()
            # Remove task from active tasks when complete
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]

        task = task_service.get_task(
            self.user_id,
            self.project_id,
            self.conversation_id,
            agent_name,
            task_id,
        )

        try:
            response = {
                "response": task.status.message.parts,
            }
        except Exception as e:
            print(f"Error getting task response: {e}")
            response = {
                "response": str(task.status.message),
            }
        return response

    async def astream(
        self, message: BaseMessage
    ) -> AsyncIterable[Union[AIMessageChunk, ToolMessageChunk]]:
        inputs = {"messages": [message]}
        config = self._get_config()

        print(
            f"Streaming agent with message: {message}, current state: {self._agent.get_state(config)}"
        )

        async for item, _ in self._agent.astream(
            inputs, config, stream_mode="messages"
        ):
            # print(f"Stream event => {item}")
            yield item

    def get_current_state(self):
        config = self._get_config()
        return self._agent.get_state(config)

    async def cancel_all_tasks(self):
        """Cancel all active remote agent tasks."""
        for task_id, task_info in list(self.active_tasks.items()):
            client = task_info["client"]
            try:
                # Call the A2AClient's cancel_task method with just the task ID
                await client.cancel_task(TaskIdParams(id=task_id))
                print(f"Successfully cancelled task {task_id}")
                # Remove from active tasks
                del self.active_tasks[task_id]
            except Exception as e:
                print(f"Error cancelling task {task_id}: {e}")
        
        return {"cancelled": True, "total_tasks": len(self.active_tasks)}
