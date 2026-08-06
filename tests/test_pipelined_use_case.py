"""Tests for PipelinedUseCase — delegates to pipeline and returns result."""

import pytest

from forging_blocks.presentation.middleware.pipeline import Pipeline

from forging_web_user_manager.pipelined_use_case import PipelinedUseCase


@pytest.mark.asyncio
async def test_execute_delegates_to_pipeline_and_returns_result():
    """PipelinedUseCase.execute() should delegate to the pipeline and return its result."""

    async def handler(request: str) -> str:
        return f"handled: {request}"

    pipeline = Pipeline[str, str](middlewares=[], handler=handler)
    use_case = PipelinedUseCase(pipeline)

    result = await use_case.execute("hello")

    assert result == "handled: hello"


@pytest.mark.asyncio
async def test_execute_with_none_request():
    """PipelinedUseCase.execute() should work with None as request."""

    async def handler(request: None) -> int:
        return 42

    pipeline = Pipeline[None, int](middlewares=[], handler=handler)
    use_case = PipelinedUseCase(pipeline)

    result = await use_case.execute(None)

    assert result == 42


@pytest.mark.asyncio
async def test_execute_with_no_argument_uses_default():
    """PipelinedUseCase.execute() called with no argument should pass None as default."""

    async def handler(request: None) -> str:
        return "no-request"

    pipeline = Pipeline[None, str](middlewares=[], handler=handler)
    use_case = PipelinedUseCase(pipeline)

    result = await use_case.execute(None)

    assert result == "no-request"
