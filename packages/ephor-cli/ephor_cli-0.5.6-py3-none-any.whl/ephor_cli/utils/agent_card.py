import requests
from google_a2a.common.types import AgentCard


def get_agent_card(remote_agent_address: str) -> AgentCard:
    """Get the agent card."""
    print(f"Getting agent card from {remote_agent_address}")
    if not remote_agent_address.startswith(
        "http"
    ) and not remote_agent_address.startswith("https"):
        remote_agent_address = f"http://{remote_agent_address}"
    agent_card = requests.get(f"{remote_agent_address}/.well-known/agent.json")
    return AgentCard(**agent_card.json())
