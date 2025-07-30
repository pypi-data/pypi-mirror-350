"""
Loki service manager for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from services.loki.client import LokiService
from services.loki.query_client import LokiQueryClient
from utils.logging import setup_logger


class LokiServiceManager:
    """Manager for Loki services."""

    def __init__(self, loki_url: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the Loki service manager.

        Args:
            loki_url: URL of the Loki server (e.g., "http://localhost:3100")
            timeout: Timeout for API calls in seconds
        """
        self.logger = setup_logger("devops_mcp_server.services.loki.manager")
        
        # Initialize the base service
        self.base_service = LokiService(loki_url, timeout)
        
        # Initialize specialized clients
        self.query = LokiQueryClient(self.base_service)
        
        self.logger.info("Loki service manager initialized")

    def is_available(self) -> bool:
        """
        Check if the Loki API is available.
        
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