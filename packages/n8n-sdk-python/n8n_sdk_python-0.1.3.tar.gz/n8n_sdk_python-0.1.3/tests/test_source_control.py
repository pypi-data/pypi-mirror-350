import os
import asyncio
import unittest
from typing import Optional, Any

from dotenv import load_dotenv

from n8n_sdk_python import N8nClient
from n8n_sdk_python.models.source_control import ScmPullResponse, ScmPullRequest
from n8n_sdk_python.utils.errors import N8nAPIError

class TestSourceControlEndToEnd(unittest.IsolatedAsyncioTestCase):
    client: N8nClient

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        base_url = os.getenv("N8N_BASE_URL")
        api_key = os.getenv("N8N_API_KEY")
        if not base_url or not api_key:
            raise ValueError("N8N_BASE_URL and N8N_API_KEY must be set in .env for testing")
        cls.client = N8nClient(base_url=base_url, api_key=api_key)

    async def test_01_pull_from_source_control(self):
        """Test pulling from source control. This test's outcome heavily depends on n8n instance configuration."""
        print("Attempting to pull from source control. This requires the Source Control feature to be licensed and connected.")
        try:
            # Attempt a non-forced pull first
            response: ScmPullResponse = await self.client.source_control.pull_from_source_control(force=False)
            self.assertIsNotNone(response)
            # Successful pull might have empty changes if already up-to-date
            self.assertIsInstance(response.variables, dict)
            self.assertIsInstance(response.credentials, list)
            self.assertIsInstance(response.workflows, list)
            self.assertIsInstance(response.tags, dict)
            print(f"Successfully called pull_from_source_control (force=False). Response: {response.model_dump_json(indent=2)}")

        except N8nAPIError as e:
            # Common errors if not configured:
            # 409 Conflict: "A git repository is not configured for this instance."
            # 402 Payment Required: "Source control is a paid feature..."
            # 501 Not Implemented: If the feature is entirely unavailable on the n8n version/distro
            if e.status_code in [409, 402, 501]:
                print(f"Source control pull failed as expected due to configuration/licensing: {e.status_code} - {e.message}")
                # This is an expected outcome if not configured, so not a test failure.
                self.skipTest(f"Skipping source control test: Feature not configured or licensed (Error {e.status_code}).")
            else:
                self.fail(f"Failed to pull from source control with an unexpected error: {e}")
        except Exception as e:
             self.fail(f"An unexpected non-API error occurred during source control pull: {e}")

    async def test_02_pull_from_source_control_forced(self):
        """Test a forced pull from source control."""
        print("Attempting a forced pull from source control.")
        try:
            response: ScmPullResponse = await self.client.source_control.pull_from_source_control(force=True)
            self.assertIsNotNone(response)
            print(f"Successfully called pull_from_source_control (force=True). Response: {response.model_dump_json(indent=2)}")

        except N8nAPIError as e:
            if e.status_code in [409, 402, 501]:
                print(f"Forced source control pull failed as expected due to configuration/licensing: {e.status_code} - {e.message}")
                self.skipTest(f"Skipping forced source control test: Feature not configured or licensed (Error {e.status_code}).")
            else:
                self.fail(f"Failed forced pull from source control with an unexpected error: {e}")
        except Exception as e:
             self.fail(f"An unexpected non-API error occurred during forced source control pull: {e}")

    async def test_03_pull_from_source_control_with_variables(self):
        """Test pulling from source control with variables."""
        print("Attempting to pull from source control with variables.")
        variables_payload = {"testVar": "sdkValue", "anotherVar": 123}
        try:
            response: ScmPullResponse = await self.client.source_control.pull_from_source_control(
                force=False, 
                variables=variables_payload
            )
            self.assertIsNotNone(response)
            # Further assertions would depend on how n8n uses these variables during a pull
            # and what the expected response structure is when variables are provided.
            # For now, primarily testing the call succeeds if configured.
            print(f"Successfully called pull_from_source_control with variables. Response: {response.model_dump_json(indent=2)}")

        except N8nAPIError as e:
            if e.status_code in [409, 402, 501]:
                print(f"Source control pull with variables failed as expected due to configuration/licensing: {e.status_code} - {e.message}")
                self.skipTest(f"Skipping source control pull with variables: Feature not configured or licensed (Error {e.status_code}).")
            else:
                self.fail(f"Failed pull from source control with variables with an unexpected error: {e}")
        except Exception as e:
             self.fail(f"An unexpected non-API error occurred during source control pull with variables: {e}")

if __name__ == '__main__':
    unittest.main() 