"""Server API configuration for ContactsManager SDK."""

# Server API base URL
SERVER_BASE_URL = "https://api.contactsmanager.io"

# Server API endpoints
SERVER_ENDPOINTS = {
    "create_user": "/api/v1/server/users/{uid}",
    "delete_user": "/api/v1/server/users/{uid}",
}


def get_server_endpoint(endpoint_name: str, **kwargs) -> str:
    """
    Get the full server endpoint URL.

    Args:
        endpoint_name: Name of the endpoint from SERVER_ENDPOINTS
        **kwargs: URL parameters to format into the endpoint

    Returns:
        Full URL for the endpoint
    """
    if endpoint_name not in SERVER_ENDPOINTS:
        raise ValueError(f"Unknown endpoint: {endpoint_name}")

    endpoint_path = SERVER_ENDPOINTS[endpoint_name].format(**kwargs)
    return f"{SERVER_BASE_URL}{endpoint_path}"
