"""Schema for a shared MCP and KG registry."""

from enum import Enum
from typing import Any

from pydantic import AnyUrl, BaseModel, Field, HttpUrl


class SchemaOrgContext(BaseModel):
    """
    Defines the JSON-LD context.
    Provides a default context for schema.org and common extensions.
    """

    context: dict[str, HttpUrl] = Field(
        default_factory=lambda: {
            "@vocab": HttpUrl("https://schema.org/"),
            "rdf": HttpUrl("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
            "rdfs": HttpUrl("http://www.w3.org/2000/01/rdf-schema#"),
            "xsd": HttpUrl("http://www.w3.org/2001/XMLSchema#"),
            "cr": HttpUrl("http://mlcommons.org/croissant/"),
            "bioschemas": HttpUrl("https://bioschemas.org/profiles/"),
            "dct": HttpUrl("http://purl.org/dc/terms/"),
            "pav": HttpUrl("http://purl.org/pav/"),
            "bc": HttpUrl("https://biocontext.org/registry/terms/"),  # Placeholder for custom terms
        },
        alias="@context",
        description="The JSON-LD context.",
    )
    id: str | None = Field(None, alias="@id", description="The JSON-LD identifier (typically a URI).")
    type: str | list[str] = Field(..., alias="@type", description="The JSON-LD type(s).")


class ResourceType(str, Enum):
    """Type of resource in the registry for internal classification."""

    MCP_SERVER = "mcp_server"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    DATASET = "dataset"
    TOOL = "tool"
    GENERIC_RESOURCE = "generic_resource"


class LicenseEnum(str, Enum):
    """Common license types, encouraging SPDX identifiers or URLs."""

    MIT = "MIT"
    APACHE_2_0 = "Apache-2.0"
    GPL_3_0_ONLY = "GPL-3.0-only"
    GPL_3_0_OR_LATER = "GPL-3.0-or-later"
    CC_BY_4_0 = "CC-BY-4.0"
    CC_BY_SA_4_0 = "CC-BY-SA-4.0"
    CC_BY_NC_4_0 = "CC-BY-NC-4.0"
    CC0_1_0 = "CC0-1.0"
    PROPRIETARY = "proprietary"  # For truly proprietary cases
    OTHER = "other"  # Use if an exact SPDX or common license URL isn't listed


class PersonOrOrganization(BaseModel):
    """
    Represents a person or an organization, mapping to schema.org:Person or schema.org:Organization.
    """

    type: str = Field(..., alias="@type", description="Typically 'Person' or 'Organization'.")
    name: str = Field(..., description="Name of the person or organization (schema:name).")
    url: HttpUrl | None = Field(None, description="URL for the person or organization (schema:url).")
    identifier: str | None = Field(None, description="Unique identifier, e.g., ORCID for a person (schema:identifier).")


class Distribution(BaseModel):
    """
    Represents a schema.org:DataDownload or cr:FileObject/cr:FileSet.
    """

    type: str | list[str] = Field(default=["DataDownload", "cr:FileObject"], alias="@type")
    name: str | None = Field(None, description="Name of the distribution (schema:name).")
    description: str | None = Field(None, description="Description of the distribution (schema:description).")
    contentUrl: HttpUrl = Field(..., description="URL to download the content (schema:contentUrl / cr:contentUrl).")
    encodingFormat: str = Field(
        ..., description="MIME type of the content (schema:encodingFormat / cr:encodingFormat)."
    )
    contentSize: str | None = Field(
        None, description="Size of the content, e.g., '10 MB' (schema:contentSize / cr:contentSize)."
    )
    sha256: str | None = Field(None, description="SHA256 checksum of the content (schema:sha256 / cr:sha256).")
    # Croissant specific for FileSet
    includes: str | None = Field(None, description="Glob pattern for files in an archive (cr:includes).")
    containedIn: HttpUrl | None = Field(None, description="If part of an archive, its URL (cr:containedIn).")
    additionalProperties: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Custom properties not fitting standard fields, mapping to schema:additionalProperty.",
    )


class RegisteredResource(SchemaOrgContext):
    """
    Base model for any resource in the registry, aligning with schema.org:CreativeWork.
    """

    # Core schema.org properties
    # @id and @type are inherited from SchemaOrgContext
    name: str = Field(..., description="Name of the resource (schema:name).")
    description: str = Field(..., description="Description of the resource (schema:description).")
    identifier: str | list[str] | None = Field(
        None,
        description="Unique identifier(s) for the resource, e.g., DOI, accession number (schema:identifier). Should be a URL or CURIE if possible.",
    )
    keywords: list[str] = Field(default_factory=list, description="Keywords describing the resource (schema:keywords).")
    license: HttpUrl | LicenseEnum | str = Field(
        ...,
        description="License under which the resource is available (schema:license). Should be a URL to the license text or an SPDX identifier.",
    )
    version: str | None = Field(None, description="Version of the resource (schema:version).")
    url: AnyUrl | None = Field(
        None,
        description="Canonical URL of the resource itself or its landing page (schema:url). Supports custom URI schemes like mcp:// for MCP servers.",
    )

    creator: list[PersonOrOrganization] = Field(
        default_factory=list, description="Creator(s) of the resource (schema:creator)."
    )
    publisher: PersonOrOrganization | None = Field(None, description="Publisher of the resource (schema:publisher).")
    provider: PersonOrOrganization | None = Field(
        None, description="The organization ultimately providing the resource (schema:provider)."
    )

    dateCreated: str | None = Field(None, description="Date of creation (schema:dateCreated, YYYY-MM-DD or ISO 8601).")
    datePublished: str | None = Field(
        None, description="Date of publication (schema:datePublished, YYYY-MM-DD or ISO 8601)."
    )
    dateModified: str | None = Field(
        None, description="Date of last modification (schema:dateModified, YYYY-MM-DD or ISO 8601)."
    )

    # For Croissant dataset representation (schema:Dataset / cr:Dataset)
    distribution: list[Distribution] = Field(
        default_factory=list,
        description="Available distributions of the dataset (schema:distribution / cr:distribution).",
    )
    # Further Croissant fields like recordSet would require more complex modeling,
    # potentially handled by a dedicated Croissant builder or by storing raw JSON for cr:RecordSet.

    # Internal registry classification
    resource_type: ResourceType = Field(..., description="Internal classification type for the registry.")

    additionalProperties: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Custom properties not fitting standard fields, mapping to schema:additionalProperty.",
    )

    class Config:
        use_enum_values = True  # Ensures enum values are used in serialization
        allow_population_by_field_name = True


class MCPServiceMetadata(RegisteredResource):
    """
    Metadata for MCP-compliant servers/tools.
    Maps to schema:SoftwareApplication, potentially bioschemas:ComputationalTool.
    """

    type: str | list[str] = Field(default=["SoftwareApplication", "bioschemas:ComputationalTool"], alias="@type")
    resource_type: ResourceType = Field(default=ResourceType.MCP_SERVER)

    # MCP-specific, to be mapped appropriately during JSON-LD serialization
    # Some could be schema:featureList, schema:softwareVersion (for mcp_version),
    # schema:WebAPI for describing tool interfaces.
    mcp_version: str = Field(..., description="MCP protocol version supported by the server.")
    server_capabilities: dict[str, Any] = Field(
        default_factory=dict,
        description="Capabilities of the MCP server (e.g., { 'prompts': true, 'resources': { 'subscribe': true } }). Maps to schema:featureList or custom terms.",
    )

    # If the MCP server offers tools, they can be listed as separate ToolMetadata entries
    # and linked via schema:hasPart or a custom relation.
    # If the MCP server offers datasets, they can be listed as separate DatasetMetadata entries
    # and linked.

    # Existing fields from MCPMetadata to integrate/map:
    # domain: str -> schema:applicationCategory or schema:applicationSubCategory
    # data_types: list[str] -> schema:inputNodeType / schema:outputNodeType (if tools) or custom
    # format: str -> schema:softwareHelp (if it means implementation language like Python) or schema:programmingLanguage
    # size: int -> This is tricky for a server; perhaps refers to a default dataset it serves? If so, belongs to that dataset's metadata.
    applicationCategory: str | None = Field(
        None,
        description="Domain of the tool/server (e.g., bioinformatics, cheminformatics) (schema:applicationCategory).",
    )
    programmingLanguage: str | None = Field(
        None, description="Implementation language/format (schema:programmingLanguage)."
    )

    # Link to offered tools/resources/prompts
    # These would typically be separate registry entries linked here.
    offeredTools: list[HttpUrl] = Field(
        default_factory=list, description="List of URIs/PIDs of tools offered by this MCP server."
    )
    offeredResources: list[HttpUrl] = Field(
        default_factory=list, description="List of URIs/PIDs of data resources offered by this MCP server."
    )
    offeredPrompts: list[HttpUrl] = Field(
        default_factory=list, description="List of URIs/PIDs of prompts offered by this MCP server."
    )


class KnowledgeGraphMetadata(RegisteredResource):
    """
    Metadata for knowledge graphs and other knowledge representations.
    Maps to schema:Dataset, cr:Dataset, bioschemas:Dataset.
    """

    type: str | list[str] = Field(default=["Dataset", "cr:Dataset", "bioschemas:Dataset"], alias="@type")
    resource_type: ResourceType = Field(default=ResourceType.KNOWLEDGE_GRAPH)

    # Knowledge graph specific, mapping to schema.org/Croissant/BioSchemas
    conformsTo: list[HttpUrl] = Field(
        default_factory=list,
        description="Ontologies or standards the KG conforms to (schema:conformsTo / dct:conformsTo). List of ontology URLs.",
    )  # Replaces ontology_used
    # node_types and edge_types are better represented within a Croissant cr:RecordSet description
    # if we are detailing the KG structure as a dataset. For a high-level overview,
    # they can be schema:keywords or schema:additionalProperty.
    # For now, let's keep them as keywords or add to additionalProperties.

    # Technical metadata already covered by RegisteredResource.distribution
    # format: str -> use distribution.encodingFormat
    # size: int -> use distribution.contentSize

    # MCP integration properties
    mcp_compatible: bool | None = Field(None, description="Indicates if the KG has an MCP-compatible interface.")
    query_interface: HttpUrl | None = Field(
        None,
        description="Endpoint for querying the KG (e.g., SPARQL endpoint). Could be part of schema:distribution with type schema:WebAPI.",
    )
    supported_tools: list[HttpUrl] = Field(
        default_factory=list, description="List of URIs/PIDs of tools that can operate on this KG."
    )


class ToolMetadata(RegisteredResource):  # New class for tools, could be offered by MCP
    """
    Metadata for a specific tool, potentially offered by an MCP server.
    Maps to schema:SoftwareApplication, bioschemas:ComputationalTool.
    """

    type: str | list[str] = Field(default=["SoftwareApplication", "bioschemas:ComputationalTool"], alias="@type")
    resource_type: ResourceType = Field(default=ResourceType.TOOL)

    applicationCategory: str | None = Field(None, description="Domain of the tool (schema:applicationCategory).")
    programmingLanguage: str | None = Field(None, description="Implementation language (schema:programmingLanguage).")
    # inputSchema and outputSchema from MCP can be represented using schema:WebAPI or by linking to JSON schema documents
    inputData: list[str] = Field(
        default_factory=list, description="Description of input data types or formats (schema:inputNodeType or custom)."
    )
    outputData: list[str] = Field(
        default_factory=list,
        description="Description of output data types or formats (schema:outputNodeType or custom).",
    )
    # tool_capabilities from MCP
    featureList: list[str] = Field(default_factory=list, description="Capabilities of the tool (schema:featureList).")


class DatasetMetadata(RegisteredResource):  # New class for generic datasets
    """
    Metadata for a generic dataset, using Croissant extensions.
    Maps to schema:Dataset, cr:Dataset, bioschemas:Dataset.
    """

    type: str | list[str] = Field(default=["Dataset", "cr:Dataset", "bioschemas:Dataset"], alias="@type")
    resource_type: ResourceType = Field(default=ResourceType.DATASET)

    # Detailed Croissant structure (recordSet, subField, source, etc.)
    # would typically be a more complex object. For now, this Pydantic model
    # focuses on top-level Croissant/Schema.org properties.
    # The full Croissant JSON-LD could be stored in an 'additionalProperties'
    # field or a dedicated field if it's too complex for direct Pydantic mapping.
    croissant_metadata: dict[str, Any] | None = Field(
        None,
        description="Full Croissant JSON-LD metadata if too complex for direct mapping, or specific cr:RecordSet details.",
    )


# Example usage (for testing, not part of the final schema file usually)
if __name__ == "__main__":
    # Example for a Knowledge Graph
    kg_meta = KnowledgeGraphMetadata.parse_obj({
        "@id": "https://example.org/kgs/mybiokg",
        "@type": ["Dataset", "cr:Dataset", "bioschemas:Dataset"],
        "name": "My Biomedical Knowledge Graph",
        "description": "A comprehensive KG integrating protein interactions and gene expressions.",
        "keywords": ["bioinformatics", "systems biology", "protein interactions", "gene expression"],
        "license": LicenseEnum.CC_BY_4_0,
        "version": "1.2.0",
        "url": AnyUrl("https://example.org/portal/mybiokg"),
        "creator": [
            {"@type": "Organization", "name": "Awesome BioData Lab", "url": HttpUrl("https://example.org/awesomelab")}
        ],
        "publisher": {
            "@type": "Organization",
            "name": "University of BioStudies",
            "url": HttpUrl("https://example.org/biostudies"),
        },
        "datePublished": "2024-05-16",
        "distribution": [
            {
                "@type": ["DataDownload", "cr:FileObject"],
                "name": "RDF Distribution",
                "description": "Gzipped RDF distribution of MyBioKG",
                "contentUrl": HttpUrl("https://example.org/downloads/mybiokg_v1.2.0.rdf.gz"),
                "encodingFormat": "application/gzip",
                "contentSize": "500 MB",
                "sha256": "abcdef123456...",
                "includes": "*.rdf",
                "containedIn": None,
                "additionalProperties": [{"@type": "cr:FileObject", "cr:encodingFormat": "application/rdf+xml"}],
            },
            {
                "@type": ["WebAPI"],
                "name": "SPARQL Endpoint",
                "description": "Public SPARQL endpoint for MyBioKG",
                "contentUrl": HttpUrl("https://example.org/sparql/mybiokg"),
                "encodingFormat": "application/sparql-results+json",
                "contentSize": None,
                "sha256": None,
                "includes": None,
                "containedIn": None,
            },
        ],
        "conformsTo": [HttpUrl("http://purl.obolibrary.org/obo/go.owl"), HttpUrl("http://edamontology.org/")],
        "mcp_compatible": True,
        "query_interface": HttpUrl("https://example.org/sparql/mybiokg"),
        "resource_type": ResourceType.KNOWLEDGE_GRAPH,
    })
    print(kg_meta.json(by_alias=True, exclude_none=True, indent=2))

    # Example for an MCP Server
    mcp_server_meta = MCPServiceMetadata.parse_obj({
        "@id": "https://example.org/mcp/protein_analyzer_v2",
        "name": "Protein Analyzer Service v2",
        "description": "An MCP-compliant service for advanced protein sequence analysis.",
        "keywords": ["protein", "sequence analysis", "MCP", "bioinformatics tool"],
        "license": LicenseEnum.APACHE_2_0,
        "version": "2.0.1",
        "url": AnyUrl("mcp://protein-analyzer.example.org"),
        "publisher": {"@type": "Organization", "name": "BioAI Corp", "url": HttpUrl("https://example.org/bioaicorp")},
        "datePublished": "2024-01-15",
        "mcp_version": "1.0",
        "server_capabilities": {"prompts": True, "resources": {"subscribe": True, "listChanged": True}, "tools": True},
        "applicationCategory": "BioinformaticsWebService",
        "programmingLanguage": "Python",
        "offeredTools": [HttpUrl("https://example.org/registry/tools/blast_wrapper_v1.2")],
        "resource_type": ResourceType.MCP_SERVER,
    })
    print(mcp_server_meta.json(by_alias=True, exclude_none=True, indent=2))

    # Example for a Tool
    tool_meta = ToolMetadata.parse_obj({
        "@id": "https://example.org/registry/tools/blast_wrapper_v1.2",
        "name": "BLAST Wrapper Tool",
        "description": "A tool that wraps NCBI BLAST for sequence alignment, offered via an MCP server.",
        "keywords": ["BLAST", "sequence alignment", "bioinformatics"],
        "license": LicenseEnum.GPL_3_0_OR_LATER,
        "version": "1.2",
        "creator": [{"@type": "Person", "name": "Dr. Jane Coder", "identifier": "orcid:0000-0002-1825-0097"}],
        "applicationCategory": "SequenceAnalysisTool",
        "programmingLanguage": "Python",
        "inputData": ["FASTA sequence (string)", "schema:Dataset (containing FASTA files)"],
        "outputData": ["schema:Dataset (alignment results in tabular format)"],
        "featureList": ["Supports protein and nucleotide BLAST", "Configurable E-value threshold"],
        "resource_type": ResourceType.TOOL,
    })
    print(tool_meta.json(by_alias=True, exclude_none=True, indent=2))
