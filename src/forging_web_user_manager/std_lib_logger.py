"""Standard-library logging adapter implementing LoggerPort."""

import logging

from forging_blocks.application.ports.outbound.logger_port import LoggerPort


class StdLibLogger(LoggerPort):
    """Adapter that delegates to Python's standard ``logging`` module."""

    def __init__(self, name: str = "web_user_manager") -> None:
        self._logger = logging.getLogger(name)

    def debug(self, msg: str, *args: str) -> None:
        self._logger.debug(msg, *args)

    def info(self, msg: str, *args: str) -> None:
        self._logger.info(msg, *args)

    def warning(self, msg: str, *args: str) -> None:
        self._logger.warning(msg, *args)

    def error(self, msg: str, *args: str) -> None:
        self._logger.error(msg, *args)
