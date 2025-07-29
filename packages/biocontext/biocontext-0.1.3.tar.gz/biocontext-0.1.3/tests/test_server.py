"""Tests for the OpenAPI server factory and MCP server implementation."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
import yaml
from fastmcp import FastMCP
from fastmcp.server.openapi import FastMCPOpenAPI, RouteMap, RouteType

from biocontext.server import (
    ConfigFileNotFoundError,
    MCPServer,
    OpenAPIServerFactory,
    UnsupportedSchemaTypeError,
)


class MockTool:
    """Mock tool class for testing."""

    def __init__(self, name):
        self.name = name


class MockResource:
    """Mock resource class for testing."""

    def __init__(self, name):
        self.name = name


class MockTemplate:
    """Mock template class for testing."""

    def __init__(self, name):
        self.name = name


@pytest.fixture
def mock_config_file(tmp_path):
    """Create a temporary config file for testing."""
    config = {
        "schemas": [
            {
                "name": "test-api",
                "url": "http://example.com/openapi.json",
                "type": "json",
                "base": "http://api.example.com",
            }
        ]
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.dump(config))
    return config_path


@pytest.fixture
def mock_openapi_spec():
    """Create a mock OpenAPI specification."""
    return {
        "info": {
            "version": "1.0.0",
            "description": "Test API",
        },
        "servers": [{"url": "http://api.example.com"}],
    }


@pytest.fixture
def mock_mcp():
    """Create a mock FastMCPOpenAPI instance."""
    mcp = AsyncMock(spec=FastMCPOpenAPI)
    mcp.name = "test-api"
    mcp.get_tools.return_value = {"test_tool": MockTool("test_tool")}
    mcp.get_resources.return_value = {"test_resource": MockResource("test_resource")}
    mcp.get_resource_templates.return_value = {"test_template": MockTemplate("test_template")}
    return mcp


@pytest.fixture
def mock_fastmcp():
    """Create a mock FastMCP instance."""
    mcp = AsyncMock(spec=FastMCP)
    mcp.name = "test-server"
    mcp.get_tools.return_value = {"test_tool": MockTool("test_tool")}
    mcp.get_resources.return_value = {"test_resource": MockResource("test_resource")}
    mcp.get_resource_templates.return_value = {"test_template": MockTemplate("test_template")}
    return mcp


@pytest.mark.asyncio
async def test_create_servers_success(mock_config_file, mock_openapi_spec, mock_mcp):
    """Test successful server creation."""
    with patch("httpx.Client") as mock_client, patch("biocontext.server.FastMCPOpenAPI", return_value=mock_mcp):
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.text = json.dumps(mock_openapi_spec)
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        factory = OpenAPIServerFactory(mock_config_file)
        servers = await factory.create_servers()

        assert len(servers) == 1
        assert servers[0] == mock_mcp


@pytest.mark.asyncio
async def test_create_servers_yaml(mock_config_file, mock_openapi_spec, mock_mcp):
    """Test server creation with YAML specification."""
    with patch("httpx.Client") as mock_client, patch("biocontext.server.FastMCPOpenAPI", return_value=mock_mcp):
        # Mock the HTTP response with YAML content
        mock_response = MagicMock()
        mock_response.text = yaml.dump(mock_openapi_spec)
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        # Update config to use YAML
        config = yaml.safe_load(mock_config_file.read_text())
        config["schemas"][0]["type"] = "yaml"
        mock_config_file.write_text(yaml.dump(config))

        factory = OpenAPIServerFactory(mock_config_file)
        servers = await factory.create_servers()

        assert len(servers) == 1
        assert servers[0] == mock_mcp


@pytest.mark.asyncio
async def test_config_file_not_found():
    """Test error when config file is not found."""
    factory = OpenAPIServerFactory(Path("nonexistent.yaml"))
    with pytest.raises(ConfigFileNotFoundError):
        await factory.create_servers()


@pytest.mark.asyncio
async def test_unsupported_schema_type(mock_config_file):
    """Test error when schema type is not supported."""
    # Update config with unsupported type
    config = yaml.safe_load(mock_config_file.read_text())
    config["schemas"][0]["type"] = "xml"
    mock_config_file.write_text(yaml.dump(config))

    with patch("httpx.Client") as mock_client:
        mock_response = MagicMock()
        mock_response.text = "<xml>test</xml>"
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        factory = OpenAPIServerFactory(mock_config_file)
        with pytest.raises(UnsupportedSchemaTypeError):
            await factory.create_servers()


@pytest.mark.asyncio
async def test_http_error_handling(mock_config_file):
    """Test handling of HTTP errors."""
    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.side_effect = httpx.RequestError("Connection error")

        factory = OpenAPIServerFactory(mock_config_file)
        servers = await factory.create_servers()
        assert len(servers) == 0


def test_get_base_path_from_servers(mock_openapi_spec):
    """Test base path resolution from OpenAPI servers."""
    factory = OpenAPIServerFactory()
    base_path = factory._get_base_path(mock_openapi_spec, {})
    assert base_path == "http://api.example.com"


def test_get_base_path_from_config():
    """Test base path resolution from config."""
    factory = OpenAPIServerFactory()
    schema_config = {"base": "http://custom.example.com"}
    base_path = factory._get_base_path({}, schema_config)
    assert base_path == "http://custom.example.com"


def test_get_base_path_none():
    """Test base path resolution when no valid path is found."""
    factory = OpenAPIServerFactory()
    base_path = factory._get_base_path({}, {})
    assert base_path is None


@pytest.mark.asyncio
async def test_check_valid_mcp(mock_mcp):
    """Test MCP validation."""
    factory = OpenAPIServerFactory()
    is_valid = await factory._check_valid_mcp(mock_mcp)
    assert is_valid is True


@pytest.mark.asyncio
async def test_check_invalid_mcp():
    """Test MCP validation with invalid names."""
    mcp = AsyncMock(spec=FastMCPOpenAPI)
    mcp.name = "test-api"
    mcp.get_tools.return_value = {"invalid@name": MockTool("invalid@name")}
    mcp.get_resources.return_value = {}
    mcp.get_resource_templates.return_value = {}

    factory = OpenAPIServerFactory()
    is_valid = await factory._check_valid_mcp(mcp)
    assert is_valid is False


@pytest.mark.asyncio
async def test_check_empty_mcp():
    """Test MCP validation with no tools/resources."""
    mcp = AsyncMock(spec=FastMCPOpenAPI)
    mcp.name = "test-api"
    mcp.get_tools.return_value = {}
    mcp.get_resources.return_value = {}
    mcp.get_resource_templates.return_value = {}

    factory = OpenAPIServerFactory()
    is_valid = await factory._check_valid_mcp(mcp)
    assert is_valid is False


@pytest.mark.asyncio
async def test_mcp_server_setup(mock_config_file, mock_openapi_spec, mock_mcp, mock_fastmcp):
    """Test MCPServer setup with OpenAPI specifications."""
    with (
        patch("httpx.Client") as mock_client,
        patch("biocontext.server.FastMCPOpenAPI", return_value=mock_mcp),
        patch("biocontext.server.FastMCP", return_value=mock_fastmcp),
    ):
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.text = json.dumps(mock_openapi_spec)
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        # Create and setup server
        server = MCPServer(name="test-server", version="1.0.0", author="Test Author", config_path=mock_config_file)

        mcp_app = await server.setup()

        assert mcp_app == mock_fastmcp
        mock_fastmcp.import_server.assert_called_once_with("test-api", mock_mcp)


@pytest.mark.asyncio
async def test_mcp_server_setup_with_core_mcp(mock_config_file, mock_openapi_spec, mock_mcp, mock_fastmcp):
    """Test MCPServer setup with core MCP."""
    with (
        patch("httpx.Client") as mock_client,
        patch("biocontext.server.FastMCPOpenAPI", return_value=mock_mcp),
        patch("biocontext.server.FastMCP", return_value=mock_fastmcp),
    ):
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.text = json.dumps(mock_openapi_spec)
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        # Create core MCP
        core_mcp = AsyncMock(spec=FastMCPOpenAPI)
        core_mcp.name = "core-api"
        core_mcp.get_tools.return_value = {"core_tool": MockTool("core_tool")}
        core_mcp.get_resources.return_value = {"core_resource": MockResource("core_resource")}
        core_mcp.get_resource_templates.return_value = {"core_template": MockTemplate("core_template")}

        # Create and setup server
        server = MCPServer(name="test-server", version="1.0.0", author="Test Author", config_path=mock_config_file)

        mcp_app = await server.setup(core_mcp=core_mcp)

        assert mcp_app == mock_fastmcp
        assert mock_fastmcp.import_server.call_count == 2
        mock_fastmcp.import_server.assert_any_call("core-api", core_mcp)
        mock_fastmcp.import_server.assert_any_call("test-api", mock_mcp)


@pytest.mark.asyncio
async def test_mcp_server_duplicate_tools(mock_config_file, mock_openapi_spec, mock_mcp, mock_fastmcp):
    """Test MCPServer handling of duplicate tools."""
    with (
        patch("httpx.Client") as mock_client,
        patch("biocontext.server.FastMCPOpenAPI", return_value=mock_mcp),
        patch("biocontext.server.FastMCP", return_value=mock_fastmcp),
    ):
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.text = json.dumps(mock_openapi_spec)
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        # Create server with different duplicate tool handling options
        for option in ["warn", "error", "replace", "ignore"]:
            server = MCPServer(
                name="test-server",
                version="1.0.0",
                author="Test Author",
                config_path=mock_config_file,
                on_duplicate_tools=option,
            )

            mcp_app = await server.setup()
            assert mcp_app == mock_fastmcp


@pytest.mark.asyncio
async def test_mcp_server_custom_route_mapping(mock_config_file, mock_openapi_spec, mock_mcp, mock_fastmcp):
    """Test MCPServer with custom route mapping."""
    with (
        patch("httpx.Client") as mock_client,
        patch("biocontext.server.FastMCPOpenAPI", return_value=mock_mcp),
        patch("biocontext.server.FastMCP", return_value=mock_fastmcp),
        patch("biocontext.server.OpenAPIServerFactory") as mock_factory,
    ):
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.text = json.dumps(mock_openapi_spec)
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        # Create custom route mapping
        custom_mappings = [
            RouteMap(
                methods=["GET", "POST"],
                pattern=r".*",
                route_type=RouteType.TOOL,
            ),
        ]

        # Mock the factory to use our custom mappings
        mock_factory_instance = AsyncMock()
        mock_factory_instance._custom_mappings = custom_mappings
        mock_factory_instance.create_servers.return_value = [mock_mcp]
        mock_factory.return_value = mock_factory_instance

        # Create and setup server
        server = MCPServer(name="test-server", version="1.0.0", author="Test Author", config_path=mock_config_file)

        mcp_app = await server.setup()
        assert mcp_app == mock_fastmcp

        # Verify the factory was created with the correct config path
        mock_factory.assert_called_once_with(config_path=mock_config_file)


@pytest.mark.asyncio
async def test_mcp_server_error_handling(mock_config_file):
    """Test MCPServer error handling."""
    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.side_effect = httpx.RequestError("Connection error")

        server = MCPServer(name="test-server", version="1.0.0", author="Test Author", config_path=mock_config_file)

        mcp_app = await server.setup()
        assert mcp_app is not None  # Server should still be created even if OpenAPI specs fail


@pytest.mark.asyncio
async def test_mcp_server_check_tools(mock_config_file, mock_openapi_spec, mock_mcp, mock_fastmcp):
    """Test MCPServer tool checking functionality."""
    with (
        patch("httpx.Client") as mock_client,
        patch("biocontext.server.FastMCPOpenAPI", return_value=mock_mcp),
        patch("biocontext.server.FastMCP", return_value=mock_fastmcp),
    ):
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.text = json.dumps(mock_openapi_spec)
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        # Create and setup server
        server = MCPServer(name="test-server", version="1.0.0", author="Test Author", config_path=mock_config_file)

        # Setup server and verify tool checking was performed
        await server.setup()

        # Verify tool checking was performed
        mock_fastmcp.get_tools.assert_called()
        mock_fastmcp.get_resources.assert_called()
        mock_fastmcp.get_resource_templates.assert_called()
