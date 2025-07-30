"""
Prometheus rule client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.prometheus.client import PrometheusService


class PrometheusRuleClient:
    """Client for Prometheus rule operations."""
    
    def __init__(self, prometheus_service: PrometheusService):
        """
        Initialize the Prometheus rule client.
        
        Args:
            prometheus_service: The base Prometheus service
        """
        self.prometheus = prometheus_service
        self.logger = prometheus_service.logger
    
    def get_rules(self, rule_type: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Get all rules.
        
        Args:
            rule_type: Type of rules to get ("alert" or "record")
            limit: Maximum number of results to return
            
        Returns:
            List of rules
        """
        result = self.prometheus._make_request("/api/v1/rules", {})
        
        # Filter by rule type if specified
        if rule_type and "data" in result and "groups" in result["data"]:
            filtered_groups = []
            
            for group in result["data"]["groups"]:
                filtered_rules = []
                
                for rule in group.get("rules", []):
                    if rule.get("type") == rule_type:
                        filtered_rules.append(rule)
                
                if filtered_rules:
                    # Apply limit to rules in each group if needed
                    if len(filtered_rules) > limit:
                        filtered_rules = filtered_rules[:limit]
                    
                    filtered_group = group.copy()
                    filtered_group["rules"] = filtered_rules
                    filtered_groups.append(filtered_group)
            
            result["data"]["groups"] = filtered_groups
            
        # Apply limit to total number of rules if needed
        elif "data" in result and "groups" in result["data"]:
            total_rules = 0
            limited_groups = []
            
            for group in result["data"]["groups"]:
                rules = group.get("rules", [])
                
                if total_rules + len(rules) <= limit:
                    limited_groups.append(group)
                    total_rules += len(rules)
                else:
                    # Add partial group to reach the limit
                    remaining = limit - total_rules
                    if remaining > 0:
                        limited_group = group.copy()
                        limited_group["rules"] = rules[:remaining]
                        limited_groups.append(limited_group)
                    break
            
            if len(limited_groups) < len(result["data"]["groups"]):
                result["data"]["groups"] = limited_groups
                result["data"]["resultLimited"] = True
        
        return result
    
    def get_alert_rules(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get all alerting rules.
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List of alerting rules
        """
        return self.get_rules("alert", limit)
    
    def get_recording_rules(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get all recording rules.
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List of recording rules
        """
        return self.get_rules("record", limit)