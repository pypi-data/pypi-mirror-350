"""Server API implementation for ContactsManager SDK."""

import requests
from typing import Dict, Any, Optional
from .server_config import get_server_endpoint
from .types import UserInfo, DeviceInfo, CreateUserResponse, DeleteUserResponse


class ServerAPIError(Exception):
    """Exception raised for server API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class ServerAPI:
    """Server API client for making requests to ContactsManager server endpoints."""

    def __init__(self, token: str):
        """
        Initialize the server API client.

        Args:
            token: JWT token for authentication
        """
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def create_user(
        self,
        uid: str,
        user_info: UserInfo,
        device_info: Optional[DeviceInfo] = None,
        expiry_seconds: int = 86400,
    ) -> CreateUserResponse:
        """
        Create or update a user on the server.

        Args:
            uid: Unique user identifier
            user_info: User information (UserInfo object) - required
            device_info: Optional device information (DeviceInfo object)
            expiry_seconds: Token validity in seconds (default: 24 hours)

        Returns:
            CreateUserResponse containing the response data with token and user information

        Raises:
            ServerAPIError: If the API request fails
        """
        url = get_server_endpoint("create_user", uid=uid)

        payload = {
            "expiry_seconds": expiry_seconds,
            "user_info": user_info.to_dict(),
        }

        if device_info is not None:
            payload["device_info"] = device_info.to_dict()

        try:
            response = requests.post(
                url, json=payload, headers=self.headers, timeout=30
            )

            if response.status_code == 200:
                response_data = response.json()
                return CreateUserResponse.from_dict(response_data)
            else:
                error_data = None
                try:
                    error_data = response.json()
                except:
                    pass

                raise ServerAPIError(
                    f"Failed to create user: {response.status_code}",
                    status_code=response.status_code,
                    response_data=error_data,
                )

        except requests.RequestException as e:
            raise ServerAPIError(f"Network error while creating user: {str(e)}")

    def delete_user(self, uid: str) -> DeleteUserResponse:
        """
        Delete a user from the server.

        Args:
            uid: Unique user identifier

        Returns:
            DeleteUserResponse containing the response data with deletion confirmation

        Raises:
            ServerAPIError: If the API request fails
        """
        url = get_server_endpoint("delete_user", uid=uid)

        try:
            response = requests.delete(url, headers=self.headers, timeout=30)

            if response.status_code == 200:
                response_data = response.json()
                return DeleteUserResponse.from_dict(response_data)
            else:
                error_data = None
                try:
                    error_data = response.json()
                except:
                    pass

                raise ServerAPIError(
                    f"Failed to delete user: {response.status_code}",
                    status_code=response.status_code,
                    response_data=error_data,
                )

        except requests.RequestException as e:
            raise ServerAPIError(f"Network error while deleting user: {str(e)}")
