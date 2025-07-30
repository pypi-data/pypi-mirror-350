"""
Base tools for Loki integration in the DevOps MCP Server.
"""
import json
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP

from services.loki.service import LokiServiceManager
from utils.logging import setup_logger


class LokiBaseTools:
    """Base class for Loki tools."""

    def __init__(self, mcp: FastMCP, loki_service: Optional[LokiServiceManager] = None):
        """
        Initialize Loki base tools.

        Args:
            mcp: The MCP server instance.
            loki_service: The Loki service manager instance (optional).
        """
        self.mcp = mcp
        self.loki_service = loki_service or LokiServiceManager()
        self.logger = setup_logger(f"devops_mcp_server.tools.loki.base")
        self.logger.info("LokiBaseTools initialized")

    def _check_service_available(self) -> bool:
        """Check if the Loki service is available."""
        if not self.loki_service:
            self.logger.warning("LokiServiceManager not initialized.")
            return False
        available = self.loki_service.is_available()
        if not available:
            self.logger.warning("Loki service is not available.")
        return available

    def _format_response(self, data: Any) -> str:
        """Format successful response data as a JSON string."""
        try:
            return json.dumps({"status": "success", "data": data})
        except TypeError as e:
            self.logger.error(f"Error serializing response to JSON: {e}")
            return json.dumps({"status": "error", "message": "Error serializing response data."})

    def _format_error(self, message: str, details: Optional[Dict[str, Any]] = None) -> str:
        """Format error response as a JSON string."""
        error_response = {"status": "error", "message": message}
        if details:
            error_response["details"] = details
        return json.dumps(error_response)