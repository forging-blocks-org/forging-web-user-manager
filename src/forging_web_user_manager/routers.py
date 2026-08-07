"""FastAPI router with user CRUD endpoints."""

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from forging_web_user_manager.pipelined_use_case import PipelinedUseCase
from forging_web_user_manager.schemas.user_register_request import UserRegisterRequest
from forging_web_user_manager.schemas.user_response import UserResponse
from forging_web_user_manager.schemas.user_update_request import UserUpdateRequest
from forging_web_user_manager.requests.register_user_request import RegisterUserRequest as RegisterUserDTO
from forging_web_user_manager.requests.delete_user_request import DeleteUserRequest
from forging_web_user_manager.requests.get_user_request import GetUserRequest
from forging_web_user_manager.requests.update_user_request import UpdateUserRequest

router = APIRouter(prefix="/users", tags=["users"])


def _get_register_usecase() -> PipelinedUseCase[RegisterUserDTO, Any]:
    raise NotImplementedError("Wired at startup")


def _get_get_usecase() -> PipelinedUseCase[GetUserRequest, Any]:
    raise NotImplementedError("Wired at startup")


def _get_list_usecase() -> PipelinedUseCase[None, Any]:
    raise NotImplementedError("Wired at startup")


def _get_update_usecase() -> PipelinedUseCase[UpdateUserRequest, Any]:
    raise NotImplementedError("Wired at startup")


def _get_delete_usecase() -> PipelinedUseCase[DeleteUserRequest, Any]:
    raise NotImplementedError("Wired at startup")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    body: UserRegisterRequest,
    usecase: PipelinedUseCase[RegisterUserDTO, Any] = Depends(_get_register_usecase),
) -> UserResponse:
    """Register a new user."""
    result = await usecase.execute(RegisterUserDTO(name=body.name, email=body.email))
    if result.is_err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(result.error.message.value))
    return UserResponse.from_dto(result.value)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    usecase: PipelinedUseCase[GetUserRequest, Any] = Depends(_get_get_usecase),
) -> UserResponse:
    """Get a user by ID."""
    result = await usecase.execute(GetUserRequest(user_id=user_id))
    if result.is_err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(result.error.message.value))
    return UserResponse.from_dto(result.value)


@router.get("", response_model=list[UserResponse])
async def list_users(
    usecase: PipelinedUseCase[None, Any] = Depends(_get_list_usecase),
) -> list[UserResponse]:
    """List all users."""
    result = await usecase.execute()
    if result.is_err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(result.error.message.value))
    return [UserResponse.from_dto(u) for u in result.value]


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    body: UserUpdateRequest,
    usecase: PipelinedUseCase[UpdateUserRequest, Any] = Depends(_get_update_usecase),
) -> UserResponse:
    """Update a user's name and/or email."""
    result = await usecase.execute(UpdateUserRequest(user_id=user_id, name=body.name, email=body.email))
    if result.is_err:
        status_code_ = status.HTTP_404_NOT_FOUND if "not found" in str(result.error.message.value).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code_, detail=str(result.error.message.value))
    return UserResponse.from_dto(result.value)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    usecase: PipelinedUseCase[DeleteUserRequest, Any] = Depends(_get_delete_usecase),
) -> None:
    """Delete a user by ID."""
    result = await usecase.execute(DeleteUserRequest(user_id=user_id))
    if result.is_err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(result.error.message.value))
