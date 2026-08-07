"""Response DTO for user endpoints."""

from dataclasses import dataclass
from uuid import UUID

from forging_web_user_manager.models.user import User


@dataclass
class UserResponse:
    """Response DTO for user endpoints."""

    id: UUID
    name: str
    email: str

    @staticmethod
    def from_domain(user: User) -> "UserResponse":
        """Create a UserResponse from a domain User."""
        assert user.id is not None
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email.value,
        )
