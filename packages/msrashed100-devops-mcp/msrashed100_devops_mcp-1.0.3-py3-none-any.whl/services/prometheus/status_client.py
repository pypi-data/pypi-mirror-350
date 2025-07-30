"""
Prometheus status client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from services.prometheus.client import PrometheusService


class PrometheusStatusClient:
    """Client for Prometheus status operations."""
    
    def __init__(self, prometheus_service: PrometheusService):
        """
        Initialize the Prometheus status client.
        
        Args:
            prometheus_service: The base Prometheus service
        """
        self.prometheus = prometheus_service
        self.logger = prometheus_service.logger
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get Prometheus server status.
        
        Returns:
            Server status information
        """
        # Combine runtime and build information
        runtime_info = self.get_runtime_info()
        build_info = self.get_build_info()
        
        return {
            "status": "success",
            "data": {
                "runtime": runtime_info.get("data", {}),
                "build": build_info.get("data", {})
            }
        }
    
    def get_runtime_info(self) -> Dict[str, Any]:
        """
        Get Prometheus runtime information.
        
        Returns:
            Runtime information
        """
        return self.prometheus._make_request("/api/v1/status/runtimeinfo")
    
    def get_build_info(self) -> Dict[str, Any]:
        """
        Get Prometheus build information.
        
        Returns:
            Build information
        """
        return self.prometheus._make_request("/api/v1/status/buildinfo")
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get Prometheus configuration.
        
        Returns:
            Current configuration
        """
        return self.prometheus._make_request("/api/v1/status/config")
    
    def get_flags(self) -> Dict[str, Any]:
        """
        Get Prometheus command-line flags.
        
        Returns:
            Command-line flags
        """
        return self.prometheus._make_request("/api/v1/status/flags")
    
    def get_tsdb_stats(self) -> Dict[str, Any]:
        """
        Get TSDB statistics.
        
        Returns:
            TSDB statistics
        """
        return self.prometheus._make_request("/api/v1/status/tsdb")