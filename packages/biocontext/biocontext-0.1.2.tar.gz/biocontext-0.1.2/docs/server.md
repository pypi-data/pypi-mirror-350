# Server Implementation

The BioContext server implementation provides a robust framework for creating and managing MCP (Model Context Protocol) servers. This document details the server's features, configuration options, and usage patterns.

## Overview

The server implementation consists of two main components:

1. `MCPServer`: The main server class that handles setup and management of MCP servers
2. `OpenAPIServerFactory`: A factory class for creating MCP servers from OpenAPI specifications

## Server Configuration

### Basic Setup

```python
from biocontext import MCPServer
from pathlib import Path

server = MCPServer(
    name="my-mcp-server",
    version="1.0.0",
    author="Your Name",
    on_duplicate_tools="error",  # Options: "warn", "error", "replace", "ignore"
    stateless_http=True,
    config_path=Path("config.yaml")
)
```

### Configuration Parameters

- `name`: The name of the MCP server
- `version`: The version of the server
- `author`: The author of the server
- `on_duplicate_tools`: How to handle duplicate tools (default: "error")
- `stateless_http`: Whether to use stateless HTTP (default: True)
- `config_path`: Path to the OpenAPI configuration file

## OpenAPI Integration

The server supports integration with OpenAPI specifications through a YAML configuration file:

```yaml
schemas:
  - name: "my-api"
    url: "https://example.com/openapi.json"
    type: "json"  # or "yaml"
    base: "https://api.example.com"  # optional base URL
```

### Schema Configuration

- `name`: Unique identifier for the schema
- `url`: URL to the OpenAPI specification
- `type`: Format of the specification ("json" or "yaml")
- `base`: Optional base URL for API endpoints

## Server Setup

```python
# Initialize server
server = MCPServer(...)

# Setup with optional core MCP
mcp_app = await server.setup(core_mcp=optional_core_mcp)
```

The setup process:
1. Loads and validates OpenAPI specifications
2. Creates MCP servers for each specification
3. Imports tools, resources, and templates
4. Validates all components
5. Logs available tools and resources

## Features

### Tool Management
- Automatic tool discovery from OpenAPI operations
- Validation of tool names and parameters
- Support for custom route mapping
- Duplicate tool handling

### Resource Management
- Resource discovery from OpenAPI schemas
- Resource template generation
- Validation of resource names and structures

### Error Handling
- Configuration file validation
- Schema download and parsing errors
- Tool and resource validation errors
- Duplicate tool handling

### Logging
- Server setup progress
- Available tools and resources
- Validation results
- Error conditions

## Best Practices

1. **Configuration Management**
   - Use version control for configuration files
   - Document schema dependencies
   - Keep base URLs configurable

2. **Error Handling**
   - Implement proper error handling for API calls
   - Monitor server logs for validation issues
   - Handle duplicate tools appropriately

3. **Performance**
   - Use stateless HTTP when possible
   - Implement proper caching strategies
   - Monitor resource usage

## Examples

### Basic Server Setup

```python
from biocontext import MCPServer
from pathlib import Path

async def setup_server():
    server = MCPServer(
        name="my-mcp-server",
        version="1.0.0",
        author="Your Name",
        config_path=Path("config.yaml")
    )

    mcp_app = await server.setup()
    return mcp_app
```

### Custom Route Mapping

```python
from fastmcp.server.openapi import RouteMap, RouteType

custom_mappings = [
    RouteMap(
        methods=["GET", "POST"],
        pattern=r".*",
        route_type=RouteType.TOOL,
    ),
]

server = MCPServer(
    name="my-mcp-server",
    version="1.0.0",
    author="Your Name",
    route_maps=custom_mappings
)
```

## Troubleshooting

Common issues and solutions:

1. **Configuration File Not Found**
   - Ensure the config file exists at the specified path
   - Check file permissions
   - Verify the path is correct

2. **Schema Download Failures**
   - Check network connectivity
   - Verify schema URLs
   - Ensure proper authentication if required

3. **Validation Errors**
   - Check tool and resource names for invalid characters
   - Verify schema format (JSON/YAML)
   - Ensure base URLs are properly configured

## API Reference

For detailed API documentation, please refer to the [API Reference](https://biocypher.github.io/biocontext/api/).
