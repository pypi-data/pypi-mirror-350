"""CLI entry point for fabric-mcp."""

import argparse
import sys

from fabric_mcp import __version__

from .core import FabricMCP
from .utils import Log


def main():
    "Argument parsing and entrypoint or fabric-mcp CLI."
    parser = argparse.ArgumentParser(
        prog="fabric-mcp",
        description="A Model Context Protocol server for Fabric AI.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version number and exit.",
    )
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Run the server in stdio mode (default).",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices=["debug", "info", "warning", "error", "critical"],
        default="info",
        help="Set the logging level (default: info)",
    )

    args = parser.parse_args()

    log = Log(args.log_level)
    logger = log.logger

    # If --stdio is not provided, and it's not just --version or --help, show help.
    # Allow running with just --log-level if --stdio is also present.
    if not args.stdio:
        # Show help if no arguments or only unrelated flags are provided
        argv_no_prog = sys.argv[1:]
        if len(sys.argv) == 1 or all(
            arg in ["--version", "-h", "--help"]
            or arg.startswith("--log-level")
            or arg.startswith("-l=")
            or arg in ["debug", "info", "warning", "error", "critical"]
            for arg in argv_no_prog
        ):
            parser.print_help(sys.stderr)
            sys.exit(1)

    # Add main logic based on args here
    if args.stdio:
        logger.info("Starting server with log level %s", log.level_name)
        fabric_mcp = FabricMCP(log_level=log.level_name)
        fabric_mcp.stdio()
        logger.info("Server stopped.")


if __name__ == "__main__":
    main()
