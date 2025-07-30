import os
import asyncio
import unittest
import uuid
from typing import Optional

from dotenv import load_dotenv

from n8n_sdk_python import N8nClient
from n8n_sdk_python.models.variables import Variable, VariablesList # VariableCreate is used internally by client method
from n8n_sdk_python.utils.errors import N8nAPIError

class TestVariablesEndToEnd(unittest.IsolatedAsyncioTestCase):
    client: N8nClient
    created_variable_id: Optional[str] = None
    variable_key_prefix = "testSdkVariableKey_"
    variable_value_prefix = "testSdkValue_"

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        base_url = os.getenv("N8N_BASE_URL")
        api_key = os.getenv("N8N_API_KEY")
        if not base_url or not api_key:
            raise ValueError("N8N_BASE_URL and N8N_API_KEY must be set in .env for testing")
        cls.client = N8nClient(base_url=base_url, api_key=api_key)

    async def test_01_create_variable(self):
        """Test creating a new variable."""
        var_key = f"{self.variable_key_prefix}{uuid.uuid4()}"
        var_value = f"{self.variable_value_prefix}{uuid.uuid4()}"
        try:
            # POST /v1/variables returns 201 with the created variable object.
            variable: Variable = await self.client.variables.create_variable(key=var_key, value=var_value)
            self.assertIsNotNone(variable)
            self.assertIsNotNone(variable.id)
            self.assertEqual(variable.key, var_key)
            self.assertEqual(variable.value, var_value) 
            TestVariablesEndToEnd.created_variable_id = variable.id
            print(f"Variable created with ID: {variable.id}, Key: {var_key}")
        except N8nAPIError as e:
            # 400 Bad Request if key already exists, though uuid should prevent this.
            if e.status_code == 400 and "already exists" in str(e).lower():
                 self.fail(f"Failed to create variable due to key conflict (key: {var_key}): {e}")
            self.fail(f"Failed to create variable: {e}")

    async def test_02_list_variables(self):
        """Test listing variables and finding the created one."""
        self.assertIsNotNone(TestVariablesEndToEnd.created_variable_id, "Variable ID not set from create test")
        created_var_id = TestVariablesEndToEnd.created_variable_id
        try:
            variables_list: VariablesList = await self.client.variables.list_variables(limit=100)
            self.assertIsNotNone(variables_list)
            self.assertIsInstance(variables_list.data, list)
            
            found_created_var = False
            for var_item in variables_list.data:
                if var_item.id == created_var_id:
                    found_created_var = True
                    self.assertTrue(var_item.key.startswith(self.variable_key_prefix))
                    self.assertTrue(var_item.value.startswith(self.variable_value_prefix))
                    break
            self.assertTrue(found_created_var, f"Created variable (ID: {created_var_id}) not found in the list.")
            print(f"Found {len(variables_list.data)} variables. Created variable is present.")
        except N8nAPIError as e:
            self.fail(f"Failed to list variables: {e}")

    async def test_99_delete_variable(self):
        """Test deleting the created variable."""
        self.assertIsNotNone(TestVariablesEndToEnd.created_variable_id, "Variable ID not set for deletion.")
        variable_id_to_delete = TestVariablesEndToEnd.created_variable_id
        try:
            # DELETE /v1/variables/{id} returns 204 No Content.
            # SDK method delete_variable returns None.
            await self.client.variables.delete_variable(variable_id=variable_id_to_delete) # type: ignore
            print(f"Variable {variable_id_to_delete} deletion call completed.")
            TestVariablesEndToEnd.created_variable_id = None # Clear ID after deletion attempt

            # Verify deletion by listing and not finding it
            await asyncio.sleep(1) # Brief delay
            variables_list: VariablesList = await self.client.variables.list_variables(limit=250)
            self.assertFalse(
                any(v.id == variable_id_to_delete for v in variables_list.data),
                f"Deleted variable {variable_id_to_delete} still found in the list."
            )
            print(f"Verified variable {variable_id_to_delete} is no longer in the list.")
        except N8nAPIError as e:
            if e.status_code == 404: # Already deleted
                print(f"Variable {variable_id_to_delete} was already deleted or not found: {e}")
                TestVariablesEndToEnd.created_variable_id = None
            else:
                self.fail(f"Failed to delete variable {variable_id_to_delete}: {e}")

    @classmethod
    def tearDownClass(cls):
        if cls.created_variable_id:
            print(f"Variable Teardown: Variable {cls.created_variable_id} might not have been deleted. Attempting cleanup.")
            try:
                asyncio.run(cls.client.variables.delete_variable(variable_id=cls.created_variable_id)) # type: ignore
                print(f"Variable Teardown: Cleaned up variable {cls.created_variable_id}.")
            except N8nAPIError as e:
                if e.status_code != 404:
                    print(f"Variable Teardown: Error during cleanup of variable {cls.created_variable_id}: {e}")
                else:
                    print(f"Variable Teardown: Variable {cls.created_variable_id} was already gone during cleanup.")

if __name__ == '__main__':
    unittest.main() 