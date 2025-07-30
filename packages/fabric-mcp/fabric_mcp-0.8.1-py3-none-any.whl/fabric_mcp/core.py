"""Core MCP server implementation using the Model Context Protocol."""

import logging
from asyncio.exceptions import CancelledError
from collections.abc import Callable
from typing import Any

from anyio import WouldBlock
from fastmcp import FastMCP

from . import __version__


class FabricMCP(FastMCP[None]):
    """Base class for the Model Context Protocol server."""

    def __init__(self, log_level: str = "INFO"):
        """Initialize the MCP server with a model."""
        super().__init__(f"Fabric MCP v{__version__}")
        self.mcp = self
        self.logger = logging.getLogger(__name__)
        self.__tools: list[Callable[..., Any]] = []
        self.log_level = log_level

        @self.tool()
        def fabric_list_patterns() -> list[str]:
            """Return a list of available fabric patterns."""
            # This is a placeholder for the actual implementation
            return ["pattern1", "pattern2", "pattern3"]

        self.__tools.append(fabric_list_patterns)

        @self.tool()
        def fabric_pattern_details(pattern_name: str) -> dict[Any, Any]:
            """Return the details of a specific fabric pattern."""
            # This is a placeholder for the actual implementation
            return {"name": pattern_name, "details": "Pattern details here"}

        self.__tools.append(fabric_pattern_details)

        @self.tool()
        def fabric_run_pattern(pattern_name: str, input_str: str) -> dict[Any, Any]:
            """
            Run a specific fabric pattern with the given arguments.

            Args:
                pattern_name (str): The name of the fabric pattern to run.
                input_str (str): The input string to be processed by the pattern.

            Returns:
                dict[Any, Any]: Contains the pattern name, input, and result.
            """
            # This is a placeholder for the actual implementation
            return {
                "name": pattern_name,
                "input": input_str,
                "result": "Pattern result here",
            }

        self.__tools.append(fabric_run_pattern)

    def stdio(self):
        """Run the MCP server."""
        try:
            self.mcp.run()
        except (KeyboardInterrupt, CancelledError, WouldBlock):
            # Handle graceful shutdown
            self.logger.info("Server stopped by user.")
