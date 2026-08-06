# Architecture: forging-blocks + FastAPI

This document explains how `forging-blocks` and FastAPI are wired together in this project.

## Layering

The project follows hexagonal architecture with three layers, all in flat packages:

```
src/forging_web_user_manager/
├── models/       Domain layer — entities and value objects
├── errors/       Domain errors with built-in mixins
├── services/     Application layer — use cases
├── requests/     Application-layer request DTOs
├── responses/    Application-layer response DTOs
├── schemas/      Presentation layer — Pydantic HTTP models
├── routers.py    Presentation layer — FastAPI endpoints
├── main.py       Composition root — wires everything together
├── repository.py Infrastructure — in-memory persistence
├── std_lib_logger.py  Infrastructure — logging adapter
└── pipelined_use_case.py  Presentation — pipeline wrapper
```

Dependencies flow inward: `routers` → `services` → `models`. Infrastructure adapters
(`repository.py`, `std_lib_logger.py`) implement ports defined by `forging-blocks`.

## Domain layer (`models/`)

### Value Objects — `Email`

```python
from forging_blocks.domain.value_object import ValueObject

class Email(ValueObject[str]):
    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        if "@" not in value:
            raise ValueError("Invalid email format")
        object.__setattr__(self, "_value", value)
```

`ValueObject` provides auto-freeze, auto-hash, and auto-equality. The `__slots__` pattern
prevents attribute dict creation. Because `ValueObject` is frozen, you must use
`object.__setattr__` to set `_value` in `__init__`.

### Entities — `User`

```python
from forging_blocks.domain.entity import Entity

class User(Entity[str]):
    def __init__(self, name: str, email: Email) -> None:
        super().__init__(None)  # draft entity, no ID yet
        self.name = name
        self.email = email

    def rename(self, new_name: str) -> Result[Self, UserError]:
        if not new_name.strip():
            return Err(UserNameEmptyError.from_string("User name cannot be empty"))
        self.name = new_name
        return Ok(self)

    def assign_id(self) -> None:
        self._id = uuid4().hex
```

`Entity[TId]` carries an `entity_id` that starts as `None` (draft) and becomes immutable
once set to a non-None value. Domain methods return `Result[Ok, Err]` — no exceptions for
validation failures.

### Domain Errors — `errors/`

```python
from forging_blocks.foundation.error import Error
from forging_blocks.foundation.mixins import ValueErrorMixin

class UserError(Error[str]):
    """Base error for user operations."""

class UserNameEmptyError(ValueErrorMixin, UserError):
    """Raised when a user name is empty."""
```

Errors extend `Error[MetadataValueType]` and can mix in `ValueErrorMixin` or
`RuntimeErrorMixin` so they're catchable as built-in exception types:

```python
try:
    raise UserNameEmptyError.from_string("empty")
except ValueError:  # caught via ValueErrorMixin
    ...
```

## Application layer (`services/`)

Use cases implement `ApplicationServicePort[Request, Response]`:

```python
from forging_blocks.application import ApplicationServicePort

class CreateUserUseCase(ApplicationServicePort[CreateUserRequest, Result[UserResponse, UserError]]):
    def __init__(self, repo: InMemoryUserRepository) -> None:
        self._repo = repo

    async def execute(self, request: CreateUserRequest) -> Result[UserResponse, UserError]:
        email = Email(request.email)
        user = User(name=request.name, email=email)
        rename_result = user.rename(request.name)
        if rename_result.is_err:
            return Err(rename_result.error)
        user.assign_id()
        await self._repo.save(user)
        return Ok(UserResponse.from_domain(user))
```

Key patterns:

- **Dependency injection via constructor** — the repository is passed in, never imported.
- **`Result` return type** — errors are values, not exceptions. The router inspects
  `result.is_err` to decide the HTTP status code.
- **`async` throughout** — `ApplicationServicePort.execute` is async; repository methods
  are async too.

## Infrastructure layer

### Repository — `InMemoryUserRepository`

```python
from forging_blocks.infrastructure.in_memory_repository import InMemoryRepository

class InMemoryUserRepository(InMemoryRepository[User, str]):
    """In-memory user storage for development and testing."""
```

`InMemoryRepository` provides `save()`, `get_by_id()`, `list_all()`, and `delete_by_id()`
out of the box. No configuration needed.

### Logger — `StdLibLogger`

```python
from forging_blocks.application.ports.outbound.logger_port import LoggerPort

class StdLibLogger(LoggerPort):
    def __init__(self, name: str = "web_user_manager") -> None:
        self._logger = logging.getLogger(name)
```

Implements `LoggerPort` (a `forging-blocks` outbound port) by delegating to Python's
`logging` module. This is what the `Pipeline` middleware uses for logging.

## Presentation layer

### Pydantic schemas (`schemas/`)

FastAPI request/response models are plain Pydantic classes — separate from domain objects
and application DTOs:

```python
class UserCreateRequest(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
```

### Router (`routers.py`)

Each endpoint receives a use case via FastAPI's `Depends`:

```python
@router.post("", status_code=201, response_model=UserResponse)
async def create_user(
    body: UserCreateRequest,
    usecase: PipelinedUseCase[CreateUserDTO, Any] = Depends(_get_create_usecase),
) -> UserResponse:
    result = await usecase.execute(CreateUserDTO(name=body.name, email=body.email))
    if result.is_err:
        raise HTTPException(status_code=400, detail=str(result.error.message.value))
    return UserResponse.from_dto(result.value)
```

The dependency function is a stub that raises `NotImplementedError` — it's replaced at
startup via `dependency_overrides`.

### Pipeline middleware (`pipelined_use_case.py`)

Every use case is wrapped in a `forging-blocks` `Pipeline` with `LoggingMiddleware` and
`TimingMiddleware`:

```python
from forging_blocks.presentation.middleware.pipeline import Pipeline
from forging_blocks.presentation.builtin import LoggingMiddleware, TimingMiddleware

pipeline = Pipeline[CreateUserRequest, Result[UserResponse, UserError]](
    middlewares=[
        LoggingMiddleware[CreateUserRequest, Result[UserResponse, UserError]](logger=logger),
        TimingMiddleware[CreateUserRequest, Result[UserResponse, UserError]](logger=logger),
    ],
    handler=CreateUserUseCase(repo).execute,
)
wrapped = PipelinedUseCase(pipeline)
```

`PipelinedUseCase` is a thin wrapper that exposes the same `execute(request)` interface
the router expects, but routes the call through the middleware chain first. Each request
produces log output like:

```
[DEBUG] web_user_manager: Processing request: CreateUserRequest(name='Alice', ...)
[INFO]  web_user_manager: Request handled in 0.0001 seconds
[DEBUG] web_user_manager: Request processed, response: Ok(User(id=b64e4122...))
```

## Composition root (`main.py`)

`create_app()` wires everything together:

1. Creates infrastructure adapters (`InMemoryUserRepository`, `StdLibLogger`)
2. Creates use cases, injecting the repository
3. Wraps each use case in a `Pipeline` with logging + timing middleware
4. Creates the FastAPI app and overrides dependency stubs with real instances

```python
def create_app() -> FastAPI:
    repo = InMemoryUserRepository()
    logger = StdLibLogger()

    create_pipeline = Pipeline[...](middlewares=[...], handler=CreateUserUseCase(repo).execute)
    # ... repeat for each use case

    app = FastAPI(title="Web User Manager")
    app.dependency_overrides[_get_create_usecase] = lambda: PipelinedUseCase(create_pipeline)
    # ... repeat for each use case

    app.include_router(router)
    return app
```

No DI container — just plain functions and lambdas. FastAPI's `dependency_overrides` is
the only framework-specific wiring mechanism.

## Request flow

```
HTTP Request
  → FastAPI router (routers.py)
    → PipelinedUseCase.execute(request)
      → Pipeline
        → LoggingMiddleware (pre-processing log)
        → TimingMiddleware (start timer)
        → UseCase.execute(request)        ← application logic
        → TimingMiddleware (log elapsed)
        → LoggingMiddleware (post-processing log)
      → Result[Response, Error]
    → HTTPException or Response model
  → HTTP Response
```
