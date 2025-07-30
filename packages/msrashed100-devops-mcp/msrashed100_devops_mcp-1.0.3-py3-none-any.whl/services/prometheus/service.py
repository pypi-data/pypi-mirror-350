"""
Prometheus service manager for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from services.prometheus.client import PrometheusService
from services.prometheus.query_client import PrometheusQueryClient
from services.prometheus.alert_client import PrometheusAlertClient
from services.prometheus.rule_client import PrometheusRuleClient
from services.prometheus.target_client import PrometheusTargetClient
from services.prometheus.status_client import PrometheusStatusClient


class PrometheusServiceManager:
    """Manager for all Prometheus services."""
    
    def __init__(self, prometheus_url: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the Prometheus service manager.
        
        Args:
            prometheus_url: URL of the Prometheus server
            timeout: Timeout for API calls in seconds
        """
        # Initialize the base service
        self.base_service = PrometheusService(prometheus_url, timeout)
        
        # Initialize specialized clients
        self.query = PrometheusQueryClient(self.base_service)
        self.alert = PrometheusAlertClient(self.base_service)
        self.rule = PrometheusRuleClient(self.base_service)
        self.target = PrometheusTargetClient(self.base_service)
        self.status = PrometheusStatusClient(self.base_service)
        
        self.logger = self.base_service.logger
        self.logger.info("Prometheus service manager initialized")
    
    def is_available(self) -> bool:
        """
        Check if the Prometheus API is available.
        
        Returns:
            True if the API is available, False otherwise
        """
        return self.base_service.is_available()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the service status.
        
        Returns:
            A dictionary with the service status
        """
        return self.base_service.get_status()