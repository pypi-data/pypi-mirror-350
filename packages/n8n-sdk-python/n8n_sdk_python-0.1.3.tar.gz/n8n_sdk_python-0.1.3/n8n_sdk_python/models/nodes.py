"""
n8n nodes data models.
Define node-related data structures.
"""

from enum import Enum
from typing import Any, Optional

from pydantic import Field, validator

from .base import N8nBaseModel


class NodeType(N8nBaseModel):
    """Node type basic information"""
    name: str = Field(..., description="Node type name")
    displayName: str = Field(..., description="Display name")
    icon: Optional[str] = Field(None, description="Icon")
    description: Optional[str] = Field(None, description="Description")
    version: int = Field(1, description="Version")
    group: list[str] = Field(default_factory=list, description="Group")
    codex: Optional[dict[str, Any]] = Field(None, description="Codex information")
    defaults: Optional[dict[str, Any]] = Field(None, description="Default values")
    sourcePath: Optional[str] = Field(None, description="Source code path")
    supportsCommunityNodes: Optional[bool] = Field(None, description="Whether it supports community nodes")

class NodePropertyType(str, Enum):
    """Node property type enum"""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    COLLECTION = "collection"
    FIXED_COLLECTION = "fixedCollection"
    OPTIONS = "options"
    MULTI_OPTIONS = "multiOptions"
    JSON = "json"
    NOTICE = "notice"
    DATE_TIME = "dateTime"
    COLOR = "color"
    CREDENTIAL = "credential"
    RESOURCE_LOCATOR = "resourceLocator"
    RESOURCE_MAPPER = "resourceMapper"

class NodePropertyOptions(N8nBaseModel):
    """Node property options"""
    name: str = Field(..., description="Option name")
    displayName: str = Field(..., description="Display name")
    description: Optional[str] = Field(None, description="Description")
    type: NodePropertyType = Field(..., description="Property type")
    default: Optional[Any] = Field(None, description="Default value")
    required: Optional[bool] = Field(False, description="Whether required")
    displayOptions: Optional[dict[str, Any]] = Field(None, description="Display options")
    options: Optional[list[dict[str, Any]]] = Field(None, description="Options list")
    placeholder: Optional[str] = Field(None, description="Placeholder")
    typeOptions: Optional[dict[str, Any]] = Field(None, description="Type options")

class NodeTypeDescription(N8nBaseModel):
    """Node type detailed description"""
    displayName: str = Field(..., description="Display name")
    name: str = Field(..., description="Node type name")
    group: list[str] = Field(default_factory=list, description="Node group")
    description: Optional[str] = Field(None, description="Node description")
    version: int = Field(1, description="Node version")
    defaults: Optional[dict[str, Any]] = Field(None, description="Default values")
    inputs: Optional[list[str]] = Field(None, description="Inputs")
    outputs: Optional[list[str]] = Field(None, description="Outputs")
    properties: list[NodePropertyOptions] = Field(default_factory=list, description="Node properties")
    credentials: Optional[list[dict[str, Any]]] = Field(None, description="Node credentials")
    icon: Optional[str] = Field(None, description="Icon")
    subtitle: Optional[str] = Field(None, description="Subtitle")
    maxNodes: Optional[int] = Field(None, description="Maximum number of nodes")
    documentationUrl: Optional[str] = Field(None, description="Documentation URL")
    codex: Optional[dict[str, Any]] = Field(None, description="Codex information")
    sourcePath: Optional[str] = Field(None, description="Source code path")
    supportsCommunityNodes: Optional[bool] = Field(None, description="Whether it supports community nodes")

class NodeParameterOption(N8nBaseModel):
    """Node parameter option"""
    name: str = Field(..., description="Option name")
    value: Any = Field(..., description="Option value")
    description: Optional[str] = Field(None, description="Option description")
    action: Optional[str] = Field(None, description="Option action")
    routing: Optional[dict[str, Any]] = Field(None, description="Routing configuration")

class NodeParameterOptions(N8nBaseModel):
    """Node parameter optional values"""
    resourceName: Optional[str] = Field(None, description="Resource name")
    resourceVersion: Optional[str] = Field(None, description="Resource version")
    operation: Optional[str] = Field(None, description="Operation name")
    properties: dict[str, Any] = Field(default_factory=dict, description="Properties")
    options: list[NodeParameterOption] = Field(default_factory=list, description="Options list")

class NodeParameterValue(N8nBaseModel):
    """Node parameter value"""
    value: Any = Field(..., description="Parameter value")
    routing: Optional[dict[str, Any]] = Field(None, description="Routing configuration")

class NodeConnection(N8nBaseModel):
    """Node connection configuration"""
    main: Optional[list[list[dict[str, Any]]]] = Field(None, description="Main connections")
    other: Optional[dict[str, list[dict[str, Any]]]] = Field(None, description="Other connections")

class NodeCreateResult(N8nBaseModel):
    """Create node result"""
    id: str = Field(..., description="Node ID")
    name: str = Field(..., description="Node name")
    type: str = Field(..., description="Node type")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Node parameters")
    position: dict[str, float] = Field(..., description="Node position")
    typeVersion: int = Field(1, description="Type version")

class NodeCreateError(N8nBaseModel):
    """Create node error"""
    message: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")

class NodeTypeList(N8nBaseModel):
    """Node type list"""
    creatorNodes: Optional[list[str]] = Field(None, description="Creator nodes")
    nodes: dict[str, NodeTypeDescription] = Field(..., description="Node type dictionary")
    count: Optional[int] = Field(None, description="Total count")
    nextCursor: Optional[str] = Field(None, description="Next page cursor")

class NodeCreateOptions(N8nBaseModel):
    """Node options query result"""
    options: dict[str, Any] = Field(..., description="Node options")

class NodeConnectionOptions(N8nBaseModel):
    """Node connection options"""
    sourceNode: str = Field(..., description="Source node ID")
    sourceNodeOutput: Optional[str] = Field(None, description="Source node output")
    targetNode: str = Field(..., description="Target node ID")
    targetNodeInput: Optional[str] = Field(None, description="Target node input") 