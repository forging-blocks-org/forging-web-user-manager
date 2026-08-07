"""Request body for POST /users."""

from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    """Request body for POST /users."""

    name: str
    email: str
