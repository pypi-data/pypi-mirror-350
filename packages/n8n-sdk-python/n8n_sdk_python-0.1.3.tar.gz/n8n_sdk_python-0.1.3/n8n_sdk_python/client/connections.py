"""
n8n 節點連接 API 客戶端。
處理節點之間連接的相關操作。
"""

from typing import Any, Optional

# Add import for BaseClient
from ..client.base import BaseClient
from ..utils.logger import log
from ..models.workflows import Workflow, Connection # Connection model is used in methods


class ConnectionsClient(BaseClient):
    """
    Client for managing connections between nodes in workflows.

    Provides methods for managing connections between nodes in workflows,
    including listing, creating, and deleting connections.
    """
    
    # Modify __init__ method
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the connections client.
        
        Args:
            base_url: Base URL for the n8n API, defaults to environment variable or localhost
            api_key: Authentication key for n8n API, defaults to environment variable
        """
        super().__init__(base_url=base_url, api_key=api_key)
        self._workflows_client_instance = None # Renamed to avoid conflict with property
    
    @property
    def workflows_client(self):
        """
        Lazy load WorkflowsClient instance to avoid circular references.
        Pass base_url and api_key from self (ConnectionsClient instance) to WorkflowsClient.

        Returns:
            WorkflowsClient instance
        """
        if self._workflows_client_instance is None:
            from .workflows import WorkflowClient # Corrected import name
            # Pass base_url and api_key from self (ConnectionsClient instance)
            self._workflows_client_instance = WorkflowClient(base_url=self.base_url, api_key=self.api_key)
        return self._workflows_client_instance
    
    async def list_connections(self, workflow_id: str, source_node: Optional[str] = None) -> dict[str, dict[str, list[list[Connection]]]]:
        """
        List connections in a workflow.
        
        Args:
            workflow_id: Workflow ID
            source_node: Optional source node name, used to filter connections
            
        Returns:
            Dictionary containing connection information, format: {node_name: {type: [[connections]]}}
        """
        workflow = await self.workflows_client.get_workflow(workflow_id)
        if not workflow:
            return {}
        
        connections = workflow.connections or {}
        
        # 如果指定了來源節點，只返回該節點的連接
        if source_node:
            if source_node in connections:
                return {source_node: connections[source_node]}
            return {}
        
        return connections
    
    async def create_connection(
        self,
        workflow_id: str,
        source_node: str,
        target_node: str,
        source_type: str = "main",
        target_type: str = "main",
        source_index: int = 0,
        target_index: int = 0
    ) -> bool:
        """
        Create a connection between two nodes in a workflow.
        
        Args:
            workflow_id: Workflow ID
            source_node: Source node name
            target_node: Target node name
            source_type: Source output type, usually 'main'
            target_type: Target input type, usually 'main'
            source_index: Source output index
            target_index: Target input index
            
        Returns:
            True if the connection was created successfully, False otherwise
        """
        # 獲取當前工作流程
        workflow = await self.workflows_client.get_workflow(workflow_id)
        if not workflow:
            return False
        
        # 確保工作流程物件有 connections 屬性
        workflow_data = workflow.model_dump()
        connections = workflow_data.get("connections", {})
        
        # 初始化連接結構
        if source_node not in connections:
            connections[source_node] = {}
        
        if source_type not in connections[source_node]:
            connections[source_node][source_type] = []
        
        # 確保有足夠的輸出索引
        while len(connections[source_node][source_type]) <= source_index:
            connections[source_node][source_type].append([])
        
        # 建立新連接
        new_connection = {
            "node": target_node,
            "type": target_type,
            "index": target_index
        }
        
        # 檢查連接是否已存在
        for existing_connection in connections[source_node][source_type][source_index]:
            if (existing_connection.get("node") == target_node and
                existing_connection.get("type") == target_type and
                existing_connection.get("index") == target_index):
                return True  # 連接已存在，視為成功
        
        # 添加新連接
        connections[source_node][source_type][source_index].append(new_connection)
        
        # 更新工作流程
        workflow_data["connections"] = connections
        result = await self.workflows_client.update_workflow(workflow_id, workflow_data)
        
        return result is not None
    
    async def delete_connection(
        self,
        workflow_id: str,
        source_node: str,
        target_node: str,
        source_type: str = "main",
        target_type: str = "main",
        source_index: Optional[int] = None,
        target_index: Optional[int] = None
    ) -> bool:
        """
        Delete a connection between two nodes in a workflow.
        
        Args:
            workflow_id: Workflow ID
            source_node: Source node name
            target_node: Target node name
            source_type: Source output type, usually 'main'
            target_type: Target input type, usually 'main'
            source_index: Source output index, if None, delete all matching connections
            target_index: Target input index, if None, delete all matching connections
            
        Returns:
            True if the connection was deleted successfully, False otherwise
        """
        # Get the current workflow
        workflow = await self.workflows_client.get_workflow(workflow_id)
        if not workflow:
            return False
        
        workflow_data = workflow.model_dump()
        connections = workflow_data.get("connections", {})
        
        # 檢查來源節點是否存在
        if source_node not in connections:
            return False
        
        # 檢查連接類型是否存在
        if source_type not in connections[source_node]:
            return False
        
        modified = False
        
        # 如果指定了來源索引，只處理該索引
        if source_index is not None:
            if source_index >= len(connections[source_node][source_type]):
                return False
            
            original_connections = connections[source_node][source_type][source_index]
            filtered_connections = []
            
            for conn in original_connections:
                if (conn.get("node") == target_node and
                    conn.get("type") == target_type and
                    (target_index is None or conn.get("index") == target_index)):
                    modified = True
                else:
                    filtered_connections.append(conn)
            
            connections[source_node][source_type][source_index] = filtered_connections
        else:
            # 處理所有來源索引
            for idx, conn_list in enumerate(connections[source_node][source_type]):
                filtered_list = [
                    conn for conn in conn_list
                    if not (conn.get("node") == target_node and
                          conn.get("type") == target_type and
                          (target_index is None or conn.get("index") == target_index))
                ]
                
                if len(filtered_list) != len(conn_list):
                    modified = True
                    connections[source_node][source_type][idx] = filtered_list
        
        if not modified:
            return False
        
        # 清理空的連接列表
        connections[source_node][source_type] = [
            conn_list for conn_list in connections[source_node][source_type] if conn_list
        ]
        
        # 清理空的連接類型
        if not connections[source_node][source_type]:
            del connections[source_node][source_type]
        
        # 清理空的來源節點
        if not connections[source_node]:
            del connections[source_node]
        
        # 更新工作流程
        workflow_data["connections"] = connections
        result = await self.workflows_client.update_workflow(workflow_id, workflow_data)
        
        return result is not None 