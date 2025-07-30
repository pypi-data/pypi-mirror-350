from typing import List, Optional

from google_a2a.common.types import AgentCard

from ephor_cli.clients.ddb.agent import AgentDDBClient
from ephor_cli.constant import DYNAMODB_TABLE_NAME
from ephor_cli.utils.agent_card import get_agent_card


class AgentService:
    """Service for high-level agent operations."""

    def __init__(
        self, table_name: str = DYNAMODB_TABLE_NAME, region: str = "us-east-1"
    ):
        self.client = AgentDDBClient(table_name, region)

    def register_agent(
        self, user_id: str, project_id: str, conversation_id: str, url: str
    ) -> Optional[AgentCard]:
        """Register an agent with a conversation."""
        agent_data = get_agent_card(url)
        if not agent_data.url:
            agent_data.url = url
        if self.client.store_agent(user_id, project_id, conversation_id, agent_data):
            return agent_data
        return None

    def list_agents(
        self, user_id: str, project_id: str, conversation_id: str
    ) -> List[AgentCard]:
        """Get all agents for a conversation."""
        return self.client.list_agents(user_id, project_id, conversation_id)

    def deregister_agent(
        self, user_id: str, project_id: str, conversation_id: str, url: str
    ) -> bool:
        """Delete an agent.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation the agent belongs to
            agent_id: The ID of the agent to delete

        Returns:
            True if the agent was deleted successfully, False otherwise
        """
        return self.client.delete_agent(user_id, project_id, conversation_id, url)

    def deregister_agents(self, user_id: str, project_id: str, conversation_id: str):
        """Deregister all agents for a conversation."""
        agents = self.list_agents(user_id, project_id, conversation_id)
        for agent in agents:
            self.deregister_agent(user_id, project_id, conversation_id, agent.url)
        return True
