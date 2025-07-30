"""
Prometheus alert tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.prometheus.service import PrometheusServiceManager
from tools.prometheus.base_tools import PrometheusBaseTools
from utils.logging import setup_logger


class PrometheusAlertTools(PrometheusBaseTools):
    """Tools for Prometheus alert operations."""
    
    def __init__(self, mcp: FastMCP, prometheus_service: Optional[PrometheusServiceManager] = None):
        """
        Initialize Prometheus alert tools.
        
        Args:
            mcp: The MCP server instance
            prometheus_service: The Prometheus service manager instance (optional)
        """
        super().__init__(mcp, prometheus_service)
        self.logger = setup_logger("devops_mcp_server.tools.prometheus.alert")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Prometheus alert tools with the MCP server."""
        
        @self.mcp.tool()
        def get_prometheus_alerts(active: bool = None, silenced: bool = None,
                                inhibited: bool = None, limit: int = 100) -> str:
            """
            Get all alerts.
            
            This tool returns all alerts that are currently active, pending, or silenced.
            
            Args:
                active: Optional filter for active alerts
                silenced: Optional filter for silenced alerts
                inhibited: Optional filter for inhibited alerts
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                List of alerts in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.alert.get_alerts(active, silenced, inhibited, limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus alerts: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_alert_groups(active: bool = None, silenced: bool = None,
                                      inhibited: bool = None, limit: int = 100) -> str:
            """
            Get alerts grouped by rules.
            
            This tool returns alerts grouped by the alerting rules that generated them.
            
            Args:
                active: Optional filter for active alerts
                silenced: Optional filter for silenced alerts
                inhibited: Optional filter for inhibited alerts
                limit: Maximum number of results per group to return (default: 100, max: 500)
                
            Returns:
                Alerts grouped by rules in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.alert.get_alert_groups(active, silenced, inhibited, limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus alert groups: {e}")
                return self._format_error(str(e))