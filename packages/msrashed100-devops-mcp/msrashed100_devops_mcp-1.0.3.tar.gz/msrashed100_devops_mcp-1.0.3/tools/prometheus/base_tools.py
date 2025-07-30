"""
Base Prometheus tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.prometheus.service import PrometheusServiceManager
from utils.logging import setup_logger
from utils.formatting import format_json_response, format_error_response


class PrometheusBaseTools:
    """Base class for Prometheus tools."""
    
    def __init__(self, mcp: FastMCP, prometheus_service: Optional[PrometheusServiceManager] = None):
        """
        Initialize Prometheus base tools.
        
        Args:
            mcp: The MCP server instance
            prometheus_service: The Prometheus service manager instance (optional)
        """
        self.mcp = mcp
        self.prometheus_service = prometheus_service or PrometheusServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.prometheus.base")
    
    def _check_service_available(self) -> bool:
        """
        Check if the Prometheus service is available.
        
        Returns:
            True if available, False otherwise
        """
        if not self.prometheus_service:
            self.logger.error("Prometheus service is not available")
            return False
        
        if not self.prometheus_service.is_available():
            self.logger.error("Prometheus API is not available")
            return False
        
        return True
    
    def _format_response(self, result: Dict[str, Any]) -> str:
        """
        Format a response from the Prometheus API.
        
        Args:
            result: The result from the Prometheus API
            
        Returns:
            Formatted response
        """
        return format_json_response(result)
    
    def _format_error(self, message: str) -> str:
        """
        Format an error message.
        
        Args:
            message: The error message
            
        Returns:
            Formatted error response
        """
        return format_error_response(message)