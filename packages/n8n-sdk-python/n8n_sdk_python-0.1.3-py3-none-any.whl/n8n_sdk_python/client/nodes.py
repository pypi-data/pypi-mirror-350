"""
N8n Nodes API client for accessing node types and operations.

This module provides a client for interacting with the n8n Nodes API,
enabling operations such as retrieving available node types, getting
detailed node type information, and fetching parameter and connection options.
These operations help with building and configuring workflow nodes programmatically.
"""

from typing import Any, Optional

from pydantic import ValidationError

from ..client.base import BaseClient
from ..utils.logger import log
from ..models.nodes import (
    NodeType,
    NodeTypeDescription,
    NodeParameterOptions,
    NodeConnectionOptions
)


class NodesClient(BaseClient):
    """
    Client for interacting with the n8n Nodes API.
    
    Provides methods for retrieving node type information, parameter options,
    and connection options, which can be used to programmatically discover
    and configure workflow nodes.
    
    Note:
        This client interacts with unofficial/internal n8n APIs that may
        change between versions.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def get_node_types(self) -> list[NodeType]:
        """
        Retrieve all available node types from the n8n instance.
        
        Returns:
            A list of NodeType objects containing basic node type information
            
        Note:
            This method catches exceptions and returns an empty list on error
        """
        try:
            response = await self.get("/node-types")
            
            node_types = []
            for item in response.get("data", []):
                try:
                    node_types.append(NodeType(**item))
                except ValidationError:
                    pass  # Ignore invalid node type data
            
            return node_types
        except Exception as e:
            log.error(f"Failed to retrieve node types list: {str(e)}")
            return []
    
    async def get_node_type(self, type_name: str) -> Optional[NodeTypeDescription]:
        """
        Retrieve detailed information about a specific node type.
        
        Args:
            type_name: Node type name, e.g., 'n8n-nodes-base.httpRequest'
            
        Returns:
            A NodeTypeDescription object containing detailed node type information,
            or None if the node type is not found or an error occurs
            
        Note:
            This method catches exceptions and returns None on error
        """
        try:
            response = await self.get(f"/node-types/{type_name}")
            
            if not response or "data" not in response:
                return None
                
            return NodeTypeDescription(**response["data"])
        except Exception as e:
            log.error(f"Failed to retrieve node type {type_name}: {str(e)}")
            return None
    
    async def get_parameter_options(
        self, 
        type_name: str,
        method_name: str,
        path: str,
        payload: Optional[dict[str, Any]] = None
    ) -> Optional[NodeParameterOptions]:
        """
        Retrieve available options for a node parameter.
        
        This is useful for dynamically populating dropdown options based on
        previously selected parameters in a node.
        
        Args:
            type_name: Node type name
            method_name: Request method name
            path: Parameter path (e.g., 'parameters.resource')
            payload: Additional request data
            
        Returns:
            A NodeParameterOptions object containing available options,
            or None if options cannot be retrieved or an error occurs
            
        Note:
            This method catches exceptions and returns None on error
        """
        try:
            request_data = {
                "nodeTypeAndVersion": type_name,
                "methodName": method_name,
                "path": path,
                **(payload or {})
            }
            
            response = await self.post(
                "/node-parameter-options", 
                json=request_data
            )
            
            if not response or "data" not in response:
                return None
                
            return NodeParameterOptions(**response["data"])
        except Exception as e:
            log.error(f"Failed to retrieve parameter options for node {type_name}: {str(e)}")
            return None
    
    async def get_connection_options(
        self, 
        node_type: str,
        connections_options: dict[str, Any],
        node_filter: Optional[dict[str, Any]] = None
    ) -> Optional[NodeConnectionOptions]:
        """
        Retrieve available connection options for a node.
        
        This is useful for determining which nodes can be connected
        to a specific node based on input/output compatibility.
        
        Args:
            node_type: Node type name
            connections_options: Connection options configuration
            node_filter: Optional node filtering conditions
            
        Returns:
            A NodeConnectionOptions object containing available connection options,
            or None if options cannot be retrieved or an error occurs
            
        Note:
            This method catches exceptions and returns None on error
        """
        try:
            request_data = {
                "nodeType": node_type,
                "connectionsOptions": connections_options,
                **({"nodeFilter": node_filter} if node_filter else {})
            }
            
            response = await self.post(
                "/node-connection-options", 
                json=request_data
            )
            
            if not response or "data" not in response:
                return None
                
            return NodeConnectionOptions(**response["data"])
        except Exception as e:
            log.error(f"Failed to retrieve node connection options: {str(e)}")
            return None 