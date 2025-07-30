"""
Loki query tools for the DevOps MCP Server.
"""
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP

from services.loki.service import LokiServiceManager
from tools.loki.base_tools import LokiBaseTools
from utils.logging import setup_logger


class LokiQueryTools(LokiBaseTools):
    """Tools for Loki query operations."""

    def __init__(self, mcp: FastMCP, loki_service: Optional[LokiServiceManager] = None):
        """
        Initialize Loki query tools.

        Args:
            mcp: The MCP server instance.
            loki_service: The Loki service manager instance (optional).
        """
        super().__init__(mcp, loki_service)
        self.logger = setup_logger("devops_mcp_server.tools.loki.query")
        self._register_tools()
        self.logger.info("LokiQueryTools initialized and tools registered")

    def _register_tools(self) -> None:
        """Register Loki query tools with the MCP server."""

        @self.mcp.tool()
        def query_loki_range(query: str, start: str, end: str, limit: int = 100,
                             direction: str = "backward", step: Optional[str] = None) -> str:
            """
            Query logs from Loki within a given time range.

            Args:
                query: LogQL query string.
                start: Start timestamp (Unix epoch ns, RFC3339 string, or relative time like '1h').
                end: End timestamp (Unix epoch ns, RFC3339 string, or relative time like 'now').
                limit: Maximum number of log lines to return (default: 100, max: 5000).
                direction: Search direction ('forward' or 'backward', default: 'backward').
                step: Query resolution step width for metric queries (e.g., '15s', '1m').

            Returns:
                Query result in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("Loki service is not available")

            limit = min(max(1, limit), 5000)  # Loki typically supports higher limits

            try:
                result = self.loki_service.query.query_range(
                    query=query, start=start, end=end, limit=limit,
                    direction=direction, step=step
                )
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error executing Loki query_range: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_loki_labels(start: Optional[str] = None, end: Optional[str] = None) -> str:
            """
            Get all label names from Loki.

            Args:
                start: Optional start time (Unix epoch ns, RFC3339, or relative time) to filter labels.
                end: Optional end time (Unix epoch ns, RFC3339, or relative time) to filter labels.

            Returns:
                List of label names in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("Loki service is not available")

            try:
                result = self.loki_service.query.get_labels(start=start, end=end)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Loki labels: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_loki_label_values(label_name: str, start: Optional[str] = None, end: Optional[str] = None) -> str:
            """
            Get all values for a specific label name from Loki.

            Args:
                label_name: The name of the label.
                start: Optional start time (Unix epoch ns, RFC3339, or relative time) to filter values.
                end: Optional end time (Unix epoch ns, RFC3339, or relative time) to filter values.

            Returns:
                List of label values in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("Loki service is not available")

            if not label_name:
                return self._format_error("Label name cannot be empty.")

            try:
                result = self.loki_service.query.get_label_values(label_name=label_name, start=start, end=end)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Loki label values for '{label_name}': {e}")
                return self._format_error(str(e))