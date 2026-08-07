"""Tests for GetUserUseCase."""

from uuid import UUID

import pytest


from forging_web_user_manager.errors.user_not_found_error import UserNotFoundError
from forging_web_user_manager.models.email import Email
from forging_web_user_manager.models.user import User
from forging_web_user_manager.responses.user_response import UserResponse
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.requests.get_user_request import GetUserRequest
from forging_web_user_manager.services.get_user_use_case import GetUserUseCase


@pytest.fixture
def repo() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def use_case(repo: InMemoryUserRepository) -> GetUserUseCase:
    return GetUserUseCase(repo)


@pytest.mark.asyncio
async def test_get_existing_user_returns_ok_with_user(
    repo: InMemoryUserRepository,
    use_case: GetUserUseCase,
) -> None:
    user = User(name="Alice", email=Email("alice@example.com"))
    await repo.save(user)
    assert user.id is not None

    request = GetUserRequest(user_id=user.id)
    result = await use_case.execute(request)

    assert result.is_ok
    assert isinstance(result.value, UserResponse)
    assert result.value.id == user.id
    assert result.value.name == "Alice"


@pytest.mark.asyncio
async def test_get_non_existent_user_returns_err(
    use_case: GetUserUseCase,
) -> None:
    request = GetUserRequest(user_id=UUID("00000000-0000-7000-8000-000000000000"))

    result = await use_case.execute(request)

    assert result.is_err
    assert isinstance(result.error, UserNotFoundError)
    assert "00000000-0000-7000-8000-000000000000" in result.error.message.value
