"""Retrieve a user by ID."""

from forging_blocks.application import ApplicationServicePort
from forging_blocks.foundation import Ok, Err, Result

from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.requests.get_user_request import GetUserRequest
from forging_web_user_manager.errors.user_not_found_error import UserNotFoundError
from forging_web_user_manager.responses.user_response import UserResponse


class GetUserUseCase(ApplicationServicePort[GetUserRequest, Result[UserResponse, UserError]]):
    """Retrieve a user by ID."""

    def __init__(self, repo: InMemoryUserRepository) -> None:
        self._repo = repo

    async def execute(self, request: GetUserRequest) -> Result[UserResponse, UserError]:
        user = await self._repo.get_by_id(request.user_id)
        if user is None:
            return Err(UserNotFoundError.from_string(f"User {request.user_id} not found"))
        return Ok(UserResponse.from_domain(user))
