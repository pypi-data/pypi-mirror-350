import datetime
import uuid
from typing import List

from ephor_cli.clients.ddb.event import EventDDBClient
from ephor_cli.constant import DYNAMODB_TABLE_NAME
from ephor_cli.types.event import Event
from langchain_core.messages import BaseMessage


class EventService:
    """Service for high-level event operations.

    This service uses the EventDDBClient for low-level DynamoDB operations.
    """

    def __init__(
        self, table_name: str = DYNAMODB_TABLE_NAME, region: str = "us-east-1"
    ):
        """Initialize the Event Service.

        Args:
            table_name: The name of the DynamoDB table
            region: AWS region for the DynamoDB table
        """
        self.client = EventDDBClient(table_name, region)

    def create_event(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        actor: str,
        message: BaseMessage,
    ) -> Event:
        """Create a new event.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the event belongs to
            event: The event data to store

        Returns:
            True if the event was created successfully, False otherwise
        """
        event = Event(
            id=str(uuid.uuid4()),
            actor=actor,
            content=message,
            timestamp=datetime.datetime.utcnow().timestamp(),
        )
        self.client.store_event(user_id, project_id, conversation_id, event)
        return event

    def list_events(
        self, user_id: str, project_id: str, conversation_id: str
    ) -> List[Event]:
        """Get all events for a conversation.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation to get events for

        Returns:
            A list of events
        """
        return self.client.list_events(user_id, project_id, conversation_id)

    def delete_event(
        self, user_id: str, project_id: str, conversation_id: str, event_id: str
    ) -> bool:
        """Delete an event.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the event belongs to
            event_id: The ID of the event to delete

        Returns:
            True if the event was deleted successfully, False otherwise
        """
        return self.client.delete_event(user_id, project_id, conversation_id, event_id)

    def delete_events(
        self, user_id: str, project_id: str, conversation_id: str
    ) -> bool:
        """Delete all events for a conversation."""
        events = self.list_events(user_id, project_id, conversation_id)
        for event in events:
            self.delete_event(user_id, project_id, conversation_id, event.id)
        return True
