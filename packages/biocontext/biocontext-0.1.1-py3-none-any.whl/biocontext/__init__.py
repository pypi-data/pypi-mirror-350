"""BioContext MCP Package - A Python package for accessing and managing MCP servers."""

from biocontext.client import MCPConnection
from biocontext.server import OpenAPIServerFactory
from biocontext.utils import slugify

__version__ = "0.1.0"

__all__ = ["MCPConnection", "OpenAPIServerFactory", "slugify"]
