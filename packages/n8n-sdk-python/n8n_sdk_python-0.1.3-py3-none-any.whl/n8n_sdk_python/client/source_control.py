"""
N8n Source Control API client for version control operations.

This module provides a client for interacting with the n8n Source Control API,
enabling operations related to version control integration, such as pulling
changes from remote Git repositories into the n8n instance.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.source_control import ScmPullResponse, ScmPullRequest


class SourceControlClient(BaseClient):
    """
    Client for interacting with the n8n Source Control API.
    
    Provides methods for version control operations, such as pulling changes
    from remote Git repositories. This enables synchronization of workflow
    and configuration changes across environments and facilitates collaborative
    development.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def pull_from_source_control(
        self,
        force: Optional[bool] = None,
        variables: Optional[dict[str, Any]] = None
    ) -> ScmPullResponse:
        """
        Pull changes from a remote Git repository into the n8n instance.
        
        This operation synchronizes workflows, credentials, and other resources
        from the connected Git repository into the n8n instance, enabling
        version control and environment synchronization.
        
        Args:
            force: Whether to force the pull operation even if there are conflicts
            variables: Dictionary of variables to set during the pull operation,
                      which can be used to override configuration values
                      
        Returns:
            A ScmPullResponse object containing details about the imported resources
            
        Raises:
            N8nAPIError: If source control is not licensed or configured, if there
                         are conflicts that cannot be resolved, or if the request fails
            
        Note:
        Requires the Source Control feature to be licensed and connected to a repository.
            
        API Docs: https://docs.n8n.io/api/v1/source-control/#pull-changes-from-the-remote-repository
        """
        payload = ScmPullRequest(force=force, variables=variables).model_dump(exclude_none=True)
        
        response_data = await self.post(endpoint="/v1/source-control/pull", json=payload)
        return ScmPullResponse(**response_data) 