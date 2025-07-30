"""
Prometheus query client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.prometheus.client import PrometheusService


class PrometheusQueryClient:
    """Client for Prometheus query operations."""
    
    def __init__(self, prometheus_service: PrometheusService):
        """
        Initialize the Prometheus query client.
        
        Args:
            prometheus_service: The base Prometheus service
        """
        self.prometheus = prometheus_service
        self.logger = prometheus_service.logger
    
    def query_instant(self, query: str, time: Optional[str] = None, 
                     timeout: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Execute an instant query.
        
        Args:
            query: PromQL expression
            time: Evaluation timestamp (RFC3339 or Unix timestamp)
            timeout: Evaluation timeout
            limit: Maximum number of results to return
            
        Returns:
            Query result
        """
        params = {"query": query}
        if time:
            params["time"] = time
        if timeout:
            params["timeout"] = timeout
            
        result = self.prometheus._make_request("/api/v1/query", params)
        
        # Apply limit to results if needed
        if result.get("data", {}).get("result") and len(result["data"]["result"]) > limit:
            result["data"]["result"] = result["data"]["result"][:limit]
            result["data"]["resultLimited"] = True
            
        return result
    
    def query_range(self, query: str, start: str, end: str, step: str,
                   timeout: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Execute a range query.
        
        Args:
            query: PromQL expression
            start: Start timestamp
            end: End timestamp
            step: Query resolution step width
            timeout: Evaluation timeout
            limit: Maximum number of results to return
            
        Returns:
            Query result
        """
        params = {
            "query": query,
            "start": start,
            "end": end,
            "step": step
        }
        if timeout:
            params["timeout"] = timeout
            
        result = self.prometheus._make_request("/api/v1/query_range", params)
        
        # Apply limit to results if needed
        if result.get("data", {}).get("result") and len(result["data"]["result"]) > limit:
            result["data"]["result"] = result["data"]["result"][:limit]
            result["data"]["resultLimited"] = True
            
        return result
    
    def get_series(self, match: List[str], start: Optional[str] = None,
                  end: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Get time series matching a label selector.
        
        Args:
            match: Series selectors (label matchers)
            start: Start timestamp
            end: End timestamp
            limit: Maximum number of results to return
            
        Returns:
            Matching series
        """
        params = {"match[]": match}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
            
        result = self.prometheus._make_request("/api/v1/series", params)
        
        # Apply limit to results if needed
        if result.get("data") and len(result["data"]) > limit:
            result["data"] = result["data"][:limit]
            result["resultLimited"] = True
            
        return result
    
    def get_labels(self, match: Optional[List[str]] = None, start: Optional[str] = None,
                  end: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Get all label names.
        
        Args:
            match: Series selectors (label matchers)
            start: Start timestamp
            end: End timestamp
            limit: Maximum number of results to return
            
        Returns:
            List of label names
        """
        params = {}
        if match:
            params["match[]"] = match
        if start:
            params["start"] = start
        if end:
            params["end"] = end
            
        result = self.prometheus._make_request("/api/v1/labels", params)
        
        # Apply limit to results if needed
        if result.get("data") and len(result["data"]) > limit:
            result["data"] = result["data"][:limit]
            result["resultLimited"] = True
            
        return result
    
    def get_label_values(self, label: str, match: Optional[List[str]] = None,
                        start: Optional[str] = None, end: Optional[str] = None,
                        limit: int = 100) -> Dict[str, Any]:
        """
        Get values for a label.
        
        Args:
            label: Label name
            match: Series selectors (label matchers)
            start: Start timestamp
            end: End timestamp
            limit: Maximum number of results to return
            
        Returns:
            List of label values
        """
        params = {}
        if match:
            params["match[]"] = match
        if start:
            params["start"] = start
        if end:
            params["end"] = end
            
        result = self.prometheus._make_request(f"/api/v1/label/{label}/values", params)
        
        # Apply limit to results if needed
        if result.get("data") and len(result["data"]) > limit:
            result["data"] = result["data"][:limit]
            result["resultLimited"] = True
            
        return result
    
    def get_metadata(self, metric: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Get metadata about metrics.
        
        Args:
            metric: Metric name
            limit: Maximum number of results to return
            
        Returns:
            Metadata about metrics
        """
        params = {}
        if metric:
            params["metric"] = metric
            
        result = self.prometheus._make_request("/api/v1/metadata", params)
        
        # Apply limit to results if needed
        if result.get("data") and len(result["data"]) > limit:
            # Convert to list, limit, and convert back to dict
            data_items = list(result["data"].items())[:limit]
            result["data"] = dict(data_items)
            result["resultLimited"] = True
            
        return result