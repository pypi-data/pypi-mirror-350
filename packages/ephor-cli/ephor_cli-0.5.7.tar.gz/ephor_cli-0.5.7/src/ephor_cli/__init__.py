from dotenv import load_dotenv

load_dotenv()

import logging
import click
from ephor_cli.types.agent import AgentConfig
from ephor_cli.types.llm import LLMProvider, Model
import yaml
import os
import sys
import requests
from ephor_cli.agent_server.server import A2AProxyServer
from ephor_cli.conversation_server.server import ConversationServer
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import colorama
from colorama import Fore, Style
from ephor_cli.constant import API_SERVER_URL

# Define version
__version__ = "0.5.7"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_required_env_vars(env_vars: list[str]) -> bool:
    """Check if required environment variables are set."""
    missing_vars = []
    for var in env_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    if missing_vars:
        click.echo(
            f"{Fore.RED}Error: Missing required environment variables: {', '.join(missing_vars)}{Style.RESET_ALL}"
        )
        click.echo(
            f"{Fore.YELLOW}Please set these variables in your environment or .env file.{Style.RESET_ALL}"
        )
        return False
    return True


def load_agent_config(config_path: str) -> AgentConfig:
    """Load agent configuration from a YAML file."""
    try:
        with open(config_path, "r") as file:
            config_dict = yaml.safe_load(file)
            return AgentConfig(**config_dict)
    except Exception as e:
        logger.error(f"Failed to load config from {config_path}: {e}")
        raise


def configure_models():
    """Helper function to configure primary and fallback models."""
    primary_model = None
    fallback_models = []

    # Configure primary model
    if click.confirm(
        f"{Fore.YELLOW}Would you like to configure a primary model?{Style.RESET_ALL}",
        default=False,
    ):
        click.echo(f"{Fore.CYAN}Configuring primary model:{Style.RESET_ALL}")
        provider = click.prompt(
            f"{Fore.CYAN}Model provider{Style.RESET_ALL}",
            type=click.Choice([p.value for p in LLMProvider], case_sensitive=False),
        )
        model_name = click.prompt(f"{Fore.CYAN}Model name{Style.RESET_ALL}")
        primary_model = Model(name=model_name, provider=LLMProvider(provider))

    # Configure fallback models
    if click.confirm(
        f"{Fore.YELLOW}Would you like to configure fallback models?{Style.RESET_ALL}",
        default=False,
    ):
        click.echo(
            f"{Fore.CYAN}Configuring fallback models (in order of preference):{Style.RESET_ALL}"
        )
        while True:
            provider = click.prompt(
                f"{Fore.CYAN}Fallback model provider{Style.RESET_ALL}",
                type=click.Choice([p.value for p in LLMProvider], case_sensitive=False),
            )
            model_name = click.prompt(
                f"{Fore.CYAN}Fallback model name{Style.RESET_ALL}"
            )
            fallback_models.append(
                Model(name=model_name, provider=LLMProvider(provider))
            )

            if not click.confirm(
                f"{Fore.YELLOW}Add another fallback model?{Style.RESET_ALL}",
                default=False,
            ):
                break

    return primary_model, fallback_models


@click.group()
def cli():
    """Ephor CLI for managing A2A proxy agents."""
    pass


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to run the server on")
@click.option("--port", default=10002, help="Port to run the server on")
@click.option("--api-url", default=API_SERVER_URL, help="API URL for agent registry")
def start_agent_server(host, port, api_url):
    """Start an A2A proxy server without pre-registering any agents."""
    # Check for required environment variables
    if not check_required_env_vars(["EPHOR_API_KEY", "ANTHROPIC_API_KEY"]):
        sys.exit(1)

    # Create and start the server
    server = A2AProxyServer(host=host, port=port, api_url=api_url)

    logger.info(f"Starting server on http://{host}:{port}")
    click.echo(
        f"Server running at: {Fore.YELLOW}{Style.BRIGHT}http://{host}:{port}{Style.RESET_ALL}"
    )
    click.echo(
        f"Your agent URL will be {Fore.CYAN}http://{host}:{port}/<agent_id> {Style.RESET_ALL}"
    )
    server.start()


@cli.command()
@click.option(
    "--output", "-o", default=None, help="Output file path for the agent config"
)
def create_agent(output):
    """Create a new agent configuration file by answering prompts."""
    try:
        colorama.init()
    except ImportError:
        # Fallback if colorama is not installed
        class DummyFore:
            def __getattr__(self, _):
                return ""

        class DummyStyle:
            def __getattr__(self, _):
                return ""

        global Fore, Style
        Fore = DummyFore()
        Style = DummyStyle()

    click.echo(
        f"{Fore.GREEN}===== Creating New Agent Configuration ====={Style.RESET_ALL}"
    )

    # Collect basic information
    name = click.prompt(f"{Fore.CYAN}Agent name{Style.RESET_ALL}")
    description = click.prompt(f"{Fore.CYAN}Agent description{Style.RESET_ALL}")
    version = click.prompt(
        f"{Fore.CYAN}Agent version{Style.RESET_ALL}", default="1.0.0"
    )
    logoUrl = click.prompt(
        f"{Fore.CYAN}Agent logo URL or path (optional){Style.RESET_ALL}", default=""
    )

    # Capabilities
    streaming = click.confirm(
        f"{Fore.CYAN}Enable streaming capability?{Style.RESET_ALL}", default=True
    )

    # Skills
    skills = []
    click.echo(f"{Fore.YELLOW}Now let's define the agent's skills:{Style.RESET_ALL}")

    while True:
        if skills and not click.confirm(
            f"{Fore.YELLOW}Add another skill?{Style.RESET_ALL}", default=False
        ):
            break

        skill_id = click.prompt(f"{Fore.CYAN}Skill ID{Style.RESET_ALL}")
        skill_name = click.prompt(f"{Fore.CYAN}Skill name{Style.RESET_ALL}")
        skill_description = click.prompt(
            f"{Fore.CYAN}Skill description{Style.RESET_ALL}"
        )

        # Tags
        tags = []
        click.echo(f"{Fore.BLUE}Enter tags (empty line to finish):{Style.RESET_ALL}")
        while True:
            tag = click.prompt(f"{Fore.BLUE}Tag{Style.RESET_ALL}", default="")
            if not tag:
                break
            tags.append(tag)

        # Examples
        examples = []
        click.echo(
            f"{Fore.BLUE}Enter example queries (empty line to finish):{Style.RESET_ALL}"
        )
        while True:
            example = click.prompt(f"{Fore.BLUE}Example{Style.RESET_ALL}", default="")
            if not example:
                break
            examples.append(example)

        skill = {
            "id": skill_id,
            "name": skill_name,
            "description": skill_description,
            "tags": tags,
            "examples": examples,
            "inputModes": ["text"],
            "outputModes": ["text"],
        }

        skills.append(skill)

    # Prompt
    click.echo(f"{Fore.YELLOW}Enter the system prompt for your agent:{Style.RESET_ALL}")
    prompt = click.edit(text="You are an agent. Your job is to...\n")

    # MCP Servers
    mcp_servers = []
    if click.confirm(
        f"{Fore.YELLOW}Would you like to configure MCP servers?{Style.RESET_ALL}",
        default=False,
    ):
        while True:
            server_name = click.prompt(f"{Fore.CYAN}Server name{Style.RESET_ALL}")
            server_url = click.prompt(f"{Fore.CYAN}Server URL{Style.RESET_ALL}")
            server_transport = click.prompt(
                f"{Fore.CYAN}Transport type{Style.RESET_ALL}",
                type=click.Choice(["sse", "websocket", "http"], case_sensitive=False),
                default="sse",
            )

            mcp_servers.append(
                {"name": server_name, "url": server_url, "transport": server_transport}
            )

            if not click.confirm(
                f"{Fore.YELLOW}Add another MCP server?{Style.RESET_ALL}", default=False
            ):
                break

    # Hive IDs
    hive_ids = []
    if click.confirm(
        f"{Fore.YELLOW}Would you like to configure Hive IDs?{Style.RESET_ALL}",
        default=False,
    ):
        click.echo(
            f"{Fore.BLUE}Enter Hive IDs (empty line to finish):{Style.RESET_ALL}"
        )
        while True:
            hive_id = click.prompt(f"{Fore.BLUE}Hive ID{Style.RESET_ALL}", default="")
            if not hive_id:
                break
            hive_ids.append(hive_id)

    # Model Configuration
    primary_model, fallback_models = configure_models()

    # Create the config dictionary
    config = {
        "name": name,
        "description": description,
        "version": version,
        "capabilities": {"streaming": streaming},
        "skills": skills,
        "prompt": prompt,
        "logoUrl": logoUrl,
    }

    if mcp_servers:
        config["mcpServers"] = mcp_servers

    if hive_ids:
        config["hiveIds"] = hive_ids

    if primary_model:
        config["primaryModel"] = {
            "name": primary_model.name,
            "provider": primary_model.provider.value,
        }

    if fallback_models:
        config["fallbackModels"] = [
            {"name": model.name, "provider": model.provider.value}
            for model in fallback_models
        ]

    # Determine output file path
    if not output:
        output = f"agent-{name.lower().replace(' ', '-')}.yml"
        if not output.endswith(".yml"):
            output += ".yml"

    # Save to file
    output_path = os.path.abspath(output)
    with open(output_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    click.echo(
        f"{Fore.GREEN}Agent configuration saved to: {output_path}{Style.RESET_ALL}"
    )


@cli.command()
@click.option(
    "--api-url",
    default=API_SERVER_URL,
    help="API URL for agent registry",
)
def list_agents(api_url):
    """List available agents from the API."""
    # Check for required environment variables
    if not check_required_env_vars(["EPHOR_API_KEY"]):
        sys.exit(1)

    click.echo(f"{Fore.GREEN}===== Available Agents ====={Style.RESET_ALL}")

    page_size = 10
    next_token = None
    has_more = True

    while has_more:
        try:
            headers = {"x-api-key": os.environ.get("EPHOR_API_KEY")}
            params = {"limit": page_size}

            if next_token:
                params["nextToken"] = next_token

            response = requests.get(f"{api_url}/agents", params=params, headers=headers)

            if response.status_code != 200:
                click.echo(
                    f"{Fore.RED}Error: Failed to fetch agents: {response.text}{Style.RESET_ALL}"
                )
                sys.exit(1)

            data = response.json()
            agents = data.get("agents", [])
            next_token = data.get("nextToken")

            if not agents:
                if next_token is None:
                    click.echo(f"{Fore.YELLOW}No agents found.{Style.RESET_ALL}")
                else:
                    click.echo(
                        f"{Fore.YELLOW}No more agents to display.{Style.RESET_ALL}"
                    )
                break

            for agent in agents:
                agent_name = agent.get("name", "Unknown")
                agent_description = agent.get("description", "No description available")
                agent_id = agent.get("id", "Unknown")
                agent_version = agent.get("version", "Unknown")

                click.echo(f"{Fore.CYAN}{agent_name} (ID: {agent_id}){Style.RESET_ALL}")
                click.echo(f"  Description: {agent_description}")
                click.echo(f"  Version: {agent_version}")
                click.echo("")

            has_more = next_token is not None

            if has_more:
                click.echo(
                    f"{Fore.YELLOW}Press Enter to show more agents or Ctrl+C to exit...{Style.RESET_ALL}"
                )
                try:
                    input()
                except KeyboardInterrupt:
                    click.echo(
                        f"{Fore.YELLOW}Operation canceled by user.{Style.RESET_ALL}"
                    )
                    break

        except requests.exceptions.RequestException as e:
            click.echo(f"{Fore.RED}Error communicating with API: {e}{Style.RESET_ALL}")
            sys.exit(1)


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to run the server on")
@click.option("--port", default=12000, help="Port to run the server on")
def start_conversation_server(host, port):
    """Start the Conversation Server for agent interactions."""
    # Check for required environment variables
    if not check_required_env_vars(["GOOGLE_API_KEY"]):
        sys.exit(1)

    click.echo(
        f"{Fore.GREEN}Starting Conversation Server on http://{host}:{port}{Style.RESET_ALL}"
    )

    # Create FastAPI app and router
    app = FastAPI()

    # Add CORS middleware to allow all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    router = APIRouter()

    # Initialize the conversation server with the router
    ConversationServer(router)

    # Include the router in the app
    app.include_router(router)

    # Start the server
    import uvicorn

    uvicorn.run(
        app,
        host=host,
        port=port,
        timeout_graceful_shutdown=0,
    )


@cli.command()
@click.option("--config", "-c", required=True, help="Path to agent config file")
@click.option(
    "--api-url",
    default=API_SERVER_URL,
    help="API URL for agent registry",
)
def push(config, api_url):
    """Push an agent configuration to the registry API."""

    # Check for required environment variables
    if not check_required_env_vars(["EPHOR_API_KEY"]):
        sys.exit(1)

    try:
        # Load the agent config
        logger.info(f"Loading agent config from {config}")
        agent_config = load_agent_config(config)

        # Convert agent config to dictionary for API, including ALL fields
        agent_data = {
            "name": agent_config.name,
            "description": agent_config.description,
            "version": agent_config.version,
            "capabilities": {"streaming": agent_config.capabilities.streaming},
            "skills": [],
            "prompt": agent_config.prompt,
            "mcpServers": [],  # Default empty list
            "supportedContentTypes": [],  # Default empty list
            "hiveIds": [],  # Default empty list
            "logoUrl": getattr(agent_config, "logoUrl", ""),
        }

        # Add skills
        for skill in agent_config.skills:
            skill_data = {
                "id": skill.id,
                "name": skill.name,
                "description": skill.description,
                "tags": skill.tags,
                "examples": skill.examples,
                "inputModes": skill.inputModes,
                "outputModes": skill.outputModes,
            }
            agent_data["skills"].append(skill_data)

        # Override defaults with values from config if present
        if hasattr(agent_config, "mcpServers") and agent_config.mcpServers:
            agent_data["mcpServers"] = [
                {
                    "name": server.name,
                    "url": server.url,
                    "transport": server.transport,
                }
                for server in agent_config.mcpServers
            ]

        if (
            hasattr(agent_config, "supported_content_types")
            and agent_config.supported_content_types
        ):
            agent_data["supportedContentTypes"] = agent_config.supported_content_types

        if hasattr(agent_config, "hiveIds") and agent_config.hiveIds:
            agent_data["hiveIds"] = agent_config.hiveIds

        # Add model configuration
        if hasattr(agent_config, "primaryModel") and agent_config.primaryModel:
            agent_data["primaryModel"] = {
                "name": agent_config.primaryModel.name,
                "provider": agent_config.primaryModel.provider.value,
            }

        if hasattr(agent_config, "fallbackModels") and agent_config.fallbackModels:
            agent_data["fallbackModels"] = [
                {"name": model.name, "provider": model.provider.value}
                for model in agent_config.fallbackModels
            ]

        # Check if agent already exists
        agent_name = agent_config.name
        try:
            headers = {"x-api-key": os.environ.get("EPHOR_API_KEY")}
            response = requests.get(
                f"{api_url}/agents?name={agent_name}", headers=headers
            )
            existing_agents = response.json()
            agent_exists = False
            for agent in existing_agents:
                if agent.get("name") == agent_name:
                    agent_exists = True
                    agent_id = agent.get("id")
                    break

            if agent_exists:
                click.echo(
                    f"{Fore.YELLOW}Agent '{agent_name}' already exists.{Style.RESET_ALL}"
                )
                update = click.confirm(
                    f"{Fore.CYAN}Do you want to update the existing agent?{Style.RESET_ALL}",
                    default=True,
                )

                if update:
                    # Update existing agent - use same data, just different endpoint
                    response = requests.put(
                        f"{api_url}/agents/{agent_id}", json=agent_data, headers=headers
                    )
                    if response.status_code in [200, 201, 204]:
                        click.echo(
                            f"{Fore.GREEN}Agent '{agent_name}' updated successfully.{Style.RESET_ALL}"
                        )
                    else:
                        click.echo(
                            f"{Fore.RED}Failed to update agent: {response.text}{Style.RESET_ALL}"
                        )
                else:
                    # Create with new name
                    new_name = click.prompt(
                        f"{Fore.CYAN}Enter a new unique name for the agent{Style.RESET_ALL}"
                    )
                    agent_data["name"] = new_name
                    response = requests.post(
                        f"{api_url}/agents", json=agent_data, headers=headers
                    )
                    if response.status_code in [200, 201]:
                        click.echo(
                            f"{Fore.GREEN}Agent '{new_name}' created successfully.{Style.RESET_ALL}"
                        )
                    else:
                        click.echo(
                            f"{Fore.RED}Failed to create agent: {response.text}{Style.RESET_ALL}"
                        )
            else:
                # Create new agent
                response = requests.post(
                    f"{api_url}/agents", json=agent_data, headers=headers
                )
                if response.status_code in [200, 201]:
                    click.echo(
                        f"{Fore.GREEN}Agent '{agent_name}' created successfully.{Style.RESET_ALL}"
                    )
                else:
                    click.echo(
                        f"{Fore.RED}Failed to create agent: {response.text}{Style.RESET_ALL}"
                    )

        except requests.exceptions.RequestException as e:
            click.echo(f"{Fore.RED}Error communicating with API: {e}{Style.RESET_ALL}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Failed to push agent: {e}")
        click.echo(f"{Fore.RED}Error: Failed to push agent: {e}{Style.RESET_ALL}")
        sys.exit(1)


@cli.command()
@click.option("--agent-id", "-a", required=True, help="Agent ID to pull")
@click.option(
    "--output", "-o", default=None, help="Output file path for the agent config"
)
@click.option(
    "--api-url",
    default=API_SERVER_URL,
    help="API URL for agent registry",
)
def pull(agent_id, output, api_url):
    """Pull an agent configuration from the registry API by ID and save as YAML."""

    # Check for required environment variables
    if not check_required_env_vars(["EPHOR_API_KEY"]):
        sys.exit(1)

    try:
        headers = {"x-api-key": os.environ.get("EPHOR_API_KEY")}

        # Fetch agent by ID
        click.echo(f"{Fore.CYAN}Fetching agent with ID: {agent_id}{Style.RESET_ALL}")
        response = requests.get(f"{api_url}/agents/{agent_id}", headers=headers)

        if response.status_code == 404:
            click.echo(
                f"{Fore.RED}Error: Agent with ID '{agent_id}' not found.{Style.RESET_ALL}"
            )
            sys.exit(1)
        elif response.status_code != 200:
            click.echo(
                f"{Fore.RED}Error: Failed to fetch agent: {response.text}{Style.RESET_ALL}"
            )
            sys.exit(1)

        agent_data = response.json()

        # Convert API response to YAML config format
        config = {
            "name": agent_data.get("name", ""),
            "description": agent_data.get("description", ""),
            "version": agent_data.get("version", "1.0.0"),
            "capabilities": {
                "streaming": agent_data.get("capabilities", {}).get("streaming", True)
            },
            "skills": [],
            "prompt": agent_data.get("prompt", ""),
            "logoUrl": agent_data.get("logoUrl", ""),
        }

        # Add skills
        for skill in agent_data.get("skills", []):
            skill_data = {
                "id": skill.get("id", ""),
                "name": skill.get("name", ""),
                "description": skill.get("description", ""),
                "tags": skill.get("tags", []),
                "examples": skill.get("examples", []),
                "inputModes": skill.get("inputModes", ["text"]),
                "outputModes": skill.get("outputModes", ["text"]),
            }
            config["skills"].append(skill_data)

        # Add optional fields if present
        if agent_data.get("mcpServers"):
            config["mcpServers"] = []
            for server in agent_data["mcpServers"]:
                server_data = {
                    "name": server.get("name", ""),
                    "url": server.get("url", ""),
                    "transport": server.get("transport", "sse"),
                }
                config["mcpServers"].append(server_data)

        if agent_data.get("hiveIds"):
            config["hiveIds"] = agent_data["hiveIds"]

        if agent_data.get("primaryModel"):
            config["primaryModel"] = {
                "name": agent_data["primaryModel"].get("name", ""),
                "provider": agent_data["primaryModel"].get("provider", ""),
            }

        if agent_data.get("fallbackModels"):
            config["fallbackModels"] = []
            for model in agent_data["fallbackModels"]:
                model_data = {
                    "name": model.get("name", ""),
                    "provider": model.get("provider", ""),
                }
                config["fallbackModels"].append(model_data)

        # Determine output file path
        if not output:
            output = f"agent-{agent_id}.yaml"

        if not output.endswith((".yml", ".yaml")):
            output += ".yaml"

        # Save to file
        output_path = os.path.abspath(output)
        with open(output_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        click.echo(
            f"{Fore.GREEN}Agent configuration saved to: {output_path}{Style.RESET_ALL}"
        )
        click.echo(f"{Fore.CYAN}Agent Name: {config['name']}{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}Version: {config['version']}{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        click.echo(f"{Fore.RED}Error communicating with API: {e}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to pull agent: {e}")
        click.echo(f"{Fore.RED}Error: Failed to pull agent: {e}{Style.RESET_ALL}")
        sys.exit(1)


@cli.command()
def version():
    """Print the current version of the Ephor CLI."""
    click.echo(f"Ephor CLI version: {__version__}")


def main():
    cli()


if __name__ == "__main__":
    main()
