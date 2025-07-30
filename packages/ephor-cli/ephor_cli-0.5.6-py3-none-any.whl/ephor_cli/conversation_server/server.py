import asyncio
from typing import Any, Dict
import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse

from ephor_cli.conversation_server.host_manager import ADKHostManager
from ephor_cli.services.agent import AgentService
from ephor_cli.services.conversation import ConversationService
from ephor_cli.services.event import EventService
from ephor_cli.services.message import MessageService
from ephor_cli.services.task import TaskService
from ephor_cli.types.agent import (
    DeregisterAgentRequest,
    DeregisterAgentResponse,
    ListAgentRequest,
    ListAgentResponse,
    RegisterAgentRequest,
    RegisterAgentResponse,
)
from ephor_cli.types.conversation import (
    CreateConversationRequest,
    CreateConversationResponse,
    GetConversationRequest,
    GetConversationResponse,
    DeleteConversationRequest,
    DeleteConversationResponse,
    ListConversationRequest,
    ListConversationResponse,
)
from ephor_cli.types.event import (
    ListEventRequest,
    ListEventResponse,
)
from ephor_cli.types.message import (
    ListMessageRequest,
    ListMessageResponse,
    MessageInfo,
    SendMessageRequest,
    SendMessageResponse,
    CancelMessageRequest,
    CancelMessageResponse,
)
from ephor_cli.types.task import (
    ListTaskRequest,
    ListTaskResponse,
    GetTaskRequest,
    GetTaskResponse,
)
from ephor_cli.types.sse import (
    SSEConnectionRequest,
)
from langchain_core.messages.utils import messages_from_dict
from langchain_core.messages.base import messages_to_dict


class ConversationServer:
    """ConversationServer is the backend to serve the agent interactions in the UI

    This defines the interface that is used by the Mesop system to interact with
    agents and provide details about the executions.
    """

    def __init__(self, router: APIRouter):
        self.conversation_service = ConversationService()
        self.agent_service = AgentService()
        self.message_service = MessageService()
        self.task_service = TaskService()
        self.event_service = EventService()

        # SSE message streams: message_id -> List[asyncio.Queue]
        self.sse_message_streams: Dict[str, list[asyncio.Queue]] = {}
        self.sse_lock = asyncio.Lock()

        # Track active message processing (message_id -> ADKHostManager)
        self.active_managers = {}

        # Add a lock for thread safety when accessing the dictionary
        self.managers_lock = asyncio.Lock()

        # Add root health check endpoint
        router.add_api_route(
            "/",
            self._health_check,
            methods=["GET"],
            summary="Root health check endpoint",
            description="Returns a 200 OK status when the server is healthy",
            tags=["Health"],
        )
        router.add_api_route(
            "/health",
            self._health_check,
            methods=["GET"],
            summary="Health check endpoint",
            description="Returns a 200 OK status when the server is healthy",
            tags=["Health"],
        )
        router.add_api_route(
            "/conversation/create",
            self._create_conversation,
            methods=["POST"],
            response_model=CreateConversationResponse,
            summary="Create a new conversation",
            description="Creates a new conversation and returns the conversation details",
            tags=["Conversation"],
        )
        router.add_api_route(
            "/conversation/get",
            self._get_conversation,
            methods=["POST"],
            response_model=GetConversationResponse,
            summary="Get a conversation",
            tags=["Conversation"],
        )
        router.add_api_route(
            "/conversation/list",
            self._list_conversations,
            methods=["POST"],
            response_model=ListConversationResponse,
            summary="List all conversations",
            description="Returns a list of all available conversations",
            tags=["Conversation"],
        )
        router.add_api_route(
            "/conversation/delete",
            self._delete_conversation,
            methods=["POST"],
            response_model=DeleteConversationResponse,
            summary="Delete a conversation",
            description="Deletes an existing conversation and all associated data",
            tags=["Conversation"],
        )
        router.add_api_route(
            "/agent/register",
            self._register_agent,
            methods=["POST"],
            response_model=RegisterAgentResponse,
            summary="Register an agent",
            description="Registers a new agent with the specified URL",
            tags=["Agent"],
        )
        router.add_api_route(
            "/agent/deregister",
            self._deregister_agent,
            methods=["POST"],
            response_model=DeregisterAgentResponse,
            summary="Deregister an agent",
            description="Deregisters an agent from the specified conversation",
            tags=["Agent"],
        )
        router.add_api_route(
            "/agent/list",
            self._list_agents,
            methods=["POST"],
            response_model=ListAgentResponse,
            summary="List agents",
            description="Lists all registered agents",
            tags=["Agent"],
        )
        router.add_api_route(
            "/message/list",
            self._list_messages,
            methods=["POST"],
            response_model=ListMessageResponse,
            summary="List messages",
            description="Lists all messages for a specified conversation",
            tags=["Message"],
        )
        router.add_api_route(
            "/message/send",
            self._send_message,
            methods=["POST"],
            response_model=SendMessageResponse,
            summary="Send a message",
            description="Sends a message to the specified conversation",
            tags=["Message"],
        )
        router.add_api_route(
            "/task/list",
            self._list_tasks,
            methods=["POST"],
            response_model=ListTaskResponse,
            summary="List tasks",
            description="Lists all active tasks",
            tags=["Task"],
        )
        router.add_api_route(
            "/task/get",
            self._get_task,
            methods=["POST"],
            response_model=GetTaskResponse,
            summary="Get a task",
            description="Get a single task by ID, including its metadata and history",
            tags=["Task"],
        )
        router.add_api_route(
            "/events/list",
            self._list_events,
            methods=["POST"],
            response_model=ListEventResponse,
            summary="List events",
            description="Retrieves all events",
            tags=["Event"],
        )
        router.add_api_route(
            "/sse",
            self._sse,
            methods=["POST"],
            summary="SSE endpoint for per-message updates",
            description="Establishes an SSE connection for a specific message",
            tags=["SSE"],
        )
        router.add_api_route(
            "/message/cancel",
            self._cancel_message,
            methods=["POST"],
            response_model=CancelMessageResponse,
            summary="Cancel message processing",
            description="Cancels an in-progress message and its associated agent tasks",
            tags=["Message"],
        )

    def _health_check(self):
        """Health check endpoint for ECS"""
        return JSONResponse(content={"status": "healthy"}, status_code=200)

    def _create_conversation(self, request: CreateConversationRequest = None):
        """Create a new conversation"""
        c = self.conversation_service.create_conversation(
            request.params.user_id, request.params.project_id
        )
        return CreateConversationResponse(result=c)

    def _get_conversation(self, request: GetConversationRequest = None):
        """Get a conversation"""
        c = self.conversation_service.get_conversation(
            request.params.user_id,
            request.params.project_id,
            request.params.conversation_id,
        )
        c.messages = messages_to_dict(c.messages)
        for task in c.tasks:
            task.history = messages_to_dict(task.history)
        return GetConversationResponse(result=c)

    def _list_conversations(self, request_data: ListConversationRequest):
        """List all conversations"""
        return ListConversationResponse(
            result=self.conversation_service.list_conversations(
                request_data.params.user_id, request_data.params.project_id
            )
        )

    def _delete_conversation(self, request: DeleteConversationRequest = None):
        """Delete an existing conversation"""
        try:
            result = self.conversation_service.delete_conversation(
                request.params.user_id,
                request.params.project_id,
                request.params.conversation_id,
            )
            return DeleteConversationResponse(result=result)
        except Exception as e:
            return DeleteConversationResponse(
                result=False, error=f"Failed to delete conversation: {e}"
            )

    async def _register_agent(self, request_data: RegisterAgentRequest):
        """Register a new agent"""
        try:
            agent = self.agent_service.register_agent(
                request_data.params.user_id,
                request_data.params.project_id,
                request_data.params.conversation_id,
                request_data.params.url,
            )
            if agent:
                return RegisterAgentResponse(result=agent)
            else:
                return RegisterAgentResponse(error="Failed to register agent")
        except Exception as e:
            return RegisterAgentResponse(error=f"Failed to register agent: {e}")

    async def _deregister_agent(self, request_data: DeregisterAgentRequest):
        """Deregister an agent from a conversation"""
        try:
            success = self.agent_service.deregister_agent(
                request_data.params.user_id,
                request_data.params.project_id,
                request_data.params.conversation_id,
                request_data.params.url,
            )
            return DeregisterAgentResponse(result=success)
        except Exception as e:
            return DeregisterAgentResponse(
                result=False, error=f"Failed to deregister agent: {e}"
            )

    async def _list_agents(self, request_data: ListAgentRequest):
        """List all registered agents"""
        return ListAgentResponse(
            result=self.agent_service.list_agents(
                request_data.params.user_id,
                request_data.params.project_id,
                request_data.params.conversation_id,
            )
        )

    async def _list_messages(self, request_data: ListMessageRequest):
        """List messages in a conversation"""
        messages = self.message_service.list_messages(
            request_data.params.user_id,
            request_data.params.project_id,
            request_data.params.conversation_id,
        )
        messages = messages_to_dict(messages)
        return ListMessageResponse(result=messages)

    async def setup_sse_consumer(self, message_id: str):
        async with self.sse_lock:
            if message_id not in self.sse_message_streams:
                self.sse_message_streams[message_id] = []
            sse_event_queue = asyncio.Queue()
            self.sse_message_streams[message_id].append(sse_event_queue)
            return sse_event_queue

    async def enqueue_events_for_sse(self, message_id: str, event):
        async with self.sse_lock:
            if message_id not in self.sse_message_streams:
                return
            for subscriber in self.sse_message_streams[message_id]:
                await subscriber.put(event)

    async def dequeue_events_for_sse(
        self, message_id: str, sse_event_queue: asyncio.Queue
    ):
        try:
            while True:
                data = await sse_event_queue.get()
                print(f"SSE Event: {data}")
                if data == "[[DONE]]":
                    break
                if hasattr(data, "model_dump_json"):
                    yield f"data: {data.model_dump_json()}\n\n"
                else:
                    yield f"data: {data}\n\n"
        finally:
            async with self.sse_lock:
                if message_id in self.sse_message_streams:
                    self.sse_message_streams[message_id].remove(sse_event_queue)

    async def _send_message(self, request_data: SendMessageRequest):
        print(f"Received message: {request_data.params.message}")
        message = messages_from_dict([request_data.params.message])[0]
        print(f"Message: {message}")
        message.id = str(uuid.uuid4())

        await self.setup_sse_consumer(message.id)

        async def enqueue_event_for_sse(data: Any):
            await self.enqueue_events_for_sse(message.id, data)

        self.manager = ADKHostManager(
            request_data.params.user_id,
            request_data.params.project_id,
            request_data.params.conversation_id,
            enqueue_event_for_sse,
        )

        # Track this manager
        async with self.managers_lock:
            print(f"Active managers for message {message.id} set")
            self.active_managers[message.id] = self.manager

        message = self.manager.sanitize_message(message)
        self.message_service.add_message(
            request_data.params.user_id,
            request_data.params.project_id,
            request_data.params.conversation_id,
            message,
        )
        print(
            f"Stored message: {self.message_service.get_message(request_data.params.user_id, request_data.params.project_id, request_data.params.conversation_id, message.id)}"
        )
        message_id = message.id

        async def process_and_respond():
            try:
                await self.manager.process_message(message)
                # Signal completion
                await self.enqueue_events_for_sse(message_id, "[[DONE]]")
            finally:
                # Clean up the active manager when done
                async with self.managers_lock:
                    if message_id in self.active_managers:
                        del self.active_managers[message_id]

        asyncio.create_task(process_and_respond())

        return SendMessageResponse(
            result=MessageInfo(
                message_id=message_id,
                conversation_id=request_data.params.conversation_id,
                project_id=request_data.params.project_id,
                user_id=request_data.params.user_id,
            )
        )

    def _list_events(self, request_data: ListEventRequest):
        """Get all events"""
        return ListEventResponse(
            result=self.event_service.list_events(
                request_data.params.user_id,
                request_data.params.project_id,
                request_data.params.conversation_id,
            )
        )

    def _list_tasks(self, request_data: ListTaskRequest):
        """List all tasks"""
        return ListTaskResponse(
            result=self.task_service.list_tasks(
                request_data.params.user_id,
                request_data.params.project_id,
                request_data.params.conversation_id,
            )
        )

    async def _get_task(self, request_data: GetTaskRequest):
        """Get a single task by ID, including its metadata and history"""
        task = self.task_service.get_task(
            request_data.params.user_id,
            request_data.params.project_id,
            request_data.params.conversation_id,
            request_data.params.agent_name,
            request_data.params.task_id,
        )
        return GetTaskResponse(result=task)

    def _sse(self, request_data: SSEConnectionRequest):
        message = self.message_service.get_message(
            request_data.params.user_id,
            request_data.params.project_id,
            request_data.params.conversation_id,
            request_data.params.message_id,
        )
        if not message:
            return JSONResponse(content={"error": "Message not found"}, status_code=404)
        message_id = message.id

        async def event_stream():
            sse_event_queue = await self.setup_sse_consumer(message_id)
            async for event in self.dequeue_events_for_sse(message_id, sse_event_queue):
                yield event

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    async def _cancel_message(self, request_data: CancelMessageRequest):
        """Cancel message processing and its associated agent tasks"""
        message_id = request_data.params.message_id
        print(f"Cancelling message {message_id}")

        # Check if the message is being processed
        async with self.managers_lock:
            manager = self.active_managers.get(message_id)

        if not manager:
            print(f"No active processing found for message {message_id}")
            return CancelMessageResponse(
                result=False,
                error=f"No active processing found for message {message_id}",
            )

        try:
            # Call the manager's cancel method
            result = await manager.cancel(message_id)

            return CancelMessageResponse(result=True, details=result)
        except Exception as e:
            print(f"Error cancelling message {message_id}: {e}")
            return CancelMessageResponse(
                result=False, error=f"Error during cancellation: {str(e)}"
            )
