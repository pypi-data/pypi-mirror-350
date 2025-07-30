"""
Base Redis client for the DevOps MCP Server.
"""
import os
import importlib
from typing import Dict, Any, Optional, List, Union

from services.base import BaseService
from core.exceptions import ServiceConnectionError, ServiceOperationError
from config.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_TIMEOUT

# Check if redis is available
try:
    redis = importlib.import_module('redis')
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class RedisService(BaseService):
    """Base service for interacting with Redis."""
    
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None,
                password: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the Redis service.
        
        Args:
            host: Redis server host (default: from settings)
            port: Redis server port (default: from settings)
            password: Redis server password (default: from settings)
            timeout: Timeout for API calls in seconds (default: from settings)
        """
        super().__init__("redis", {
            "host": host or REDIS_HOST,
            "port": port or REDIS_PORT,
            "password": password or REDIS_PASSWORD,
            "timeout": timeout or REDIS_TIMEOUT
        })
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize the Redis client."""
        try:
            self.host = self.config.get("host")
            self.port = self.config.get("port")
            self.password = self.config.get("password")
            self.timeout = self.config.get("timeout")
            
            self.logger.info(f"Initializing Redis client with host: {self.host}, port: {self.port}")
            
            if not REDIS_AVAILABLE:
                self.logger.error("redis module is not installed. Please install it with 'pip install redis'")
                self.client = None
                return
            
            # Initialize Redis client
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password if self.password else None,
                socket_timeout=self.timeout,
                decode_responses=True  # Automatically decode responses to strings
            )
            
            # Test connection
            self.is_available()
            
            self.logger.info("Redis client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Redis client: {e}")
            raise ServiceConnectionError("redis", str(e))
    
    def is_available(self) -> bool:
        """
        Check if the Redis server is available.
        
        Returns:
            True if the server is available, False otherwise
        """
        if not REDIS_AVAILABLE:
            self.logger.warning("redis module is not installed. Redis service is not available.")
            return False
            
        if self.client is None:
            return False
            
        try:
            # Ping the Redis server
            self.client.ping()
            return True
        except Exception as e:
            self.logger.warning(f"Redis server is not available: {e}")
            return False
    
    def _handle_error(self, operation: str, error: Exception) -> None:
        """
        Handle an error from the Redis server.
        
        Args:
            operation: The operation that failed
            error: The exception that was raised
            
        Raises:
            ServiceOperationError: With details about the failure
        """
        self.logger.error(f"Error during Redis {operation}: {error}")
        raise ServiceOperationError("redis", f"{operation} failed: {str(error)}")