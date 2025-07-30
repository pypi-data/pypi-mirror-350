import os
import asyncio
import unittest
import uuid
from typing import Optional

from dotenv import load_dotenv

from n8n_sdk_python import N8nClient
from n8n_sdk_python.models.workflows import Node, WorkflowSettings
# Connection model is not directly used for assertion from list_connections, but good for reference
# from n8n_sdk_python.models.workflows import Connection
from n8n_sdk_python.utils.errors import N8nAPIError

class TestConnectionsEndToEnd(unittest.IsolatedAsyncioTestCase):
    client: N8nClient
    workflow_id_for_connection_tests: Optional[str] = None
    # Node names to be used in tests
    node1_name = "StartNodeConn"
    node2_name = "MiddleNodeConn"
    node3_name = "EndNodeConn"

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        base_url = os.getenv("N8N_BASE_URL")
        api_key = os.getenv("N8N_API_KEY")
        if not base_url or not api_key:
            raise ValueError("N8N_BASE_URL and N8N_API_KEY must be set in .env for testing")
        cls.client = N8nClient(base_url=base_url, api_key=api_key)

        test_workflow_name = f"Test Connections Workflow - {uuid.uuid4()}"
        nodes_data = [
            Node(name=cls.node1_name, type="n8n-nodes-base.start", typeVersion="1", position=[100, 100]),
            Node(name=cls.node2_name, type="n8n-nodes-base.noOp", typeVersion="1", position=[300, 100]),
            Node(name=cls.node3_name, type="n8n-nodes-base.noOp", typeVersion="1", position=[500, 100])
        ]
        connections_data = {
            cls.node1_name: { "main": [ [ { "node": cls.node2_name, "type": "main", "index": 0 } ] ] }
        }
        settings_data = WorkflowSettings(timezone="UTC")

        try:
            workflow = asyncio.run(cls.client.workflows.create_workflow(
                name=test_workflow_name,
                nodes=nodes_data, # type: ignore
                connections=connections_data, # type: ignore
                settings=settings_data
            ))
            cls.workflow_id_for_connection_tests = workflow.id
            print(f"Connection Test Setup: Created workflow {workflow.id} for connection tests.")
        except N8nAPIError as e:
            print(f"Connection Test Setup: Failed to create workflow for connection tests: {e}")
            raise RuntimeError(f"Failed to create workflow in setUpClass for connection tests: {e}")

    async def test_01_list_initial_connections(self):
        """Test listing initial connections of the test workflow."""
        self.assertIsNotNone(self.workflow_id_for_connection_tests, "Workflow ID for connections test not set.")
        workflow_id = self.workflow_id_for_connection_tests
        try:
            connections_map = await self.client.connections.list_connections(workflow_id=workflow_id) # type: ignore
            self.assertIsNotNone(connections_map)
            self.assertIn(self.node1_name, connections_map)
            self.assertIn("main", connections_map[self.node1_name])
            self.assertTrue(len(connections_map[self.node1_name]["main"]) > 0)
            self.assertTrue(len(connections_map[self.node1_name]["main"][0]) > 0)
            initial_conn_details = connections_map[self.node1_name]["main"][0][0]
            
            self.assertEqual(initial_conn_details.get("node"), self.node2_name)
            self.assertEqual(initial_conn_details.get("type"), "main")
            self.assertEqual(initial_conn_details.get("index"), 0)
            print(f"Initial connections for workflow {workflow_id}: {connections_map}")
        except N8nAPIError as e:
            self.fail(f"Failed to list initial connections: {e}")

    async def test_02_create_new_connection(self):
        """Test creating a new connection between node2 and node3."""
        self.assertIsNotNone(self.workflow_id_for_connection_tests, "Workflow ID for connections test not set.")
        workflow_id = self.workflow_id_for_connection_tests
        try:
            success = await self.client.connections.create_connection(
                workflow_id=workflow_id, # type: ignore
                source_node=self.node2_name,
                target_node=self.node3_name,
                source_type="main",
                target_type="main",
                source_index=0,
                target_index=0
            )
            self.assertTrue(success, "Failed to create connection report from SDK.")
            print(f"Successfully created connection from {self.node2_name} to {self.node3_name} in workflow {workflow_id}.")

            connections_map = await self.client.connections.list_connections(workflow_id=workflow_id) # type: ignore
            self.assertIn(self.node2_name, connections_map)
            self.assertIn("main", connections_map[self.node2_name])
            self.assertTrue(len(connections_map[self.node2_name]["main"]) > 0, f"{self.node2_name} main output list is empty.")
            self.assertTrue(len(connections_map[self.node2_name]["main"][0]) > 0, f"{self.node2_name} main output first target list is empty.")
            new_conn_details = connections_map[self.node2_name]["main"][0][0]
            self.assertEqual(new_conn_details.get("node"), self.node3_name)
        except N8nAPIError as e:
            self.fail(f"Failed to create or verify new connection: {e}")

    async def test_03_delete_connection(self):
        """Test deleting the connection between node2 and node3."""
        self.assertIsNotNone(self.workflow_id_for_connection_tests, "Workflow ID for connections test not set.")
        workflow_id = self.workflow_id_for_connection_tests
        try:
            success = await self.client.connections.delete_connection(
                workflow_id=workflow_id, # type: ignore
                source_node=self.node2_name,
                target_node=self.node3_name,
                source_type="main",
                target_type="main", # This was target_type in create, should be same for delete
                source_index=0,
                target_index=0     # This was target_index in create
            )
            self.assertTrue(success, "Failed to delete connection report from SDK.")
            print(f"Successfully deleted connection from {self.node2_name} to {self.node3_name} in workflow {workflow_id}.")

            connections_map = await self.client.connections.list_connections(workflow_id=workflow_id) # type: ignore
            node2_connections = connections_map.get(self.node2_name, {}).get("main", [])
            
            found_deleted_connection = False
            if node2_connections and node2_connections[0]: # Check if the list and sublist exist
                for conn_details in node2_connections[0]:
                    if conn_details.get("node") == self.node3_name:
                        found_deleted_connection = True
                        break
            self.assertFalse(found_deleted_connection, f"Connection from {self.node2_name} to {self.node3_name} was not deleted.")
        except N8nAPIError as e:
            self.fail(f"Failed to delete or verify connection deletion: {e}")

    @classmethod
    def tearDownClass(cls):
        if cls.workflow_id_for_connection_tests:
            print(f"Connection Test Teardown: Deleting workflow {cls.workflow_id_for_connection_tests}")
            try:
                asyncio.run(cls.client.workflows.delete_workflow(workflow_id=cls.workflow_id_for_connection_tests)) # type: ignore
                print(f"Connection Test Teardown: Successfully deleted workflow {cls.workflow_id_for_connection_tests}")
            except N8nAPIError as e:
                print(f"Connection Test Teardown: Error deleting workflow {cls.workflow_id_for_connection_tests}: {e}")

if __name__ == '__main__':
    unittest.main() 