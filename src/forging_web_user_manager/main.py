"""FastAPI application entry point."""

import logging
from typing import Any

from fastapi import FastAPI

from forging_blocks.foundation import Result
from forging_blocks.presentation.builtin import LoggingMiddleware, TimingMiddleware
from forging_blocks.presentation.middleware.pipeline import Pipeline

from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.pipelined_use_case import PipelinedUseCase
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.requests.create_user_request import CreateUserRequest
from forging_web_user_manager.requests.delete_user_request import DeleteUserRequest
from forging_web_user_manager.requests.get_user_request import GetUserRequest
from forging_web_user_manager.requests.update_user_request import UpdateUserRequest
from forging_web_user_manager.responses.user_response import UserResponse
from forging_web_user_manager.routers import (
    _get_create_usecase,
    _get_delete_usecase,
    _get_get_usecase,
    _get_list_usecase,
    _get_update_usecase,
    router,
)
from forging_web_user_manager.services.create_user_use_case import CreateUserUseCase
from forging_web_user_manager.services.delete_user_use_case import DeleteUserUseCase
from forging_web_user_manager.services.get_user_use_case import GetUserUseCase
from forging_web_user_manager.services.list_users_use_case import ListUsersUseCase
from forging_web_user_manager.services.update_user_use_case import UpdateUserUseCase
from forging_web_user_manager.std_lib_logger import StdLibLogger


def create_app() -> FastAPI:
    """Create and wire the FastAPI application."""
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    repo = InMemoryUserRepository()
    logger = StdLibLogger()

    create_pipeline = Pipeline[CreateUserRequest, Result[UserResponse, UserError]](
        middlewares=[
            LoggingMiddleware[CreateUserRequest, Result[UserResponse, UserError]](logger=logger),
            TimingMiddleware[CreateUserRequest, Result[UserResponse, UserError]](logger=logger),
        ],
        handler=CreateUserUseCase(repo).execute,
    )
    get_pipeline = Pipeline[GetUserRequest, Result[UserResponse, UserError]](
        middlewares=[
            LoggingMiddleware[GetUserRequest, Result[UserResponse, UserError]](logger=logger),
            TimingMiddleware[GetUserRequest, Result[UserResponse, UserError]](logger=logger),
        ],
        handler=GetUserUseCase(repo).execute,
    )
    list_pipeline = Pipeline[None, Result[list[UserResponse], UserError]](
        middlewares=[
            LoggingMiddleware[None, Result[list[UserResponse], UserError]](logger=logger),
            TimingMiddleware[None, Result[list[UserResponse], UserError]](logger=logger),
        ],
        handler=ListUsersUseCase(repo).execute,
    )
    update_pipeline = Pipeline[UpdateUserRequest, Result[UserResponse, UserError]](
        middlewares=[
            LoggingMiddleware[UpdateUserRequest, Result[UserResponse, UserError]](logger=logger),
            TimingMiddleware[UpdateUserRequest, Result[UserResponse, UserError]](logger=logger),
        ],
        handler=UpdateUserUseCase(repo).execute,
    )
    delete_pipeline = Pipeline[DeleteUserRequest, Any](
        middlewares=[
            LoggingMiddleware[DeleteUserRequest, Any](logger=logger),
            TimingMiddleware[DeleteUserRequest, Any](logger=logger),
        ],
        handler=DeleteUserUseCase(repo).execute,
    )

    app = FastAPI(title="Web User Manager")

    app.dependency_overrides[_get_create_usecase] = lambda: PipelinedUseCase(create_pipeline)
    app.dependency_overrides[_get_get_usecase] = lambda: PipelinedUseCase(get_pipeline)
    app.dependency_overrides[_get_list_usecase] = lambda: PipelinedUseCase(list_pipeline)
    app.dependency_overrides[_get_update_usecase] = lambda: PipelinedUseCase(update_pipeline)
    app.dependency_overrides[_get_delete_usecase] = lambda: PipelinedUseCase(delete_pipeline)

    app.include_router(router)
    return app


def main() -> None:
    """Entry point: start the uvicorn server."""
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
