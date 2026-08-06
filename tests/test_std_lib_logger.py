"""Tests for StdLibLogger adapter."""

import logging

import pytest

from forging_web_user_manager.std_lib_logger import StdLibLogger


@pytest.fixture
def logger() -> StdLibLogger:
    """Return a StdLibLogger with a test-specific logger name."""
    return StdLibLogger("test_logger")


def test_info_logs_at_info_level(logger: StdLibLogger, caplog: pytest.LogCaptureFixture):
    """info() emits a log record at INFO level."""
    caplog.set_level(logging.INFO, logger="test_logger")

    logger.info("hello info")

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelno == logging.INFO
    assert record.message == "hello info"


def test_debug_logs_at_debug_level(
    logger: StdLibLogger, caplog: pytest.LogCaptureFixture
):
    """debug() emits a log record at DEBUG level."""
    caplog.set_level(logging.DEBUG, logger="test_logger")

    logger.debug("hello debug")

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelno == logging.DEBUG
    assert record.message == "hello debug"


def test_warning_logs_at_warning_level(
    logger: StdLibLogger, caplog: pytest.LogCaptureFixture
):
    """warning() emits a log record at WARNING level."""
    caplog.set_level(logging.WARNING, logger="test_logger")

    logger.warning("hello warning")

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelno == logging.WARNING
    assert record.message == "hello warning"


def test_error_logs_at_error_level(
    logger: StdLibLogger, caplog: pytest.LogCaptureFixture
):
    """error() emits a log record at ERROR level."""
    caplog.set_level(logging.ERROR, logger="test_logger")

    logger.error("hello error")

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelno == logging.ERROR
    assert record.message == "hello error"
