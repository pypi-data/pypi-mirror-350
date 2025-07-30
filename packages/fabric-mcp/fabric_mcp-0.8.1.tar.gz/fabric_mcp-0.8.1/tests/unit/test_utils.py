"""Unit tests for the Log class in the fabric_mcp.utils module."""

import logging

import pytest

from fabric_mcp.utils import Log


def test_log_init_valid_level():
    """Test Log initialization with a valid log level."""
    log = Log("DEBUG")
    assert log.level_name == "DEBUG"
    assert log.level == logging.DEBUG
    assert isinstance(log.logger, logging.Logger)


def test_log_init_invalid_level():
    """Test Log initialization with an invalid log level."""
    with pytest.raises(KeyError) as excinfo:
        Log("INVALID")
    assert "Invalid log level: INVALID" in str(excinfo.value)


def test_log_level_name_property():
    """Test the level_name property."""
    log = Log("WARNING")
    assert log.level_name == "WARNING"


def test_log_level_property():
    """Test the level property."""
    log = Log("ERROR")
    assert log.level == logging.ERROR


def test_log_logger_property():
    """Test the logger property."""
    log = Log("INFO")
    assert isinstance(log.logger, logging.Logger)
    # Check if basicConfig was called (indirectly by checking handlers)
    # Note: This might be fragile depending on logging internals/setup
    assert logging.getLogger().hasHandlers()


def test_log_level_static_method_valid():
    """Test the log_level static method with valid levels."""
    assert Log.log_level("DEBUG") == logging.DEBUG
    assert Log.log_level("info") == logging.INFO  # Test case insensitivity if intended
    assert Log.log_level("WARNING") == logging.WARNING
    assert Log.log_level("ERROR") == logging.ERROR
    assert Log.log_level("CRITICAL") == logging.CRITICAL


def test_log_level_static_method_invalid():
    """Test the log_level static method with an invalid level."""
    with pytest.raises(KeyError) as excinfo:
        Log.log_level("invalid_level")
    assert "Invalid log level: invalid_level" in str(excinfo.value)


@pytest.fixture(autouse=True)
def reset_logging():
    """Fixture to reset logging configuration after each test."""
    logging.shutdown()
    # If basicConfig sets handlers on the root logger, remove them
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    yield
    logging.shutdown()
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
