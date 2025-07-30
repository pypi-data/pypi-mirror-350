"""
N8n Tags API client for managing workflow organization tags.

This module provides a client for interacting with the n8n Tags API,
enabling operations such as creating, listing, retrieving, updating, and
deleting tags used for organizing workflows in an n8n instance.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.workflows import Tag, TagList


class TagClient(BaseClient):
    """
    Client for interacting with the n8n Tags API.
    
    Provides methods for tag management, including creating, listing,
    retrieving, updating, and deleting tags. Tags are used to organize
    and categorize workflows within the n8n instance.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_tag(
        self,
        name: str
    ) -> Tag:
        """
        Create a new tag in the n8n instance.
        
        Tags provide a way to organize and categorize workflows.
        
        Args:
            name: The name for the new tag
            
        Returns:
            A Tag object representing the created tag
            
        Raises:
            N8nAPIError: If a tag with the same name already exists or if the request fails
            
        API Docs: https://docs.n8n.io/api/v1/tags/#create-a-tag
        """
        payload = {"name": name}
        response_data = await self.post(endpoint="/v1/tags", json=payload)
        return Tag(**response_data)

    async def list_tags(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None
    ) -> TagList:
        """
        Retrieve all tags from the n8n instance with pagination.
        
        Args:
            limit: Maximum number of tags to return (max 250)
            cursor: Pagination cursor for retrieving additional pages
            
        Returns:
            A TagList object containing tag data and pagination info
            
        Raises:
            N8nAPIError: If the API request fails
            
        API Docs: https://docs.n8n.io/api/v1/tags/#retrieve-all-tags
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        
        response_data = await self.get(endpoint="/v1/tags", params=params)
        return TagList(**response_data)

    async def get_tag(
        self,
        tag_id: str
    ) -> Tag:
        """
        Retrieve a specific tag from the n8n instance by ID.
        
        Args:
            tag_id: The ID of the tag to retrieve
            
        Returns:
            A Tag object containing the tag details
            
        Raises:
            N8nAPIError: If the tag is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/tags/#retrieves-a-tag
        """
        response_data = await self.get(endpoint=f"/v1/tags/{tag_id}")
        return Tag(**response_data)

    async def delete_tag(
        self,
        tag_id: str
    ) -> Tag: # API doc states it returns the deleted tag object
        """
        Delete a specific tag from the n8n instance.
        
        Deleting a tag will remove it from all workflows that have it applied.
        
        Args:
            tag_id: The ID of the tag to delete
            
        Returns:
            A Tag object representing the deleted tag
            
        Raises:
            N8nAPIError: If the tag is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/tags/#delete-a-tag
        """
        response_data = await self.delete(endpoint=f"/v1/tags/{tag_id}")
        return Tag(**response_data)

    async def update_tag(
        self,
        tag_id: str,
        name: str
    ) -> Tag:
        """
        Update a specific tag in the n8n instance.
        
        Args:
            tag_id: The ID of the tag to update
            name: The new name for the tag
            
        Returns:
            A Tag object representing the updated tag
            
        Raises:
            N8nAPIError: If the tag is not found, a tag with the new name
                         already exists, or if the request fails
            
        API Docs: https://docs.n8n.io/api/v1/tags/#update-a-tag
        """
        payload = {"name": name}
        response_data = await self.put(endpoint=f"/v1/tags/{tag_id}", json=payload)
        return Tag(**response_data) 