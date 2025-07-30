"""
Base Prometheus client for the DevOps MCP Server.
"""
import os
import requests
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

from services.base import BaseService
from core.exceptions import ServiceConnectionError, ServiceOperationError
from config.settings import PROMETHEUS_URL, PROMETHEUS_TIMEOUT


class PrometheusService(BaseService):
    """Base service for interacting with Prometheus."""
    
    def __init__(self, prometheus_url: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the Prometheus service.
        
        Args:
            prometheus_url: URL of the Prometheus server (default: from settings)
            timeout: Timeout for API calls in seconds (default: from settings)
        """
        super().__init__("prometheus", {
            "prometheus_url": prometheus_url or PROMETHEUS_URL,
            "timeout": timeout or PROMETHEUS_TIMEOUT
        })
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize the Prometheus client."""
        try:
            self.base_url = self.config.get("prometheus_url")
            self.timeout = self.config.get("timeout")
            self.session = requests.Session()
            
            self.logger.info(f"Initializing Prometheus client with URL: {self.base_url}")
            
            # Test connection
            self.is_available()
            
            self.logger.info("Prometheus client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Prometheus client: {e}")
            raise ServiceConnectionError("prometheus", str(e))
    
    def is_available(self) -> bool:
        """
        Check if the Prometheus API is available.
        
        Returns:
            True if the API is available, False otherwise
        """
        try:
            response = self.session.get(
                urljoin(self.base_url, "/-/healthy"),
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.warning(f"Prometheus API is not available: {e}")
            return False
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     method: str = "GET") -> Dict[str, Any]:
        """
        Make a request to the Prometheus API.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            method: HTTP method
            
        Returns:
            Response data
            
        Raises:
            ServiceOperationError: If the request fails
        """
        try:
            url = urljoin(self.base_url, endpoint)
            
            if method == "GET":
                response = self.session.get(url, params=params, timeout=self.timeout)
            else:
                response = self.session.post(url, json=params, timeout=self.timeout)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making request to Prometheus API: {e}")
            raise ServiceOperationError("prometheus", f"API request failed: {str(e)}")
        except ValueError as e:
            self.logger.error(f"Error parsing Prometheus API response: {e}")
            raise ServiceOperationError("prometheus", f"Failed to parse API response: {str(e)}")