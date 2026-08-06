"""Tests for DeleteUserUseCase."""

from typing import cast

import pytest


from forging_web_user_manager.errors.user_not_found_error import UserNotFoundError
from forging_web_user_manager.models.email import Email
from forging_web_user_manager.models.user import User
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.requests.delete_user_request import DeleteUserRequest
from forging_web_user_manager.services.delete_user_use_case import DeleteUserUseCase


@pytest.fixture
def repo() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def use_case(repo: InMemoryUserRepository) -> DeleteUserUseCase:
    return DeleteUserUseCase(repo)


@pytest.mark.asyncio
async def test_delete_existing_user_returns_ok_none(
    repo: InMemoryUserRepository,
    use_case: DeleteUserUseCase,
) -> None:
    user = User(name="Alice", email=Email("alice@example.com"))
    user.assign_id()
    await repo.save(user)

    request = DeleteUserRequest(user_id=cast(str, user.id))
    result = await use_case.execute(request)

    assert result.is_ok
    assert result.value is None


@pytest.mark.asyncio
async def test_delete_non_existent_user_returns_err(
    use_case: DeleteUserUseCase,
) -> None:
    request = DeleteUserRequest(user_id="nonexistent")

    result = await use_case.execute(request)

    assert result.is_err
    assert isinstance(result.error, UserNotFoundError)
    assert "nonexistent" in result.error.message.value


@pytest.mark.asyncio
async def test_deleted_user_is_no_longer_retrievable(
    repo: InMemoryUserRepository,
    use_case: DeleteUserUseCase,
) -> None:
    user = User(name="Alice", email=Email("alice@example.com"))
    user.assign_id()
    await repo.save(user)

    delete_request = DeleteUserRequest(user_id=cast(str, user.id))
    await use_case.execute(delete_request)

    retrieved = await repo.get_by_id(cast(str, user.id))
    assert retrieved is None
