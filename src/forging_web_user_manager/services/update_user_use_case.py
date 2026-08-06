"""Update a user's name and/or email."""

from forging_blocks.application import ApplicationServicePort
from forging_blocks.foundation import Ok, Err, Result

from forging_web_user_manager.models.email import Email
from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.requests.update_user_request import UpdateUserRequest
from forging_web_user_manager.errors.user_not_found_error import UserNotFoundError
from forging_web_user_manager.responses.user_response import UserResponse


class UpdateUserUseCase(ApplicationServicePort[UpdateUserRequest, Result[UserResponse, UserError]]):
    """Update a user's name and/or email."""

    def __init__(self, repo: InMemoryUserRepository) -> None:
        self._repo = repo

    async def execute(self, request: UpdateUserRequest) -> Result[UserResponse, UserError]:
        user = await self._repo.get_by_id(request.user_id)
        if user is None:
            return Err(UserNotFoundError.from_string(f"User {request.user_id} not found"))

        if request.name is not None:
            result = user.rename(request.name)
            if result.is_err:
                return Err(result.error)

        if request.email is not None:
            try:
                new_email = Email(request.email)
            except ValueError:
                return Err(UserError.from_string("Invalid email format"))
            user.update_email(new_email)

        await self._repo.save(user)
        return Ok(UserResponse.from_domain(user))
