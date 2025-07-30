import os
import asyncio
import unittest
from typing import Optional

from dotenv import load_dotenv

from n8n_sdk_python import N8nClient
from n8n_sdk_python.models.workflows import Workflow, WorkflowSettings, Node, Tag, WorkflowTagUpdateRequestItem
from n8n_sdk_python.utils.errors import N8nAPIError

class TestWorkflowEndToEnd(unittest.IsolatedAsyncioTestCase):
    """
    End-to-end tests for n8n Workflow client methods.
    Tests are prefixed with numbers to ensure execution order.
    """
    client: N8nClient
    created_workflow_id: Optional[str] = None
    created_tag_id: Optional[str] = None # Assuming a way to create/get a tag for testing

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        base_url = os.getenv("N8N_BASE_URL")
        api_key = os.getenv("N8N_API_KEY")
        if not base_url or not api_key:
            raise ValueError("N8N_BASE_URL and N8N_API_KEY must be set in .env for testing")
        cls.client = N8nClient(base_url=base_url, api_key=api_key)
        # Note: For tag testing, we might need a predefined tag or create one if TagClient exists
        # For now, we'll assume a tag might be created manually or this part of test is skipped if no tag id.

    async def test_01_create_workflow(self):
        """Test creating a new workflow."""
        test_workflow_name = "Test SDK Workflow Create"
        nodes = [
            Node(name="Start", type="n8n-nodes-base.scheduleTrigger", typeVersion=1.2, position=[250, 300]),
            Node(name="NoOp", type="n8n-nodes-base.noOp", typeVersion=1, position=[450, 300])
        ]
        connections = {
            "Start": { "main": [ [ { "node": "NoOp", "type": "main", "index": 0 } ] ] }
        }
        settings = WorkflowSettings(timezone="Europe/Berlin") # Example setting

        try:
            workflow = await self.client.workflows.create_workflow(
                name=test_workflow_name,
                nodes=nodes, # type: ignore
                connections=connections, # type: ignore
                settings=settings
            )
            self.assertIsNotNone(workflow)
            self.assertEqual(workflow.name, test_workflow_name)
            self.assertTrue(len(workflow.nodes) == 2)
            TestWorkflowEndToEnd.created_workflow_id = workflow.id
            print(f"Workflow created with ID: {workflow.id}")
        except N8nAPIError as e:
            self.fail(f"Failed to create workflow: {e}")

    async def test_02_get_workflow(self):
        """Test retrieving the created workflow."""
        self.assertIsNotNone(TestWorkflowEndToEnd.created_workflow_id, "Workflow ID not set from create test")
        workflow_id = TestWorkflowEndToEnd.created_workflow_id
        try:
            workflow = await self.client.workflows.get_workflow(workflow_id=workflow_id) # type: ignore
            self.assertIsNotNone(workflow)
            self.assertEqual(workflow.id, workflow_id)
        except N8nAPIError as e:
            self.fail(f"Failed to get workflow {workflow_id}: {e}")

    async def test_03_update_workflow(self):
        """Test updating the created workflow."""
        self.assertIsNotNone(TestWorkflowEndToEnd.created_workflow_id, "Workflow ID not set")
        workflow_id = TestWorkflowEndToEnd.created_workflow_id
        updated_name = "Test SDK Workflow Updated"
        nodes = [
            Node(name="Start", type="n8n-nodes-base.scheduleTrigger", typeVersion=1.2, position=[250, 300]),
            Node(name="Set", type="n8n-nodes-base.set", typeVersion=1, position=[450, 300], parameters={"values":{"string":[{"name":"newName","value":"newValue"}]}})
        ]
        connections = {
             "Start": { "main": [ [ { "node": "Set", "type": "main", "index": 0 } ] ] }
        }
        try:
            workflow = await self.client.workflows.update_workflow(
                workflow_id=workflow_id, # type: ignore
                name=updated_name,
                nodes=nodes, # type: ignore
                connections=connections # type: ignore
            )
            self.assertIsNotNone(workflow)
            self.assertEqual(workflow.name, updated_name)
            self.assertEqual(workflow.nodes[1].name, "Set") # type: ignore
        except N8nAPIError as e:
            self.fail(f"Failed to update workflow {workflow_id}: {e}")

    async def test_04_activate_workflow(self):
        """Test activating the workflow."""
        self.assertIsNotNone(TestWorkflowEndToEnd.created_workflow_id, "Workflow ID not set")
        workflow_id = TestWorkflowEndToEnd.created_workflow_id
        try:
            workflow = await self.client.workflows.activate_workflow(workflow_id=workflow_id) # type: ignore
            self.assertIsNotNone(workflow)
            self.assertTrue(workflow.active)
        except N8nAPIError as e:
            self.fail(f"Failed to activate workflow {workflow_id}: {e}")

    async def test_05_deactivate_workflow(self):
        """Test deactivating the workflow."""
        self.assertIsNotNone(TestWorkflowEndToEnd.created_workflow_id, "Workflow ID not set")
        workflow_id = TestWorkflowEndToEnd.created_workflow_id
        try:
            workflow = await self.client.workflows.deactivate_workflow(workflow_id=workflow_id) # type: ignore
            self.assertIsNotNone(workflow)
            self.assertFalse(workflow.active)
        except N8nAPIError as e:
            self.fail(f"Failed to deactivate workflow {workflow_id}: {e}")

    # For tag tests, we'd ideally have a tag to work with.
    # This might require creating a tag or having a known tag ID.
    # Let's assume we have a way to get a tag ID, or we create one if Tag client is available.
    # For now, these tests might be illustrative.

    async def test_06_update_workflow_tags(self):
        """Test updating workflow tags. This test assumes a tag exists or can be created."""
        self.assertIsNotNone(TestWorkflowEndToEnd.created_workflow_id, "Workflow ID not set")
        workflow_id = TestWorkflowEndToEnd.created_workflow_id
        
        # Placeholder: In a real scenario, you'd get or create a tag first.
        # For this example, let's assume a tag with ID "test-tag-id-123" exists.
        # Or, if you have a TagClient, you'd create one and store its ID.
        # For now, we'll try with a made-up one, which will likely fail if tag doesn't exist or API behavior.
        # This part needs a robust way to manage test tags.
        
        # We should first try to get existing tags for this workflow to avoid errors if no tag client is used.
        try:
            initial_tags = await self.client.workflows.get_workflow_tags(workflow_id=workflow_id) # type: ignore
            print(f"Initial tags for workflow {workflow_id}: {initial_tags}")
        except N8nAPIError as e:
            # If getting tags fails (e.g. workflow has no tags yet, or API issue)
            print(f"Could not get initial tags for workflow {workflow_id}: {e}. Proceeding with update attempt.")


        # Attempt to add a tag. If your n8n instance doesn't have a tag with this ID,
        # or if the API requires existing tags for update, this might behave differently.
        # The API for updating tags usually expects a list of tag IDs.
        # If the tag ID doesn't exist, n8n might ignore it or error.
        # Let's assume a tag "test-tag-for-sdk" is available
        # For a robust test, one should create this tag first.
        # Since there is no client.tags.create_tag, we assume one exists or this test might be limited
        
        # Let's try to add a dummy tag. The API might require the tag to exist.
        # The `update_workflow_tags` endpoint usually *sets* the tags, not appends.
        # So, if you send an empty list, it clears tags.
        # If you send a list of tag IDs, it sets those as the workflow's tags.
        
        # This test is simplified. A full test would:
        # 1. Create a tag using a (hypothetical) TagClient.
        # 2. Store its ID in TestWorkflowEndToEnd.created_tag_id.
        # 3. Use that ID here.
        # 4. Clean up the tag in tearDownClass.
        
        # For now, let's assume a tag with a known name we want to assign.
        # The API expects tag IDs. If you don't have a tag client to create/get tags,
        # this test is hard to make fully robust without prior manual setup in n8n.
        # Let's try to assign a non-existent tag ID and see how the API responds,
        # or if the API allows creating tags on the fly via this endpoint (unlikely).
        # A more realistic approach is to have a predefined tag in your test n8n instance.
        
        # As a placeholder, we will attempt to set an empty list of tags, effectively clearing them.
        # Then, if a tag client were available, we'd create a tag and then assign it.
        # Without a tag client, a truly robust test for adding tags is difficult.
        
        print("Attempting to clear tags (setting to empty list).")
        try:
            updated_tags_cleared = await self.client.workflows.update_workflow_tags(
                workflow_id=workflow_id, # type: ignore
                tags=[] # Clear all tags
            )
            self.assertIsInstance(updated_tags_cleared, list)
            self.assertEqual(len(updated_tags_cleared), 0)
            print(f"Tags cleared for workflow {workflow_id}.")
        except N8nAPIError as e:
            self.fail(f"Failed to clear tags for workflow {workflow_id}: {e}")

        # If we had a created_tag_id:
        # if TestWorkflowEndToEnd.created_tag_id:
        #     print(f"Attempting to set tag ID: {TestWorkflowEndToEnd.created_tag_id}")
        #     try:
        #         updated_tags_set = await self.client.workflows.update_workflow_tags(
        #             workflow_id=workflow_id,
        #             tags=[WorkflowTagUpdateRequestItem(id=TestWorkflowEndToEnd.created_tag_id)]
        #         )
        #         self.assertTrue(any(tag.id == TestWorkflowEndToEnd.created_tag_id for tag in updated_tags_set))
        #         print(f"Tag {TestWorkflowEndToEnd.created_tag_id} set for workflow {workflow_id}.")
        #     except N8nAPIError as e:
        #         self.fail(f"Failed to set tag {TestWorkflowEndToEnd.created_tag_id} for workflow {workflow_id}: {e}")
        # else:
        #     print("Skipping setting specific tag as no created_tag_id is available.")


    async def test_07_get_workflow_tags(self):
        """Test retrieving workflow tags after update."""
        self.assertIsNotNone(TestWorkflowEndToEnd.created_workflow_id, "Workflow ID not set")
        workflow_id = TestWorkflowEndToEnd.created_workflow_id
        try:
            tags = await self.client.workflows.get_workflow_tags(workflow_id=workflow_id) # type: ignore
            self.assertIsInstance(tags, list)
            # After clearing, we expect 0 tags. If a specific tag was set, check for it.
            self.assertEqual(len(tags), 0, "Expected tags to be cleared.")
            print(f"Retrieved tags for workflow {workflow_id}: {tags}")
        except N8nAPIError as e:
            self.fail(f"Failed to get tags for workflow {workflow_id}: {e}")
            
    # Transfer workflow test requires another project ID. This is complex for an automated E2E test
    # without more setup (e.g., ensuring another project exists and getting its ID).
    # async def test_transfer_workflow(self):
    #     """Test transferring the workflow to another project."""
    #     pass

    async def test_99_delete_workflow(self):
        """Test deleting the created workflow."""
        self.assertIsNotNone(TestWorkflowEndToEnd.created_workflow_id, "Workflow ID not set for deletion")
        workflow_id = TestWorkflowEndToEnd.created_workflow_id
        try:
            response = await self.client.workflows.delete_workflow(workflow_id=workflow_id) # type: ignore
            self.assertIsNotNone(response) # Delete often returns the deleted object or a success indicator
            print(f"Workflow {workflow_id} deleted successfully.")
            TestWorkflowEndToEnd.created_workflow_id = None # Clear ID after deletion
        except N8nAPIError as e:
            # If API returns 404 because it's already deleted somehow, we might consider it a pass for cleanup
            if e.status_code == 404:
                print(f"Workflow {workflow_id} was already deleted or not found during cleanup: {e}")
                TestWorkflowEndToEnd.created_workflow_id = None 
            else:
                self.fail(f"Failed to delete workflow {workflow_id}: {e}")

    @classmethod
    def tearDownClass(cls):
        """Clean up any resources after all tests are run."""
        if cls.created_workflow_id:
            print(f"Workflow {cls.created_workflow_id} might not have been deleted by tests. Attempting cleanup.")
            try:
                asyncio.run(cls.client.workflows.delete_workflow(workflow_id=cls.created_workflow_id)) # type: ignore
                print(f"Cleaned up workflow {cls.created_workflow_id} in tearDownClass.")
            except N8nAPIError as e:
                print(f"Error during tearDownClass cleanup of workflow {cls.created_workflow_id}: {e}")
        # If a tag was created and its ID stored in cls.created_tag_id, clean it up here too.
        # if cls.created_tag_id:
        #     try:
        #         asyncio.run(cls.client.tags.delete_tag(tag_id=cls.created_tag_id)) # Hypothetical
        #         print(f"Cleaned up tag {cls.created_tag_id} in tearDownClass.")
        #     except Exception as e:
        #         print(f"Error during tearDownClass cleanup of tag {cls.created_tag_id}: {e}")


if __name__ == '__main__':
    unittest.main()
