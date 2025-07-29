import uuid
from typing import Any, Optional, Union

from .schema import KnowledgeGraphMetadata, MCPServiceMetadata, ResourceType


class RegistryError(Exception):
    """Custom exception for registry-related errors."""

    MCP_NOT_FOUND = "MCP tool not found: {}"
    GRAPH_NOT_FOUND = "Knowledge graph not found: {}"

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message.format(*args) if args else message)


class RegistryClient:
    """Client for interacting with the BioContext registry."""

    def __init__(self, base_url: str) -> None:
        """Initialize the registry client.

        Args:
            base_url: Base URL of the registry API
        """
        self.base_url = base_url.rstrip("/")
        # For testing purposes, we'll store metadata in memory
        self._mcp_store: dict[str, MCPServiceMetadata] = {}
        self._graph_store: dict[str, KnowledgeGraphMetadata] = {}

    async def register_mcp(self, metadata: MCPServiceMetadata) -> str:
        """Register a new MCP tool.

        Args:
            metadata: MCP tool metadata

        Returns:
            str: Tool identifier
        """
        identifier = metadata.identifier
        if isinstance(identifier, list):
            identifier = identifier[0] if identifier else str(uuid.uuid4())
        if identifier is None:
            identifier = str(uuid.uuid4())
        self._mcp_store[identifier] = metadata
        return identifier

    async def register_graph(self, metadata: KnowledgeGraphMetadata) -> str:
        """Register a new knowledge graph.

        Args:
            metadata: Knowledge graph metadata

        Returns:
            str: Knowledge graph identifier
        """
        identifier = metadata.identifier
        if isinstance(identifier, list):
            identifier = identifier[0] if identifier else str(uuid.uuid4())
        if identifier is None:
            identifier = str(uuid.uuid4())
        self._graph_store[identifier] = metadata
        return identifier

    async def search(
        self,
        query: str,
        resource_type: Optional[ResourceType] = None,
        filters: Optional[dict[str, Any]] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Union[MCPServiceMetadata, KnowledgeGraphMetadata]]:
        """Search for resources in the registry.

        Args:
            query: Search query string
            resource_type: Type of resource to search for
            filters: Additional filters to apply
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            List of matching resources
        """
        results: list[Union[MCPServiceMetadata, KnowledgeGraphMetadata]] = []

        # Search MCP tools
        if resource_type in [None, ResourceType.MCP_SERVER]:
            for metadata in self._mcp_store.values():
                if self._matches_filters(metadata, query, filters):
                    results.append(metadata)

        # Search knowledge graphs
        if resource_type in [None, ResourceType.KNOWLEDGE_GRAPH]:
            for graph_metadata in self._graph_store.values():
                if self._matches_filters(graph_metadata, query, filters):
                    results.append(graph_metadata)

        # Apply pagination
        return results[offset : offset + limit]

    async def get_mcp(self, identifier: str) -> MCPServiceMetadata:
        """Get MCP tool metadata by identifier.

        Args:
            identifier: Tool identifier

        Returns:
            MCP tool metadata

        Raises:
            RegistryError: If tool is not found
        """
        if identifier not in self._mcp_store:
            raise RegistryError(RegistryError.MCP_NOT_FOUND, identifier)
        return self._mcp_store[identifier]

    async def get_graph(self, identifier: str) -> KnowledgeGraphMetadata:
        """Get knowledge graph metadata by identifier.

        Args:
            identifier: Knowledge graph identifier

        Returns:
            Knowledge graph metadata

        Raises:
            RegistryError: If knowledge graph is not found
        """
        if identifier not in self._graph_store:
            raise RegistryError(RegistryError.GRAPH_NOT_FOUND, identifier)
        return self._graph_store[identifier]

    async def update_metadata(
        self,
        identifier: str,
        metadata: Union[MCPServiceMetadata, KnowledgeGraphMetadata],
    ) -> bool:
        """Update resource metadata.

        Args:
            identifier: Resource identifier
            metadata: Updated metadata

        Returns:
            bool: True if update was successful

        Raises:
            RegistryError: If resource is not found
        """
        if isinstance(metadata, MCPServiceMetadata):
            if identifier not in self._mcp_store:
                raise RegistryError(RegistryError.MCP_NOT_FOUND, identifier)
            self._mcp_store[identifier] = metadata
        else:
            if identifier not in self._graph_store:
                raise RegistryError(RegistryError.GRAPH_NOT_FOUND, identifier)
            self._graph_store[identifier] = metadata
        return True

    def _matches_filters(
        self,
        metadata: Union[MCPServiceMetadata, KnowledgeGraphMetadata],
        query: str,
        filters: Optional[dict[str, Any]] = None,
    ) -> bool:
        """Check if metadata matches the search query and filters.

        Args:
            metadata: Resource metadata
            query: Search query string
            filters: Additional filters to apply

        Returns:
            bool: True if metadata matches
        """
        # Basic text search
        searchable_fields = [
            metadata.name,
            metadata.description,
            *metadata.keywords,
        ]
        if not any(query.lower() in field.lower() for field in searchable_fields):
            return False

        # Apply filters
        if filters:
            for key, value in filters.items():
                if key.startswith("properties."):
                    prop_key = key.split(".", 1)[1]
                    found = False
                    for prop in getattr(metadata, "additionalProperties", []):
                        if prop.get("name") == prop_key and prop.get("value") == value:
                            found = True
                            break
                    if not found:
                        return False
                else:
                    if not hasattr(metadata, key):
                        return False
                    if getattr(metadata, key) != value:
                        return False

        return True
