# forging-web-user-manager

Example CRUD user manager built with [forging-blocks](https://github.com/forging-blocks-org/forging-blocks)
and FastAPI, demonstrating domain modeling, hexagonal architecture, and middleware pipelines.

## Quick start

```bash
# Install dependencies
uv sync

# Run the server
uv run forging-web-user-manager

# Or directly
uv run python -m uvicorn forging_web_user_manager.main:create_app --reload
```

Server starts at `http://0.0.0.0:8000`. Interactive docs at `http://0.0.0.0:8000/docs`.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/users` | Create a user |
| GET | `/users` | List all users |
| GET | `/users/{id}` | Get user by ID |
| PUT | `/users/{id}` | Update user name/email |
| DELETE | `/users/{id}` | Delete user |

## Run tests

```bash
uv run pytest tests/ -v
```

## Run with Docker or Podman

```bash
# Docker
docker compose up --build

# Podman (requires podman-compose)
pip install podman-compose
podman-compose up --build
```

Server starts at `http://localhost:8000`. The container includes a healthcheck
on `/users` and restarts automatically unless stopped.

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for how forging-blocks and FastAPI are wired together.
