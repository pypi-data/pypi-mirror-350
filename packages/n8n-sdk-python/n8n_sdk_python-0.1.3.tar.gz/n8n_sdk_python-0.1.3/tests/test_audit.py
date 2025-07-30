import os
import asyncio
import unittest
from typing import Optional

from dotenv import load_dotenv

from n8n_sdk_python import N8nClient
from n8n_sdk_python.models.audit import AuditResponse, AuditAdditionalOptions
from n8n_sdk_python.utils.errors import N8nAPIError

class TestAuditEndToEnd(unittest.IsolatedAsyncioTestCase):
    client: N8nClient

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        base_url = os.getenv("N8N_BASE_URL")
        api_key = os.getenv("N8N_API_KEY")
        if not base_url or not api_key:
            raise ValueError("N8N_BASE_URL and N8N_API_KEY must be set in .env for testing")
        cls.client = N8nClient(base_url=base_url, api_key=api_key)

    async def test_01_generate_audit_report_default(self):
        """Test generating an audit report with default options."""
        try:
            report: AuditResponse = await self.client.audit.generate_audit_report()
            self.assertIsNotNone(report)
            # Basic checks, actual content can vary wildly
            self.assertIsInstance(report.credentials_risk_report, (dict, type(None)))
            self.assertIsInstance(report.database_risk_report, (dict, type(None)))
            self.assertIsInstance(report.filesystem_risk_report, (dict, type(None)))
            self.assertIsInstance(report.nodes_risk_report, (dict, type(None)))
            self.assertIsInstance(report.instance_risk_report, (dict, type(None)))
            print("Successfully generated default audit report.")
        except N8nAPIError as e:
            self.fail(f"Failed to generate default audit report: {e}")

    async def test_02_generate_audit_report_with_options(self):
        """Test generating an audit report with specific options."""
        options = AuditAdditionalOptions(
            days_abandoned_workflow=30,
            categories=["credentials", "nodes"]
        )
        try:
            report: AuditResponse = await self.client.audit.generate_audit_report(options=options)
            self.assertIsNotNone(report)
            if options.categories:
                self.assertIn("credentials", [cat.lower() for cat in options.categories])
                self.assertIn("nodes", [cat.lower() for cat in options.categories])

                # Check if only requested categories are present or if others are None/empty
                if "credentials" in options.categories:
                    self.assertIsNotNone(report.credentials_risk_report, "Credentials report should be present if requested.")
                if "nodes" in options.categories:
                    self.assertIsNotNone(report.nodes_risk_report, "Nodes report should be present if requested.")

                # Assuming categories not requested might be None or have empty sections
                if "database" not in options.categories:
                    self.assertTrue(report.database_risk_report is None or \
                                    (isinstance(report.database_risk_report, dict) and not report.database_risk_report.get("sections")),
                                    "Database report should be absent or empty if not requested.")

            print(f"Successfully generated audit report with options: {options.model_dump_json()}")
        except N8nAPIError as e:
            self.fail(f"Failed to generate audit report with options: {e}")

    async def test_03_generate_audit_report_with_dict_options(self):
        """Test generating an audit report with options as dict."""
        options_dict = {
            "days_abandoned_workflow": 10,
            "categories": ["instance"]
        }
        try:
            report: AuditResponse = await self.client.audit.generate_audit_report(options=options_dict) # type: ignore
            self.assertIsNotNone(report)
            if "instance" in options_dict.get("categories", []):
                 self.assertIsNotNone(report.instance_risk_report, "Instance report should be present if requested.")

            print(f"Successfully generated audit report with dict options: {options_dict}")
        except N8nAPIError as e:
            self.fail(f"Failed to generate audit report with dict options: {e}")

if __name__ == '__main__':
    unittest.main() 