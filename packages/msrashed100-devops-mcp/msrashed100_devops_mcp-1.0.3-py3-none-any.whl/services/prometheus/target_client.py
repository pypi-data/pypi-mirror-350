"""
Prometheus target client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.prometheus.client import PrometheusService


class PrometheusTargetClient:
    """Client for Prometheus target operations."""
    
    def __init__(self, prometheus_service: PrometheusService):
        """
        Initialize the Prometheus target client.
        
        Args:
            prometheus_service: The base Prometheus service
        """
        self.prometheus = prometheus_service
        self.logger = prometheus_service.logger
    
    def get_targets(self, state: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Get all targets.
        
        Args:
            state: Filter targets by state ("active", "dropped", or "all")
            limit: Maximum number of results to return
            
        Returns:
            List of targets
        """
        params = {}
        if state:
            params["state"] = state
            
        result = self.prometheus._make_request("/api/v1/targets", params)
        
        # Apply limit to active targets if needed
        if "data" in result and "activeTargets" in result["data"] and len(result["data"]["activeTargets"]) > limit:
            result["data"]["activeTargets"] = result["data"]["activeTargets"][:limit]
            result["data"]["resultLimited"] = True
        
        # Apply limit to dropped targets if needed
        if "data" in result and "droppedTargets" in result["data"] and len(result["data"]["droppedTargets"]) > limit:
            result["data"]["droppedTargets"] = result["data"]["droppedTargets"][:limit]
            result["data"]["resultLimited"] = True
            
        return result
    
    def get_target_metadata(self, match_target: Optional[str] = None, metric: Optional[str] = None,
                           limit: int = 100) -> Dict[str, Any]:
        """
        Get metadata for targets.
        
        Args:
            match_target: Target selector
            metric: Metric name
            limit: Maximum number of results to return
            
        Returns:
            Metadata for targets
        """
        params = {}
        if match_target:
            params["match_target"] = match_target
        if metric:
            params["metric"] = metric
            
        result = self.prometheus._make_request("/api/v1/targets/metadata", params)
        
        # Apply limit to results if needed
        if "data" in result and len(result["data"]) > limit:
            result["data"] = result["data"][:limit]
            result["resultLimited"] = True
            
        return result