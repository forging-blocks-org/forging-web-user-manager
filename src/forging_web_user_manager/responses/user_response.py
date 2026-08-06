"""Response DTO for user endpoints."""

from dataclasses import dataclass

from forging_web_user_manager.models.user import User


@dataclass
class UserResponse:
    """Response DTO for user endpoints."""

    id: str
    name: str
    email: str

    @staticmethod
    def from_domain(user: User) -> "UserResponse":
        """Create a UserResponse from a domain User."""
        return UserResponse(
            id=user.id,  # type: ignore[reportArgumentType]
            name=user.name,
            email=user.email.value,
        )
