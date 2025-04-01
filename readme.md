
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
