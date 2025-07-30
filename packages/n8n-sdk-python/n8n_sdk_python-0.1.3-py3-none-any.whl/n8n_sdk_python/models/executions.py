"""
This module contains the models for executions in the n8n workflow engine.
Defines the data structures for workflow executions, including the status, data, and other related information.
"""

from enum import Enum
from datetime import datetime
from typing import Any, Optional

from pydantic import Field, validator, RootModel

from .base import N8nBaseModel


class ExecutionStatus(str, Enum):
    """Execution status enum, defines possible states of workflow execution"""
    ERROR = "error"  # Execution failed
    SUCCESS = "success"  # Execution completed successfully
    WAITING = "waiting"  # Waiting, possibly for external trigger or scheduled execution
    # RUNNING status is not listed in the current n8n API documentation, so not adding it

class ExecutionData(N8nBaseModel):
    """Execution data, contains detailed information about workflow execution"""
    resultData: Optional[dict[str, Any]] = Field(None, description="Result data from workflow execution, including outputs from nodes")
    executionData: Optional[dict[str, Any]] = Field(None, description="Execution context data, including environment and parameters")
    lastNodeExecuted: Optional[str] = Field(None, description="Name of the last successfully executed node, useful for diagnostics")
    error: Optional[dict[str, Any]] = Field(None, description="Details of errors that occurred during execution, including type and message")
    metadata: Optional[dict[str, Any]] = Field(None, description="Metadata associated with the execution, such as duration and node execution statistics")

class DataItem(N8nBaseModel, RootModel[dict[str, Any]]):
    """Data item in execution data, represents the data object processed by nodes
    
    According to GET /executions and GET /executions/{id}, the data field is an object {}.
    Actual structure depends on the specific workflow implementation and data types being processed.
    """
    pass

class BinaryDataItem(N8nBaseModel):
    """Binary data item, used to store and transfer binary content such as files"""
    # NOTE: Binary data structure is not explicitly defined in API docs, but defined based on typical n8n usage
    fileId: str = Field(..., description="Unique identifier of the file, used to reference stored binary data")
    data: str = Field(..., description="Base64 encoded binary data content, used for direct transfer of small files")
    mimeType: str = Field(..., description="MIME type of the file, such as 'application/pdf', 'image/png', etc.")

class Execution(N8nBaseModel):
    """Workflow execution record, containing complete execution details"""
    id: int | str = Field(..., description="Unique identifier of the execution, can be integer or string")
    data: Optional[DataItem] = Field(None, description="Detailed execution data, only included when querying with includeData=true")
    finished: bool = Field(False, description="Whether execution is completed, completion can be success or failure")
    mode: str = Field("manual", description="Execution mode, possible values include 'manual', 'webhook', 'cli', etc.")
    retryOf: Optional[int | str] = Field(None, description="ID of the original execution being retried") 
    retrySuccessId: Optional[int | str] = Field(None, description="ID of the successful retry execution, if a previous execution was retried and succeeded") 
    startedAt: datetime = Field(..., description="Timestamp when execution started")
    stoppedAt: Optional[datetime] = Field(None, description="Timestamp when execution ended, null if not finished")
    workflowId: str = Field(..., description="Unique identifier of the workflow this execution belongs to")
    waitTill: Optional[datetime] = Field(None, description="Timestamp until which execution is waiting, used for delayed execution")
    customData: Optional[dict[str, Any]] = Field(None, description="Custom data related to the execution, can be used to store user-specific information")

class ExecutionShort(N8nBaseModel):
    """Simplified execution record, used for list display, contains only basic information"""
    id: int | str = Field(..., description="Unique identifier of the execution")
    finished: bool = Field(False, description="Whether execution is completed")
    mode: str = Field("manual", description="Execution mode or trigger method")
    retryOf: Optional[int | str] = Field(None, description="ID of the original execution this execution is retrying")
    retrySuccessId: Optional[int | str] = Field(None, description="ID of the successful retry execution")
    startedAt: datetime = Field(..., description="Execution start time")
    stoppedAt: Optional[datetime] = Field(None, description="Execution end time, null if not finished")
    workflowId: str = Field(..., description="ID of the workflow this execution belongs to")
    waitTill: Optional[datetime] = Field(None, description="Timestamp until which execution is waiting") 
    customData: Optional[dict[str, Any]] = Field(None, description="Custom data")

class ExecutionList(N8nBaseModel):
    """Execution records list response model, used to get multiple execution records"""
    data: list[ExecutionShort] = Field(..., description="List of execution records, can be complete or simplified depending on request parameters")
    nextCursor: Optional[str] = Field(None, description="Pagination cursor, used to get next page of data")
    # count: Optional[int] = Field(None, description="Total count, not mentioned in API docs")

class ExecutionCreate(N8nBaseModel):
    """Trigger workflow execution request model
    
    Note: In the current n8n API documentation (N8N-API.md), there is no clearly defined request body structure for creating executions.
    This model may be used for internal implementation or future API extensions.
    """
    pass  # NOTE: According to API docs, POST /executions doesn't define a request body

class ExecutionStopResult(N8nBaseModel):
    """Stop execution result response model"""
    success: bool = Field(..., description="Whether the operation completed successfully")
    message: Optional[str] = Field(None, description="Detailed description of the operation result or error message")

class ExecutionRetryResult(N8nBaseModel):
    """Retry execution result response model"""
    executionId: str = Field(..., description="Unique identifier of the newly created retry execution")
    success: bool = Field(..., description="Whether the retry operation was successfully submitted") 