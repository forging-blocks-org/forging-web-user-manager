FROM python:3.14-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_SYSTEM_PYTHON=1

COPY pyproject.toml ./
RUN uv sync --no-dev --no-install-project --frozen 2>/dev/null || uv sync --no-dev --no-install-project

COPY README.md ./
COPY src/ ./src/
RUN uv sync --no-dev --frozen 2>/dev/null || uv sync --no-dev

EXPOSE 8000

CMD ["uv", "run", "forging-web-user-manager"]
