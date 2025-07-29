import os
import sys

from kusto_mcp import __version__
from kusto_mcp.common import logger


def main() -> None:
    # writing to stderr because stdout is used for the transport
    # and we want to see the logs in the console
    logger.error("Starting Kusto MCP server")
    logger.error(f"Version: {__version__}")
    logger.error(f"Python version: {sys.version}")
    logger.error(f"Platform: {sys.platform}")
    # print pid
    logger.error(f"PID: {os.getpid()}")
    # import later to allow for environment variables to be set from command line
    from kusto_mcp.kusto_service import mcp

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
