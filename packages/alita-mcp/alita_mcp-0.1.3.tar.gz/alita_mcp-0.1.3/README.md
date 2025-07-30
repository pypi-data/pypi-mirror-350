# Alita MCP Client

A command-line client for interacting with the MCP system.

## Installation

### Using pipx (Recommended)

[pipx](https://pypa.github.io/pipx/) installs the package in an isolated environment and makes the CLI commands available globally.

#### macOS

```bash
# Install pipx if not already installed
brew install pipx
pipx ensurepath

# Install alita-mcp
pipx install alita-mcp
```

Add the following to your `~/.zprofile` or `~/.bash_profile`:

```bash
# For zsh (~/.zprofile)
export PATH="$PATH:$HOME/.local/bin"
export PYTHONPATH="$PYTHONPATH:$HOME/.local/pipx/venvs/alita-mcp/lib/python3.x/site-packages"

# For bash (~/.bash_profile)
export PATH="$PATH:$HOME/.local/bin"
export PYTHONPATH="$PYTHONPATH:$HOME/.local/pipx/venvs/alita-mcp/lib/python3.x/site-packages"
```

Then reload your profile:

```bash
source ~/.zprofile  # or source ~/.bash_profile for bash
```

#### Windows

```powershell
# Install pipx if not already installed
python -m pip install --user pipx
python -m pipx ensurepath

# Install alita-mcp
pipx install alita-mcp
```

### From PyPI

```bash
pip install alita-mcp
```

### From Source

```bash
git clone https://github.com/yourusername/alita-mcp-client.git
cd alita-mcp-client
pip install -e .
```

## Configuration

### Bootstrap Configuration

Before using the client, you need to bootstrap it with your deployment URL and authentication token. You can do this in two ways:

#### Interactive Mode

```bash
alita-mcp bootstrap
```

First, this will prompt you to enter your deployment URL and authentication token step by step.  
Next, you will be asked to provide details for MCP servers.

#### Command Line Parameters

```bash
alita-mcp bootstrap --deployment_url https://api.example.com --auth_token YOUR_TOKEN --host 0.0.0.0 --port 8000
```

### Configuration Storage

The client stores configuration in your operating system's app data directory:

- Windows: `%APPDATA%\alita-mcp-client`
- macOS: `~/Library/Application Support/alita-mcp-client`
- Linux: `~/.config/alita-mcp-client`

## Usage

### Running with stdio Transport (Default)

The standard I/O transport is used by default for communication:

```bash
# Using a specific application within a project (application_id and version_id are optional)
alita-mcp run --project_id YOUR_PROJECT_ID [--app_id YOUR_APP_ID] [--version_id YOUR_VERSION_ID]

# Using all available agents in a project
alita-mcp run --project_id YOUR_PROJECT_ID
```

### Running with SSE Transport

Server-Sent Events (SSE) transport can be used for web-based applications:

```bash
# Using a specific application (application_id and version_id are optional)
alita-mcp run --project_id YOUR_PROJECT_ID [--app_id YOUR_APP_ID] [--version_id YOUR_VERSION_ID] --transport sse --port 8000

# Using all available agents in a project
alita-mcp run --project_id YOUR_PROJECT_ID --transport sse --port 8000
```

This will start the MCP server listening on all interfaces (0.0.0.0) on port 8000 by default. You can customize the host and port during the bootstrap process.

## Publishing to PyPI

To build and publish the package to PyPI:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Development

For development:

```bash
# Install in editable mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```