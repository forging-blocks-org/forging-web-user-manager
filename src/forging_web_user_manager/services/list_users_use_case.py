"""List all users."""

from forging_blocks.application import ApplicationServicePort
from forging_blocks.foundation import Ok, Result

from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.responses.user_response import UserResponse


class ListUsersUseCase(ApplicationServicePort[None, Result[list[UserResponse], UserError]]):
    """List all users."""

    def __init__(self, repo: InMemoryUserRepository) -> None:
        self._repo = repo

    async def execute(self, request: None = None) -> Result[list[UserResponse], UserError]:
        users = await self._repo.list_all()
        return Ok([UserResponse.from_domain(u) for u in users])
