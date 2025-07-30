import os
import asyncio
import unittest
import uuid
from typing import Optional, Any

from dotenv import load_dotenv

from n8n_sdk_python import N8nClient
from n8n_sdk_python.models.users import (
    UsersList, UserCreateItem, UserCreateResponseItem, User, UserRole
)
from n8n_sdk_python.utils.errors import N8nAPIError

class TestUsersEndToEnd(unittest.IsolatedAsyncioTestCase):
    client: N8nClient
    created_user_email: Optional[str] = None
    created_user_id: Optional[str] = None # Store ID if returned by create, or from get_user later
    user_email_prefix = "test-sdk-user-"
    user_email_domain = "@example.com"

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        base_url = os.getenv("N8N_BASE_URL")
        api_key = os.getenv("N8N_API_KEY")
        if not base_url or not api_key:
            raise ValueError("N8N_BASE_URL and N8N_API_KEY must be set in .env for testing")
        cls.client = N8nClient(base_url=base_url, api_key=api_key)

    async def test_01_create_user(self):
        """Test creating a new user."""
        unique_part = uuid.uuid4()
        user_email = f"{self.user_email_prefix}{unique_part}{self.user_email_domain}"
        # Default role for creation according to N8N-API.md for POST /users can be specified.
        # Let's try creating with a specific role, e.g., member.
        user_to_create = UserCreateItem(email=user_email, role=UserRole.MEMBER)
        
        try:
            # POST /v1/users expects a list of users and returns a list of responses.
            response_list: list[UserCreateResponseItem] = await self.client.users.create_users(users=[user_to_create])
            self.assertIsInstance(response_list, list)
            self.assertEqual(len(response_list), 1, "Expected one response item for one created user.")
            
            response_item = response_list[0]
            # Check for errors in response item first
            if response_item.error:
                self.fail(f"Failed to create user {user_email}. API Error: {response_item.error}")
            
            self.assertIsNotNone(response_item.user, "User object in creation response is None.")
            created_user_info = response_item.user
            self.assertIsNotNone(created_user_info.id) # type: ignore
            self.assertEqual(created_user_info.email, user_email) # type: ignore
            
            TestUsersEndToEnd.created_user_email = user_email
            TestUsersEndToEnd.created_user_id = created_user_info.id # type: ignore
            print(f"User created with ID: {created_user_info.id}, Email: {user_email}") # type: ignore

        except N8nAPIError as e:
            # 403 Forbidden is likely if the API key doesn't have owner/admin rights
            if e.status_code == 403:
                self.fail(f"Failed to create user due to permissions (403 Forbidden). API key might need owner rights. Error: {e}")
            self.fail(f"Failed to create user: {e}")

    async def test_02_get_user(self):
        """Test retrieving the created user by email and ID."""
        self.assertIsNotNone(TestUsersEndToEnd.created_user_email, "User email not set from create test")
        self.assertIsNotNone(TestUsersEndToEnd.created_user_id, "User ID not set from create test")
        user_email = TestUsersEndToEnd.created_user_email
        user_id = TestUsersEndToEnd.created_user_id

        try:
            # Get by email
            user_by_email: User = await self.client.users.get_user(user_id_or_email=user_email, include_role=True) # type: ignore
            self.assertIsNotNone(user_by_email)
            self.assertEqual(user_by_email.email, user_email)
            self.assertEqual(user_by_email.id, user_id)
            self.assertIsNotNone(user_by_email.role, "User role should be included.")
            # Role might be owner if instance auto-assigns, or the role we set (member)
            # self.assertEqual(user_by_email.role, UserRole.MEMBER.value) 
            print(f"Successfully retrieved user by email: {user_email}, Role: {user_by_email.role}")

            # Get by ID
            user_by_id: User = await self.client.users.get_user(user_id_or_email=user_id, include_role=True) # type: ignore
            self.assertIsNotNone(user_by_id)
            self.assertEqual(user_by_id.id, user_id)
            self.assertEqual(user_by_id.email, user_email)
            print(f"Successfully retrieved user by ID: {user_id}")
        except N8nAPIError as e:
            self.fail(f"Failed to get user {user_email} (ID: {user_id}): {e}")

    async def test_03_list_users(self):
        """Test listing users and finding the created one."""
        self.assertIsNotNone(TestUsersEndToEnd.created_user_email, "User email not set.")
        try:
            users_list_response: UsersList = await self.client.users.list_users(limit=100, include_role=True)
            self.assertIsNotNone(users_list_response)
            self.assertIsInstance(users_list_response.data, list)
            found = any(u.email == TestUsersEndToEnd.created_user_email for u in users_list_response.data)
            self.assertTrue(found, f"Created user {TestUsersEndToEnd.created_user_email} not found in the list.")
            print(f"Found {len(users_list_response.data)} users. Created user is present.")
        except N8nAPIError as e:
            self.fail(f"Failed to list users: {e}")

    async def test_04_update_user_role(self):
        """Test updating the role of the created user."""
        self.assertIsNotNone(TestUsersEndToEnd.created_user_id, "User ID not set.")
        user_id = TestUsersEndToEnd.created_user_id
        new_role = UserRole.ADMIN # Promote to admin for test
        try:
            # PATCH /v1/users/{id}/role returns 200 OK (no specific body in N8N-API.md for success)
            # SDK method returns None.
            await self.client.users.update_user_role(user_id_or_email=user_id, new_role=new_role) # type: ignore
            print(f"User role update call for {user_id} to {new_role.value} completed.")

            # Verify by getting the user again
            updated_user: User = await self.client.users.get_user(user_id_or_email=user_id, include_role=True) # type: ignore
            self.assertEqual(updated_user.role, new_role.value, f"User role was not updated to {new_role.value}.")
            print(f"Successfully verified user {user_id} role updated to {new_role.value}.")
        except N8nAPIError as e:
            self.fail(f"Failed to update user role for {user_id}: {e}")

    async def test_99_delete_user(self):
        """Test deleting the created user."""
        self.assertIsNotNone(TestUsersEndToEnd.created_user_id, "User ID not set for deletion.")
        user_id_to_delete = TestUsersEndToEnd.created_user_id
        try:
            # DELETE /v1/users/{id} returns 204 No Content. SDK method returns None.
            await self.client.users.delete_user(user_id_or_email=user_id_to_delete) # type: ignore
            print(f"User {user_id_to_delete} deletion call completed.")
            TestUsersEndToEnd.created_user_id = None
            TestUsersEndToEnd.created_user_email = None

            # Verify deletion by trying to get it again
            await asyncio.sleep(1) # Small delay
            with self.assertRaises(N8nAPIError) as context:
                await self.client.users.get_user(user_id_or_email=user_id_to_delete) # type: ignore
            self.assertEqual(context.exception.status_code, 404, "Expected 404 when getting a deleted user.")
            print(f"Verified user {user_id_to_delete} is no longer accessible (404).")
        except N8nAPIError as e:
            if e.status_code == 404: # Already deleted
                print(f"User {user_id_to_delete} was already deleted or not found: {e}")
                TestUsersEndToEnd.created_user_id = None
                TestUsersEndToEnd.created_user_email = None
            else:
                self.fail(f"Failed to delete user {user_id_to_delete}: {e}")

    @classmethod
    def tearDownClass(cls):
        if cls.created_user_id:
            print(f"User Teardown: User {cls.created_user_id} ({cls.created_user_email}) might not have been deleted. Attempting cleanup.")
            try:
                asyncio.run(cls.client.users.delete_user(user_id_or_email=cls.created_user_id)) # type: ignore
                print(f"User Teardown: Cleaned up user {cls.created_user_id}.")
            except N8nAPIError as e:
                if e.status_code != 404:
                    print(f"User Teardown: Error during cleanup of user {cls.created_user_id}: {e}")
                else:
                    print(f"User Teardown: User {cls.created_user_id} was already gone during cleanup.")

if __name__ == '__main__':
    unittest.main() 