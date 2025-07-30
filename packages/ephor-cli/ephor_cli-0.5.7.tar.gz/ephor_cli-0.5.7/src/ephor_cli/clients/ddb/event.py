import datetime
from typing import List

from ephor_cli.clients.ddb.base import BaseDDBClient
from ephor_cli.types.event import Event


class EventDDBClient(BaseDDBClient):
    """DynamoDB client for event operations."""

    def _get_event_pk(self, user_id: str, project_id: str, conversation_id: str) -> str:
        """Create the partition key for an event."""
        return (
            f"USER#{user_id}#PROJECT#{project_id}#CONVERSATION#{conversation_id}#EVENTS"
        )

    def _get_event_sk(self, event_id: str) -> str:
        """Create the sort key for an event."""
        return f"EVENT#{event_id}"

    def store_event(
        self, user_id: str, project_id: str, conversation_id: str, event: Event
    ) -> bool:
        """Store an event in DynamoDB.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the event belongs to
            event: The event to store

        Returns:
            True if successful, False otherwise
        """
        try:
            item = {
                "created_at": datetime.datetime.utcnow().isoformat(),
                **event.model_dump(),
                "PK": self._get_event_pk(user_id, project_id, conversation_id),
                "SK": self._get_event_sk(event.id),
            }

            self.table.put_item(Item=self.sanitize_for_dynamodb(item))
            return True
        except Exception as e:
            print(f"Error storing event: {e}")
            return False

    def list_events(
        self, user_id: str, project_id: str, conversation_id: str
    ) -> List[Event]:
        """List all events for a conversation.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation to get events for

        Returns:
            A list of events
        """
        response = self.table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={
                ":pk": self._get_event_pk(user_id, project_id, conversation_id)
            },
        )

        events = []
        for item in response.get("Items", []):
            # Remove DynamoDB-specific fields
            for key in ["PK", "SK", "created_at"]:
                if key in item:
                    del item[key]
            events.append(item)

        return [Event(**event) for event in events]

    def delete_event(
        self, user_id: str, project_id: str, conversation_id: str, event_id: str
    ) -> bool:
        """Delete an event from DynamoDB.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the event belongs to
            event_id: The ID of the event to delete

        Returns:
            True if the event was deleted successfully, False otherwise
        """
        try:
            self.table.delete_item(
                Key={
                    "PK": self._get_event_pk(user_id, project_id, conversation_id),
                    "SK": self._get_event_sk(event_id),
                }
            )
            return True
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False
