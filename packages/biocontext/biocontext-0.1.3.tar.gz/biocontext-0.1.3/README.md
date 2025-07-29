# BioContext

[![Release](https://img.shields.io/github/v/release/biocypher/biocontext)](https://img.shields.io/github/v/release/biocypher/biocontext)
[![Build status](https://img.shields.io/github/actions/workflow/status/biocypher/biocontext/main.yml?branch=main)](https://github.com/biocypher/biocontext/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/biocypher/biocontext/branch/main/graph/badge.svg)](https://codecov.io/gh/biocypher/biocontext)
[![Commit activity](https://img.shields.io/github/commit-activity/m/biocypher/biocontext)](https://img.shields.io/github/commit-activity/m/biocypher/biocontext)
[![License](https://img.shields.io/github/license/biocypher/biocontext)](https://img.shields.io/github/license/biocypher/biocontext)

Python package for use with BioContext MCP servers to enable LLM tool use.

- **Github repository**: <https://github.com/biocypher/biocontext/>
- **Documentation**: <https://biocypher.github.io/biocontext/>

## Installation

```bash
pip install biocontext
```

### Development

Install the project using `make install`. Test code quality using `make check`.
Run tests using `make test`. Bump version using `./bump.sh <patch|minor|major>`.
Build and deploy docs locally using `uv run mkdocs serve`.

## Basic Functionality

### Client

The BioContext client provides an async connection to MCP (Model Context
Protocol) servers. It allows you to discover and use tools and resources
provided by MCP servers:

```python
from biocontext import MCPConnection

# Initialize connection
async with MCPConnection("my-mcp-server", base_url="http://example.com") as connection:
    # Get available tools
    tools = await connection.get_tools()

    # Get available resources
    resources = await connection.get_resources()

    # Call a specific tool
    result = await connection.call_tool("tool_name", {"param": "value"})
```

### Server

BioContext provides a flexible server implementation for creating and managing MCP (Model Context Protocol) servers. The server supports both core MCP functionality and integration with OpenAPI specifications:

```python
from biocontext import MCPServer
from pathlib import Path

# Initialize server with basic configuration
server = MCPServer(
    name="my-mcp-server",
    version="1.0.0",
    author="Your Name",
    config_path=Path("config.yaml")
)

# Setup server with optional core MCP
mcp_app = await server.setup()

# The server now provides:
# - Tools from OpenAPI specifications
# - Resources and resource templates
# - Automatic validation of tools and resources
# - Logging of available tools and resources
```

The server supports configuration through a YAML file that specifies OpenAPI schemas to integrate:

```yaml
schemas:
  - name: "my-api"
    url: "https://example.com/openapi.json"
    type: "json"  # or "yaml"
    base: "https://api.example.com"  # optional base URL
```

Key features of the server implementation:
- Automatic downloading and parsing of OpenAPI specifications
- Support for both JSON and YAML OpenAPI formats
- Validation of tools, resources, and templates
- Custom route mapping for tool endpoints
- Comprehensive logging of server setup and available tools
- Error handling for configuration and schema issues

For more detailed information about server configuration and usage, please refer to the [Server Documentation](https://biocypher.github.io/biocontext/server/).

### Registry

The registry helps you discover and use biological tools and knowledge
resources. It maintains metadata about MCP servers, knowledge graphs, and tools,
making it easy to find what you need:

```python
from biocontext import Registry

# Initialize registry
registry = Registry()

# Find tools for a specific task
protein_tools = registry.search_resources(
    type="tool",
    keywords=["protein", "sequence analysis"]
)

# Find knowledge graphs about specific topics
disease_kgs = registry.search_resources(
    type="knowledge_graph",
    keywords=["disease", "pathway"]
)

# Find MCP servers that provide specific capabilities
servers = registry.search_resources(
    type="mcp_server",
    capabilities=["protein analysis", "sequence alignment"]
)

# Get detailed information about a specific resource
tool_info = registry.get_resource("protein-analyzer-v1")
print(f"Tool: {tool_info.name}")
print(f"Description: {tool_info.description}")
print(f"Input types: {tool_info.inputData}")
print(f"Output types: {tool_info.outputData}")
print(f"Available at: {tool_info.url}")
```

The registry uses schema.org and BioSchemas standards to provide rich metadata
about each resource, including:

- Detailed descriptions and capabilities
- Input/output data types
- License information
- Version history
- Related tools and knowledge graphs
- Query interfaces and endpoints

## Documentation

Please visit our [documentation](https://biocypher.github.io/biocontext/).

## License

MIT License - see LICENSE file for details
