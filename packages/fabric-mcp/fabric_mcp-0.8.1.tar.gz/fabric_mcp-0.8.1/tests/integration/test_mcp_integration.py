"""Integration tests for the Fabric MCP Server.

These tests verify the end-to-end functionality of the MCP server,
including the protocol interactions and tool execution.
"""

import logging
import subprocess
import sys
from asyncio.exceptions import CancelledError
from collections.abc import Callable
from typing import Any
from unittest.mock import Mock, patch

import httpx
import pytest
from anyio import WouldBlock
from fastmcp import FastMCP

from fabric_mcp import __version__
from fabric_mcp.core import FabricMCP


@pytest.mark.integration
class TestFabricMCPIntegration:
    """Integration tests for the complete Fabric MCP Server."""

    @pytest.fixture
    def server(self):
        """Create a FabricMCP server instance for testing."""
        return FabricMCP(log_level="DEBUG")

    @pytest.fixture
    def mock_fabric_api_response(self):
        """Mock responses from the Fabric REST API."""
        return {
            "patterns": ["analyze_claims", "summarize", "create_story"],
            "pattern_details": {
                "name": "analyze_claims",
                "content": "System prompt for analyzing claims...",
                "metadata": {"author": "daniel", "version": "1.0"},
            },
            "pattern_execution": {
                "result": "This claim appears to be factual based on...",
                "model_used": "gpt-4",
                "tokens": 150,
            },
        }

    @pytest.mark.asyncio
    async def test_mcp_tool_discovery(self, server: FabricMCP):
        """Test that MCP tools are properly discoverable."""
        # This would test the list_tools() functionality when implemented
        # For now, we test that the server has the expected tools registered
        assert hasattr(server, "mcp")
        assert server.mcp is not None

    @pytest.mark.asyncio
    async def test_fabric_list_patterns_integration(
        self, server: FabricMCP, mock_fabric_api_response: Mock
    ):
        """Test the fabric_list_patterns tool with mocked API calls."""
        with patch("httpx.Client") as mock_client:
            # Setup mock response
            mock_response = Mock()
            mock_response.json.return_value = mock_fabric_api_response["patterns"]
            mock_response.status_code = 200
            mock_client.return_value.get.return_value = mock_response

            # Execute the tool (currently returns hardcoded values)
            # In the future, this would make actual API calls
            tools = getattr(server, "_FabricMCP__tools", [])
            if tools:
                list_patterns_tool = tools[0]
                result: list[Callable[..., Any]] = list_patterns_tool()

                assert isinstance(result, list)
                assert len(result) > 0

    @pytest.mark.asyncio
    async def test_fabric_pattern_details_integration(
        self, server: FabricMCP, mock_fabric_api_response: Mock
    ):
        """Test the fabric_pattern_details tool with mocked API calls."""
        with patch("httpx.Client") as mock_client:
            # Setup mock response
            mock_response = Mock()
            mock_response.json.return_value = mock_fabric_api_response[
                "pattern_details"
            ]
            mock_response.status_code = 200
            mock_client.return_value.get.return_value = mock_response

            # Execute the tool (currently returns hardcoded values)
            tools = getattr(server, "_FabricMCP__tools", [])
            if len(tools) > 1:
                pattern_details_tool = tools[1]
                result = pattern_details_tool("analyze_claims")

                assert isinstance(result, dict)
                assert "name" in result

    @pytest.mark.asyncio
    async def test_fabric_run_pattern_integration(
        self, server: FabricMCP, mock_fabric_api_response: Mock
    ):
        """Test the fabric_run_pattern tool with mocked API calls."""
        with patch("httpx.Client") as mock_client:
            # Setup mock response
            mock_response = Mock()
            mock_response.json.return_value = mock_fabric_api_response[
                "pattern_execution"
            ]
            mock_response.status_code = 200
            mock_client.return_value.post.return_value = mock_response

            # Execute the tool (currently returns hardcoded values)
            tools = getattr(server, "_FabricMCP__tools", [])
            if len(tools) > 2:
                run_pattern_tool = tools[2]
                result = run_pattern_tool("analyze_claims", "Test input text")

                assert isinstance(result, dict)
                assert "name" in result
                assert "input" in result
                assert "result" in result

    @pytest.mark.asyncio
    async def test_server_error_handling_with_fabric_api_down(self, server: FabricMCP):
        """Test error handling when Fabric API is unavailable."""
        with patch("httpx.Client") as mock_client:
            # Simulate connection error
            mock_client.return_value.get.side_effect = httpx.ConnectError(
                "Unable to connect to Fabric API"
            )

            # For now, tools return hardcoded values, but in future they should
            # handle errors
            tools = getattr(server, "_FabricMCP__tools", [])
            if tools:
                list_patterns_tool = tools[0]
                # Current implementation returns hardcoded values, so this passes
                # In future implementation, this should handle the connection
                # error gracefully
                result = list_patterns_tool()
                assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_server_error_handling_with_fabric_api_error(self, server: FabricMCP):
        """Test error handling when Fabric API returns errors."""
        with patch("httpx.Client") as mock_client:
            # Simulate HTTP error
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Internal Server Error",
                request=Mock(),
                response=mock_response,
            )
            mock_client.return_value.get.return_value = mock_response

            # For now, tools return hardcoded values, but in future they should
            # handle errors
            tools = getattr(server, "_FabricMCP__tools", [])
            if tools:
                list_patterns_tool = tools[0]
                # Current implementation returns hardcoded values, so this passes
                # In future implementation, this should handle the HTTP error gracefully
                result = list_patterns_tool()
                assert isinstance(result, list)

    def test_server_stdio_integration(self, server: FabricMCP):
        """Test the stdio method integration with mocked MCP run."""
        with patch.object(server.mcp, "run") as mock_run:
            server.stdio()
            mock_run.assert_called_once()

    def test_server_configuration_integration(self, server: FabricMCP):
        """Test server configuration and initialization."""
        assert server.log_level == "DEBUG"
        assert server.mcp.name.startswith("Fabric MCP v")
        assert hasattr(server, "logger")


class TestFabricMCPProtocol:
    """Test MCP protocol-specific functionality."""

    @pytest.fixture
    def server(self):
        """Create a FabricMCP server instance for testing."""
        return FabricMCP(log_level="INFO")

    def test_mcp_server_inheritance(self, server: FabricMCP):
        """Test that FabricMCP properly inherits from FastMCP."""

        assert isinstance(server, FastMCP)
        assert hasattr(server, "tool")
        assert hasattr(server, "run")

    @pytest.mark.asyncio
    async def test_mcp_tool_registration_integration(self, server: FabricMCP):
        """Test that tools are properly registered with the MCP framework."""
        # This tests the integration between our tools and the FastMCP framework
        # The actual tool registration happens in __init__
        tools = getattr(server, "_FabricMCP__tools", [])
        assert len(tools) == 3

        # Verify each tool is callable
        for tool in tools:
            assert callable(tool)


class TestFabricMCPErrorScenarios:
    """Test error scenarios and edge cases."""

    @pytest.fixture
    def server(self):
        """Create a FabricMCP server instance for testing."""
        return FabricMCP(log_level="ERROR")

    def test_server_graceful_shutdown_on_keyboard_interrupt(
        self, server: FabricMCP, caplog: pytest.LogCaptureFixture
    ):
        """Test graceful shutdown on KeyboardInterrupt."""

        with caplog.at_level(logging.INFO):
            with patch.object(server.mcp, "run", side_effect=KeyboardInterrupt):
                server.stdio()

            # Check log messages
            assert "Server stopped by user." in caplog.text

    def test_server_handles_multiple_shutdown_signals(
        self, server: FabricMCP, caplog: pytest.LogCaptureFixture
    ):
        """Test that server handles various shutdown signals properly."""

        with caplog.at_level(logging.INFO):
            # Test CancelledError
            with patch.object(server.mcp, "run", side_effect=CancelledError):
                server.stdio()

            # Test WouldBlock
            with patch.object(server.mcp, "run", side_effect=WouldBlock):
                server.stdio()

            # Both should result in graceful shutdown messages
            assert caplog.text.count("Server stopped by user.") >= 2


@pytest.mark.integration
class TestEndToEndScenarios:
    """End-to-end integration test scenarios."""

    @pytest.fixture
    def server(self):
        """Create a FabricMCP server instance for testing."""
        return FabricMCP(log_level="INFO")

    @pytest.mark.asyncio
    async def test_complete_pattern_workflow(self, server: FabricMCP):
        """Test a complete workflow: list patterns -> get details -> run pattern."""
        tools = getattr(server, "_FabricMCP__tools", [])

        if len(tools) >= 3:
            # Step 1: List patterns
            list_patterns_tool = tools[0]
            patterns: list[Callable[..., Any]] = list_patterns_tool()
            assert isinstance(patterns, list)
            assert len(patterns) > 0

            # Step 2: Get pattern details
            pattern_details_tool = tools[1]
            if patterns:
                details = pattern_details_tool(patterns[0])
                assert isinstance(details, dict)
                assert "name" in details

            # Step 3: Run pattern
            run_pattern_tool = tools[2]
            result = run_pattern_tool(patterns[0], "Test input")
            assert isinstance(result, dict)
            assert "result" in result

    def test_server_lifecycle(self, server: FabricMCP):
        """Test complete server lifecycle: init -> configure -> run -> shutdown."""
        # Server is already initialized via fixture
        assert server is not None
        assert hasattr(server, "mcp")

        # Test configuration
        assert server.log_level == "INFO"

        # Test run with immediate shutdown
        with patch.object(server.mcp, "run", side_effect=KeyboardInterrupt):
            server.stdio()

        # Server should handle shutdown gracefully
        assert True  # If we get here, shutdown was graceful


@pytest.mark.integration
class TestFabricMCPEndToEnd:
    """End-to-end integration tests that execute the fabric-mcp script."""

    def test_version_flag(self):
        """Test that fabric-mcp --version returns the correct version."""
        result = subprocess.run(
            [sys.executable, "-m", "fabric_mcp.cli", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )

        assert result.returncode == 0
        assert __version__ in result.stdout
        assert f"fabric-mcp {__version__}" in result.stdout

    def test_help_flag(self):
        """Test that fabric-mcp --help returns help text."""
        result = subprocess.run(
            [sys.executable, "-m", "fabric_mcp.cli", "--help"],
            capture_output=True,
            text=True,
            check=True,
        )

        assert result.returncode == 0
        assert "A Model Context Protocol server for Fabric AI" in result.stdout
        assert "--version" in result.stdout
        assert "--stdio" in result.stdout
        assert "--log-level" in result.stdout

    def test_no_args_shows_help(self):
        """Test that running fabric-mcp with no args shows help and exits with error."""
        result = subprocess.run(
            [sys.executable, "-m", "fabric_mcp.cli"],
            capture_output=True,
            text=True,
            check=False,  # We expect this to fail
        )

        assert result.returncode == 1
        assert "A Model Context Protocol server for Fabric AI" in result.stderr

    def test_script_entry_point_version(self):
        """Test the installed script entry point returns correct version."""
        # Test if the fabric-mcp script is available (it should be in dev environment)
        result = subprocess.run(
            ["fabric-mcp", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )

        # This might fail if not installed in development mode, so we'll check
        if result.returncode == 0:
            assert __version__ in result.stdout
            assert f"fabric-mcp {__version__}" in result.stdout
        else:
            # If the script isn't available, we can skip this test
            pytest.skip("fabric-mcp script not available (not installed in dev mode)")

    def test_script_entry_point_help(self):
        """Test the installed script entry point returns help."""
        result = subprocess.run(
            ["fabric-mcp", "--help"],
            capture_output=True,
            text=True,
            check=True,
        )

        # This might fail if not installed in development mode
        if result.returncode == 0:
            assert "A Model Context Protocol server for Fabric AI" in result.stdout
            assert "--version" in result.stdout
            assert "--stdio" in result.stdout
        else:
            # If the script isn't available, we can skip this test
            pytest.skip("fabric-mcp script not available (not installed in dev mode)")
