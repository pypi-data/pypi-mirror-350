import os
import asyncio
import unittest
import uuid
from typing import Optional

from dotenv import load_dotenv

from n8n_sdk_python import N8nClient
from n8n_sdk_python.models.workflows import Tag, TagList # Models are in workflows for now
from n8n_sdk_python.utils.errors import N8nAPIError

class TestTagsEndToEnd(unittest.IsolatedAsyncioTestCase):
    client: N8nClient
    created_tag_id: Optional[str] = None
    tag_name_prefix = "TestSDKTag-"

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        base_url = os.getenv("N8N_BASE_URL")
        api_key = os.getenv("N8N_API_KEY")
        if not base_url or not api_key:
            raise ValueError("N8N_BASE_URL and N8N_API_KEY must be set in .env for testing")
        cls.client = N8nClient(base_url=base_url, api_key=api_key)

    async def test_01_create_tag(self):
        """Test creating a new tag."""
        tag_name = f"{self.tag_name_prefix}{uuid.uuid4()}"
        try:
            tag: Tag = await self.client.tags.create_tag(name=tag_name)
            self.assertIsNotNone(tag)
            self.assertIsNotNone(tag.id)
            self.assertEqual(tag.name, tag_name)
            TestTagsEndToEnd.created_tag_id = tag.id
            print(f"Tag created with ID: {tag.id}, Name: {tag_name}")
        except N8nAPIError as e:
            # Check for 409 Conflict if tag name already exists (though uuid should make it unique)
            if e.status_code == 409:
                self.fail(f"Failed to create tag due to conflict (name likely exists): {e}")
            self.fail(f"Failed to create tag: {e}")

    async def test_02_get_tag(self):
        """Test retrieving the created tag."""
        self.assertIsNotNone(TestTagsEndToEnd.created_tag_id, "Tag ID not set from create test")
        tag_id = TestTagsEndToEnd.created_tag_id
        try:
            tag: Tag = await self.client.tags.get_tag(tag_id=tag_id) # type: ignore
            self.assertIsNotNone(tag)
            self.assertEqual(tag.id, tag_id)
            self.assertTrue(tag.name.startswith(self.tag_name_prefix))
            print(f"Successfully retrieved tag {tag_id}")
        except N8nAPIError as e:
            self.fail(f"Failed to get tag {tag_id}: {e}")

    async def test_03_list_tags(self):
        """Test listing tags and finding the created one."""
        self.assertIsNotNone(TestTagsEndToEnd.created_tag_id, "Tag ID not set.")
        try:
            tag_list: TagList = await self.client.tags.list_tags(limit=100) # Use a limit to find ours
            self.assertIsNotNone(tag_list)
            self.assertIsInstance(tag_list.data, list)
            self.assertTrue(
                any(t.id == TestTagsEndToEnd.created_tag_id for t in tag_list.data),
                "Created tag not found in the list."
            )
            print(f"Found {len(tag_list.data)} tags. Created tag is present.")
        except N8nAPIError as e:
            self.fail(f"Failed to list tags: {e}")

    async def test_04_update_tag(self):
        """Test updating the created tag."""
        self.assertIsNotNone(TestTagsEndToEnd.created_tag_id, "Tag ID not set.")
        tag_id = TestTagsEndToEnd.created_tag_id
        updated_tag_name = f"{self.tag_name_prefix}Updated-{uuid.uuid4()}"
        try:
            tag: Tag = await self.client.tags.update_tag(tag_id=tag_id, name=updated_tag_name) # type: ignore
            self.assertIsNotNone(tag)
            self.assertEqual(tag.id, tag_id)
            self.assertEqual(tag.name, updated_tag_name)
            print(f"Successfully updated tag {tag_id} to name {updated_tag_name}")
        except N8nAPIError as e:
            if e.status_code == 409: # Name conflict on update
                self.fail(f"Failed to update tag due to name conflict: {e}")
            self.fail(f"Failed to update tag {tag_id}: {e}")

    async def test_99_delete_tag(self):
        """Test deleting the created tag."""
        self.assertIsNotNone(TestTagsEndToEnd.created_tag_id, "Tag ID not set for deletion.")
        tag_id = TestTagsEndToEnd.created_tag_id
        try:
            # N8N-API.md: DELETE /tags/{id} returns the deleted tag object (200 OK)
            deleted_tag: Tag = await self.client.tags.delete_tag(tag_id=tag_id) # type: ignore
            self.assertIsNotNone(deleted_tag)
            self.assertEqual(deleted_tag.id, tag_id)
            print(f"Tag {tag_id} deleted successfully (response: {deleted_tag.name}).")
            TestTagsEndToEnd.created_tag_id = None # Clear ID after deletion

            # Verify deletion by trying to get it again
            with self.assertRaises(N8nAPIError) as context:
                await self.client.tags.get_tag(tag_id=tag_id) # type: ignore
            self.assertEqual(context.exception.status_code, 404, "Expected 404 when getting a deleted tag.")
            print(f"Verified tag {tag_id} is no longer accessible (404).")
        except N8nAPIError as e:
            if e.status_code == 404: # Already deleted
                print(f"Tag {tag_id} was already deleted or not found: {e}")
                TestTagsEndToEnd.created_tag_id = None
            else:
                self.fail(f"Failed to delete tag {tag_id}: {e}")

    @classmethod
    def tearDownClass(cls):
        if cls.created_tag_id:
            print(f"Tag Teardown: Tag {cls.created_tag_id} might not have been deleted. Attempting cleanup.")
            try:
                asyncio.run(cls.client.tags.delete_tag(tag_id=cls.created_tag_id)) # type: ignore
                print(f"Tag Teardown: Cleaned up tag {cls.created_tag_id}.")
            except N8nAPIError as e:
                if e.status_code != 404:
                    print(f"Tag Teardown: Error during cleanup of tag {cls.created_tag_id}: {e}")
                else:
                    print(f"Tag Teardown: Tag {cls.created_tag_id} was already gone during cleanup.")

if __name__ == '__main__':
    unittest.main() 