"""OpenAPI MCP server factory implementation."""

import json
import logging
from pathlib import Path

import httpx
import yaml
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
