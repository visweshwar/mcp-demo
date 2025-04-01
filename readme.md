# Prerequisites

1. Have Python 3.10 or higher installed
1. Preferably having uv installed
    1. Steps to install uv https://docs.astral.sh/uv/getting-started/installation/
1. Use node 22+ NPM 10.0.0 or higher
    1. Steps to install NPM https://docs.npmjs.com/downloading-and-installing-node-js-and-npm
 1. Install a MCP Client
    1. Claude Desktop: https://claude.ai/download
    1. Continue on VSCode:[Link for Continue on VSCode](https://marketplace.visualstudio.com/items?itemName=Continue.continue)
    1. Cursor: [Link for Cursor MCP Instructions](https://docs.cursor.com/context/model-context-protocol)





# Local MCP Server

## Install dependencies
#Create virtual environment with uv for python 3.11 and install dependencies using uv pip

```sh
uv python install 3.11
uv venv --python 3.11
uv .venv/bin/pip install -r requirements.txt
```

## Env File
 
```properties
AZURE_OPENAI_API_KEY= The API key for your Azure OpenAI service
AZURE_OPENAI_ENDPOINT= The endpoint for your Azure OpenAI service
AZURE_OPENAI_EMBEDDING_DEPLOYMENT= The deployment name for your Azure OpenAI embedding service
AZURE_OPENAI_DEPLOYMENT= The deployment name for your Azure OpenAI model
AZURE_OPENAI_EMBEDDING_VERSION= The version of the Azure OpenAI embedding service
``` 

## Build the local context
Run the notebook to build the local context.The notebook is located at notebook/langchain_tool.ipynb

## Replace Value in the Server file
Replace the PATH value in paychex-mcp.py with the path to your local context

```python
PATH = "<PATH_TO_YOUR_REPO>/notebook/"
```

# MCP Inspector

## Run the mcp inspector locally
The MCP inspector is a developer tool for testing and debugging MCP servers.
```sh
bash-3.2$ npx @modelcontextprotocol/inspector
```

## Usage
Add the env values and arguments to your MCP Inspector command

```bash
bash-3.2$  npx @modelcontextprotocol/inspector \
  <path_to_repo>/.venv/bin/python \
  /<path_to_repo>/paychex-mcp.py \
  -e AZURE_OPENAI_API_KEY=<API_KEY> \
  -e AZURE_OPENAI_ENDPOINT=<ENDPOINT> \
  -e AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<EMBEDDING_DEPLOYMENT> \
  -e AZURE_OPENAI_DEPLOYMENT=<DEPLOYMENT> \
  -e AZURE_OPENAI_EMBEDDING_VERSION=<EMBEDDING_VERSION>
```

## MCP Inspector Flags

You can pass both arguments and environment variables to your MCP server. Arguments are passed directly to your server, while environment variables can be set using the -e flag:

### Pass arguments only
npx @modelcontextprotocol/inspector build/index.js arg1 arg2

### Pass environment variables only
npx @modelcontextprotocol/inspector -e KEY=value -e KEY2=$VALUE2 node build/index.js

### Pass both environment variables and arguments
npx @modelcontextprotocol/inspector -e KEY=value -e KEY2=$VALUE2 node build/index.js arg1 arg2

#### Use -- to separate inspector flags from server arguments
npx @modelcontextprotocol/inspector -e KEY=$VALUE -- node build/index.js -e server-flag

### Use MCP Inspector with other MCP Servers
 npx -y @modelcontextprotocol/inspector npx  @modelcontextprotocol/server-filesystem arg1 agr2

# Using MCP COnfiguration files 
 

The `mcp-config` folder contains configuration files necessary to set up and run MCP (Model Context Protocol) servers for various environments. Here are the steps to utilize these configuration files effectively:

### Step 1: Locate the MCP Configuration Files

Navigate to the `mcp-config` folder in your project directory. Inside, you will find JSON configuration files for different setups, such as:

- `claude_desktop_config.json` for Claude Desktop setup.
- `config.yaml` for continue VS Code Extension setup.

### Step 2: Edit Configuration Files

Before using the configuration files, you might need to edit them to match your local or deployment environments. For example, in `claude_desktop_config.json` or `config.yaml`, replace placeholders such as `<path to your Python executable>`, `<your Azure OpenAI API key>`, and others with actual values relevant to your setup.
 