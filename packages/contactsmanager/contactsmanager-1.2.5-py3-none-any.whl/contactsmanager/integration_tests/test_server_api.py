import unittest
import httpx
import time
from pathlib import Path

from contactsmanager import ContactsManagerClient
from contactsmanager.types import UserInfo, DeviceInfo
from contactsmanager.server_api import ServerAPIError
from contactsmanager.integration_tests.env_loader import load_env_config


class TestServerAPI(unittest.TestCase):
    """Integration tests for Server API create/delete user functionality."""

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

        # Initialize the client
        self.client = ContactsManagerClient(
            api_key=self.api_key, api_secret=self.api_secret, org_id=self.org_id
        )

    def test_create_user_with_email(self):
        """Test creating a user with email through the server API."""
        # Create unique user ID for this test
        user_id = f"test_user_email_{int(time.time())}"

        user_info = UserInfo(
            user_id=user_id,
            full_name="Test User Email",
            email=f"test_{int(time.time())}@example.com",
        )

        device_info = DeviceInfo(
            device_type="test", os="integration-test", app_version="1.0.0"
        )

        try:
            # Create user
            response = self.client.create_user(user_info, device_info)

            # Verify response structure
            self.assertEqual(response.status, "success")
            self.assertIsNotNone(response.data.token)
            self.assertIsNotNone(response.data.token.token)
            self.assertIsInstance(response.data.token.expires_at, int)
            self.assertIsNotNone(response.data.user)
            self.assertEqual(response.data.user.organization_user_id, user_id)
            self.assertEqual(response.data.user.email, user_info.email)
            self.assertEqual(response.data.user.full_name, user_info.full_name)
            self.assertIsInstance(response.data.created, bool)

        except ServerAPIError as e:
            self.fail(f"Server API error: {e}")

    def test_create_user_with_phone(self):
        """Test creating a user with phone through the server API."""
        # Create unique user ID for this test
        user_id = f"test_user_phone_{int(time.time())}"

        user_info = UserInfo(
            user_id=user_id,
            full_name="Test User Phone",
            phone=f"+1555{int(time.time()) % 10000:04d}",
        )

        device_info = DeviceInfo(device_type="mobile", os="iOS", app_version="2.0.0")

        try:
            # Create user
            response = self.client.create_user(user_info, device_info)

            # Verify response structure
            self.assertEqual(response.status, "success")
            self.assertIsNotNone(response.data.token)
            self.assertIsNotNone(response.data.user)
            self.assertEqual(response.data.user.organization_user_id, user_id)
            self.assertEqual(response.data.user.phone, user_info.phone)
            self.assertEqual(response.data.user.full_name, user_info.full_name)

        except ServerAPIError as e:
            self.fail(f"Server API error: {e}")

    def test_create_user_with_both_email_and_phone(self):
        """Test creating a user with both email and phone."""
        # Create unique user ID for this test
        user_id = f"test_user_both_{int(time.time())}"

        user_info = UserInfo(
            user_id=user_id,
            full_name="Test User Both",
            email=f"test_both_{int(time.time())}@example.com",
            phone=f"+1555{int(time.time()) % 10000:04d}",
            avatar_url="https://example.com/avatar.jpg",
            metadata={"test_type": "integration", "timestamp": int(time.time())},
        )

        try:
            # Create user
            response = self.client.create_user(user_info)

            # Verify response structure
            self.assertEqual(response.status, "success")
            self.assertIsNotNone(response.data.user)
            self.assertEqual(response.data.user.organization_user_id, user_id)
            self.assertEqual(response.data.user.email, user_info.email)
            self.assertEqual(response.data.user.phone, user_info.phone)
            self.assertEqual(response.data.user.full_name, user_info.full_name)
            self.assertEqual(response.data.user.avatar_url, user_info.avatar_url)
            self.assertIsNotNone(response.data.user.contact_metadata)

        except ServerAPIError as e:
            self.fail(f"Server API error: {e}")

    def test_update_existing_user(self):
        """Test updating an existing user."""
        # Create unique user ID for this test
        user_id = f"test_user_update_{int(time.time())}"

        # First, create a user
        user_info_create = UserInfo(
            user_id=user_id,
            full_name="Original Name",
            email=f"original_{int(time.time())}@example.com",
        )

        try:
            # Create user
            create_response = self.client.create_user(user_info_create)
            self.assertEqual(create_response.status, "success")
            self.assertTrue(create_response.data.created)

            # Now update the same user
            user_info_update = UserInfo(
                user_id=user_id,
                full_name="Updated Name",
                email=f"updated_{int(time.time())}@example.com",
                phone=f"+1555{int(time.time()) % 10000:04d}",
            )

            # Update user (should not create a new one)
            update_response = self.client.create_user(user_info_update)
            self.assertEqual(update_response.status, "success")
            # Note: created flag might be False for updates, depending on server implementation
            self.assertEqual(update_response.data.user.organization_user_id, user_id)
            self.assertEqual(update_response.data.user.full_name, "Updated Name")

        except ServerAPIError as e:
            self.fail(f"Server API error: {e}")

    def test_delete_user(self):
        """Test deleting a user through the server API."""
        # Create unique user ID for this test
        user_id = f"test_user_delete_{int(time.time())}"

        # First, create a user to delete
        user_info = UserInfo(
            user_id=user_id,
            full_name="User To Delete",
            email=f"delete_{int(time.time())}@example.com",
        )

        try:
            # Create user
            create_response = self.client.create_user(user_info)
            self.assertEqual(create_response.status, "success")

            # Now delete the user
            delete_response = self.client.delete_user(user_id)

            # Verify delete response
            self.assertEqual(delete_response.status, "success")
            self.assertIn("deleted", delete_response.message.lower())
            self.assertIsNotNone(delete_response.data.deleted_contact_id)

        except ServerAPIError as e:
            self.fail(f"Server API error: {e}")

    def test_delete_nonexistent_user(self):
        """Test deleting a user that doesn't exist."""
        # Use a user ID that definitely doesn't exist
        user_id = f"nonexistent_user_{int(time.time())}"

        try:
            # Attempt to delete non-existent user
            delete_response = self.client.delete_user(user_id)
            # This might succeed with a message indicating no user was found
            # or it might raise an error - both are valid depending on implementation

        except ServerAPIError as e:
            # If it raises an error, it should be a 404 or similar
            self.assertIn(str(e.status_code), ["404", "400"])

    def test_create_user_with_custom_expiry(self):
        """Test creating a user with custom token expiry."""
        # Create unique user ID for this test
        user_id = f"test_user_expiry_{int(time.time())}"

        user_info = UserInfo(
            user_id=user_id,
            full_name="Test User Expiry",
            email=f"expiry_{int(time.time())}@example.com",
        )

        # Use 1 hour expiry instead of default 24 hours
        expiry_seconds = 3600

        try:
            # Create user with custom expiry
            response = self.client.create_user(user_info, expiry_seconds=expiry_seconds)

            # Verify response
            self.assertEqual(response.status, "success")
            self.assertIsNotNone(response.data.token)

            # Verify token expiry is approximately correct (within 60 seconds tolerance)
            expected_expiry = int(time.time()) + expiry_seconds
            actual_expiry = response.data.token.expires_at
            self.assertLess(abs(actual_expiry - expected_expiry), 60)

        except ServerAPIError as e:
            self.fail(f"Server API error: {e}")

    def test_server_api_direct_calls(self):
        """Test making direct calls to server API endpoints."""
        # Skip this test if we don't have a server API URL
        if not self.config.get("api_base_url"):
            self.skipTest("Missing api_base_url in test config")

        # Create unique user ID for this test
        user_id = f"test_direct_api_{int(time.time())}"

        # Generate a token for authentication
        token_data = self.client.generate_token(user_id=user_id)
        token = token_data["token"]

        # Test the server create-user endpoint directly
        headers = {"Authorization": f"Bearer {token}"}
        create_url = f"{self.api_base_url}/api/v1/server/users/{user_id}"

        user_info_dict = {
            "userId": user_id,
            "fullName": "Direct API Test User",
            "email": f"direct_{int(time.time())}@example.com",
        }

        with httpx.Client() as http_client:
            # Test create user endpoint
            response = http_client.post(
                create_url,
                json={
                    "expiry_seconds": 86400,
                    "user_info": user_info_dict,
                    "device_info": {"deviceType": "test", "os": "integration-test"},
                },
                headers=headers,
            )

            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "success")
            self.assertIn("token", data["data"])
            self.assertIn("user", data["data"])

            # Test delete user endpoint
            delete_url = f"{self.api_base_url}/api/v1/server/users/{user_id}"
            delete_response = http_client.delete(delete_url, headers=headers)

            self.assertEqual(delete_response.status_code, 200)
            delete_data = delete_response.json()
            self.assertEqual(delete_data["status"], "success")


if __name__ == "__main__":
    unittest.main()
