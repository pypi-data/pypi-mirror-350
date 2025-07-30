"""
Prometheus target tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.prometheus.service import PrometheusServiceManager
from tools.prometheus.base_tools import PrometheusBaseTools
from utils.logging import setup_logger


class PrometheusTargetTools(PrometheusBaseTools):
    """Tools for Prometheus target operations."""
    
    def __init__(self, mcp: FastMCP, prometheus_service: Optional[PrometheusServiceManager] = None):
        """
        Initialize Prometheus target tools.
        
        Args:
            mcp: The MCP server instance
            prometheus_service: The Prometheus service manager instance (optional)
        """
        super().__init__(mcp, prometheus_service)
        self.logger = setup_logger("devops_mcp_server.tools.prometheus.target")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Prometheus target tools with the MCP server."""
        
        @self.mcp.tool()
        def get_prometheus_targets(state: str = None, limit: int = 100) -> str:
            """
            Get all targets.
            
            This tool returns all scrape targets that Prometheus is configured to monitor.
            
            Args:
                state: Optional filter targets by state ("active", "dropped", or "all")
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                List of targets in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.target.get_targets(state, limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus targets: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_target_metadata(match_target: str = None, metric: str = None, limit: int = 100) -> str:
            """
            Get metadata for targets.
            
            This tool returns metadata about metrics scraped from targets.
            
            Args:
                match_target: Optional target selector
                metric: Optional metric name
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                Metadata for targets in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.target.get_target_metadata(match_target, metric, limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus target metadata: {e}")
                return self._format_error(str(e))