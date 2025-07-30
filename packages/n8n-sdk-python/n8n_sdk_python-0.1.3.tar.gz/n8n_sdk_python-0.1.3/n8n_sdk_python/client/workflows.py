"""
N8n Workflow API client for managing automated workflows.

This module provides a client for interacting with the n8n Workflow API,
enabling operations such as creating, listing, retrieving, updating, and
deleting workflows, as well as activating and deactivating workflows,
transferring workflows between projects, and managing workflow tags.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.workflows import (
    Workflow, WorkflowList, WorkflowCreate, WorkflowUpdate, Tag, WorkflowTagUpdateRequestItem,
    Node, Connection, WorkflowSettings, WorkflowStaticData # WorkflowTransferPayload removed from imports
)
from ..models.base import N8nBaseModel # For generic responses
from ..utils.logger import log # Import logger


class WorkflowClient(BaseClient):
    """
    Client for interacting with the n8n Workflow API.
    
    Provides methods for workflow management, including creating, listing,
    retrieving, updating, and deleting workflows, as well as activating
    and deactivating workflows, transferring workflows between projects,
    and managing workflow tags.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_workflow(
        self,
        name: str,
        nodes: list[Node | dict[str, Any]],
        connections: dict[str, dict[str, list[Connection]]] | dict[str, Any], # Placeholder for now, complex conversion needed
        settings: Optional[WorkflowSettings | dict[str, Any]] = None,
        static_data: Optional[WorkflowStaticData | dict[str, int]] = None # Assuming WorkflowStaticData model
    ) -> Workflow:
        """
        Create a new workflow in the n8n instance.
        
        Args:
            name: The name of the workflow
            nodes: List of workflow nodes, either as Node instances or dictionaries
            connections: Dictionary of node connections defining the workflow structure
            settings: Optional workflow settings, either as a WorkflowSettings instance
                     or a dictionary
            static_data: Optional static data for the workflow, either as a 
                        WorkflowStaticData instance or a dictionary
                        
        Returns:
            A Workflow object representing the created workflow
            
        Raises:
            TypeError: If parameters are not of the expected format
            N8nAPIError: If the API request fails
            
        API Docs: https://docs.n8n.io/api/v1/workflows/#create-a-workflow
        """
        _nodes: list[Node] = []
        for node_input in nodes:
            if isinstance(node_input, dict):
                _nodes.append(Node(**node_input))
            elif isinstance(node_input, Node):
                _nodes.append(node_input)
            else:
                raise TypeError(f"Each item in 'nodes' must be a Node instance or a dict, got {type(node_input).__name__}")

        _settings: WorkflowSettings = WorkflowSettings()
        if settings is not None:
            if isinstance(settings, dict):
                _settings = WorkflowSettings(**settings)
            elif isinstance(settings, WorkflowSettings):
                _settings = settings
            else:
                raise TypeError(f"Parameter 'settings' must be a WorkflowSettings instance or a dict, got {type(settings).__name__}")

        _static_data: Optional[WorkflowStaticData] = None
        if static_data is not None:
            if isinstance(static_data, dict):
                _static_data = WorkflowStaticData(**static_data)
            elif isinstance(static_data, WorkflowStaticData):
                _static_data = static_data
            else:
                # Assuming str is not a valid type if model is WorkflowStaticData based on previous analysis
                raise TypeError(f"Parameter 'static_data' must be a WorkflowStaticData instance or a dict, got {type(static_data).__name__}")
        
        # TODO: Deep conversion for connections if it's a dict[str, Any]
        # For now, assuming if connections is dict[str, Any], it matches the structure Pydantic can parse
        # or it's already the correct ConnectionsDict type.
        # A proper conversion would iterate through the structure and convert Connection dicts.
        _connections = connections # Needs more robust handling if type is dict[str, Any]

        payload_model = WorkflowCreate(
            name=name,
            nodes=_nodes,
            connections=_connections, # type: ignore 
            settings=_settings,
            staticData=_static_data
        )
        payload = payload_model.model_dump(exclude_none=True)
        
        log.debug(f"Attempting to create workflow. Payload being sent: {payload}")

        response_data = await self.post(endpoint="/v1/workflows", json=payload)
        return Workflow(**response_data)

    async def list_workflows(
        self,
        active: Optional[bool] = None,
        tags: Optional[str] = None, # Comma-separated string of tag names
        name: Optional[str] = None,
        project_id: Optional[str] = None,
        exclude_pinned_data: Optional[bool] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None
    ) -> WorkflowList:
        """
        Retrieve all workflows from the n8n instance with optional filtering.
        
        Args:
            active: Filter by workflow active status
            tags: Comma-separated string of tag names to filter by
            name: Filter workflows by name
            project_id: Filter workflows by project ID
            exclude_pinned_data: Whether to exclude pinned data from the response
            limit: Maximum number of workflows to return (max 250)
            cursor: Pagination cursor for retrieving additional pages
            
        Returns:
            A WorkflowList object containing workflow data and pagination info
            
        API Docs: https://docs.n8n.io/api/v1/workflows/#retrieve-all-workflows
        """
        params: dict[str, Any] = {}
        if active is not None:
            params["active"] = active
        if tags is not None:
            params["tags"] = tags
        if name is not None:
            params["name"] = name
        if project_id is not None:
            params["projectId"] = project_id
        if exclude_pinned_data is not None:
            params["excludePinnedData"] = exclude_pinned_data
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        
        response_data = await self.get(endpoint="/v1/workflows", params=params)
        return WorkflowList(**response_data)

    async def get_workflow(
        self,
        workflow_id: str,
        exclude_pinned_data: Optional[bool] = None
    ) -> Workflow:
        """
        Retrieve a specific workflow from the n8n instance by ID.
        
        Args:
            workflow_id: The ID of the workflow to retrieve
            exclude_pinned_data: Whether to exclude pinned data from the response
            
        Returns:
            A Workflow object containing detailed workflow information
            
        Raises:
            N8nAPIError: If the workflow is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/workflows/#retrieves-a-workflow
        """
        params: dict[str, Any] = {}
        if exclude_pinned_data is not None:
            params["excludePinnedData"] = exclude_pinned_data
            
        response_data = await self.get(endpoint=f"/v1/workflows/{workflow_id}", params=params)
        return Workflow(**response_data)

    async def delete_workflow(
        self,
        workflow_id: str
    ) -> Workflow: # API doc states it returns the deleted workflow object
        """
        Delete a specific workflow from the n8n instance.
        
        Args:
            workflow_id: The ID of the workflow to delete
            
        Returns:
            A Workflow object representing the deleted workflow
            
        Raises:
            N8nAPIError: If the workflow is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/workflows/#delete-a-workflow
        """
        response_data = await self.delete(endpoint=f"/v1/workflows/{workflow_id}")
        return Workflow(**response_data)

    async def update_workflow(
        self,
        workflow_id: str,
        name: str, 
        nodes: list[Node | dict[str, Any]],
        connections: dict[str, dict[str, list[Connection]]] | dict[str, Any], # Placeholder for now
        settings: Optional[WorkflowSettings | dict[str, Any]] = None,
        static_data: Optional[WorkflowStaticData | dict[str, Any]] = None # Assuming WorkflowStaticData
    ) -> Workflow:
        """
        Update an existing workflow in the n8n instance.
        
        Args:
            workflow_id: The ID of the workflow to update
            name: The updated name of the workflow
            nodes: List of workflow nodes, either as Node instances or dictionaries
            connections: Dictionary of node connections defining the workflow structure
            settings: Optional workflow settings, either as a WorkflowSettings instance
                     or a dictionary
            static_data: Optional static data for the workflow, either as a 
                        WorkflowStaticData instance or a dictionary
                        
        Returns:
            A Workflow object representing the updated workflow
            
        Raises:
            TypeError: If parameters are not of the expected format
            N8nAPIError: If the workflow is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/workflows/#update-a-workflow
        """
        _nodes: list[Node] = []
        if nodes:
            for node_input in nodes:
                if isinstance(node_input, dict):
                    _nodes.append(Node(**node_input))
                elif isinstance(node_input, Node):
                    _nodes.append(node_input)
                else:
                    raise TypeError(f"Each item in 'nodes' must be a Node instance or a dict, got {type(node_input).__name__}")

        _settings: WorkflowSettings = WorkflowSettings()
        if settings is not None:
            if isinstance(settings, dict):
                _settings = WorkflowSettings(**settings)
            elif isinstance(settings, WorkflowSettings):
                _settings = settings
            else:
                raise TypeError(f"Parameter 'settings' must be a WorkflowSettings instance or a dict, got {type(settings).__name__}")

        _static_data: Optional[WorkflowStaticData] = None
        if static_data is not None:
            if isinstance(static_data, dict):
                _static_data = WorkflowStaticData(**static_data)
            elif isinstance(static_data, WorkflowStaticData):
                _static_data = static_data
            else:
                raise TypeError(f"Parameter 'static_data' must be a WorkflowStaticData instance or a dict, got {type(static_data).__name__}")

        # TODO: Deep conversion for connections
        _connections = connections # Needs robust handling

        update_payload_model = WorkflowUpdate(
            name=name, 
            nodes=_nodes, 
            connections=_connections, # type: ignore
            settings=_settings,
            staticData=_static_data
        )
        update_payload = update_payload_model.model_dump(exclude_none=True)
        
        response_data = await self.put(endpoint=f"/v1/workflows/{workflow_id}", json=update_payload)
        return Workflow(**response_data)

    async def activate_workflow(
        self,
        workflow_id: str
    ) -> Workflow:
        """
        Activate a workflow in the n8n instance.
        
        Activating a workflow enables its triggers to start accepting events,
        allowing automated execution when trigger conditions are met.
        
        Args:
            workflow_id: The ID of the workflow to activate
            
        Returns:
            A Workflow object representing the activated workflow
            
        Raises:
            N8nAPIError: If the workflow is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/workflows/#activate-a-workflow
        """
        response_data = await self.post(endpoint=f"/v1/workflows/{workflow_id}/activate")
        return Workflow(**response_data)

    async def deactivate_workflow(
        self,
        workflow_id: str
    ) -> Workflow:
        """
        Deactivate a workflow in the n8n instance.
        
        Deactivating a workflow prevents its triggers from accepting events,
        stopping automated execution until the workflow is activated again.
        
        Args:
            workflow_id: The ID of the workflow to deactivate
            
        Returns:
            A Workflow object representing the deactivated workflow
            
        Raises:
            N8nAPIError: If the workflow is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/workflows/#deactivate-a-workflow
        """
        response_data = await self.post(endpoint=f"/v1/workflows/{workflow_id}/deactivate")
        return Workflow(**response_data)

    async def transfer_workflow_to_project(
        self,
        workflow_id: str,
        destination_project_id: str # Parameter type simplified to str
    ) -> N8nBaseModel: # API returns 200, docs don't specify body. Assuming generic success.
        """
        Transfer a workflow to another project in the n8n instance.
        
        This operation moves a workflow from its current project to a different project,
        maintaining all workflow configurations and connections.
        
        Args:
            workflow_id: The ID of the workflow to transfer
            destination_project_id: The ID of the destination project
            
        Returns:
            A basic response object indicating success
            
        Raises:
            N8nAPIError: If the workflow or project is not found, or if the request fails
            
        API Docs: https://docs.n8n.io/api/v1/workflows/#transfer-a-workflow-to-another-project
        """
        _payload = {"destinationProjectId": destination_project_id} # Direct payload construction
        response_data = await self.put(endpoint=f"/v1/workflows/{workflow_id}/transfer", json=_payload)
        return N8nBaseModel()

    async def get_workflow_tags(
        self,
        workflow_id: str
    ) -> list[Tag]:
        """
        Get the tags associated with a workflow in the n8n instance.
        
        Tags are labels that can be applied to workflows for organization and filtering.
        
        Args:
            workflow_id: The ID of the workflow to get tags for
            
        Returns:
            A list of Tag objects representing the tags associated with the workflow
            
        Raises:
            N8nAPIError: If the workflow is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/workflows/#get-workflow-tags
        """
        response_data = await self.get(endpoint=f"/v1/workflows/{workflow_id}/tags")
        return [Tag(**tag_data) for tag_data in response_data]

    async def update_workflow_tags(
        self,
        workflow_id: str,
        tags: list[WorkflowTagUpdateRequestItem | dict[str, Any]] 
    ) -> list[Tag]:
        """
        Update the tags associated with a workflow in the n8n instance.
        
        This operation replaces all existing tags on the workflow with the provided tags.
        
        Args:
            workflow_id: The ID of the workflow to update tags for
            tags: List of tag objects to associate with the workflow, either as
                 WorkflowTagUpdateRequestItem instances or dictionaries with an 'id' field
                 
        Returns:
            A list of Tag objects representing the updated tags associated with the workflow
            
        Raises:
            TypeError: If tag items are not of the expected format
            N8nAPIError: If the workflow or any tag is not found, or if the request fails
            
        API Docs: https://docs.n8n.io/api/v1/workflows/#update-tags-of-a-workflow
        """
        _tags: list[WorkflowTagUpdateRequestItem] = []
        if tags:
            for tag_input in tags:
                if isinstance(tag_input, dict):
                    _tags.append(WorkflowTagUpdateRequestItem(**tag_input))
                elif isinstance(tag_input, WorkflowTagUpdateRequestItem):
                    _tags.append(tag_input)
                else:
                    raise TypeError(f"Each item in 'tags' must be a WorkflowTagUpdateRequestItem instance or a dict, got {type(tag_input).__name__}")
        
        payload = [tag_item.model_dump() for tag_item in _tags]
        response_data = await self.put(endpoint=f"/v1/workflows/{workflow_id}/tags", json=payload)
        return [Tag(**tag_data) for tag_data in response_data] 