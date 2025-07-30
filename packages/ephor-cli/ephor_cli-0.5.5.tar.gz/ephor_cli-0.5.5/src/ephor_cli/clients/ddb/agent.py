import datetime
import hashlib
from typing import List
from google_a2a.common.types import AgentCard
from ephor_cli.clients.ddb.base import BaseDDBClient


class AgentDDBClient(BaseDDBClient):
    """DynamoDB client for agent operations."""

    def _get_agent_pk(self, user_id: str, project_id: str, conversation_id: str) -> str:
        """Create the partition key for an agent."""
        return (
            f"USER#{user_id}#PROJECT#{project_id}#CONVERSATION#{conversation_id}#AGENTS"
        )

    def _hash_url(self, url: str) -> str:
        """Hash the agent URL to create a unique agent ID."""
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    def _get_agent_sk(self, agent_url: str) -> str:
        """Create the sort key for an agent using the hashed URL as ID."""
        agent_id = self._hash_url(agent_url)
        return f"AGENT#{agent_id}"

    def store_agent(
        self, user_id: str, project_id: str, conversation_id: str, agent: AgentCard
    ) -> bool:
        """Store an agent in DynamoDB."""
        try:
            item = {
                "created_at": datetime.datetime.utcnow().isoformat(),
                **agent.model_dump(),
                "PK": self._get_agent_pk(user_id, project_id, conversation_id),
                "SK": self._get_agent_sk(agent.url),
            }
            self.table.put_item(Item=self.sanitize_for_dynamodb(item))
            return True
        except Exception as e:
            print(f"Error storing agent: {e}")
            return False

    def list_agents(
        self, user_id: str, project_id: str, conversation_id: str
    ) -> List[AgentCard]:
        """List all agents for a conversation."""
        response = self.table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={
                ":pk": self._get_agent_pk(user_id, project_id, conversation_id)
            },
        )
        agents = []
        for item in response.get("Items", []):
            for key in ["PK", "SK", "created_at"]:
                if key in item:
                    del item[key]
            # AgentCard expects url, not id
            agents.append(AgentCard.model_validate(item))
        return agents

    def delete_agent(
        self, user_id: str, project_id: str, conversation_id: str, agent_url: str
    ) -> bool:
        """Delete an agent from DynamoDB.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the agent belongs to
            agent_url: The URL of the agent to delete

        Returns:
            True if the agent was deleted successfully, False otherwise
        """
        try:
            self.table.delete_item(
                Key={
                    "PK": self._get_agent_pk(user_id, project_id, conversation_id),
                    "SK": self._get_agent_sk(agent_url),
                }
            )
            return True
        except Exception as e:
            print(f"Error deleting agent: {e}")
            return False
