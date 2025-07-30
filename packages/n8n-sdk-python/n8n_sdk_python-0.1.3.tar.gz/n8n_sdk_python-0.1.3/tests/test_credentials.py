import os
import asyncio
import unittest
import uuid
from typing import Optional, Any

from dotenv import load_dotenv

from n8n_sdk_python import N8nClient
from n8n_sdk_python.models.credentials import (
    CredentialListItem,
    CredentialDetail,
    CredentialTestResult,
    CredentialTypeDescription,
    CredentialShort,
    CredentialDataSchemaResponse,
    CredentialCreate
)
from n8n_sdk_python.utils.errors import N8nAPIError

class TestCredentialsEndToEnd(unittest.IsolatedAsyncioTestCase):
    client: N8nClient
    created_credential_id: Optional[str] = None
    # Use a common credential type for testing that doesn't require complex external setup
    # 'n8n-nodes-base.httpHeaderAuth' is a good candidate or a custom one if available.
    # For simplicity, let's use a type that is generally available.
    # The actual type might need adjustment based on the n8n instance's available node types.
    # Using 'n8n-nodes-base.headerAuth' as it's often present and simple.
    test_cred_type = "n8n-nodes-base.headerAuth"
    test_cred_name_prefix = "TestSDKCred-"

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        base_url = os.getenv("N8N_BASE_URL")
        api_key = os.getenv("N8N_API_KEY")
        if not base_url or not api_key:
            raise ValueError("N8N_BASE_URL and N8N_API_KEY must be set in .env for testing")
        cls.client = N8nClient(base_url=base_url, api_key=api_key)

    async def test_01_create_credential(self):
        """Test creating a new credential."""
        cred_name = f"{self.test_cred_name_prefix}{uuid.uuid4()}"
        # Data for 'n8n-nodes-base.headerAuth' typically includes 'name' and 'value' for the header
        cred_data = {"name": "X-Test-Header", "value": "sdk-test-value"}
        try:
            credential: CredentialShort = await self.client.credentials.create_credential(
                name=cred_name,
                credential_type=self.test_cred_type,
                data=cred_data
            )
            self.assertIsNotNone(credential)
            self.assertIsNotNone(credential.id)
            self.assertEqual(credential.name, cred_name)
            self.assertEqual(credential.type, self.test_cred_type) 
            TestCredentialsEndToEnd.created_credential_id = credential.id
            print(f"Credential created with ID: {credential.id}, Name: {cred_name}")
        except N8nAPIError as e:
            # If the type doesn't exist, this will fail. Common issue.
            if "not found" in str(e).lower() and f"type '{self.test_cred_type}'" in str(e).lower():
                 self.fail(f"Credential type '{self.test_cred_type}' not found on n8n instance. Please use a valid type. Error: {e}") 
            self.fail(f"Failed to create credential: {e}")

    async def test_02_get_credential(self):
        """Test retrieving the created credential."""
        self.assertIsNotNone(TestCredentialsEndToEnd.created_credential_id, "Credential ID not set from create test")
        cred_id = TestCredentialsEndToEnd.created_credential_id
        try:
            credential: Optional[CredentialDetail] = await self.client.credentials.get_credential(credential_id=cred_id) # type: ignore
            self.assertIsNotNone(credential)
            self.assertEqual(credential.id, cred_id) # type: ignore
            self.assertEqual(credential.type, self.test_cred_type) # type: ignore
            # Ensure data is present, though specific fields depend on type and n8n version masking
            self.assertIsNotNone(credential.data) # type: ignore
            print(f"Successfully retrieved credential {cred_id}")
        except N8nAPIError as e:
            self.fail(f"Failed to get credential {cred_id}: {e}")

    async def test_03_list_credentials(self):
        """Test listing credentials and finding the created one."""
        self.assertIsNotNone(TestCredentialsEndToEnd.created_credential_id, "Credential ID not set.")
        try:
            credentials: list[CredentialListItem] = await self.client.credentials.get_credentials()
            self.assertIsInstance(credentials, list)
            self.assertTrue(any(c.id == TestCredentialsEndToEnd.created_credential_id for c in credentials))
            print(f"Found {len(credentials)} credentials. Created one is present.")
            
            # Test filtering by type
            typed_credentials: list[CredentialListItem] = await self.client.credentials.get_credentials(credential_type=self.test_cred_type)
            self.assertTrue(all(c.type == self.test_cred_type for c in typed_credentials))
            self.assertTrue(any(c.id == TestCredentialsEndToEnd.created_credential_id for c in typed_credentials))
            print(f"Found {len(typed_credentials)} credentials of type {self.test_cred_type}.")
        except N8nAPIError as e:
            self.fail(f"Failed to list credentials: {e}")

    async def test_04_update_credential(self):
        """Test updating the created credential."""
        self.assertIsNotNone(TestCredentialsEndToEnd.created_credential_id, "Credential ID not set.")
        cred_id = TestCredentialsEndToEnd.created_credential_id
        updated_name = f"{self.test_cred_name_prefix}Updated-{uuid.uuid4()}"
        # Data for update. For 'headerAuth', it might be the same structure.
        updated_data = {"name": "X-Updated-Test-Header", "value": "sdk-updated-value"}
        
        # The update_credential in SDK expects a full dict usually, not just name/data.
        # Let's form the update payload based on what create_credential might expect or what get_credential returns.
        # The API itself for PATCH /v1/credentials/{id} might accept partial updates.
        # SDK's update_credential: credential_data: dict[str, Any]
        # This typically means the full new state or a subset of fields to change.
        # For n8n, PATCH usually means providing only fields to change.
        # Let's try with only 'name' and 'data'.
        update_payload = {"name": updated_name, "data": updated_data}

        try:
            credential: Optional[CredentialDetail] = await self.client.credentials.update_credential(
                credential_id=cred_id, # type: ignore
                credential_data=update_payload 
            )
            self.assertIsNotNone(credential)
            self.assertEqual(credential.id, cred_id) # type: ignore
            self.assertEqual(credential.name, updated_name) # type: ignore
            # Verify updated data if possible (n8n might mask sensitive data on return)
            # For headerAuth, 'name' in data should be X-Updated-Test-Header
            self.assertIn("name", credential.data) # type: ignore
            self.assertEqual(credential.data["name"], "X-Updated-Test-Header") # type: ignore
            print(f"Successfully updated credential {cred_id} to name {updated_name}")
        except N8nAPIError as e:
            self.fail(f"Failed to update credential {cred_id}: {e}")

    async def test_05_test_credential(self):
        """Test testing the credential's validity."""
        # Testing a credential might not always be meaningful for all types without specific setup.
        # For 'headerAuth', a test might not do much or always succeed if structure is valid.
        # This test primarily checks if the endpoint can be called.
        self.assertIsNotNone(TestCredentialsEndToEnd.created_credential_id, "Credential ID not set.")
        cred_id = TestCredentialsEndToEnd.created_credential_id
        try:
            result: Optional[CredentialTestResult] = await self.client.credentials.test_credential(credential_id=cred_id) # type: ignore
            self.assertIsNotNone(result)
            self.assertIn(result.status, ["success", "error"]) # type: ignore
            print(f"Credential test for {cred_id} resulted in status: {result.status} with message: {result.message}") # type: ignore
            # For many simple credential types like headerAuth, a structural check might always pass.
            # self.assertEqual(result.status, "success", f"Expected test to succeed for {self.test_cred_type}")
        except N8nAPIError as e:
            self.fail(f"Failed to test credential {cred_id}: {e}")

    async def test_06_get_credential_types(self):
        """Test retrieving all credential types and the specific test type."""
        try:
            types: dict[str, CredentialTypeDescription] = await self.client.credentials.get_credential_types()
            self.assertIsInstance(types, dict)
            self.assertIn(self.test_cred_type, types, f"Test credential type {self.test_cred_type} not found in instance types.")
            print(f"Found {len(types)} credential types. Test type '{self.test_cred_type}' is present.")
            
            cred_type_desc: Optional[CredentialTypeDescription] = await self.client.credentials.get_credential_type(type_name=self.test_cred_type)
            self.assertIsNotNone(cred_type_desc)
            self.assertEqual(cred_type_desc.name, self.test_cred_type) # type: ignore
        except N8nAPIError as e:
            self.fail(f"Failed to get credential types: {e}")

    async def test_07_get_credential_schema(self):
        """Test retrieving the schema for the test credential type."""
        try:
            schema: CredentialDataSchemaResponse = await self.client.credentials.get_credential_schema(credential_type_name=self.test_cred_type)
            self.assertIsNotNone(schema)
            self.assertIsInstance(schema.properties, dict) # type: ignore
            # For 'n8n-nodes-base.headerAuth', schema should define 'name' and 'value'
            self.assertIn("name", schema.properties) # type: ignore
            self.assertIn("value", schema.properties) # type: ignore
            print(f"Successfully retrieved schema for credential type {self.test_cred_type}")
        except N8nAPIError as e:
            self.fail(f"Failed to get credential schema for {self.test_cred_type}: {e}")

    # test_08_transfer_credential_to_project - Requires another project to exist, complex for basic E2E. Placeholder.
    # async def test_08_transfer_credential_to_project(self):
    #     pass 

    async def test_99_delete_credential(self):
        """Test deleting the created credential."""
        self.assertIsNotNone(TestCredentialsEndToEnd.created_credential_id, "Credential ID not set for deletion.")
        cred_id = TestCredentialsEndToEnd.created_credential_id
        try:
            response: CredentialShort = await self.client.credentials.delete_credential(credential_id=cred_id) # type: ignore
            self.assertIsNotNone(response)
            self.assertEqual(response.id, cred_id)
            print(f"Credential {cred_id} deleted successfully.")
            TestCredentialsEndToEnd.created_credential_id = None # Clear ID after deletion
        except N8nAPIError as e:
            if e.status_code == 404:
                print(f"Credential {cred_id} was already deleted or not found during cleanup: {e}")
                TestCredentialsEndToEnd.created_credential_id = None
            else:
                self.fail(f"Failed to delete credential {cred_id}: {e}")

    @classmethod
    def tearDownClass(cls):
        if cls.created_credential_id:
            print(f"Credential Teardown: Credential {cls.created_credential_id} might not have been deleted. Attempting cleanup.")
            try:
                asyncio.run(cls.client.credentials.delete_credential(credential_id=cls.created_credential_id)) # type: ignore
                print(f"Credential Teardown: Cleaned up credential {cls.created_credential_id}.")
            except N8nAPIError as e:
                # If it's already gone (404), that's fine for cleanup.
                if e.status_code != 404:
                    print(f"Credential Teardown: Error during cleanup of credential {cls.created_credential_id}: {e}")
                else:
                    print(f"Credential Teardown: Credential {cls.created_credential_id} was already gone during cleanup.")

if __name__ == '__main__':
    unittest.main() 