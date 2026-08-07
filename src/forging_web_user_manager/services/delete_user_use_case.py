"""Delete a user by ID."""

from forging_blocks.application import ApplicationServicePort
from forging_blocks.foundation import Ok, Err, Result
from forging_blocks.infrastructure import RepositoryNotFoundError

from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.requests.delete_user_request import DeleteUserRequest
from forging_web_user_manager.errors.user_not_found_error import UserNotFoundError


class DeleteUserUseCase(ApplicationServicePort[DeleteUserRequest, Result[None, UserError]]):
    """Delete a user by ID."""

    def __init__(self, repo: InMemoryUserRepository) -> None:
        self._repo = repo

    async def execute(self, request: DeleteUserRequest) -> Result[None, UserError]:
        try:
            await self._repo.delete_by_id(request.user_id)
        except RepositoryNotFoundError:
            return Err(UserNotFoundError.from_string(f"User {request.user_id} not found"))
        return Ok(None)
