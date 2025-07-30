import datetime
from typing import Optional, List

from ephor_cli.clients.ddb.base import BaseDDBClient
from ephor_cli.types.conversation import ConversationMetadata


class ConversationDDBClient(BaseDDBClient):
    """DynamoDB client for conversation operations."""

    def _get_conversation_pk(self, user_id: str, project_id: str) -> str:
        """Create the partition key for a conversation."""
        return f"USER#{user_id}#PROJECT#{project_id}#CONVERSATIONS"

    def _get_conversation_sk(self, conversation_id: str) -> str:
        """Create the sort key for a conversation."""
        return f"CONVERSATION#{conversation_id}"

    def store_conversation_metadata(
        self, conversation: ConversationMetadata
    ) -> ConversationMetadata:
        """Store a conversation metadata in DynamoDB.

        Args:
            conversation: The conversation object to store

        Returns:
            The same conversation object
        """
        # Store conversation metadata
        conversation_dict = conversation.model_dump()

        conversation_dict.pop("messages", [])
        conversation_dict.pop("tasks", [])
        conversation_dict.pop("events", [])
        conversation_dict.pop("agents", [])

        # Create metadata item
        metadata_item = {
            "created_at": datetime.datetime.utcnow().isoformat(),
            "updated_at": datetime.datetime.utcnow().isoformat(),
            **conversation_dict,
            "PK": self._get_conversation_pk(
                conversation.user_id, conversation.project_id
            ),
            "SK": self._get_conversation_sk(conversation.conversation_id),
        }

        # Store conversation metadata
        self.table.put_item(Item=self.sanitize_for_dynamodb(metadata_item))

        return conversation

    def get_conversation_metadata(
        self, conversation_id: str, project_id: str, user_id: str
    ) -> Optional[ConversationMetadata]:
        """Get a conversation metadata by ID without messages, tasks, or events.

        Args:
            conversation_id: The ID of the conversation to retrieve
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to

        Returns:
            The conversation metadata if found, None otherwise
        """
        response = self.table.get_item(
            Key={
                "PK": self._get_conversation_pk(user_id, project_id),
                "SK": self._get_conversation_sk(conversation_id),
            }
        )

        if "Item" not in response:
            return None

        # Remove DynamoDB-specific fields
        item = response["Item"]
        for key in ["PK", "SK"]:
            if key in item:
                del item[key]
        # Use Pydantic to convert dict to ConversationMetadata
        return ConversationMetadata.model_validate(item)

    def list_conversation_metadatas(
        self, user_id: str, project_id: str
    ) -> List[ConversationMetadata]:
        """List all conversations metadata for a user and project.

        Args:
            user_id: The ID of the user who owns the conversations
            project_id: The ID of the project the conversations belong to

        Returns:
            A list of conversation metadata
        """
        response = self.table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={
                ":pk": self._get_conversation_pk(user_id, project_id)
            },
        )

        conversations = []
        for item in response.get("Items", []):
            # Remove DynamoDB-specific fields
            for key in ["PK", "SK"]:
                if key in item:
                    del item[key]
            # Use Pydantic to convert dict to ConversationMetadata
            conversations.append(ConversationMetadata.model_validate(item))

        return conversations

    def update_conversation_metadata(
        self, user_id: str, project_id: str, conversation_id: str, updates: dict
    ) -> bool:
        """Update an existing conversation metadata in DynamoDB.

        This method allows updating specific fields of a conversation without
        requiring the entire Conversation object.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation to update
            updates: Dictionary of fields to update and their new values

        Returns:
            True if the update was successful, False otherwise
        """
        if not updates:
            return False

        updates.pop("messages", [])
        updates.pop("tasks", [])
        updates.pop("events", [])
        updates.pop("agents", [])

        # Build update expression dynamically
        update_expression_parts = ["SET updated_at = :updated_at"]
        expression_attr_values = {":updated_at": datetime.datetime.utcnow().isoformat()}
        expression_attr_names = {}

        # Add each field to the update expression
        for key, value in updates.items():
            # Sanitize for DynamoDB
            value = self.sanitize_for_dynamodb(value)

            update_expression_parts.append(f"#{key} = :{key}")
            expression_attr_values[f":{key}"] = value
            expression_attr_names[f"#{key}"] = key

        update_expression = ", ".join(update_expression_parts)

        try:
            result = self.table.update_item(
                Key={
                    "PK": self._get_conversation_pk(user_id, project_id),
                    "SK": self._get_conversation_sk(conversation_id),
                },
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attr_names,
                ExpressionAttributeValues=expression_attr_values,
            )
            print("Result", result)
            return True
        except Exception as e:
            print(f"DynamoDB update_conversation error: {type(e).__name__}: {str(e)}")
            import traceback

            traceback.print_exc()
            return False

    def delete_conversation_metadata(
        self, conversation_id: str, project_id: str, user_id: str
    ) -> bool:
        """Delete a conversation metadata.

        Args:
            conversation_id: The ID of the conversation to delete
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to

        Returns:
            True if the conversation was deleted, False otherwise
        """
        try:
            self.table.delete_item(
                Key={
                    "PK": self._get_conversation_pk(user_id, project_id),
                    "SK": self._get_conversation_sk(conversation_id),
                }
            )
            return True
        except Exception as e:
            print(f"Error deleting conversation: {e}")
            return False
