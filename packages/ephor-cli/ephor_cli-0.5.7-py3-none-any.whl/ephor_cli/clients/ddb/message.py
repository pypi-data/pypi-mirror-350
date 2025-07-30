import datetime
from typing import List

from ephor_cli.clients.ddb.base import BaseDDBClient
from langchain_core.messages.base import messages_to_dict
from langchain_core.messages.utils import messages_from_dict
from langchain_core.messages import BaseMessage


class MessageDDBClient(BaseDDBClient):
    """DynamoDB client for message operations."""

    def _get_message_pk(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        task_id: str | None = None,
    ) -> str:
        """Create the partition key for a message."""
        if task_id:
            return f"USER#{user_id}#PROJECT#{project_id}#CONVERSATION#{conversation_id}#TASK#{task_id}#MESSAGES"
        else:
            return f"USER#{user_id}#PROJECT#{project_id}#CONVERSATION#{conversation_id}#MESSAGES"

    def _get_message_sk(self, message_id: str) -> str:
        """Create the sort key for a message."""
        return f"MESSAGE#{message_id}"

    def store_message(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        message: BaseMessage,
        task_id: str | None = None,
    ) -> bool:
        """Store a message in DynamoDB.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the message belongs to
            message: The message to store

        Returns:
            True if successful, False otherwise
        """
        message_dict = messages_to_dict([message])[0]
        message_dict = self.sanitize_for_dynamodb(message_dict)
        try:
            item = {
                "created_at": datetime.datetime.utcnow().isoformat(),
                **message_dict,
                "PK": self._get_message_pk(
                    user_id, project_id, conversation_id, task_id
                ),
                "SK": self._get_message_sk(message.id),
            }

            self.table.put_item(Item=self.sanitize_for_dynamodb(item))
            return True
        except Exception as e:
            print(f"Error storing message: {e}")
            return False

    def list_messages(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        task_id: str | None = None,
    ) -> List[BaseMessage]:
        """List all messages for a conversation.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation to get messages for

        Returns:
            A list of messages
        """
        response = self.table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={
                ":pk": self._get_message_pk(
                    user_id, project_id, conversation_id, task_id
                )
            },
        )

        messages = []
        for item in response.get("Items", []):
            # Remove DynamoDB-specific fields
            for key in ["PK", "SK", "created_at"]:
                if key in item:
                    del item[key]
            # Convert Decimal to float for JSON compatibility
            item = self.sanitize_from_dynamodb(item)
            messages.append(item)

        return messages_from_dict(messages)

    def delete_message(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        message_id: str,
        task_id: str | None = None,
    ) -> bool:
        """Delete a message from DynamoDB.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the message belongs to
            message_id: The ID of the message to delete

        Returns:
            True if the message was deleted successfully, False otherwise
        """
        try:
            self.table.delete_item(
                Key={
                    "PK": self._get_message_pk(
                        user_id, project_id, conversation_id, task_id
                    ),
                    "SK": self._get_message_sk(message_id),
                }
            )
            return True
        except Exception as e:
            print(f"Error deleting message: {e}")
            return False

    def get_message(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        message_id: str,
        task_id: str | None = None,
    ) -> BaseMessage:
        """Get a message from DynamoDB.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the message belongs to
            message_id: The ID of the message to get

        Returns:
            The message
        """
        response = self.table.get_item(
            Key={
                "PK": self._get_message_pk(
                    user_id, project_id, conversation_id, task_id
                ),
                "SK": self._get_message_sk(message_id),
            }
        )
        if "Item" in response:
            item = response["Item"]
            # Remove DynamoDB-specific fields
            for key in ["PK", "SK", "created_at"]:
                if key in item:
                    del item[key]
            # Convert Decimal to float for JSON compatibility
            item = self.sanitize_from_dynamodb(item)
            return messages_from_dict([item])[0]
        return None
