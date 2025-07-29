# BioContext Registry Usage Guide

This guide demonstrates how to use the BioContext Registry to discover and manage biomedical tools and knowledge graphs that implement the Model Context Protocol (MCP) standard.

## Installation

```bash
pip install biocontext
```

## Basic Usage

### Initializing the Registry Client

```python
from biocontext.registry import RegistryClient

# Initialize the client with the registry API endpoint
client = RegistryClient("http://localhost:8000")
```

### Registering an MCP Server

```python
from biocontext.registry import MCPServiceMetadata, LicenseEnum, ResourceType
from pydantic import HttpUrl, AnyUrl

# Create MCP server metadata
mcp_metadata = MCPServiceMetadata(
    id="https://example.org/mcp/gene-expression-analyzer",
    name="Gene Expression Analysis Service",
    description="MCP-compliant service for analyzing gene expression data",
    version="1.0.0",
    license=LicenseEnum.MIT,
    keywords=["gene expression", "differential expression", "pathway analysis"],
    creator=[{"@type": "Person", "name": "Jane Doe"}],
    mcp_version="1.0",
    server_capabilities={
        "prompts": True,
        "resources": {"subscribe": True, "listChanged": True},
        "tools": True
    },
    applicationCategory="BioinformaticsWebService",
    programmingLanguage="Python",
    url=AnyUrl("mcp://gene-expression.example.org"),
    resource_type=ResourceType.MCP_SERVER
)

# Register the MCP server
async def register_mcp_server():
    try:
        identifier = await client.register_mcp(mcp_metadata)
        print(f"Registered MCP server with identifier: {identifier}")
    except Exception as e:
        print(f"Error registering server: {e}")
```

### Registering a Knowledge Graph

```python
from biocontext.registry import KnowledgeGraphMetadata, ResourceType
from pydantic import HttpUrl

# Create knowledge graph metadata
graph_metadata = KnowledgeGraphMetadata(
    id="https://example.org/kg/disease-gene",
    name="Disease-Gene Knowledge Graph",
    description="Knowledge graph connecting diseases and genes for use with MCP tools",
    version="1.0.0",
    license=LicenseEnum.APACHE_2_0,
    keywords=["disease", "gene", "knowledge graph"],
    creator=[{"@type": "Person", "name": "John Smith"}],
    distribution=[
        {
            "@type": ["DataDownload", "cr:FileObject"],
            "name": "RDF Distribution",
            "description": "Gzipped RDF distribution",
            "contentUrl": HttpUrl("https://example.org/downloads/disease-gene.rdf.gz"),
            "encodingFormat": "application/gzip",
            "contentSize": "500 MB"
        }
    ],
    conformsTo=[HttpUrl("http://purl.obolibrary.org/obo/hpo.owl")],
    mcp_compatible=True,
    query_interface=HttpUrl("https://example.org/sparql/disease-gene"),
    resource_type=ResourceType.KNOWLEDGE_GRAPH
)

# Register the knowledge graph
async def register_graph():
    try:
        identifier = await client.register_graph(graph_metadata)
        print(f"Registered knowledge graph with identifier: {identifier}")
    except Exception as e:
        print(f"Error registering knowledge graph: {e}")
```

### Registering a Tool

```python
from biocontext.registry import ToolMetadata, ResourceType, LicenseEnum

# Create tool metadata
tool_metadata = ToolMetadata(
    id="https://example.org/tools/expression-analyzer",
    name="Expression Analysis Tool",
    description="Tool for analyzing gene expression data",
    version="1.0.0",
    license=LicenseEnum.MIT,
    keywords=["gene expression", "analysis", "bioinformatics"],
    creator=[{"@type": "Person", "name": "Jane Doe"}],
    applicationCategory="SequenceAnalysisTool",
    programmingLanguage="Python",
    inputData=["FASTA sequence", "Expression matrix"],
    outputData=["Analysis results", "Visualization"],
    featureList=["Differential expression", "Pathway enrichment"],
    resource_type=ResourceType.TOOL
)

# Register the tool
async def register_tool():
    try:
        identifier = await client.register_tool(tool_metadata)
        print(f"Registered tool with identifier: {identifier}")
    except Exception as e:
        print(f"Error registering tool: {e}")
```

### Searching for Resources

```python
from biocontext.registry import ResourceType

async def search_resources():
    try:
        # Search for MCP servers
        mcp_servers = await client.search(
            query="gene expression",
            resource_type=ResourceType.MCP_SERVER,
            filters={
                "applicationCategory": "BioinformaticsWebService",
                "mcp_version": "1.0"
            },
            limit=5
        )
        print(f"Found {len(mcp_servers)} MCP servers")

        # Search for knowledge graphs
        knowledge_graphs = await client.search(
            query="disease",
            resource_type=ResourceType.KNOWLEDGE_GRAPH,
            filters={
                "mcp_compatible": True
            },
            limit=5
        )
        print(f"Found {len(knowledge_graphs)} knowledge graphs")

        # Search for tools
        tools = await client.search(
            query="sequence analysis",
            resource_type=ResourceType.TOOL,
            filters={
                "applicationCategory": "SequenceAnalysisTool"
            },
            limit=5
        )
        print(f"Found {len(tools)} tools")
    except Exception as e:
        print(f"Error searching resources: {e}")
```

### Retrieving Specific Resources

```python
from biocontext.registry import RegistryError

async def get_resources():
    try:
        # Get a specific MCP server
        server = await client.get_mcp("gene-expression-analyzer")
        print(f"Server name: {server.name}")
        print(f"Server capabilities: {server.server_capabilities}")

        # Get a specific knowledge graph
        graph = await client.get_graph("disease-gene")
        print(f"Knowledge graph name: {graph.name}")
        print(f"MCP compatible: {graph.mcp_compatible}")

        # Get a specific tool
        tool = await client.get_tool("expression-analyzer")
        print(f"Tool name: {tool.name}")
        print(f"Features: {tool.featureList}")
    except RegistryError as e:
        print(f"Resource not found: {e}")
    except Exception as e:
        print(f"Error retrieving resources: {e}")
```

### Updating Resource Metadata

```python
async def update_resource():
    try:
        # Get existing MCP server
        server = await client.get_mcp("gene-expression-analyzer")

        # Update metadata
        server.version = "1.0.1"
        server.server_capabilities["resources"]["listChanged"] = True

        # Save updates
        success = await client.update_metadata("gene-expression-analyzer", server)
        print(f"Update successful: {success}")
    except RegistryError as e:
        print(f"Resource not found: {e}")
    except Exception as e:
        print(f"Error updating resource: {e}")
```

## Advanced Usage

### Using Schema.org Properties

All resources in the registry follow the Schema.org metadata model:

```python
# Add Schema.org properties to MCP server metadata
mcp_metadata.publisher = {
    "@type": "Organization",
    "name": "BioAI Corp",
    "url": HttpUrl("https://example.org/bioaicorp")
}
mcp_metadata.datePublished = "2024-01-15"
mcp_metadata.dateModified = "2024-02-01"

# Add Schema.org properties to knowledge graph
graph_metadata.provider = {
    "@type": "Organization",
    "name": "BioKG Foundation",
    "url": HttpUrl("https://example.org/biokg")
}
graph_metadata.dateCreated = "2024-01-01"
```

### Complex Search Queries

```python
async def complex_search():
    try:
        # Search for MCP servers with specific capabilities
        results = await client.search(
            query="gene expression analysis",
            resource_type=ResourceType.MCP_SERVER,
            filters={
                "applicationCategory": "BioinformaticsWebService",
                "mcp_version": "1.0",
                "server_capabilities.prompts": True,
                "server_capabilities.resources.subscribe": True
            },
            limit=10,
            offset=0
        )
        print(f"Found {len(results)} matching servers")
    except Exception as e:
        print(f"Error performing complex search: {e}")
```

## Best Practices

1. **Metadata Quality**:

    - Provide clear descriptions of resource capabilities
    - Use appropriate Schema.org properties
    - Include comprehensive distribution information
    - Document resource dependencies and requirements

2. **Versioning**:

    - Use semantic versioning
    - Document changes between versions
    - Track MCP version compatibility
    - Maintain backward compatibility when possible

3. **Search Optimization**:

    - Use specific domain keywords
    - Include relevant Schema.org properties
    - Document resource capabilities clearly
    - Provide example use cases

4. **Error Handling**:

```python
from biocontext.registry import RegistryError

async def safe_operation():
    try:
        result = await client.get_mcp("non-existent-server")
    except RegistryError as e:
        print(f"Resource not found: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

## Contributing

To contribute to the registry:

1. Follow the Schema.org metadata model
2. Implement the MCP standard for services
3. Provide comprehensive documentation
4. Include unit tests
5. Update the registry client as needed
