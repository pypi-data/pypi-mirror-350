"""
Prometheus resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.prometheus.service import PrometheusServiceManager
from utils.logging import setup_logger


class PrometheusResources:
    """Prometheus resources for the MCP server."""
    
    def __init__(self, mcp: FastMCP, prometheus_service: Optional[PrometheusServiceManager] = None):
        """
        Initialize Prometheus resources.
        
        Args:
            mcp: The MCP server instance
            prometheus_service: The Prometheus service manager instance (optional)
        """
        self.mcp = mcp
        self.prometheus_service = prometheus_service or PrometheusServiceManager()
        self.logger = setup_logger("devops_mcp_server.resources.prometheus")
        self._register_resources()
    
    def _register_resources(self) -> None:
        """Register Prometheus resources with the MCP server."""
        
        @self.mcp.resource("prom://.*")
        def handle_prometheus_resource(uri: str):
            """Handle Prometheus resource requests."""
            if not self.prometheus_service:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message="Prometheus service is not available"
                )
            
            # Parse URI
            if not uri.startswith("prom://"):
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid URI format: {uri}"
                )
            
            path = uri[len("prom://"):]
            
            try:
                if path == "query" or path.startswith("query/"):
                    # Handle query resource
                    return self._handle_query_resource(path)
                elif path == "metrics":
                    # Handle metrics resource
                    return self._handle_metrics_resource()
                elif path == "alerts":
                    # Handle alerts resource
                    return self._handle_alerts_resource()
                elif path == "rules":
                    # Handle rules resource
                    return self._handle_rules_resource()
                elif path == "targets":
                    # Handle targets resource
                    return self._handle_targets_resource()
                elif path == "status":
                    # Handle status resource
                    return self._handle_status_resource()
                else:
                    raise JSONRPCError(
                        code=INVALID_REQUEST,
                        message=f"Invalid Prometheus resource: {uri}"
                    )
            except Exception as e:
                self.logger.error(f"Error handling Prometheus resource: {e}")
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Error handling Prometheus resource: {str(e)}"
                )
        
        @self.mcp.list_resource_templates()
        def list_prometheus_resource_templates():
            """List Prometheus resource templates."""
            templates = []
            
            # Add template for query
            templates.append({
                "uriTemplate": "prom://query/{query}",
                "name": "Prometheus query",
                "mimeType": "application/json",
                "description": "Execute a PromQL query"
            })
            
            # Add template for metrics
            templates.append({
                "uriTemplate": "prom://metrics",
                "name": "Prometheus metrics",
                "mimeType": "application/json",
                "description": "List all metrics"
            })
            
            # Add template for alerts
            templates.append({
                "uriTemplate": "prom://alerts",
                "name": "Prometheus alerts",
                "mimeType": "application/json",
                "description": "List all alerts"
            })
            
            # Add template for rules
            templates.append({
                "uriTemplate": "prom://rules",
                "name": "Prometheus rules",
                "mimeType": "application/json",
                "description": "List all rules"
            })
            
            # Add template for targets
            templates.append({
                "uriTemplate": "prom://targets",
                "name": "Prometheus targets",
                "mimeType": "application/json",
                "description": "List all targets"
            })
            
            # Add template for status
            templates.append({
                "uriTemplate": "prom://status",
                "name": "Prometheus status",
                "mimeType": "application/json",
                "description": "Get Prometheus status"
            })
            
            return templates
    
    def _handle_query_resource(self, path: str) -> Dict[str, Any]:
        """
        Handle query resource.
        
        Args:
            path: Resource path
            
        Returns:
            Resource response
        """
        if path == "query":
            # Return list of recent queries (not supported by Prometheus API)
            return {
                "contents": [
                    {
                        "uri": "prom://query",
                        "mimeType": "application/json",
                        "text": '{"message": "Use prom://query/{query} to execute a specific query"}'
                    }
                ]
            }
        else:
            # Execute query
            query = path[len("query/"):]
            result = self.prometheus_service.query.query_instant(query)
            
            return {
                "contents": [
                    {
                        "uri": f"prom://query/{query}",
                        "mimeType": "application/json",
                        "text": self._format_json(result)
                    }
                ]
            }
    
    def _handle_metrics_resource(self) -> Dict[str, Any]:
        """
        Handle metrics resource.
        
        Returns:
            Resource response
        """
        # Get all metric names by querying for empty label set
        result = self.prometheus_service.query.get_labels()
        
        return {
            "contents": [
                {
                    "uri": "prom://metrics",
                    "mimeType": "application/json",
                    "text": self._format_json(result)
                }
            ]
        }
    
    def _handle_alerts_resource(self) -> Dict[str, Any]:
        """
        Handle alerts resource.
        
        Returns:
            Resource response
        """
        result = self.prometheus_service.alert.get_alerts()
        
        return {
            "contents": [
                {
                    "uri": "prom://alerts",
                    "mimeType": "application/json",
                    "text": self._format_json(result)
                }
            ]
        }
    
    def _handle_rules_resource(self) -> Dict[str, Any]:
        """
        Handle rules resource.
        
        Returns:
            Resource response
        """
        result = self.prometheus_service.rule.get_rules()
        
        return {
            "contents": [
                {
                    "uri": "prom://rules",
                    "mimeType": "application/json",
                    "text": self._format_json(result)
                }
            ]
        }
    
    def _handle_targets_resource(self) -> Dict[str, Any]:
        """
        Handle targets resource.
        
        Returns:
            Resource response
        """
        result = self.prometheus_service.target.get_targets()
        
        return {
            "contents": [
                {
                    "uri": "prom://targets",
                    "mimeType": "application/json",
                    "text": self._format_json(result)
                }
            ]
        }
    
    def _handle_status_resource(self) -> Dict[str, Any]:
        """
        Handle status resource.
        
        Returns:
            Resource response
        """
        result = self.prometheus_service.status.get_status()
        
        return {
            "contents": [
                {
                    "uri": "prom://status",
                    "mimeType": "application/json",
                    "text": self._format_json(result)
                }
            ]
        }
    
    def _format_json(self, data: Any) -> str:
        """Format data as JSON string."""
        import json
        return json.dumps(data, indent=2)