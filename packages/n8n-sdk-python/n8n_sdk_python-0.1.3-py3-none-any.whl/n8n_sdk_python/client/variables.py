"""
N8n Variables API client for managing environment variables.

This module provides a client for interacting with the n8n Variables API,
enabling operations such as creating, listing, and deleting environment
variables that can be used in workflows and external integrations.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.variables import Variable, VariablesList, VariableCreate
from ..models.base import N8nBaseModel # For generic 204 response


class VariableClient(BaseClient):
    """
    Client for interacting with the n8n Variables API.
    
    Provides methods for environment variable management, including creating,
    listing, and deleting variables. These variables can be used in workflows
    to parameterize behavior across different environments or to store
    configuration values.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_variable(
        self,
        key: str,
        value: str # Model VariableCreate specifies value as str
    ) -> Variable: # Tools-API.md suggests Variable or operation status. N8N-API.md says 201, implies returning created object.
        """
        Create a new environment variable in the n8n instance.
        
        Variables can be used in workflows with the expression syntax
        and provide a way to parameterize workflows across environments.
        
        Args:
            key: The name/key of the variable
            value: The value of the variable
            
        Returns:
            A Variable object representing the created variable
            
        Raises:
            N8nAPIError: If a variable with the same key already exists or if the request fails
            
        API Docs: https://docs.n8n.io/api/v1/variables/#create-a-variable
        """
        payload = VariableCreate(key=key, value=value).model_dump()
        response_data = await self.post(endpoint="/v1/variables", json=payload)
        # N8N-API.md doesn't show response body for 201, but typically created object is returned.
        # Assuming response_data is the created Variable object based on common REST patterns.
        return Variable(**response_data) 

    async def list_variables(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None
    ) -> VariablesList:
        """
        Retrieve all environment variables from the n8n instance with pagination.
        
        Args:
            limit: Maximum number of variables to return (max 250)
            cursor: Pagination cursor for retrieving additional pages
            
        Returns:
            A VariablesList object containing variable data and pagination info
            
        Raises:
            N8nAPIError: If the API request fails
            
        API Docs: https://docs.n8n.io/api/v1/variables/#retrieve-variables
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        
        response_data = await self.get(endpoint="/v1/variables", params=params)
        return VariablesList(**response_data)

    async def delete_variable(
        self,
        variable_id: str
    ) -> None: # API returns 204 No Content
        """
        Delete an environment variable from the n8n instance.
        
        Deleting a variable that is used in active workflows may cause those
        workflows to fail if they depend on the variable's value.
        
        Args:
            variable_id: The ID of the variable to delete
            
        Returns:
            None: The API returns 204 No Content on success
            
        Raises:
            N8nAPIError: If the variable is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/variables/#delete-a-variable
        """
        await self.delete(endpoint=f"/v1/variables/{variable_id}")
        return None 