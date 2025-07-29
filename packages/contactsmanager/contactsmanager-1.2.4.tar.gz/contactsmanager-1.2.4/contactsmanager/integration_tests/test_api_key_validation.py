import unittest
import httpx
from pathlib import Path

from contactsmanager import ContactsManagerClient
from contactsmanager.integration_tests.env_loader import load_env_config


class TestApiKeyValidation(unittest.TestCase):
    """Integration tests for API key validation."""

    def setUp(self):
        """Set up test environment."""
        # Load configuration from environment variables or file
        self.config = load_env_config()

        if not self.config:
            self.fail(
                "No test configuration found. Please set TEST_CONFIG environment variable or create test_config.json"
            )

        # Extract credentials
        self.api_key = self.config.get("api_key")
        self.api_secret = self.config.get("api_secret")
        self.org_id = self.config.get("org_id")

        if not self.api_key or not self.api_secret or not self.org_id:
            self.fail("Missing required credentials in test configuration")

        # Get API base URL from config or use default
        self.api_base_url = self.config.get(
            "api_base_url", "https://api.contactsmanager.io"
        )

    def test_valid_api_key(self):
        """Test that a valid API key is accepted."""
        client = ContactsManagerClient(
            api_key=self.api_key, api_secret=self.api_secret, org_id=self.org_id
        )
        self.assertEqual(client.api_key, self.api_key)
        self.assertEqual(client.api_secret, self.api_secret)
        self.assertEqual(client.org_id, self.org_id)

    def test_invalid_api_key_empty(self):
        """Test that an empty API key is rejected."""
        with self.assertRaises(ValueError) as context:
            ContactsManagerClient(
                api_key="", api_secret=self.api_secret, org_id=self.org_id
            )
        self.assertIn("API key is required", str(context.exception))

    def test_invalid_api_key_type(self):
        """Test that a non-string API key is rejected."""
        with self.assertRaises(ValueError) as context:
            ContactsManagerClient(
                api_key=123, api_secret=self.api_secret, org_id=self.org_id
            )
        self.assertIn(
            "API key is required and must be a string", str(context.exception)
        )

    def test_invalid_api_secret_empty(self):
        """Test that an empty API secret is rejected."""
        with self.assertRaises(ValueError) as context:
            ContactsManagerClient(
                api_key=self.api_key, api_secret="", org_id=self.org_id
            )
        self.assertIn("API secret is required", str(context.exception))

    def test_invalid_api_secret_type(self):
        """Test that a non-string API secret is rejected."""
        with self.assertRaises(ValueError) as context:
            ContactsManagerClient(
                api_key=self.api_key, api_secret=123, org_id=self.org_id
            )
        self.assertIn(
            "API secret is required and must be a string", str(context.exception)
        )

    def test_invalid_org_id_empty(self):
        """Test that an empty org ID is rejected."""
        with self.assertRaises(ValueError) as context:
            ContactsManagerClient(
                api_key=self.api_key, api_secret=self.api_secret, org_id=""
            )
        self.assertIn("Organization ID is required", str(context.exception))

    def test_invalid_org_id_type(self):
        """Test that a non-string org ID is rejected."""
        with self.assertRaises(ValueError) as context:
            ContactsManagerClient(
                api_key=self.api_key, api_secret=self.api_secret, org_id=123
            )
        self.assertIn(
            "Organization ID is required and must be a string", str(context.exception)
        )

    def test_server_api_key_validation(self):
        """Test the server-side API key validation endpoint."""
        # Skip this test if we don't have a server API URL
        if not self.config.get("api_base_url"):
            self.skipTest("Missing api_base_url in test config")

        # Initialize the client
        client = ContactsManagerClient(
            api_key=self.api_key, api_secret=self.api_secret, org_id=self.org_id
        )

        # Generate a token for authentication
        token_data = client.generate_token(user_id="test_user")
        token = token_data["token"]

        # Test the validate-key endpoint
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{self.api_base_url}/api/v1/client/validate-key"

        with httpx.Client() as http_client:
            # Test with valid API key
            response = http_client.post(
                url, json={"api_key": self.api_key}, headers=headers
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "success")
            self.assertTrue(data["data"]["valid"])

            # Test with invalid API key
            response = http_client.post(
                url, json={"api_key": "invalid_api_key"}, headers=headers
            )
            self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
