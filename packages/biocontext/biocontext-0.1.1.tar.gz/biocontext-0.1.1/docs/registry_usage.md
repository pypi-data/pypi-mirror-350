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

### Registering an MCP Tool

```python
from biocontext.registry import MCPMetadata, License

# Create MCP metadata for a biomedical tool
mcp_metadata = MCPMetadata(
    identifier="gene-expression-analyzer-001",
    name="Gene Expression Analysis Tool",
    description="MCP-compliant tool for analyzing gene expression data",
    version="1.0.0",
    domain="bioinformatics",
    data_types=["RNA-seq", "microarray"],
    format="python",
    size=1024 * 1024,  # 1MB
    license=License.MIT,
    doi="10.1234/tool.001",
    keywords=["gene expression", "differential expression", "pathway analysis"],
    authors=["Jane Doe", "John Smith"],
    properties={
        "mcp_version": "1.0",
        "input_schema": "gene_expression_matrix",
        "output_schema": "differential_expression_results",
        "supported_models": ["gpt-4", "claude-3"],
        "tool_capabilities": ["differential_expression", "pathway_enrichment"]
    }
)

# Register the MCP tool
async def register_mcp_tool():
    try:
        identifier = await client.register_mcp(mcp_metadata)
        print(f"Registered MCP tool with identifier: {identifier}")
    except Exception as e:
        print(f"Error registering tool: {e}")
```

### Registering a Knowledge Graph

```python
from biocontext.registry import KnowledgeGraphMetadata

# Create knowledge graph metadata
graph_metadata = KnowledgeGraphMetadata(
    identifier="disease-gene-001",
    name="Disease-Gene Knowledge Graph",
    description="Knowledge graph connecting diseases and genes for use with MCP tools",
    version="1.0.0",
    ontology_used=["GO", "HPO", "DO"],
    node_types=["Gene", "Disease", "Phenotype"],
    edge_types=["ASSOCIATED_WITH", "ENCODES", "CAUSES"],
    format="neo4j",
    size=2048 * 1024,  # 2MB
    license=License.APACHE2,
    doi="10.1234/disease-gene.001",
    keywords=["disease", "gene", "knowledge graph"],
    authors=["Jane Doe", "John Smith"],
    properties={
        "mcp_compatible": True,
        "query_interface": "cypher",
        "supported_tools": ["gene-expression-analyzer-001"]
    }
)

# Register the knowledge graph
async def register_graph():
    try:
        identifier = await client.register_graph(graph_metadata)
        print(f"Registered knowledge graph with identifier: {identifier}")
    except Exception as e:
        print(f"Error registering knowledge graph: {e}")
```

### Searching for Resources

```python
from biocontext.registry import ResourceType

async def search_resources():
    try:
        # Search for gene expression analysis tools
        expression_tools = await client.search(
            query="gene expression",
            resource_type=ResourceType.MCP,
            filters={
                "domain": "bioinformatics",
                "properties.mcp_version": "1.0"
            },
            limit=5
        )
        print(f"Found {len(expression_tools)} gene expression tools")

        # Search for disease-related knowledge graphs
        disease_graphs = await client.search(
            query="disease",
            resource_type=ResourceType.KNOWLEDGE_GRAPH,
            filters={
                "ontology_used": "HPO",
                "properties.mcp_compatible": True
            },
            limit=5
        )
        print(f"Found {len(disease_graphs)} disease knowledge graphs")
    except Exception as e:
        print(f"Error searching resources: {e}")
```

### Retrieving Specific Resources

```python
from biocontext.registry import RegistryError

async def get_resources():
    try:
        # Get a specific MCP tool
        tool = await client.get_mcp("gene-expression-analyzer-001")
        print(f"Tool name: {tool.name}")
        print(f"Supported models: {tool.properties['supported_models']}")

        # Get a specific knowledge graph
        graph = await client.get_graph("disease-gene-001")
        print(f"Knowledge graph name: {graph.name}")
        print(f"MCP compatible: {graph.properties['mcp_compatible']}")
    except RegistryError as e:
        print(f"Resource not found: {e}")
    except Exception as e:
        print(f"Error retrieving resources: {e}")
```

### Updating Resource Metadata

```python
async def update_resource():
    try:
        # Get existing MCP tool
        tool = await client.get_mcp("gene-expression-analyzer-001")

        # Update metadata
        tool.version = "1.0.1"
        tool.properties["supported_models"].append("llama-2")

        # Save updates
        success = await client.update_metadata("gene-expression-analyzer-001", tool)
        print(f"Update successful: {success}")
    except RegistryError as e:
        print(f"Resource not found: {e}")
    except Exception as e:
        print(f"Error updating resource: {e}")
```

## Advanced Usage

### Using MCP-Specific Properties

Both MCP tools and Knowledge Graphs can include MCP-specific properties:

```python
# Add MCP-specific properties to tool metadata
mcp_metadata.properties.update({
    "mcp_version": "1.0",
    "input_schema": "gene_expression_matrix",
    "output_schema": "differential_expression_results",
    "supported_models": ["gpt-4", "claude-3"],
    "tool_capabilities": ["differential_expression", "pathway_enrichment"],
    "example_prompts": [
        "Analyze differential expression between control and treatment groups",
        "Perform pathway enrichment analysis on differentially expressed genes"
    ]
})

# Add MCP integration properties to knowledge graph
graph_metadata.properties.update({
    "mcp_compatible": True,
    "query_interface": "cypher",
    "supported_tools": ["gene-expression-analyzer-001"],
    "example_queries": [
        "MATCH (g:Gene)-[:ASSOCIATED_WITH]->(d:Disease) RETURN g, d LIMIT 10"
    ]
})
```

### Complex Search Queries

```python
async def complex_search():
    try:
        # Search for tools with specific MCP capabilities
        results = await client.search(
            query="gene expression analysis",
            resource_type=ResourceType.MCP,
            filters={
                "domain": "bioinformatics",
                "properties.mcp_version": "1.0",
                "properties.supported_models": "gpt-4",
                "properties.tool_capabilities": "pathway_enrichment"
            },
            limit=10,
            offset=0
        )
        print(f"Found {len(results)} matching tools")
    except Exception as e:
        print(f"Error performing complex search: {e}")
```

## Best Practices

1. **Metadata Quality**:

    - Provide clear descriptions of tool capabilities
    - Specify MCP version and compatibility
    - Document input/output schemas
    - Include example prompts and usage

2. **Versioning**:

    - Use semantic versioning
    - Document changes between versions
    - Track MCP version compatibility
    - Maintain backward compatibility when possible

3. **Search Optimization**:

    - Use specific domain keywords
    - Include MCP-specific properties
    - Document tool capabilities clearly
    - Provide example use cases

4. **Error Handling**:

```python
from biocontext.registry import RegistryError

async def safe_operation():
    try:
        result = await client.get_mcp("non-existent-tool")
    except RegistryError as e:
        print(f"Resource not found: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

## Contributing

To contribute to the registry:

1. Follow the MCP standard for tool implementation
2. Provide comprehensive documentation
3. Include unit tests
4. Update the registry client as needed
