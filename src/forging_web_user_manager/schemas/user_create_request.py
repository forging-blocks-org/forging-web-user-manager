"""Request body for POST /users."""

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    """Request body for POST /users."""

    name: str
    email: str
