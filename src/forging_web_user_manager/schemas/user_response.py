"""Response body for user endpoints."""

from uuid import UUID

from pydantic import BaseModel

from forging_web_user_manager.responses.user_response import UserResponse as UserResponseDTO


class UserResponse(BaseModel):
    """Response body for user endpoints."""

    id: UUID
    name: str
    email: str

    @staticmethod
    def from_dto(dto: UserResponseDTO) -> "UserResponse":
        """Create a UserResponse from a response DTO."""
        return UserResponse(
            id=dto.id,
            name=dto.name,
            email=dto.email,
        )
