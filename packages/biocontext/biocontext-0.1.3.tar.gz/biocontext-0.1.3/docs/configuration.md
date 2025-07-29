# Configuration

## Server Configuration

The `MCPServer` class can be configured with the following parameters:

```python
from biocontext import MCPServer
from pathlib import Path

server = MCPServer(
    name="my-server",
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

## OpenAPI Server Configuration

Create a `config.yaml` file in your project directory:

```yaml
schemas:
  - name: example-server
    url: https://api.example.com/openapi.json
    type: json  # or "yaml"
    base: https://api.example.com  # optional base URL
```

### Schema Configuration

- `name`: Unique identifier for the schema
- `url`: URL to the OpenAPI specification
- `type`: Format of the specification ("json" or "yaml")
- `base`: Optional base URL for API endpoints

## Custom Route Mapping

You can customize how routes are mapped to tools by providing custom route mappings:

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
    name="my-server",
    version="1.0.0",
    author="Your Name",
    route_maps=custom_mappings
)
```
