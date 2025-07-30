"""
N8n Execution API client for managing workflow executions.

This module provides a client for interacting with the n8n Execution API,
enabling operations such as retrieving, listing, and deleting workflow
executions in an n8n instance.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.executions import (
    ExecutionList, Execution, ExecutionStatus
)


class ExecutionClient(BaseClient):
    """
    Client for interacting with the n8n Execution API.
    
    Provides methods for managing workflow executions, including listing
    all executions with various filters, retrieving specific execution
    details, and deleting executions from the n8n instance.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def list_executions(
        self,
        include_data: Optional[bool] = None,
        status: Optional[ExecutionStatus] = None, # Use ExecutionStatus enum from models
        workflow_id: Optional[str] = None,
        project_id: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None
    ) -> ExecutionList:
        """
        Retrieve all workflow executions from the n8n instance with optional filtering.
        
        Args:
            include_data: Whether to include detailed execution data in the response
            status: Filter executions by status (error, success, waiting)
            workflow_id: Filter executions by workflow ID
            project_id: Filter executions by project ID
            limit: Maximum number of executions to return (max 250)
            cursor: Pagination cursor for retrieving additional pages
            
        Returns:
            An ExecutionList object containing execution data and pagination info
            
        Raises:
            N8nAPIError: If the API request fails
            
        API Docs: https://docs.n8n.io/api/v1/executions/#retrieve-all-executions
        """
        params: dict[str, Any] = {}
        if include_data is not None:
            params["includeData"] = include_data
        if status is not None:
            params["status"] = status.value # Get the string value from enum
        if workflow_id is not None:
            params["workflowId"] = workflow_id
        if project_id is not None:
            params["projectId"] = project_id
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        
        response_data = await self.get(endpoint="/v1/executions", params=params)
        return ExecutionList(**response_data)

    async def get_execution(
        self,
        execution_id: int | str, # Changed Union to |
        include_data: Optional[bool] = None
    ) -> Execution:
        """
        Retrieve details of a specific workflow execution from the n8n instance.
        
        Args:
            execution_id: The ID of the execution to retrieve
            include_data: Whether to include detailed execution data in the response
            
        Returns:
            An Execution object containing detailed execution information
            
        Raises:
            N8nAPIError: If the execution is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/executions/#retrieve-an-execution
        """
        params: dict[str, Any] = {}
        if include_data is not None:
            params["includeData"] = include_data
            
        response_data = await self.get(endpoint=f"/v1/executions/{execution_id}", params=params)
        return Execution(**response_data)

    async def delete_execution(
        self,
        execution_id: int | str 
    ) -> Execution: # API doc states it returns the deleted execution object
        """
        Delete a specific workflow execution from the n8n instance.
        
        Args:
            execution_id: The ID of the execution to delete
            
        Returns:
            An Execution object representing the deleted execution
            
        Raises:
            N8nAPIError: If the execution is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/executions/#delete-an-execution
        """
        response_data = await self.delete(endpoint=f"/v1/executions/{execution_id}")
        return Execution(**response_data) 