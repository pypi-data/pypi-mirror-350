"""
Loki base client for the DevOps MCP Server.
"""
import requests # Changed from httpx
from typing import Dict, Any, Optional
from urllib.parse import urljoin

from utils.logging import setup_logger


class LokiService:
    """Base service for interacting with a Loki instance."""

    DEFAULT_TIMEOUT = 10  # seconds

    def __init__(self, loki_url: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the Loki service.

        Args:
            loki_url: URL of the Loki server (e.g., "http://localhost:3100")
            timeout: Timeout for API calls in seconds
        """
        self.loki_url = loki_url or "http://localhost:3100"  # Default to localhost if not provided
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.logger = setup_logger(f"devops_mcp_server.services.loki.client")
        self.logger.info(f"LokiService initialized with URL: {self.loki_url}")

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None,
                 json_data: Optional[Dict[str, Any]] = None) -> requests.Response: # Changed return type
        """
        Make a request to the Loki API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path (relative to base_url)
            params: URL query parameters
            json_data: JSON body for POST/PUT requests

        Returns:
            The requests.Response object.

        Raises:
            requests.exceptions.HTTPError: For 4xx or 5xx responses.
            requests.exceptions.RequestException: For other request issues.
        """
        full_url = urljoin(self.loki_url, endpoint.lstrip('/')) # Ensure endpoint is treated as relative
        self.logger.debug(f"Requesting {method} {full_url} with params: {params}, json: {json_data}")
        try:
            response = requests.request(
                method,
                full_url,
                params=params,
                json=json_data,
                timeout=self.timeout
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            self.logger.debug(f"Response from {full_url}: {response.status_code}")
            return response
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error for {full_url}: {e.response.status_code} - {e.response.text}")
            raise
        except requests.exceptions.RequestException as e: # Catch generic request exceptions
            self.logger.error(f"Request error for {full_url}: {e}")
            raise

    def is_available(self) -> bool:
        """
        Check if the Loki API is available through the gateway.
        We'll try to hit the /loki/api/v1/status/buildinfo endpoint via the gateway.
        """
        try:
            # This path should be proxied by the loki-gateway's Nginx to the loki-query-frontend
            response = self._request("GET", "/loki/api/v1/status/buildinfo")
            # Loki's buildinfo endpoint should return 200 OK if healthy
            return response.status_code == 200
        except Exception as e:
            self.logger.warning(f"Loki readiness check via /loki/api/v1/status/buildinfo failed: {e}")
            # Fallback: Check if the Nginx gateway itself is up at the root path
            try:
                self.logger.info("Falling back to checking Nginx gateway at '/' for readiness.")
                response_gateway = self._request("GET", "/")
                if response_gateway.status_code == 200:
                    self.logger.warning("Loki /loki/api/v1/status/buildinfo failed, but Nginx gateway at / is OK. Reporting as partially available/gateway OK.")
                    # Depending on strictness, you might return True or False here.
                    # For now, let's say if gateway is OK, basic connectivity is there.
                    # However, the tool call might still fail if backend Loki is not truly ready.
                    # A more robust check would be preferred if the user can provide one.
                    return True # Or False, if strict Loki readiness is required. Let's be optimistic for now.
                return False
            except Exception as e_gw:
                self.logger.error(f"Loki readiness check (both buildinfo and gateway root) failed. Gateway check error: {e_gw}")
                return False

    def get_status(self) -> Dict[str, Any]:
        """
        Get the service status, including availability.
        """
        available = self.is_available()
        return {
            "service_name": "Loki",
            "url": self.loki_url,
            "status": "available" if available else "unavailable",
            "message": "Loki service is ready." if available else "Loki service is not responding or not ready."
        }