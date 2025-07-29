# ContactsManager Python SDK

[![PyPI version](https://img.shields.io/pypi/v/contactsmanager.svg)](https://pypi.org/project/contactsmanager/)
[![Build Status](https://github.com/arpwal/contactsmanager-py/actions/workflows/python-package.yml/badge.svg)](https://github.com/arpwal/contactsmanager-py/actions/workflows/python-package.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/arpwal/contactsmanager-py)

A Python SDK for the ContactsManager API that handles user management, authentication, and token generation for [contactsmanager.io](https://www.contactsmanager.io) integration.

## Overview

The ContactsManager SDK enables developers to easily integrate social features into their applications. It provides secure user management and token generation, helping you build features like activity feeds, follow/unfollow functionality, and contact management while ensuring user data privacy and security.

## Installation

```bash
pip install contactsmanager
```

## Quick Start

```python
from contactsmanager import ContactsManagerClient
from contactsmanager.types import UserInfo, DeviceInfo

# Initialize the client
client = ContactsManagerClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    org_id="your_org_id"
)

# Create a user on the server and get a token
user_info = UserInfo(
    user_id="user123",
    full_name="John Doe",
    email="john@example.com",
    phone="+1234567890"  # Optional
)

device_info = DeviceInfo(
    device_type="mobile",
    os="iOS",
    app_version="1.0.0"
)

# Create user and get token in one call
response = client.create_user(user_info, device_info)

print(f"User created: {response.data.created}")
print(f"Token: {response.data.token.token}")
print(f"Expires at: {response.data.token.expires_at}")
print(f"User ID: {response.data.user.organization_user_id}")
```

## Core Features

### 1. User Management

Create or update users on the ContactsManager server:

```python
from contactsmanager.types import UserInfo, DeviceInfo

# Create user with email only
user_info = UserInfo(
    user_id="user123",
    full_name="John Doe",
    email="john@example.com"
)

response = client.create_user(user_info)

# Create user with phone only
user_info = UserInfo(
    user_id="user456",
    full_name="Jane Smith",
    phone="+1234567890"
)

response = client.create_user(user_info)

# Create user with both email and phone
user_info = UserInfo(
    user_id="user789",
    full_name="Bob Wilson",
    email="bob@example.com",
    phone="+1234567890",
    avatar_url="https://example.com/avatar.jpg",
    metadata={"role": "admin", "department": "engineering"}
)

response = client.create_user(user_info)
```

### 2. Delete Users

Remove users from the ContactsManager server:

```python
# Delete a user
response = client.delete_user("user123")

print(f"Status: {response.status}")
print(f"Message: {response.message}")
print(f"Deleted contact ID: {response.data.deleted_contact_id}")
```

### 3. Token Generation Only

Generate tokens without creating users (for existing users):

```python
# Generate a token for an existing user
token_response = client.generate_token(
    user_id="user123",
    device_info={
        "device_type": "mobile",
        "os": "iOS",
        "app_version": "1.0.0"
    }
)

print(f"Token: {token_response['token']}")
print(f"Expires at: {token_response['expires_at']}")
```

### 4. Custom Token Expiration

Control how long tokens remain valid:

```python
# Create user with 1-hour token expiration
response = client.create_user(
    user_info,
    device_info,
    expiry_seconds=3600  # 1 hour instead of default 24 hours
)

# Generate token with custom expiration
token_response = client.generate_token(
    user_id="user123",
    expiration_seconds=7200  # 2 hours
)
```

## Implementation Flow

Here's how to integrate ContactsManager into your application:

### Server-Side Implementation

```python
from contactsmanager import ContactsManagerClient
from contactsmanager.types import UserInfo, DeviceInfo

# 1. Initialize the client (do this once, typically in your app setup)
client = ContactsManagerClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    org_id="your_org_id"
)

# 2. When a user signs up or logs in, create/update them on ContactsManager
def handle_user_login(user_data):
    user_info = UserInfo(
        user_id=user_data["id"],  # Your internal user ID
        full_name=user_data["name"],
        email=user_data.get("email"),
        phone=user_data.get("phone")
    )

    device_info = DeviceInfo(
        device_type=user_data.get("device_type", "web"),
        os=user_data.get("os"),
        app_version=user_data.get("app_version")
    )

    # Create/update user and get token
    response = client.create_user(user_info, device_info)

    # Return the token to your client app
    return {
        "contactsmanager_token": response.data.token.token,
        "expires_at": response.data.token.expires_at,
        "user_created": response.data.created
    }

# 3. When a user deletes their account, remove them from ContactsManager
def handle_user_deletion(user_id):
    response = client.delete_user(user_id)
    return response.status == "success"
```

### Client-Side Usage

Once you have the token from your server, use it in your client application:

```javascript
// In your mobile app or web frontend
const contactsManagerToken = "token_from_your_server";

// Use this token with ContactsManager client SDKs
// to access social features, contact sync, etc.
```

## Data Types

### UserInfo

```python
from contactsmanager.types import UserInfo

user_info = UserInfo(
    user_id="string",        # Required: Your internal user ID
    full_name="string",      # Required: User's display name
    email="string",          # Optional: User's email
    phone="string",          # Optional: User's phone number
    avatar_url="string",     # Optional: URL to user's avatar image
    metadata={}              # Optional: Additional user data
)
```

### DeviceInfo

```python
from contactsmanager.types import DeviceInfo

device_info = DeviceInfo(
    device_type="string",    # Optional: "mobile", "web", "desktop"
    os="string",             # Optional: "iOS", "Android", "Windows"
    app_version="string",    # Optional: Your app version
    locale="string",         # Optional: User's locale
    timezone="string"        # Optional: User's timezone
)
```

## Error Handling

```python
from contactsmanager.server_api import ServerAPIError

try:
    response = client.create_user(user_info)
    print("User created successfully!")
except ServerAPIError as e:
    print(f"Server error: {e}")
    print(f"Status code: {e.status_code}")
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Webhook Verification

Verify webhooks from ContactsManager:

```python
# Set your webhook secret (get this from ContactsManager dashboard)
client.set_webhook_secret("your_webhook_secret")

# In your webhook handler
def handle_webhook(request):
    payload = request.get_json()
    signature = request.headers.get('X-ContactsManager-Signature')

    if client.verify_webhook_signature(payload, signature):
        # Process the webhook
        print("Webhook verified!")
        return {"status": "success"}
    else:
        print("Invalid webhook signature")
        return {"error": "Invalid signature"}, 401
```

## Requirements

- Python 3.8+
- PyJWT>=2.0.0
- httpx>=0.24.0

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/arpwal/contactsmanager-py.git
cd contactsmanager-py

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Running Integration Tests

Integration tests validate the SDK against real-world scenarios, including server-side API functionality.

#### Local Setup

1. Create a `.env` file with your test configuration:

   ```bash
   # Copy the template file
   cp env.template .env

   # Edit the .env file with your credentials
   # The configuration is a JSON string in the TEST_CONFIG variable
   TEST_CONFIG='{"api_key":"your_api_key","api_secret":"your_api_secret","org_id":"your_org_id","api_base_url":"https://api.contactsmanager.io"}'
   ```

2. Run the integration tests:
   ```bash
   ./run_integration_tests.sh
   ```

### Releasing new versions

The SDK uses an automated process for releases:

1. Update the version in `contactsmanager/__init__.py` using the provided script:

   ```bash
   ./bump_version.sh 0.1.1
   ```

2. Commit and push the change to the main branch:

   ```bash
   git add contactsmanager/__init__.py
   git commit -m "Bump version to 0.1.1"
   git push origin main
   ```

3. The GitHub Actions workflow will:
   - Run all tests across multiple Python versions
   - Run integration tests
   - Create a new GitHub release with the version tag
   - Build and publish the package to PyPI

## License

MIT License

## About ContactsManager.io

[ContactsManager.io](https://www.contactsmanager.io) provides a platform for app developers to integrate social features into their applications. Our SDK ensures that contact information stays with users only, with multi-layer encryption and military-grade security to prevent spam and data misuse.

For more information and documentation, visit [contactsmanager.io](https://www.contactsmanager.io).
