"""
n8n workflow data models.
Define workflow-related data structures.
"""

from typing import Any, Optional

from pydantic import Field, validator, RootModel
from datetime import datetime

from .base import N8nBaseModel


class NodeParameter(N8nBaseModel, RootModel[dict[str, Any]]):
    """Node parameters, allows arbitrary structure for defining node configuration and behavior"""
    pass

class Connection(N8nBaseModel):
    """Connection between nodes, defines data flow in the workflow"""
    node: str = Field(..., description="Target node name, indicates the node where data flows to")
    type: str = Field("main", description="Connection type, mainly 'main', indicating standard data flow")
    index: int = Field(0, description="Target node input index, determines which input port the data enters")

class NodeConnection(N8nBaseModel):
    """Node connection collection, includes various types of connections"""
    main: Optional[list[list[Connection]]] = Field(None, description="Main connections list, each output port corresponds to a connection list")

class NodeCredential(N8nBaseModel):
    """Credential reference used by a node for accessing external services"""
    id: Optional[str] = Field(None, description="Unique identifier of the credential")
    name: str = Field(..., description="Display name of the credential, used for identification in the interface")

class Node(N8nBaseModel):
    """Node in a workflow, represents a processing step or operation"""
    id: Optional[str] = Field(None, description="Unique identifier of the node, typically a UUID, n8n will generate it automatically")
    name: str = Field(..., description="Display name of the node, used for identification in the interface")
    type: str = Field(..., description="Node type, such as 'n8n-nodes-base.HttpRequest', specifies node functionality and behavior")
    typeVersion: int | float = Field(1, description="Version number of the node type, controls node features")
    position: list[float] = Field(..., description="Node position coordinates in the workflow editor [x, y]")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Node parameter settings, defines how the node works")
    credentials: Optional[dict[str, NodeCredential]] = Field(
        None, description="Credentials used by the node, keys are credential types, values are credential references"
    )
    disabled: Optional[bool] = Field(False, description="Whether the node is disabled, disabled nodes are skipped during execution")
    notes: Optional[str] = Field("", description="Note text for the node, used to record node purpose or important information")
    webhookId: Optional[str] = Field(None, description="Unique identifier for webhook nodes, used for external triggering")
    notesInFlow: Optional[bool] = Field(False, description="Whether to display node notes in the workflow diagram")
    executeOnce: Optional[bool] = Field(False, description="Whether the node executes only once when the workflow starts")
    onError: Optional[str] = Field("stopWorkflow", description="Node error handling strategy, such as 'stopWorkflow' or 'continueWorkflow'")
    continueOnFail: Optional[bool] = Field(False, description="Whether to continue workflow execution when the node fails")
    alwaysOutputData: Optional[bool] = Field(False, description="Whether the node still outputs data even if it fails")
    retryOnFail: Optional[bool] = Field(False, description="Whether to retry automatically when the node fails")
    maxTries: Optional[int] = Field(1, description="Maximum number of retries when the node fails")
    waitBetweenTries: Optional[int] = Field(1000, description="Wait time between retries (milliseconds)")
    createdAt: Optional[datetime] = Field(None, description="Node creation time")
    updatedAt: Optional[datetime] = Field(None, description="Node last update time")

class WorkflowSettings(N8nBaseModel):
    """Workflow execution and behavior settings"""
    saveExecutionProgress: Optional[bool] = Field(True, description="Whether to save workflow execution progress information")
    saveDataErrorExecution: Optional[str] = Field("all", description="Data saving strategy for error executions: 'all', 'none' or specific node ID")
    saveDataSuccessExecution: Optional[str] = Field("all", description="Data saving strategy for successful executions: 'all', 'none' or specific node ID")
    saveManualExecutions: Optional[bool] = Field(True, description="Whether to save manually triggered executions")
    executionTimeout: Optional[int] = Field(3600, description="Workflow execution timeout in seconds")
    timezone: Optional[str] = Field("America/New_York", description="Timezone used by the workflow, default is 'America/New_York'")
    errorWorkflow: Optional[str] = Field(None, description="ID of the error handling workflow to trigger when workflow errors")
    executionOrder: Optional[str] = Field("v1", description="Workflow execution order strategy, currently supports 'v1'")

class Tag(N8nBaseModel):
    """Tag, used for organizing and categorizing workflows"""
    id: str = Field(..., description="Unique identifier of the tag")
    name: str = Field(..., description="Display name of the tag")
    createdAt: Optional[datetime] = Field(None, description="Tag creation time")
    updatedAt: Optional[datetime] = Field(None, description="Tag last update time")

class TagList(N8nBaseModel):
    """Tag list response model, used for API responses when getting tag lists"""
    data: list[Tag] = Field(..., description="List of tag objects")
    nextCursor: Optional[str] = Field(None, description="Pagination cursor, used to get the next page of data")
    count: Optional[int] = Field(None, description="Total number of tags")
    
class WorkflowStaticData(N8nBaseModel):
    """Workflow static data, used to save state between executions"""
    lastId: Optional[int] = Field(None, description="Last used ID or counter, used to generate unique values")
    # Add other fields if necessary based on actual staticData structure

class Workflow(N8nBaseModel):
    """Complete workflow model, contains all workflow definitions and metadata"""
    id: str = Field(..., description="Unique identifier of the workflow")
    name: str = Field(..., description="Display name of the workflow")
    active: bool = Field(False, description="Whether the workflow is active, only active workflows will be triggered for execution")
    connections: dict[str, dict[str, list[list[Connection]]]] = Field(
        default_factory=dict, description="Defines connections between nodes, guiding how data flows from one node to another"
    )
    nodes: list[Node] = Field(default_factory=list, description="Collection of all nodes in the workflow, defining the workflow's processing logic")
    settings: Optional[WorkflowSettings] = Field(None, description="Workflow execution settings and behavior configuration")
    tags: Optional[list[Tag]] = Field(None, description="List of tags assigned to the workflow, used for organization and categorization")
    pinData: Optional[dict[str, Any]] = Field(None, description="Test data pinned to workflow nodes")
    staticData: Optional[WorkflowStaticData | dict[str, Any]] = Field(None, description="Workflow's persistent static data, saved between executions")
    versionId: Optional[str] = Field(None, description="Workflow version identifier, used for tracking changes")
    meta: Optional[dict[str, Any]] = Field(None, description="Workflow metadata, contains additional descriptive information")
    updatedAt: Optional[datetime] = Field(None, description="Time when the workflow was last updated")
    createdAt: Optional[datetime] = Field(None, description="Time when the workflow was created")

class WorkflowShort(N8nBaseModel):
    """Brief workflow information model, used for list display, contains only basic properties"""
    id: str = Field(..., description="Unique identifier of the workflow")
    name: str = Field(..., description="Display name of the workflow")
    active: bool = Field(False, description="Whether the workflow is active")
    createdAt: Optional[datetime] = Field(None, description="Time when the workflow was created")
    updatedAt: Optional[datetime] = Field(None, description="Time when the workflow was last updated")
    tags: Optional[list[Tag]] = Field(None, description="List of tags assigned to the workflow")

class WorkflowList(N8nBaseModel):
    """Workflow list response model, used for API responses when getting workflow lists"""
    data: list[WorkflowShort] = Field(..., description="List of brief workflow information")
    nextCursor: Optional[str] = Field(None, description="Pagination cursor, used to get the next page of workflow list")
    count: Optional[int] = Field(None, description="Total number of workflows")

class WorkflowCreate(N8nBaseModel):
    """Create workflow request model, defines the data required to create a new workflow"""
    name: str = Field(..., description="Name of the new workflow, must be provided")
    nodes: list[Node] = Field(default_factory=list, description="Collection of nodes in the workflow, defining processing logic")
    connections: dict[str, dict[str, list[list[Connection]]]] = Field(
        default_factory=dict, description="Definition of connections between nodes, guiding data flow"
    )
    settings: Optional[WorkflowSettings] = Field(None, description="Workflow execution and behavior settings")
    staticData: Optional[WorkflowStaticData | dict[str, Any]] = Field(None, description="Initial static data for the workflow")

class WorkflowUpdate(N8nBaseModel):
    """Update workflow request model, defines properties that can be changed when updating an existing workflow"""
    name: Optional[str] = Field(None, description="New name for the workflow")
    active: Optional[bool] = Field(None, description="Whether the workflow is active")
    nodes: Optional[list[Node]] = Field(None, description="New collection of nodes in the workflow")
    connections: Optional[dict[str, dict[str, list[list[Connection]]]]] = Field(None, description="New definition of node connections")
    settings: Optional[WorkflowSettings] = Field(None, description="New values for workflow settings")
    staticData: Optional[WorkflowStaticData | dict[str, Any]] = Field(None, description="New value for workflow static data")

class WorkflowTransferRequest(N8nBaseModel):
    """Workflow transfer request model, used to transfer workflow to another project"""
    destinationProjectId: str = Field(..., description="Unique identifier of the destination project, workflow will be transferred to this project")

class WorkflowTagUpdateRequestItem(N8nBaseModel):
    """Single tag item in workflow tag update request, used to add or remove tags"""
    id: str = Field(..., description="Unique identifier of the tag")

# NOTE: WorkflowRunResult model is custom, used to handle workflow execution results
class WorkflowRunResult(N8nBaseModel):
    """Workflow execution result, contains execution identifier and generated data"""
    executionId: str = Field(..., description="Unique identifier of the execution, can be used to query execution details")
    data: Optional[dict[str, Any]] = Field(None, description="Data or results generated by the execution")
