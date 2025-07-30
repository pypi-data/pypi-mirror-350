from typing import Any, List, Union

from google_a2a.common.types import TaskStatus

from ephor_cli.clients.ddb.task import TaskDDBClient
from ephor_cli.constant import DYNAMODB_TABLE_NAME
from ephor_cli.services.message import MessageService
from ephor_cli.types.task import Task, TaskMetadata


class TaskService:
    """Service for high-level task operations.

    This service uses the TaskDDBClient for low-level DynamoDB operations.
    """

    def __init__(
        self, table_name: str = DYNAMODB_TABLE_NAME, region: str = "us-east-1"
    ):
        """Initialize the Task Service.

        Args:
            table_name: The name of the DynamoDB table
            region: AWS region for the DynamoDB table
        """
        self.client = TaskDDBClient(table_name, region)
        self.message_service = MessageService(table_name, region)

    def create_task(
        self,
        task_id: str,
        user_id: str,
        project_id: str,
        conversation_id: str,
        agent_name: str,
        tool_call_id: str,
        status: TaskStatus,
        metadata: dict[str, Any] = {},
    ) -> TaskMetadata:
        """Create a new task.

        Args:
            task_id: The ID of the task
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the task belongs to
            task: The task data to store

        Returns:
            True if the task was created successfully, False otherwise
        """
        task = TaskMetadata(
            id=task_id,
            tool_call_id=tool_call_id,
            conversation_id=conversation_id,
            project_id=project_id,
            user_id=user_id,
            agent_name=agent_name,
            status=status,
            metadata=metadata,
        )
        self.client.store_task_metadata(task)
        return task

    def update_task(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        agent_name: str,
        task_id: str,
        updates: dict[str, Any],
    ) -> Task:
        """Update the metadata for a task.

        Args:
            task: The task metadata to update
        """
        return self.client.update_task_metadata(
            user_id, project_id, conversation_id, agent_name, task_id, updates
        )

    def list_tasks(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        agent_name: str = None,
        fetch_history: bool = False,
    ) -> List[Union[TaskMetadata, Task]]:
        """Get all tasks for a conversation.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation to get tasks for

        Returns:
            A list of tasks
        """
        task_metadatas = self.client.list_task_metadatas(
            user_id, project_id, conversation_id, agent_name
        )
        tasks = []
        for task_metadata in task_metadatas:
            if fetch_history:
                task = self.get_task(
                    user_id,
                    project_id,
                    conversation_id,
                    task_metadata.agent_name,
                    task_metadata.id,
                )
                tasks.append(task)
            else:
                tasks.append(task_metadata)
        return tasks

    def delete_task(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        agent_name: str,
        task_id: str,
    ) -> bool:
        """Delete a task.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the task belongs to
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted successfully, False otherwise
        """
        self.message_service.delete_messages(
            user_id, project_id, conversation_id, task_id
        )
        self.client.delete_task_metadata(
            user_id, project_id, conversation_id, agent_name, task_id
        )

    def delete_tasks(self, user_id: str, project_id: str, conversation_id: str) -> bool:
        """Delete all tasks for a conversation.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation to delete tasks for

        Returns:
            True if all tasks were deleted successfully, False otherwise
        """
        tasks = self.list_tasks(user_id, project_id, conversation_id)
        for task in tasks:
            self.delete_task(
                user_id, project_id, conversation_id, task.agent_name, task.id
            )
        return True

    def get_task(
        self,
        user_id: str,
        project_id: str,
        conversation_id: str,
        agent_name: str,
        task_id: str,
    ) -> Task | None:
        """Get a single task by ID."""
        task_metadata = self.client.get_task_metadata(
            user_id, project_id, conversation_id, agent_name, task_id
        )
        if not task_metadata:
            return None
        messages = self.message_service.list_messages(
            user_id, project_id, conversation_id, task_metadata.id
        )
        return Task(
            id=task_metadata.id,
            conversation_id=task_metadata.conversation_id,
            project_id=task_metadata.project_id,
            user_id=task_metadata.user_id,
            tool_call_id=task_metadata.tool_call_id,
            agent_name=task_metadata.agent_name,
            status=task_metadata.status,
            metadata=task_metadata.metadata,
            history=messages,
        )
