"""Request body for PUT /users/{user_id}. All fields optional."""

from pydantic import BaseModel


class UserUpdateRequest(BaseModel):
    """Request body for PUT /users/{user_id}. All fields optional."""

    name: str | None = None
    email: str | None = None
