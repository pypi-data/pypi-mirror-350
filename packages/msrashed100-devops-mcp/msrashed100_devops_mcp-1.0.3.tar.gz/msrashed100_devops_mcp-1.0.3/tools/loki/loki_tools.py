"""
Main Loki tools aggregator for the DevOps MCP Server.
"""
from typing import Optional
from mcp.server.fastmcp import FastMCP

from services.loki.service import LokiServiceManager
from tools.loki.query_tools import LokiQueryTools
from utils.logging import setup_logger


class LokiTools:
    """Main class for all Loki tools."""

    def __init__(self, mcp: FastMCP, loki_service: Optional[LokiServiceManager] = None):
        """
        Initialize Loki tools.

        Args:
            mcp: The MCP server instance.
            loki_service: The Loki service manager instance (optional).
        """
        self.mcp = mcp
        self.loki_service = loki_service or LokiServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.loki")

        # Initialize specialized tools
        self.query_tools = LokiQueryTools(mcp, self.loki_service)
        # Add other specialized Loki tools here if needed in the future
        # e.g., self.alert_tools = LokiAlertTools(mcp, self.loki_service)

        self.logger.info("LokiTools initialized successfully with query_tools.")