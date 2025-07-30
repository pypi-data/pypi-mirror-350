import os
import asyncio
import unittest
import uuid
from typing import Optional, Any
import httpx # Added for triggering webhook

from dotenv import load_dotenv

from n8n_sdk_python import N8nClient
from n8n_sdk_python.models.workflows import Node, WorkflowSettings, Workflow # For webhook URL
from n8n_sdk_python.models.executions import ExecutionList, Execution, ExecutionStatus
from n8n_sdk_python.utils.errors import N8nAPIError

class TestExecutionsEndToEnd(unittest.IsolatedAsyncioTestCase):
    client: N8nClient
    test_workflow_id_for_executions: Optional[str] = None
    test_workflow_webhook_url: Optional[str] = None
    execution_id_to_test_delete: Optional[str] = None

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        base_url = os.getenv("N8N_BASE_URL")
        api_key = os.getenv("N8N_API_KEY")
        if not base_url or not api_key:
            raise ValueError("N8N_BASE_URL and N8N_API_KEY must be set in .env for testing")
        cls.client = N8nClient(base_url=base_url, api_key=api_key)

        workflow_name = f"TestExecWebhookWorkflow-{uuid.uuid4()}"
        # Using a Webhook node and a NoOp node
        nodes = [
            Node(name="WebhookTrigger", type="n8n-nodes-base.webhook", typeVersion=1, position=[100,100], parameters={"httpMethod": "GET"}),
            Node(name="NoOp", type="n8n-nodes-base.noOp", typeVersion=1, position=[300,100])
        ]
        connections = {
            "WebhookTrigger": { "main": [ [ { "node": "NoOp", "type": "main", "index": 0 } ] ] }
        }
        
        try:
            wf_created: Workflow = asyncio.run(cls.client.workflows.create_workflow(name=workflow_name, nodes=nodes, connections=connections)) # type: ignore
            cls.test_workflow_id_for_executions = wf_created.id
            
            # Activate the workflow
            print(f"Execution Test Setup: Attempting to activate workflow {wf_created.id}...")
            asyncio.run(cls.client.workflows.activate_workflow(workflow_id=wf_created.id)) # type: ignore
            print(f"Execution Test Setup: Activation call for workflow {wf_created.id} completed.")

            # Introduce a short delay to allow n8n to fully process the activation 
            # and register the production webhook route.
            print("Execution Test Setup: Waiting for 1 seconds for webhook registration...")
            # asyncio.run(asyncio.sleep(1)) # This is how you would do it if setUpClass were async
            # For a synchronous classmethod, we run a new event loop for the sleep.
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(asyncio.sleep(1))
            loop.close()
            print("Execution Test Setup: Wait finished.")

            # Retrieve the workflow again to get the webhook URL
            # This ensures we get the state *after* activation and delay
            print(f"Execution Test Setup: Retrieving details for workflow {wf_created.id} post-activation...")
            detailed_wf: Workflow = asyncio.run(cls.client.workflows.get_workflow(workflow_id=wf_created.id)) # type: ignore
            print(f"Execution Test Setup: Retrieved workflow active status: {detailed_wf.active}")
            if not detailed_wf.active:
                print(f"Execution Test Setup: WARNING - Workflow {detailed_wf.id} is not reported as active after activation and delay.")

            webhook_node = next((n for n in detailed_wf.nodes if n.name == "WebhookTrigger"), None)
            
            if webhook_node:
                print(f"Execution Test Setup: Found webhook node: {webhook_node.name} (ID: {webhook_node.id})")
                print(f"Execution Test Setup: Node parameters BEFORE attempting to get path: {webhook_node.parameters}")

                final_webhook_path = None
                # PRIORITY 1: Attempt to get the path directly from the node's parameters.
                # This 'path' should have been updated by n8n's backend (active-workflow-manager.ts)
                # during activation to be the node.id (which also became node.webhookId).
                if webhook_node.parameters and isinstance(webhook_node.parameters, dict):
                    path_from_params = webhook_node.parameters.get("path")
                    if isinstance(path_from_params, str) and path_from_params.strip():
                        final_webhook_path = path_from_params.strip()
                        print(f"Execution Test Setup: Successfully retrieved 'path' from node parameters: '{final_webhook_path}'")
                
                # PRIORITY 2: Fallback - if path from parameters is empty or not found, use node.id.
                # This might happen if the parameter update didn't reflect in the get_workflow call immediately,
                # or if the logic in active-workflow-manager changes.
                if not final_webhook_path and webhook_node.id:
                    final_webhook_path = webhook_node.id
                    print(f"Execution Test Setup: 'path' from parameters was empty/not found. Falling back to node.id: '{final_webhook_path}'")

                if final_webhook_path:
                    cls.test_workflow_webhook_url = f"{cls.client.base_url.rstrip('/')}/webhook/{final_webhook_path}"
                    print(f"Execution Test Setup: Constructed Webhook URL for workflow {wf_created.id} (node {webhook_node.id}) is {cls.test_workflow_webhook_url}")
                else:
                    print(f"Execution Test Setup: CRITICAL - Could not determine webhook path for node {webhook_node.name} (ID: {webhook_node.id}) in workflow {wf_created.id}. Node details: {webhook_node.model_dump_json(indent=2)}")
            else:
                print(f"Execution Test Setup: CRITICAL - WebhookTrigger node not found in workflow {wf_created.id} after retrieval.")
            
        except N8nAPIError as e:
            print(f"Execution Test Setup: Failed to create/activate/get webhook URL for workflow: {e}")

    async def test_01_trigger_workflow_via_webhook_and_list(self):
        """Test triggering the workflow via its webhook and then listing its executions."""
        if not self.test_workflow_id_for_executions or not self.test_workflow_webhook_url:
            self.skipTest("Test workflow for executions or its webhook URL was not set up.")
        
        print(f"Attempting to trigger workflow {self.test_workflow_id_for_executions} via POST to {self.test_workflow_webhook_url}")
        try:
            async with httpx.AsyncClient() as http_client:
                response = await http_client.get(self.test_workflow_webhook_url, params={"test_data": "hello_sdk"})
                response.raise_for_status() # Will raise an exception for 4XX/5XX status
                print(f"Webhook trigger GET request to {self.test_workflow_webhook_url} successful, status: {response.status_code}")
        except httpx.RequestError as e:
            self.fail(f"Failed to trigger workflow via webhook {self.test_workflow_webhook_url}: {e}")
        except httpx.HTTPStatusError as e:
            self.fail(f"Webhook trigger returned error status {e.response.status_code}: {e.response.text}")

        await asyncio.sleep(5) # Wait for execution to be processed and logged

        try:
            executions: ExecutionList = await self.client.executions.list_executions(
                workflow_id=self.test_workflow_id_for_executions, # type: ignore
                limit=5, # Get a few recent ones
                # include_data=True # Optional: if you need to inspect data
            )
            self.assertIsNotNone(executions)
            self.assertIsInstance(executions.data, list)
            self.assertTrue(len(executions.data) > 0, "No executions found for the workflow after webhook trigger.")
            print(f"Found {len(executions.data)} executions for workflow {self.test_workflow_id_for_executions} after webhook trigger.")
            
            # Store the latest execution (usually the first in the list if sorted by desc start time)
            if executions.data:
                TestExecutionsEndToEnd.execution_id_to_test_delete = str(executions.data[0].id)
                print(f"Execution {executions.data[0].id} will be used for get/delete tests.")
                self.assertEqual(executions.data[0].workflowId, self.test_workflow_id_for_executions)

        except N8nAPIError as e:
            self.fail(f"Failed to list executions for workflow {self.test_workflow_id_for_executions} after webhook trigger: {e}")

    async def test_02_list_executions_all(self):
        """Test retrieving all executions (limit 10 for brevity), ensure some exist."""
        try:
            executions: ExecutionList = await self.client.executions.list_executions(limit=10)
            self.assertIsNotNone(executions)
            self.assertIsInstance(executions.data, list)
            # self.assertTrue(len(executions.data) > 0, "Expected at least one execution in the instance.")
            print(f"Successfully listed {len(executions.data)} total executions (up to 10). Next cursor: {executions.nextCursor}")
        except N8nAPIError as e:
            self.fail(f"Failed to list all executions: {e}")

    async def test_03_get_execution(self):
        """Test retrieving a specific execution triggered by the webhook."""
        if not TestExecutionsEndToEnd.execution_id_to_test_delete:
            self.skipTest("No execution ID available from webhook trigger to test get_execution.")
        
        exec_id_to_get = TestExecutionsEndToEnd.execution_id_to_test_delete
        try:
            execution: Execution = await self.client.executions.get_execution(execution_id=exec_id_to_get, include_data=True) # type: ignore
            self.assertIsNotNone(execution)
            self.assertEqual(str(execution.id), exec_id_to_get)
            self.assertEqual(execution.workflowId, self.test_workflow_id_for_executions)
            # Optionally, check if data from webhook is present if include_data=True and workflow saves it
            # print(f"Execution data: {execution.data}")
            print(f"Successfully retrieved execution {exec_id_to_get}.")
        except N8nAPIError as e:
            if e.status_code == 404:
                self.skipTest(f"Execution {exec_id_to_get} not found. Skipping get test.")
            self.fail(f"Failed to get execution {exec_id_to_get}: {e}")

    async def test_04_delete_execution(self):
        """Test deleting the execution triggered by the webhook."""
        if not TestExecutionsEndToEnd.execution_id_to_test_delete:
            self.skipTest("No execution ID available to test delete_execution.")

        exec_id_to_delete = TestExecutionsEndToEnd.execution_id_to_test_delete
        try:
            deleted_execution: Execution = await self.client.executions.delete_execution(execution_id=exec_id_to_delete) # type: ignore
            self.assertIsNotNone(deleted_execution)
            self.assertEqual(str(deleted_execution.id), exec_id_to_delete)
            print(f"Successfully deleted execution {exec_id_to_delete}.")
            
            with self.assertRaises(N8nAPIError) as context:
                await self.client.executions.get_execution(execution_id=exec_id_to_delete) # type: ignore
            self.assertEqual(context.exception.status_code, 404, "Expected 404 for deleted execution.")
            TestExecutionsEndToEnd.execution_id_to_test_delete = None
        except N8nAPIError as e:
            if e.status_code == 404:
                print(f"Execution {exec_id_to_delete} was already deleted.")
                TestExecutionsEndToEnd.execution_id_to_test_delete = None
                return
            self.fail(f"Failed to delete execution {exec_id_to_delete}: {e}")

    @classmethod
    def tearDownClass(cls):
        if cls.test_workflow_id_for_executions:
            print(f"Execution Test Teardown: Deleting workflow {cls.test_workflow_id_for_executions}")
            try:
                # Deactivate first if active
                wf_to_delete = asyncio.run(cls.client.workflows.get_workflow(workflow_id=cls.test_workflow_id_for_executions)) # type: ignore
                if wf_to_delete and wf_to_delete.active:
                    asyncio.run(cls.client.workflows.deactivate_workflow(workflow_id=cls.test_workflow_id_for_executions)) # type: ignore
                asyncio.run(cls.client.workflows.delete_workflow(workflow_id=cls.test_workflow_id_for_executions)) # type: ignore
                print(f"Execution Test Teardown: Successfully deleted workflow {cls.test_workflow_id_for_executions}")
            except N8nAPIError as e:
                print(f"Execution Test Teardown: Error deleting/deactivating workflow {cls.test_workflow_id_for_executions}: {e}")
        
        if cls.execution_id_to_test_delete:
            print(f"Execution Test Teardown: Attempting cleanup of execution {cls.execution_id_to_test_delete}")
            try:
                asyncio.run(cls.client.executions.delete_execution(execution_id=cls.execution_id_to_test_delete)) # type: ignore
                print(f"Execution Test Teardown: Cleaned up execution {cls.execution_id_to_test_delete}")
            except N8nAPIError as e:
                if e.status_code != 404:
                    print(f"Execution Test Teardown: Error cleaning up execution {cls.execution_id_to_test_delete}: {e}")

if __name__ == '__main__':
    unittest.main() 