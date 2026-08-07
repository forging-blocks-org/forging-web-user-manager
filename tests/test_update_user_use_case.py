"""Tests for UpdateUserUseCase."""

from uuid import UUID

import pytest


from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.errors.user_name_empty_error import UserNameEmptyError
from forging_web_user_manager.errors.user_not_found_error import UserNotFoundError
from forging_web_user_manager.models.email import Email
from forging_web_user_manager.models.user import User
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.requests.update_user_request import UpdateUserRequest
from forging_web_user_manager.responses.user_response import UserResponse
from forging_web_user_manager.services.update_user_use_case import UpdateUserUseCase


@pytest.fixture
def repo() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def use_case(repo: InMemoryUserRepository) -> UpdateUserUseCase:
    return UpdateUserUseCase(repo)


async def _create_and_save_user(
    repo: InMemoryUserRepository, name: str = "Alice", email: str = "alice@example.com"
) -> User:
    user = User(name=name, email=Email(email))
    await repo.save(user)
    return user


@pytest.mark.asyncio
async def test_update_existing_user_name_returns_ok_with_updated_user(
    repo: InMemoryUserRepository,
    use_case: UpdateUserUseCase,
) -> None:
    user = await _create_and_save_user(repo)
    assert user.id is not None

    request = UpdateUserRequest(user_id=user.id, name="Alice Updated")
    result = await use_case.execute(request)

    assert result.is_ok
    updated = result.value
    assert isinstance(updated, UserResponse)
    assert updated.name == "Alice Updated"
    assert updated.email == "alice@example.com"


@pytest.mark.asyncio
async def test_update_existing_user_email_returns_ok_with_updated_user(
    repo: InMemoryUserRepository,
    use_case: UpdateUserUseCase,
) -> None:
    user = await _create_and_save_user(repo)
    assert user.id is not None

    request = UpdateUserRequest(user_id=user.id, email="alice.new@example.com")
    result = await use_case.execute(request)

    assert result.is_ok
    updated = result.value
    assert isinstance(updated, UserResponse)
    assert updated.name == "Alice"
    assert updated.email == "alice.new@example.com"


@pytest.mark.asyncio
async def test_update_non_existent_user_returns_err(
    use_case: UpdateUserUseCase,
) -> None:
    request = UpdateUserRequest(user_id=UUID("00000000-0000-7000-8000-000000000000"), name="New Name")

    result = await use_case.execute(request)

    assert result.is_err
    assert isinstance(result.error, UserNotFoundError)
    assert "00000000-0000-7000-8000-000000000000" in result.error.message.value


@pytest.mark.asyncio
async def test_update_with_empty_name_returns_err(
    repo: InMemoryUserRepository,
    use_case: UpdateUserUseCase,
) -> None:
    user = await _create_and_save_user(repo)
    assert user.id is not None

    request = UpdateUserRequest(user_id=user.id, name="")
    result = await use_case.execute(request)

    assert result.is_err
    assert isinstance(result.error, UserNameEmptyError)
    assert result.error.message.value == "User name cannot be empty"


@pytest.mark.asyncio
async def test_update_with_invalid_email_returns_err(
    repo: InMemoryUserRepository,
    use_case: UpdateUserUseCase,
) -> None:
    user = await _create_and_save_user(repo)
    assert user.id is not None

    request = UpdateUserRequest(user_id=user.id, email="bademail")
    result = await use_case.execute(request)

    assert result.is_err
    assert isinstance(result.error, UserError)
    assert result.error.message.value == "Invalid email format"
