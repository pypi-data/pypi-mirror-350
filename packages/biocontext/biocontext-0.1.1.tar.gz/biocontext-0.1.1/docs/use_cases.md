# Use Cases

## Connecting to Existing MCP Servers

Use `MCPConnection` to connect to any MCP server and access its tools:

```python
from biocontext import MCPConnection

async def use_remote_tools():
    async with MCPConnection("my-server") as conn:
        # List available tools
        tools = await conn.get_tools()
        print(f"Available tools: {list(tools.keys())}")

        # Call a tool
        result = await conn.call_tool("search", {"query": "example"})
        print(f"Search results: {result}")
```

## Creating MCP Servers from OpenAPI Specs

Use `OpenAPIServerFactory` to create MCP servers from OpenAPI specifications:

```python
from biocontext import OpenAPIServerFactory

async def create_servers():
    # Create servers from OpenAPI specs
    factory = OpenAPIServerFactory()
    servers = await factory.create_servers()

    # Use the created servers
    for server in servers:
        tools = await server.get_tools()
        print(f"Server {server.name} has tools: {list(tools.keys())}")
```

## Integration with LLMs

The package is designed to work seamlessly with LLMs. Here's a typical workflow:

1. Connect to or create MCP servers
2. Get available tools and their descriptions
3. Use the tools in your LLM prompts
4. Call tools based on LLM decisions

Example with an LLM:

```python
from biocontext import MCPConnection

async def llm_workflow():
    async with MCPConnection("my-server") as conn:
        # Get tool descriptions for the LLM
        tools = await conn.get_tools()

        # Example LLM prompt
        prompt = f"""
        Available tools:
        {tools}

        User request: Search for information about proteins
        """

        # LLM decides to use the search tool
        result = await conn.call_tool("search", {"query": "proteins"})
```
