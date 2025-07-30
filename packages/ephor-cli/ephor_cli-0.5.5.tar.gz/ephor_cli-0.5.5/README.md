# Ephor CLI

A command-line tool that lets you create expert agents, test, run and deploy them.

## Installation

This package requires a two-step installation:

1. First, install the Google A2A package from GitHub:

   ```
   uv pip install git+https://github.com/djsamseng/A2A.git@prefixPythonPackage#subdirectory=samples/python
   ```

   or using pip:

   ```
   pip install git+https://github.com/djsamseng/A2A.git@prefixPythonPackage#subdirectory=samples/python
   ```

2. Then, install the ephor-cli package:
   ```
   uv pip install ephor-cli
   ```
   or using pip:
   ```
   pip install ephor-cli
   ```

## Usage

The ephor-cli provides several commands:

```bash
# Show available commands
ephor-cli --help

# Run a sample agent
ephor-cli run-sample giphy-agent

# Create a new agent configuration file
ephor-cli create-agent --output my-agent.yml

# Run the agent
ephor-cli up --config path/to/agent-config.yml
```

### Running agents

Before running agents, make sure to set your ANTHROPIC_API_KEY environment variable:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

To run one or more agents:

```bash
ephor-cli up -c configs/sample-agent.yml -c configs/another-agent.yml
```

### Creating a new agent

The interactive agent creation wizard helps you configure a new agent:

```bash
ephor-cli create-agent -o configs/custom-agent.yml
```

This will guide you through creating a new agent configuration with colored prompts.
