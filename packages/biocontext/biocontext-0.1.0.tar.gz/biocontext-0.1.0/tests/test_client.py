"""Tests for the MCP client connection."""

from unittest.mock import AsyncMock, patch

import pytest
from fastmcp import Client, FastMCP

from biocontext.client import MCPConnection, MCPNotInitializedError


@pytest.fixture
def mock_client():
    """Create a mock FastMCP client."""
    client = AsyncMock(spec=Client)
    client.aclose = AsyncMock()
    return client


@pytest.fixture
def mock_mcp():
    """Create a mock FastMCP instance."""
    mcp = AsyncMock(spec=FastMCP)
    mcp.name = "test-mcp"
    mcp.get_tools.return_value = {"test_tool": {"description": "A test tool"}}
    mcp.get_resources.return_value = {"test_resource": {"type": "string"}}
    return mcp


@pytest.mark.asyncio
async def test_connection_initialization():
    """Test MCP connection initialization."""
    connection = MCPConnection("test-mcp", "http://example.com")
    assert connection.name == "test-mcp"
    assert connection.base_url == "http://example.com"
    assert connection._client is None


@pytest.mark.asyncio
async def test_connection_context_manager(mock_client, mock_mcp):
    """Test MCP connection as async context manager."""
    with (
        patch("biocontext.client.Client", return_value=mock_client),
        patch("biocontext.client.FastMCP", return_value=mock_mcp),
    ):
        async with MCPConnection("test-mcp") as connection:
            assert connection._client == mock_client
            assert connection._mcp == mock_mcp

        # Verify client was closed
        mock_client.aclose.assert_called_once()


@pytest.mark.asyncio
async def test_get_tools(mock_client, mock_mcp):
    """Test getting tools from MCP server."""
    with (
        patch("biocontext.client.Client", return_value=mock_client),
        patch("biocontext.client.FastMCP", return_value=mock_mcp),
    ):
        async with MCPConnection("test-mcp") as connection:
            tools = await connection.get_tools()
            assert tools == {"test_tool": {"description": "A test tool"}}
            mock_mcp.get_tools.assert_called_once()


@pytest.mark.asyncio
async def test_get_resources(mock_client, mock_mcp):
    """Test getting resources from MCP server."""
    with (
        patch("biocontext.client.Client", return_value=mock_client),
        patch("biocontext.client.FastMCP", return_value=mock_mcp),
    ):
        async with MCPConnection("test-mcp") as connection:
            resources = await connection.get_resources()
            assert resources == {"test_resource": {"type": "string"}}
            mock_mcp.get_resources.assert_called_once()


@pytest.mark.asyncio
async def test_call_tool(mock_client, mock_mcp):
    """Test calling a tool on MCP server."""
    mock_client.call_tool.return_value = ["result"]
    with (
        patch("biocontext.client.Client", return_value=mock_client),
        patch("biocontext.client.FastMCP", return_value=mock_mcp),
    ):
        async with MCPConnection("test-mcp") as connection:
            result = await connection.call_tool("test_tool", {"param": "value"})
            assert result == ["result"]
            mock_client.call_tool.assert_called_once_with("test_tool", {"param": "value"})


@pytest.mark.asyncio
async def test_not_initialized_error():
    """Test error when using uninitialized connection."""
    connection = MCPConnection("test-mcp")

    with pytest.raises(MCPNotInitializedError):
        await connection.get_tools()

    with pytest.raises(MCPNotInitializedError):
        await connection.get_resources()

    with pytest.raises(MCPNotInitializedError):
        await connection.call_tool("test_tool", {})


@pytest.mark.asyncio
async def test_connection_with_base_url(mock_client, mock_mcp):
    """Test connection with base URL."""
    with (
        patch("biocontext.client.Client", return_value=mock_client),
        patch("biocontext.client.FastMCP", return_value=mock_mcp),
    ):
        async with MCPConnection("test-mcp", "http://example.com") as connection:
            assert connection.base_url == "http://example.com"
            assert connection._client == mock_client
            assert connection._mcp == mock_mcp


@pytest.mark.asyncio
async def test_connection_error_handling(mock_client, mock_mcp):
    """Test error handling in connection."""
    mock_client.call_tool.side_effect = Exception("Test error")
    with (
        patch("biocontext.client.Client", return_value=mock_client),
        patch("biocontext.client.FastMCP", return_value=mock_mcp),
    ):
        async with MCPConnection("test-mcp") as connection:
            with pytest.raises(Exception) as exc_info:
                await connection.call_tool("test_tool", {})
            assert str(exc_info.value) == "Test error"
