"""Create a new user with the given name and email."""

from forging_blocks.application import ApplicationServicePort
from forging_blocks.foundation import Ok, Err, Result

from forging_web_user_manager.models.email import Email
from forging_web_user_manager.models.user import User
from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.requests.create_user_request import CreateUserRequest
from forging_web_user_manager.responses.user_response import UserResponse


class CreateUserUseCase(ApplicationServicePort[CreateUserRequest, Result[UserResponse, UserError]]):
    """Create a new user with the given name and email."""

    def __init__(self, repo: InMemoryUserRepository) -> None:
        self._repo = repo

    async def execute(self, request: CreateUserRequest) -> Result[UserResponse, UserError]:
        try:
            email = Email(request.email)
        except ValueError:
            return Err(UserError.from_string("Invalid email format"))

        user = User(name=request.name, email=email)
        rename_result = user.rename(request.name)
        if rename_result.is_err:
            return Err(rename_result.error)

        user.assign_id()
        await self._repo.save(user)
        return Ok(UserResponse.from_domain(user))
