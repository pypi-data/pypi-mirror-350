"""
Prometheus query tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.prometheus.service import PrometheusServiceManager
from tools.prometheus.base_tools import PrometheusBaseTools
from utils.logging import setup_logger


class PrometheusQueryTools(PrometheusBaseTools):
    """Tools for Prometheus query operations."""
    
    def __init__(self, mcp: FastMCP, prometheus_service: Optional[PrometheusServiceManager] = None):
        """
        Initialize Prometheus query tools.
        
        Args:
            mcp: The MCP server instance
            prometheus_service: The Prometheus service manager instance (optional)
        """
        super().__init__(mcp, prometheus_service)
        self.logger = setup_logger("devops_mcp_server.tools.prometheus.query")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Prometheus query tools with the MCP server."""
        
        @self.mcp.tool()
        def query_prometheus(query: str, time: str = None, timeout: str = None, limit: int = 100) -> str:
            """
            Execute a Prometheus instant query.
            
            This tool executes a PromQL expression at a single point in time.
            
            Args:
                query: PromQL expression (e.g., "up", "rate(node_cpu_seconds_total[5m])")
                time: Optional evaluation timestamp (RFC3339 or Unix timestamp)
                timeout: Optional evaluation timeout
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                Query result in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.query.query_instant(query, time, timeout, limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error executing Prometheus query: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def query_prometheus_range(query: str, start: str, end: str, step: str,
                                  timeout: str = None, limit: int = 100) -> str:
            """
            Execute a Prometheus range query.
            
            This tool executes a PromQL expression over a range of time.
            
            Args:
                query: PromQL expression (e.g., "up", "rate(node_cpu_seconds_total[5m])")
                start: Start timestamp (RFC3339 or Unix timestamp)
                end: End timestamp (RFC3339 or Unix timestamp)
                step: Query resolution step width (e.g., "15s", "1m", "1h")
                timeout: Optional evaluation timeout
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                Query result in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.query.query_range(query, start, end, step, timeout, limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error executing Prometheus range query: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_series(match: List[str], start: str = None, end: str = None, limit: int = 100) -> str:
            """
            Get time series matching a label selector.
            
            This tool finds time series that match a label selector.
            
            Args:
                match: Series selectors (label matchers, e.g., "up", "node_cpu_seconds_total{job='node'}")
                start: Optional start timestamp (RFC3339 or Unix timestamp)
                end: Optional end timestamp (RFC3339 or Unix timestamp)
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                Matching series in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.query.get_series(match, start, end, limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus series: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_labels(match: List[str] = None, start: str = None, end: str = None, limit: int = 100) -> str:
            """
            Get all label names.
            
            This tool returns all label names that are available in the system.
            
            Args:
                match: Optional series selectors (label matchers)
                start: Optional start timestamp (RFC3339 or Unix timestamp)
                end: Optional end timestamp (RFC3339 or Unix timestamp)
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                List of label names in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.query.get_labels(match, start, end, limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus labels: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_label_values(label: str, match: List[str] = None, start: str = None,
                                       end: str = None, limit: int = 100) -> str:
            """
            Get values for a label.
            
            This tool returns all values for a given label name.
            
            Args:
                label: Label name
                match: Optional series selectors (label matchers)
                start: Optional start timestamp (RFC3339 or Unix timestamp)
                end: Optional end timestamp (RFC3339 or Unix timestamp)
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                List of label values in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.query.get_label_values(label, match, start, end, limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus label values: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_prometheus_metadata(metric: str = None, limit: int = 100) -> str:
            """
            Get metadata about metrics.
            
            This tool returns metadata about metrics (type, help text, etc.).
            
            Args:
                metric: Optional metric name
                limit: Maximum number of results to return (default: 100, max: 500)
                
            Returns:
                Metadata about metrics in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Prometheus service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.prometheus_service.query.get_metadata(metric, limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Prometheus metadata: {e}")
                return self._format_error(str(e))