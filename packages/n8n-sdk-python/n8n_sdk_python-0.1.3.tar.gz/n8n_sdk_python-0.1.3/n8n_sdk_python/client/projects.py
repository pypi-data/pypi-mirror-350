"""
N8n Projects API client for managing project resources.

This module provides a client for interacting with the n8n Projects API,
enabling operations such as creating, listing, retrieving, updating, and
deleting projects in an n8n instance. Projects are used for organizing
and managing resources such as workflows and credentials.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.projects import Project, ProjectList, ProjectCreate, ProjectUpdate # ProjectUpdate is also needed
from ..models.base import N8nBaseModel # For generic 204 response


class ProjectClient(BaseClient):
    """
    Client for interacting with the n8n Projects API.
    
    Provides methods for project management, including creating, listing,
    updating, and deleting projects within the n8n instance. Projects
    serve as containers for organizing workflows, credentials, and other
    resources.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_project(
        self,
        name: str
    ) -> Project: # Tools-API.md suggests Project or operation status. N8N-API.md says 201, implies returning created object.
        """
        Create a new project in the n8n instance.
        
        Args:
            name: The name for the new project
            
        Returns:
            A Project object representing the created project
            
        Raises:
            N8nAPIError: If the API request fails, such as with duplicate name
            
        API Docs: https://docs.n8n.io/api/v1/projects/#create-a-project
        """
        payload = ProjectCreate(name=name).model_dump()
        response_data = await self.post(endpoint="/v1/projects", json=payload)
        # N8N-API.md doesn't show response body for 201, but typically created object is returned.
        return Project(**response_data)

    async def list_projects(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None
    ) -> ProjectList:
        """
        Retrieve all projects from the n8n instance with pagination.
        
        Args:
            limit: Maximum number of projects to return (max 250)
            cursor: Pagination cursor for retrieving additional pages
            
        Returns:
            A ProjectList object containing project data and pagination info
            
        Raises:
            N8nAPIError: If the API request fails
            
        API Docs: https://docs.n8n.io/api/v1/projects/#retrieve-projects
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        
        response_data = await self.get(endpoint="/v1/projects", params=params)
        return ProjectList(**response_data)

    async def delete_project(
        self,
        project_id: str
    ) -> None: # API returns 204 No Content
        """
        Delete a project from the n8n instance.
        
        Note that this operation may fail if the project contains resources
        such as workflows or credentials. Those resources would need to be
        deleted or transferred first.
        
        Args:
            project_id: The ID of the project to delete
            
        Returns:
            None: The API returns 204 No Content on success
            
        Raises:
            N8nAPIError: If the project is not found, contains resources that
                         prevent deletion, or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/projects/#delete-a-project
        """
        await self.delete(endpoint=f"/v1/projects/{project_id}")
        return None

    async def update_project(
        self,
        project_id: str,
        name: str
    ) -> None: # API returns 204 No Content
        """
        Update a project's properties in the n8n instance.
        
        Currently only supports updating the project name.
        
        Args:
            project_id: The ID of the project to update
            name: The new name for the project
            
        Returns:
            None: The API returns 204 No Content on success
            
        Raises:
            N8nAPIError: If the project is not found, the new name conflicts
                         with an existing project, or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/projects/#update-a-project
        """
        payload = ProjectUpdate(name=name).model_dump()
        await self.put(endpoint=f"/v1/projects/{project_id}", json=payload)
        return None 