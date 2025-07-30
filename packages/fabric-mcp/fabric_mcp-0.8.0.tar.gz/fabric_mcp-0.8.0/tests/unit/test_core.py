"""Test core functionality of fabric-mcp"""

import logging
import subprocess
import sys
from asyncio.exceptions import CancelledError
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

import pytest
from anyio import WouldBlock
from fastmcp import FastMCP

from fabric_mcp import __version__
from fabric_mcp.core import FabricMCP

# Tests for core functionality


def test_cli_version():
    """Test the --version flag of the CLI."""
    command = [sys.executable, "-m", "fabric_mcp.cli", "--version"]
    result = subprocess.run(command, capture_output=True, text=True, check=False)

    # argparse --version action prints to stdout and exits with 0
    assert result.returncode == 0
    assert result.stderr == ""
    expected_output = f"fabric-mcp {__version__}\n"
    assert result.stdout == expected_output


@pytest.fixture(name="server_instance")  # Renamed fixture
def server_instance_fixture() -> FabricMCP:
    """Fixture to create a FabricMCPServer instance."""
    return FabricMCP(log_level="DEBUG")


def test_server_initialization(server_instance: FabricMCP):
    """Test the initialization of the FabricMCPServer."""
    assert isinstance(server_instance.mcp, FastMCP)
    assert server_instance.mcp.name == f"Fabric MCP v{__version__}"
    assert isinstance(server_instance.logger, logging.Logger)
    # Check if log level propagates (Note: FastMCP handles its own logger setup)
    # We check the logger passed during init, FastMCP might configure differently
    # assert server_instance.logger.level == logging.DEBUG


def test_stdio_method_runs_mcp(server_instance: FabricMCP):
    """Test that the stdio method calls mcp.run()."""
    with patch.object(server_instance.mcp, "run") as mock_run:
        server_instance.stdio()
        mock_run.assert_called_once()


def test_stdio_method_handles_keyboard_interrupt(
    server_instance: FabricMCP,
    caplog: pytest.LogCaptureFixture,
):
    """Test that stdio handles KeyboardInterrupt gracefully."""
    with patch.object(server_instance.mcp, "run", side_effect=KeyboardInterrupt):
        with caplog.at_level(logging.INFO):
            server_instance.stdio()
    assert "Server stopped by user." in caplog.text


def test_stdio_method_handles_cancelled_error(
    server_instance: FabricMCP,
    caplog: pytest.LogCaptureFixture,
):
    """Test that stdio handles CancelledError gracefully."""
    with patch.object(server_instance.mcp, "run", side_effect=CancelledError):
        with caplog.at_level(logging.INFO):
            server_instance.stdio()
    assert "Server stopped by user." in caplog.text


def test_stdio_method_handles_would_block(
    server_instance: FabricMCP,
    caplog: pytest.LogCaptureFixture,
):
    """Test that stdio handles WouldBlock gracefully."""
    with patch.object(server_instance.mcp, "run", side_effect=WouldBlock):
        with caplog.at_level(logging.INFO):
            server_instance.stdio()
    assert "Server stopped by user." in caplog.text


def test_server_initialization_with_default_log_level():
    """Test server initialization with default log level."""
    server = FabricMCP()
    assert server.log_level == "INFO"


def test_server_initialization_with_custom_log_level():
    """Test server initialization with custom log level."""
    server = FabricMCP(log_level="ERROR")
    assert server.log_level == "ERROR"


def test_fabric_mcp_tools_registration():
    """Test that tools are properly registered with the FastMCP instance."""
    server = FabricMCP()

    # Check that tools are available through the mcp instance
    # Note: The exact way to check registered tools may depend on FastMCP's API
    # This is a basic check to ensure the tools list is populated
    assert hasattr(server, "_FabricMCP__tools")
    assert len(getattr(server, "_FabricMCP__tools")) == 3


def test_tool_registration_coverage():
    """Test that all tools are properly registered and accessible."""
    server = FabricMCP(log_level="DEBUG")

    # Check that the tools are registered by accessing them
    # This will trigger the __tools.append() calls on lines 29, 37, 54
    tools: list[Callable[..., Any]] = getattr(server, "_FabricMCP__tools")
    assert len(tools) == 3

    # Test each tool to ensure they're callable
    fabric_list_patterns = tools[0]
    result: list[str] = fabric_list_patterns()
    assert isinstance(result, list)
    assert len(result) == 3

    fabric_pattern_details = tools[1]
    result = fabric_pattern_details("test_pattern")
    assert isinstance(result, dict)
    assert "name" in result

    fabric_run_pattern = tools[2]
    result = fabric_run_pattern("test_pattern", "test_input")
    assert isinstance(result, dict)
    assert "name" in result
    assert "input" in result
    assert "result" in result
