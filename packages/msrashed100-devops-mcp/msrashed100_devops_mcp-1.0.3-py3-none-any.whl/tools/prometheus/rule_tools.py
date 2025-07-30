"""
Prometheus rule tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.prometheus.service import PrometheusServiceManager
from tools.prometheus.base_tools import PrometheusBaseTools
from utils.logging import setup_logger


class PrometheusRuleTools(PrometheusBaseTools):
    """Tools for Prometheus rule operations."""
    
    def __init__(self, mcp: FastMCP, prometheus_service: Optional[PrometheusServiceManager] = None):
        """
        Initialize Prometheus rule tools.
        
        Args:
            mcp: The MCP server instance
            prometheus_service: The Prometheus service manager instance (optional)
        """
        super().__init__(mcp, prometheus_service)
        self.logger = setup_logger("devops_mcp_server.tools.prometheus.rule")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Prometheus rule tools with the MCP server."""
        
        @self.mcp.tool()
        def get_prometheus_rules(rule_type: str = None, limit: int = 100) -> str:
            """
            Get all rules.
            
            This tool returns all recording and alerting rules.
            
            Args:
                rule_type: Optional type of rules to get ("alert" or "record")
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                List of rules in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.rule.get_rules(rule_type, limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus rules: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_alert_rules(limit: int = 100) -> str:
            """
            Get all alerting rules.
            
            This tool returns all alerting rules.
            
            Args:
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                List of alerting rules in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.rule.get_alert_rules(limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus alert rules: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_recording_rules(limit: int = 100) -> str:
            """
            Get all recording rules.
            
            This tool returns all recording rules.
            
            Args:
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                List of recording rules in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.rule.get_recording_rules(limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus recording rules: {e}")
                return self._format_error(str(e))