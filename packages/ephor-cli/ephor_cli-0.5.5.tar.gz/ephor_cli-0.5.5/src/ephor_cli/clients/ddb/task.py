import datetime

from ephor_cli.clients.ddb.base import BaseDDBClient
from ephor_cli.types.task import TaskMetadata


class TaskDDBClient(BaseDDBClient):
    """DynamoDB client for task operations."""

    def _get_task_pk(self, user_id: str, project_id: str, conversation_id: str) -> str:
        """Create the partition key for a task."""
        return (
            f"USER#{user_id}#PROJECT#{project_id}#CONVERSATION#{conversation_id}#TASKS"
        )

    def _get_task_sk(self, agent_name: str, task_id: str) -> str:
        """Create the sort key for a task."""
        return f"AGENT#{agent_name}#TASK#{task_id}"

    def store_task_metadata(self, task: TaskMetadata):
        """Store a task in DynamoDB.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the task belongs to
            task: The task to store

        Returns:
            True if successful, False otherwise
        """
        task_dict = task.model_dump()

        task_dict.pop("history", [])
        task_dict.pop("artifacts", [])

        try:
            item = {
                "created_at": datetime.datetime.utcnow().isoformat(),
                **task_dict,
                "PK": self._get_task_pk(
                    task.user_id, task.project_id, task.conversation_id
                ),
                "SK": self._get_task_sk(task.agent_name, task.id),
            }

            self.table.put_item(Item=self.sanitize_for_dynamodb(item))
        except Exception as e:
            print(f"Error storing task: {e}")
            raise e

    def delete_task_metadata(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        agent_name: str,
        task_id: str,
    ) -> bool:
        """Delete a task from DynamoDB.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the task belongs to
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted successfully, False otherwise
        """
        try:
            self.table.delete_item(
                Key={
                    "PK": self._get_task_pk(user_id, project_id, conversation_id),
                    "SK": self._get_task_sk(agent_name, task_id),
                }
            )
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False

    def update_task_metadata(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        agent_name: str,
        task_id: str,
        updates: dict,
    ) -> bool:
        """Update fields of a task in DynamoDB."""
        if not updates:
            return False
        update_expression_parts = ["SET updated_at = :updated_at"]
        expression_attr_values = {":updated_at": datetime.datetime.utcnow().isoformat()}
        expression_attr_names = {}
        for key, value in updates.items():
            update_expression_parts.append(f"#{key} = :{key}")
            expression_attr_values[f":{key}"] = self.sanitize_for_dynamodb(value)
            expression_attr_names[f"#{key}"] = key
        update_expression = ", ".join(update_expression_parts)
        try:
            self.table.update_item(
                Key={
                    "PK": self._get_task_pk(user_id, project_id, conversation_id),
                    "SK": self._get_task_sk(agent_name, task_id),
                },
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attr_names,
                ExpressionAttributeValues=expression_attr_values,
            )
            return True
        except Exception as e:
            print(f"Error updating task: {e}")
            return False

    def list_task_metadatas(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        agent_name: str = None,
    ) -> list[TaskMetadata]:
        """List all tasks for a conversation.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation to get tasks for

        Returns:
            A list of TaskMetadata
        """
        key_condition_expression = "PK = :pk"
        expression_attribute_values = {
            ":pk": self._get_task_pk(user_id, project_id, conversation_id)
        }

        if agent_name:
            key_condition_expression = "PK = :pk and begins_with(SK, :sk)"
            expression_attribute_values[":sk"] = f"AGENT#{agent_name}#TASK#"

        response = self.table.query(
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )

        tasks = []
        for item in response.get("Items", []):
            # Remove DynamoDB-specific fields
            for key in ["PK", "SK", "created_at"]:
                if key in item:
                    del item[key]
            tasks.append(TaskMetadata.model_validate(item))

        return tasks

    def get_task_metadata(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        agent_name: str,
        task_id: str,
    ) -> TaskMetadata | None:
        """Get a single task metadata by ID without artifacts or history.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the task belongs to
            task_id: The ID of the task to retrieve

        Returns:
            The TaskMetadata if found, None otherwise
        """
        response = self.table.get_item(
            Key={
                "PK": self._get_task_pk(user_id, project_id, conversation_id),
                "SK": self._get_task_sk(agent_name, task_id),
            }
        )

        if "Item" not in response:
            return None

        item = response["Item"]
        for key in ["PK", "SK", "created_at"]:
            if key in item:
                del item[key]
        return TaskMetadata.model_validate(item)
