import os
import asyncio
import unittest
import uuid
from typing import Optional

from dotenv import load_dotenv

from n8n_sdk_python import N8nClient
from n8n_sdk_python.models.projects import Project, ProjectList
from n8n_sdk_python.utils.errors import N8nAPIError

class TestProjectsEndToEnd(unittest.IsolatedAsyncioTestCase):
    client: N8nClient
    created_project_id: Optional[str] = None
    project_name_prefix = "TestSDKProject-"

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        base_url = os.getenv("N8N_BASE_URL")
        api_key = os.getenv("N8N_API_KEY")
        if not base_url or not api_key:
            raise ValueError("N8N_BASE_URL and N8N_API_KEY must be set in .env for testing")
        cls.client = N8nClient(base_url=base_url, api_key=api_key)

    async def test_01_create_project(self):
        """Test creating a new project."""
        project_name = f"{self.project_name_prefix}{uuid.uuid4()}"
        try:
            project: Project = await self.client.projects.create_project(name=project_name)
            self.assertIsNotNone(project)
            self.assertIsNotNone(project.id)
            self.assertEqual(project.name, project_name)
            TestProjectsEndToEnd.created_project_id = project.id
            print(f"Project created with ID: {project.id}, Name: {project_name}")
        except N8nAPIError as e:
            self.fail(f"Failed to create project: {e}")

    async def test_02_list_projects(self):
        """Test listing projects and finding the created one."""
        self.assertIsNotNone(TestProjectsEndToEnd.created_project_id, "Project ID not set from create test")
        try:
            project_list: ProjectList = await self.client.projects.list_projects(limit=100) # High limit to find ours
            self.assertIsNotNone(project_list)
            self.assertIsInstance(project_list.data, list)
            self.assertTrue(
                any(p.id == TestProjectsEndToEnd.created_project_id for p in project_list.data),
                "Created project not found in the list."
            )
            print(f"Found {len(project_list.data)} projects. Created project is present.")
        except N8nAPIError as e:
            self.fail(f"Failed to list projects: {e}")

    async def test_03_update_project(self):
        """Test updating the created project."""
        self.assertIsNotNone(TestProjectsEndToEnd.created_project_id, "Project ID not set.")
        project_id = TestProjectsEndToEnd.created_project_id
        updated_project_name = f"{self.project_name_prefix}Updated-{uuid.uuid4()}"
        try:
            # According to N8N-API.md, PUT /projects/{projectId} returns 204 No Content
            # The SDK method update_project returns None.
            await self.client.projects.update_project(project_id=project_id, name=updated_project_name) # type: ignore
            print(f"Update project call for {project_id} completed. Verifying name change by listing.")
            
            # Verify by listing/getting - N8N API for GET /projects doesn't allow fetching by ID directly.
            # We have to list and find.
            project_list: ProjectList = await self.client.projects.list_projects(limit=250)
            updated_project_found = False
            for p in project_list.data:
                if p.id == project_id:
                    self.assertEqual(p.name, updated_project_name, "Project name was not updated.")
                    updated_project_found = True
                    break
            self.assertTrue(updated_project_found, "Updated project not found in list to verify name change.")
            print(f"Successfully updated project {project_id} to name {updated_project_name}")
        except N8nAPIError as e:
            self.fail(f"Failed to update project {project_id}: {e}")

    async def test_99_delete_project(self):
        """Test deleting the created project."""
        self.assertIsNotNone(TestProjectsEndToEnd.created_project_id, "Project ID not set for deletion.")
        project_id = TestProjectsEndToEnd.created_project_id
        try:
            # According to N8N-API.md, DELETE /projects/{projectId} returns 204 No Content
            # The SDK method delete_project returns None.
            await self.client.projects.delete_project(project_id=project_id) # type: ignore
            print(f"Project {project_id} deletion call completed.")
            TestProjectsEndToEnd.created_project_id = None # Clear ID after deletion attempt

            # Verify deletion by listing
            await asyncio.sleep(1) # Give a moment for deletion to propagate if needed
            project_list: ProjectList = await self.client.projects.list_projects(limit=250)
            self.assertFalse(
                any(p.id == project_id for p in project_list.data),
                f"Deleted project {project_id} still found in the list."
            )
            print(f"Verified project {project_id} is no longer in the list.")
        except N8nAPIError as e:
            if e.status_code == 404: # If it was somehow already deleted
                print(f"Project {project_id} was already deleted or not found: {e}")
                TestProjectsEndToEnd.created_project_id = None
            else:
                self.fail(f"Failed to delete project {project_id}: {e}")

    @classmethod
    def tearDownClass(cls):
        if cls.created_project_id:
            print(f"Project Teardown: Project {cls.created_project_id} might not have been deleted. Attempting cleanup.")
            try:
                asyncio.run(cls.client.projects.delete_project(project_id=cls.created_project_id)) # type: ignore
                print(f"Project Teardown: Cleaned up project {cls.created_project_id}.")
            except N8nAPIError as e:
                if e.status_code != 404:
                    print(f"Project Teardown: Error during cleanup of project {cls.created_project_id}: {e}")
                else:
                    print(f"Project Teardown: Project {cls.created_project_id} was already gone during cleanup.")

if __name__ == '__main__':
    unittest.main() 