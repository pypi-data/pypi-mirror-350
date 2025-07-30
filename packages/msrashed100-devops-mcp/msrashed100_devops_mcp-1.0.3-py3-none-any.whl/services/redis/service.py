"""
Redis service manager for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from services.redis.client import RedisService
from services.redis.key_value_client import RedisKeyValueClient
from services.redis.info_client import RedisInfoClient


class RedisServiceManager:
    """Manager for all Redis services."""
    
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None,
                password: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the Redis service manager.
        
        Args:
            host: Redis server host
            port: Redis server port
            password: Redis server password
            timeout: Timeout for API calls in seconds
        """
        # Initialize the base service
        self.base_service = RedisService(host, port, password, timeout)
        
        # Initialize specialized clients
        self.key_value = RedisKeyValueClient(self.base_service)
        self.info = RedisInfoClient(self.base_service)
        
        self.logger = self.base_service.logger
        self.logger.info("Redis service manager initialized")
    
    def is_available(self) -> bool:
        """
        Check if the Redis server is available.
        
        Returns:
            True if the server is available, False otherwise
        """
        return self.base_service.is_available()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the service status.
        
        Returns:
            A dictionary with the service status
        """
        return self.base_service.get_status()