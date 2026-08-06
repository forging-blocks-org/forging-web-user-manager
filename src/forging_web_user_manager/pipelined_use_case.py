"""Wraps a use case with a middleware pipeline so callers invoke
``pipeline.execute(request)`` transparently through the same
``execute`` method.
"""

from forging_blocks.presentation.middleware.pipeline import Pipeline


class PipelinedUseCase[RequestType, ResponseType]:
    """Wraps a use case with a middleware pipeline.

    The router calls ``execute(request)`` as before, but the call
    flows through the pipeline's middleware chain before reaching
    the use case.
    """

    def __init__(self, pipeline: Pipeline[RequestType, ResponseType]) -> None:
        self._pipeline = pipeline

    async def execute(self, request: RequestType = None) -> ResponseType:
        """Execute the request through the pipeline."""
        return await self._pipeline.execute(request)
