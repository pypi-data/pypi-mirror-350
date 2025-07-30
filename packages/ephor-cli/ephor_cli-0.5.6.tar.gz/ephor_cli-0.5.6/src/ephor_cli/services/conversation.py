import uuid
from datetime import datetime, timezone
from typing import List, Optional

from ephor_cli.clients.ddb.conversation import ConversationDDBClient
from ephor_cli.constant import DYNAMODB_TABLE_NAME
from ephor_cli.services.agent import AgentService
from ephor_cli.services.event import EventService
from ephor_cli.services.message import MessageService
from ephor_cli.services.task import TaskService
from ephor_cli.types.conversation import (
    Conversation,
    ConversationMetadata,
)


class ConversationService:
    """Service for high-level conversation operations.

    This service coordinates with other services to provide complete conversation functionality.
    """

    def __init__(
        self, table_name: str = DYNAMODB_TABLE_NAME, region: str = "us-east-1"
    ):
        """Initialize the Conversation Service.

        Args:
            table_name: The name of the DynamoDB table
            region: AWS region for the DynamoDB table
        """
        self.client = ConversationDDBClient(table_name, region)
        self.message_service = MessageService(table_name, region)
        self.task_service = TaskService(table_name, region)
        self.event_service = EventService(table_name, region)
        self.agent_service = AgentService(table_name, region)

    def create_conversation(
        self, user_id: str, project_id: str
    ) -> ConversationMetadata:
        """Create a new conversation for a user and project.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to

        Returns:
            The created conversation
        """
        now = datetime.now(timezone.utc).isoformat()
        conversation = ConversationMetadata(
            conversation_id=str(uuid.uuid4()),
            user_id=user_id,
            project_id=project_id,
            name="",
            created_at=now,
            updated_at=now,
        )
        self.client.store_conversation_metadata(conversation)
        return conversation

    def get_conversation(
        self, user_id: str, project_id: str, conversation_id: str
    ) -> Optional[Conversation]:
        """Get a complete conversation with its messages, tasks, and events.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation to retrieve

        Returns:
            The complete conversation or None if not found
        """
        # Get the conversation metadata
        conversation = self.client.get_conversation_metadata(
            conversation_id, project_id, user_id
        )

        if not conversation:
            return None

        # Get all messages, tasks, and events for this conversation
        messages = self.message_service.list_messages(
            user_id, project_id, conversation_id
        )
        tasks = self.task_service.list_tasks(
            user_id, project_id, conversation_id, fetch_history=True
        )
        events = self.event_service.list_events(user_id, project_id, conversation_id)
        agents = self.agent_service.list_agents(user_id, project_id, conversation_id)

        # Update the conversation with the retrieved data
        conversation_dict = conversation.model_dump()
        conversation_dict["messages"] = messages
        conversation_dict["tasks"] = tasks
        conversation_dict["events"] = events
        conversation_dict["agents"] = agents

        return Conversation.model_validate(conversation_dict)

    def list_conversations(
        self, user_id: str, project_id: str
    ) -> List[ConversationMetadata]:
        """List all conversations for a user and project.

        Args:
            user_id: The ID of the user who owns the conversations
            project_id: The ID of the project the conversations belong to

        Returns:
            A list of conversation metadata
        """
        return self.client.list_conversation_metadatas(user_id, project_id)

    def update_conversation_metadata(
        self, user_id: str, project_id: str, conversation_id: str, updates: dict
    ) -> bool:
        """Update an existing conversation's metadata.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation to update
            updates: Dictionary of fields to update and their new values

        Returns:
            True if successful, False otherwise
        """
        return self.client.update_conversation_metadata(
            user_id, project_id, conversation_id, updates
        )

    def delete_conversation(
        self, user_id: str, project_id: str, conversation_id: str
    ) -> bool:
        """Delete a conversation and all its related data.

        This will delete the conversation metadata as well as all messages, tasks,
        and events associated with the conversation.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation to delete

        Returns:
            True if successful, False otherwise
        """
        self.message_service.delete_messages(user_id, project_id, conversation_id)
        self.task_service.delete_tasks(user_id, project_id, conversation_id)
        self.event_service.delete_events(user_id, project_id, conversation_id)
        self.agent_service.deregister_agents(user_id, project_id, conversation_id)
        return self.client.delete_conversation_metadata(
            conversation_id, project_id, user_id
        )
