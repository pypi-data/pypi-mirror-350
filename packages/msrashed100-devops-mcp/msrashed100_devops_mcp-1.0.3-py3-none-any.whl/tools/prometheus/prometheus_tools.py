"""
Prometheus tools for the DevOps MCP Server.
"""
from typing import Optional
from mcp.server.fastmcp import FastMCP

from services.prometheus.service import PrometheusServiceManager
from tools.prometheus.query_tools import PrometheusQueryTools
from tools.prometheus.alert_tools import PrometheusAlertTools
from tools.prometheus.rule_tools import PrometheusRuleTools
from tools.prometheus.target_tools import PrometheusTargetTools
from tools.prometheus.status_tools import PrometheusStatusTools
from utils.logging import setup_logger


class PrometheusTools:
    """Tools for interacting with Prometheus."""
    
    def __init__(self, mcp: FastMCP, prometheus_service: Optional[PrometheusServiceManager] = None):
        """
        Initialize Prometheus tools.
        
        Args:
            mcp: The MCP server instance
            prometheus_service: The Prometheus service manager instance (optional)
        """
        self.mcp = mcp
        self.prometheus_service = prometheus_service or PrometheusServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.prometheus")
        
        # Initialize specialized tools
        self.query_tools = PrometheusQueryTools(mcp, self.prometheus_service)
        self.alert_tools = PrometheusAlertTools(mcp, self.prometheus_service)
        self.rule_tools = PrometheusRuleTools(mcp, self.prometheus_service)
        self.target_tools = PrometheusTargetTools(mcp, self.prometheus_service)
        self.status_tools = PrometheusStatusTools(mcp, self.prometheus_service)
        
        self.logger.info("Prometheus tools initialized successfully")