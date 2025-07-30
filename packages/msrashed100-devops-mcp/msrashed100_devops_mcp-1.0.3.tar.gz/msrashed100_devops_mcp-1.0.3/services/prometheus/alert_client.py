"""
Prometheus alert client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.prometheus.client import PrometheusService


class PrometheusAlertClient:
    """Client for Prometheus alert operations."""
    
    def __init__(self, prometheus_service: PrometheusService):
        """
        Initialize the Prometheus alert client.
        
        Args:
            prometheus_service: The base Prometheus service
        """
        self.prometheus = prometheus_service
        self.logger = prometheus_service.logger
    
    def get_alerts(self, active: Optional[bool] = None, silenced: Optional[bool] = None,
                  inhibited: Optional[bool] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Get all alerts.
        
        Args:
            active: Filter for active alerts
            silenced: Filter for silenced alerts
            inhibited: Filter for inhibited alerts
            limit: Maximum number of results to return
            
        Returns:
            List of alerts
        """
        params = {}
        if active is not None:
            params["active"] = str(active).lower()
        if silenced is not None:
            params["silenced"] = str(silenced).lower()
        if inhibited is not None:
            params["inhibited"] = str(inhibited).lower()
            
        result = self.prometheus._make_request("/api/v1/alerts", params)
        
        # Apply limit to results if needed
        if result.get("data", {}).get("alerts") and len(result["data"]["alerts"]) > limit:
            result["data"]["alerts"] = result["data"]["alerts"][:limit]
            result["data"]["resultLimited"] = True
            
        return result
    
    def get_alert_groups(self, active: Optional[bool] = None, silenced: Optional[bool] = None,
                        inhibited: Optional[bool] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Get alerts grouped by rules.
        
        Args:
            active: Filter for active alerts
            silenced: Filter for silenced alerts
            inhibited: Filter for inhibited alerts
            limit: Maximum number of results to return
            
        Returns:
            Alerts grouped by rules
        """
        # Alertmanager API endpoint for grouped alerts
        # This is typically available at /api/v2/alerts/groups in Alertmanager
        # For Prometheus itself, we can use the regular alerts endpoint and group them
        alerts_result = self.get_alerts(active, silenced, inhibited, limit)
        
        # Group alerts by rule name
        if "data" in alerts_result and "alerts" in alerts_result["data"]:
            alerts = alerts_result["data"]["alerts"]
            groups = {}
            
            for alert in alerts:
                rule_name = alert.get("labels", {}).get("alertname", "unknown")
                if rule_name not in groups:
                    groups[rule_name] = []
                groups[rule_name].append(alert)
            
            # Apply limit to each group if needed
            for rule_name, group_alerts in groups.items():
                if len(group_alerts) > limit:
                    groups[rule_name] = group_alerts[:limit]
            
            return {
                "status": alerts_result.get("status", "success"),
                "data": {
                    "groups": [
                        {
                            "name": rule_name,
                            "alerts": group_alerts
                        }
                        for rule_name, group_alerts in groups.items()
                    ]
                }
            }
        
        return alerts_result