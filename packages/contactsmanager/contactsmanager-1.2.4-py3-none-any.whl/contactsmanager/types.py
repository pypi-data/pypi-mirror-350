"""Type definitions for ContactsManager SDK."""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class UserInfo:
    """User information structure."""

    user_id: str  # Required field
    full_name: str  # Required field, cannot be empty
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Validate the UserInfo after initialization."""
        # Validate user_id
        if (
            not self.user_id
            or not isinstance(self.user_id, str)
            or not self.user_id.strip()
        ):
            raise ValueError("user_id is required and must be a non-empty string")

        # Validate full_name
        if (
            not self.full_name
            or not isinstance(self.full_name, str)
            or not self.full_name.strip()
        ):
            raise ValueError("full_name is required and must be a non-empty string")

        # Validate that at least one of email or phone is provided
        if not self.email and not self.phone:
            raise ValueError("At least one of email or phone must be provided")

        # Validate email format if provided
        if self.email and not isinstance(self.email, str):
            raise ValueError("email must be a string")

        # Validate phone format if provided
        if self.phone and not isinstance(self.phone, str):
            raise ValueError("phone must be a string")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format expected by the API."""
        result = {
            "userId": self.user_id,
            "fullName": self.full_name,
        }

        if self.email is not None:
            result["email"] = self.email
        if self.phone is not None:
            result["phone"] = self.phone
        if self.avatar_url is not None:
            result["avatarUrl"] = self.avatar_url
        if self.metadata is not None:
            result["metadata"] = self.metadata

        return result


@dataclass
class DeviceInfo:
    """Device information structure."""

    device_type: Optional[str] = None
    os: Optional[str] = None
    app_version: Optional[str] = None
    locale: Optional[str] = None
    timezone: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format expected by the API."""
        result = {}
        if self.device_type is not None:
            result["deviceType"] = self.device_type
        if self.os is not None:
            result["os"] = self.os
        if self.app_version is not None:
            result["appVersion"] = self.app_version
        if self.locale is not None:
            result["locale"] = self.locale
        if self.timezone is not None:
            result["timezone"] = self.timezone

        # Add any additional info
        if self.additional_info:
            result.update(self.additional_info)

        return result


@dataclass
class TokenData:
    """Token data structure."""

    token: str
    expires_at: int


@dataclass
class CMUser:
    """ContactsManager User structure (user-facing representation of canonical organization contact)."""

    id: str
    organization_id: str
    organization_user_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    contact_metadata: Optional[Dict[str, Any]] = None
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class CreateUserData:
    """Data structure for create user response."""

    token: TokenData
    user: CMUser
    created: bool


@dataclass
class CreateUserResponse:
    """Response structure for create user endpoint."""

    status: str
    data: CreateUserData

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreateUserResponse":
        """Create instance from API response dictionary."""
        token_data = TokenData(
            token=data["data"]["token"]["token"],
            expires_at=data["data"]["token"]["expires_at"],
        )

        user_data = data["data"]["user"]
        user = CMUser(
            id=user_data["id"],
            organization_id=user_data["organization_id"],
            organization_user_id=user_data.get("organization_user_id"),
            email=user_data.get("email"),
            phone=user_data.get("phone"),
            full_name=user_data.get("full_name"),
            avatar_url=user_data.get("avatar_url"),
            contact_metadata=user_data.get("contact_metadata"),
            is_active=user_data.get("is_active", True),
            created_at=user_data.get("created_at"),
            updated_at=user_data.get("updated_at"),
        )

        create_data = CreateUserData(
            token=token_data, user=user, created=data["data"]["created"]
        )

        return cls(status=data["status"], data=create_data)


@dataclass
class DeleteUserData:
    """Data structure for delete user response."""

    deleted_contact_id: str


@dataclass
class DeleteUserResponse:
    """Response structure for delete user endpoint."""

    status: str
    message: str
    data: DeleteUserData

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeleteUserResponse":
        """Create instance from API response dictionary."""
        delete_data = DeleteUserData(
            deleted_contact_id=data["data"]["deleted_contact_id"]
        )

        return cls(status=data["status"], message=data["message"], data=delete_data)
