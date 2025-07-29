"""OpenAPI MCP server factory implementation."""

import json
import logging
from pathlib import Path
from typing import Literal

import httpx
import yaml
from fastmcp import FastMCP
from fastmcp.server.openapi import FastMCPOpenAPI, RouteMap, RouteType

from biocontext.utils import slugify


class OpenAPIServerError(Exception):
    """Base exception for OpenAPI server errors."""


class ConfigFileNotFoundError(OpenAPIServerError):
    """Raised when the configuration file is not found."""


class UnsupportedSchemaTypeError(OpenAPIServerError):
    """Raised when an unsupported schema type is encountered."""


class OpenAPIServerFactory:
    """A factory for creating MCP servers from OpenAPI specifications.

    This class reads OpenAPI specifications from a configuration file and creates
    corresponding MCP servers. It handles downloading and parsing the specifications,
    validating the created servers, and managing their lifecycle.
    """

    def __init__(self, config_path: Path | None = None):
        """Initialize the OpenAPI server factory.

        Args:
            config_path: Optional path to the OpenAPI configuration file
        """
        self.config_path = config_path or Path(__file__).parent / "config" / "config.yaml"
        self._custom_mappings = [
            RouteMap(
                methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
                pattern=r".*",
                route_type=RouteType.TOOL,
            ),
        ]

    async def create_servers(self) -> list[FastMCPOpenAPI]:
        """Create MCP servers from OpenAPI specifications.

        Returns:
            List of configured FastMCPOpenAPI instances
        """
        if not self.config_path.exists():
            raise ConfigFileNotFoundError()

        schema_config = yaml.safe_load(self.config_path.read_text(encoding="utf-8"))
        openapi_mcps: list[FastMCPOpenAPI] = []

        for schema in schema_config.get("schemas", []):
            try:
                with httpx.Client() as client:
                    schema_request = client.get(schema["url"], timeout=30)
                    schema_request.raise_for_status()

                    if schema["type"] == "json":
                        spec = json.loads(schema_request.text)
                    elif schema["type"] == "yaml":
                        spec = yaml.safe_load(schema_request.text)
                    else:
                        raise UnsupportedSchemaTypeError()

                    base_path = self._get_base_path(spec, schema)
                    if not base_path:
                        logging.error(f"Base path not found in schema: {schema['url']}")
                        continue

                    mcp = FastMCPOpenAPI(
                        name=schema["name"],
                        version=spec.get("info", {}).get("version", "1.0.0"),
                        description=spec.get("info", {}).get("description", ""),
                        openapi_spec=spec,
                        client=httpx.AsyncClient(base_url=base_path),
                        route_maps=self._custom_mappings,
                    )

                    if await self._check_valid_mcp(mcp):
                        openapi_mcps.append(mcp)

            except httpx.RequestError:
                logging.exception(f"Failed to download schema from {schema['url']}")
                continue

        return openapi_mcps

    def _get_base_path(self, spec: dict, schema: dict) -> str | None:
        """Get the base path from the OpenAPI spec or schema config."""
        if (
            isinstance(spec.get("servers", False), list)
            and len(spec["servers"]) > 0
            and "url" in spec["servers"][0]
            and spec["servers"][0]["url"].startswith("http")
        ):
            return str(spec["servers"][0]["url"])
        base = schema.get("base")
        return base if isinstance(base, str) else None

    async def _check_valid_mcp(self, mcp: FastMCPOpenAPI) -> bool:
        """Check if an MCP server is valid.

        Args:
            mcp: The OpenAPI-based MCP to check

        Returns:
            Whether the MCP server is valid
        """
        tools = await mcp.get_tools()
        resources = await mcp.get_resources()
        templates = await mcp.get_resource_templates()

        prefix_length = len(slugify(mcp.name)) + 1
        keys = [*tools.keys(), *resources.keys(), *templates.keys()]

        if not keys:
            logging.error(f"No tools, resources, or templates found in MCP server {mcp.name}.")
            return False

        def is_valid_name(name: str) -> bool:
            return all(c.isalnum() or c in ["_", "-"] for c in name)

        for name in keys:
            if not is_valid_name(name) or (len(name) + prefix_length) > 64:
                logging.error(f"Invalid name `{name}` in MCP server {mcp.name}.")
                return False

        return True


class MCPServer:
    """Abstract MCP server implementation that can be used by concrete server implementations.

    This class provides the core functionality for setting up and managing MCP servers,
    while allowing concrete implementations to handle deployment-specific concerns.
    """

    def __init__(
        self,
        name: str,
        version: str,
        author: str,
        on_duplicate_tools: Literal["warn", "error", "replace", "ignore"] = "error",
        stateless_http: bool = True,
        config_path: Path | None = None,
    ):
        """Initialize the MCP server.

        Args:
            name: Name of the MCP server
            version: Version of the MCP server
            author: Author of the MCP server
            on_duplicate_tools: How to handle duplicate tools
            stateless_http: Whether to use stateless HTTP
            config_path: Optional path to the OpenAPI configuration file
        """
        self.mcp_app: FastMCP = FastMCP(
            name=name,
            version=version,
            author=author,
            on_duplicate_tools=on_duplicate_tools,
            stateless_http=stateless_http,
        )
        self.openapi_factory = OpenAPIServerFactory(config_path=config_path)
        self.logger = logging.getLogger(__name__)

    async def setup(self, core_mcp: FastMCPOpenAPI | None = None) -> FastMCP:
        """Setup the MCP server with core and OpenAPI-based MCPs.

        Args:
            core_mcp: Optional core MCP to include in setup

        Returns:
            The configured FastMCP instance
        """
        self.logger.info("Setting up MCP server...")

        # Get core MCP and OpenAPI MCPs
        mcps = []
        if core_mcp:
            mcps.append(core_mcp)
        mcps.extend(await self.openapi_factory.create_servers())

        # Import all MCPs
        for mcp in mcps:
            await self.mcp_app.import_server(
                slugify(mcp.name),
                mcp,
            )
        self.logger.info("MCP server setup complete.")

        # Check tools
        await self._check_tools()

        return self.mcp_app

    async def _check_tools(self) -> None:
        """Check the MCP server for valid tools, resources, and templates."""
        self.logger.info("Checking MCP server for valid tools...")
        tools = await self.mcp_app.get_tools()
        resources = await self.mcp_app.get_resources()
        templates = await self.mcp_app.get_resource_templates()

        self.logger.info(f"{self.mcp_app.name} - {len(tools)} Tool(s): {', '.join([t.name for t in tools.values()])}")
        self.logger.info(
            f"{self.mcp_app.name} - {len(resources)} Resource(s): {', '.join([(r.name if r.name is not None else '') for r in resources.values()])}"
        )
        self.logger.info(
            f"{self.mcp_app.name} - {len(templates)} Resource Template(s): {', '.join([t.name for t in templates.values()])}"
        )
        self.logger.info("MCP server tools check complete.")
