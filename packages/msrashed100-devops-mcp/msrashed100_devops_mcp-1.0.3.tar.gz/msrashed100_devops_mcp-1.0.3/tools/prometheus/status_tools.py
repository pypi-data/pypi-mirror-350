"""
Prometheus status tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.prometheus.service import PrometheusServiceManager
from tools.prometheus.base_tools import PrometheusBaseTools
from utils.logging import setup_logger


class PrometheusStatusTools(PrometheusBaseTools):
    """Tools for Prometheus status operations."""
    
    def __init__(self, mcp: FastMCP, prometheus_service: Optional[PrometheusServiceManager] = None):
        """
        Initialize Prometheus status tools.
        
        Args:
            mcp: The MCP server instance
            prometheus_service: The Prometheus service manager instance (optional)
        """
        super().__init__(mcp, prometheus_service)
        self.logger = setup_logger("devops_mcp_server.tools.prometheus.status")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Prometheus status tools with the MCP server."""
        
        @self.mcp.tool()
        def get_prometheus_status() -> str:
            """
            Get Prometheus server status.
            
            This tool returns information about the Prometheus server, including runtime and build information.
            
            Returns:
                Server status information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            try:
                result = self.prometheus_service.status.get_status()
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus status: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_runtime_info() -> str:
            """
            Get Prometheus runtime information.
            
            This tool returns runtime information about the Prometheus server.
            
            Returns:
                Runtime information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            try:
                result = self.prometheus_service.status.get_runtime_info()
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus runtime info: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_build_info() -> str:
            """
            Get Prometheus build information.
            
            This tool returns build information about the Prometheus server.
            
            Returns:
                Build information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            try:
                result = self.prometheus_service.status.get_build_info()
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus build info: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_config() -> str:
            """
            Get Prometheus configuration.
            
            This tool returns the current configuration of the Prometheus server.
            
            Returns:
                Current configuration in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            try:
                result = self.prometheus_service.status.get_config()
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus config: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_flags() -> str:
            """
            Get Prometheus command-line flags.
            
            This tool returns the command-line flags that Prometheus was started with.
            
            Returns:
                Command-line flags in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            try:
                result = self.prometheus_service.status.get_flags()
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus flags: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_tsdb_stats() -> str:
            """
            Get TSDB statistics.
            
            This tool returns statistics about the Prometheus time series database.
            
            Returns:
                TSDB statistics in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            try:
                result = self.prometheus_service.status.get_tsdb_stats()
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus TSDB stats: {e}")
                return self._format_error(str(e))