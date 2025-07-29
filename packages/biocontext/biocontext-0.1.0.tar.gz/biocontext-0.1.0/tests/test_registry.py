import pytest
from pydantic import HttpUrl

from biocontext.registry.client import RegistryClient, RegistryError
from biocontext.registry.schema import (
    Distribution,
    KnowledgeGraphMetadata,
    LicenseEnum,
    MCPServiceMetadata,
    PersonOrOrganization,
    ResourceType,
)


@pytest.fixture
def sample_mcp_metadata():
    return MCPServiceMetadata(
        **{"@id": "https://example.org/mcp/test-tool-001"},
        name="Test MCP Tool",
        description="A test MCP-compliant tool for unit testing",
        version="1.0.0",
        license=LicenseEnum.MIT,
        keywords=["test", "sequence analysis", "structure prediction"],
        creator=[PersonOrOrganization(**{"@type": "Person", "name": "Test Author"})],
        mcp_version="1.0",
        server_capabilities={"prompts": True, "resources": {"subscribe": True}, "tools": True},
        applicationCategory="bioinformatics",
        programmingLanguage="python",
        resource_type=ResourceType.MCP_SERVER,
    )


@pytest.fixture
def sample_kg_metadata():
    return KnowledgeGraphMetadata(
        **{"@id": "https://example.org/kg/test-kg-001"},
        name="Test Knowledge Graph",
        description="A test knowledge graph for use with MCP tools",
        version="1.0.0",
        license=LicenseEnum.APACHE_2_0,
        keywords=["test", "knowledge graph", "disease"],
        creator=[PersonOrOrganization(**{"@type": "Person", "name": "Test Author"})],
        conformsTo=[HttpUrl("http://purl.obolibrary.org/obo/go.owl"), HttpUrl("http://purl.obolibrary.org/obo/hp.owl")],
        mcp_compatible=True,
        query_interface=HttpUrl("https://example.org/sparql/test-kg"),
        supported_tools=[HttpUrl("https://example.org/mcp/test-tool-001")],
        resource_type=ResourceType.KNOWLEDGE_GRAPH,
        distribution=[
            Distribution(
                name="RDF Distribution",
                description="Test knowledge graph distribution",
                contentUrl=HttpUrl("https://example.org/downloads/test-kg.rdf"),
                encodingFormat="application/rdf+xml",
                contentSize="2 MB",
            )
        ],
    )


@pytest.fixture
def registry_client():
    return RegistryClient("http://localhost:8000")


class TestMCPServiceMetadata:
    def test_mcp_metadata_creation(self, sample_mcp_metadata):
        assert sample_mcp_metadata.id == "https://example.org/mcp/test-tool-001"
        assert sample_mcp_metadata.name == "Test MCP Tool"
        assert sample_mcp_metadata.applicationCategory == "bioinformatics"
        assert sample_mcp_metadata.license == LicenseEnum.MIT
        assert sample_mcp_metadata.mcp_version == "1.0"
        assert sample_mcp_metadata.server_capabilities["prompts"] is True

    def test_mcp_metadata_optional_fields(self):
        metadata = MCPServiceMetadata(
            id="https://example.org/mcp/minimal-tool",
            name="Minimal MCP Tool",
            description="Minimal test case",
            version="1.0.0",
            license=LicenseEnum.MIT,
            mcp_version="1.0",
            server_capabilities={"prompts": True},
            resource_type=ResourceType.MCP_SERVER,
        )
        assert metadata.keywords == []
        assert metadata.creator == []
        assert metadata.applicationCategory is None
        assert metadata.programmingLanguage is None


class TestKnowledgeGraphMetadata:
    def test_kg_metadata_creation(self, sample_kg_metadata):
        assert sample_kg_metadata.id == "https://example.org/kg/test-kg-001"
        assert sample_kg_metadata.name == "Test Knowledge Graph"
        assert len(sample_kg_metadata.conformsTo) == 2
        assert sample_kg_metadata.license == LicenseEnum.APACHE_2_0
        assert sample_kg_metadata.mcp_compatible is True
        assert len(sample_kg_metadata.supported_tools) == 1
        assert len(sample_kg_metadata.distribution) == 1

    def test_kg_metadata_optional_fields(self):
        metadata = KnowledgeGraphMetadata(
            id="https://example.org/kg/minimal-kg",
            name="Minimal KG",
            description="Minimal test case",
            version="1.0.0",
            license=LicenseEnum.MIT,
            mcp_compatible=True,
            resource_type=ResourceType.KNOWLEDGE_GRAPH,
        )
        assert metadata.conformsTo == []
        assert metadata.supported_tools == []
        assert metadata.distribution == []
        assert metadata.query_interface is None


class TestRegistryClient:
    @pytest.mark.asyncio
    async def test_register_mcp(self, registry_client, sample_mcp_metadata):
        # This is a mock test - actual implementation will depend on backend
        identifier = await registry_client.register_mcp(sample_mcp_metadata)
        assert isinstance(identifier, str)
        assert len(identifier) > 0

    @pytest.mark.asyncio
    async def test_register_graph(self, registry_client, sample_kg_metadata):
        # This is a mock test - actual implementation will depend on backend
        identifier = await registry_client.register_graph(sample_kg_metadata)
        assert isinstance(identifier, str)
        assert len(identifier) > 0

    @pytest.mark.asyncio
    async def test_search(self, registry_client, sample_mcp_metadata):
        # Register a tool first
        await registry_client.register_mcp(sample_mcp_metadata)

        # Search for the tool
        results = await registry_client.search(
            query="sequence analysis",
            resource_type=ResourceType.MCP_SERVER,
            filters={"applicationCategory": "bioinformatics", "mcp_version": "1.0"},
            limit=5,
            offset=0,
        )
        assert isinstance(results, list)
        assert len(results) > 0
        assert results[0].id == sample_mcp_metadata.id

    @pytest.mark.asyncio
    async def test_get_mcp(self, registry_client, sample_mcp_metadata):
        # Register the MCP tool first
        identifier = await registry_client.register_mcp(sample_mcp_metadata)

        # Now try to get it
        metadata = await registry_client.get_mcp(identifier)
        assert isinstance(metadata, MCPServiceMetadata)
        assert metadata.id == sample_mcp_metadata.id
        assert metadata.name == sample_mcp_metadata.name
        assert metadata.applicationCategory == sample_mcp_metadata.applicationCategory

    @pytest.mark.asyncio
    async def test_get_nonexistent_mcp(self, registry_client):
        # Test getting a non-existent MCP tool
        with pytest.raises(RegistryError) as exc_info:
            await registry_client.get_mcp("nonexistent-tool")
        assert "MCP tool not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_graph(self, registry_client, sample_kg_metadata):
        # Register the knowledge graph first
        identifier = await registry_client.register_graph(sample_kg_metadata)

        # Now try to get it
        metadata = await registry_client.get_graph(identifier)
        assert isinstance(metadata, KnowledgeGraphMetadata)
        assert metadata.id == sample_kg_metadata.id
        assert metadata.name == sample_kg_metadata.name
        assert metadata.mcp_compatible == sample_kg_metadata.mcp_compatible

    @pytest.mark.asyncio
    async def test_get_nonexistent_graph(self, registry_client):
        # Test getting a non-existent knowledge graph
        with pytest.raises(RegistryError) as exc_info:
            await registry_client.get_graph("nonexistent-kg")
        assert "Knowledge graph not found" in str(exc_info.value)
