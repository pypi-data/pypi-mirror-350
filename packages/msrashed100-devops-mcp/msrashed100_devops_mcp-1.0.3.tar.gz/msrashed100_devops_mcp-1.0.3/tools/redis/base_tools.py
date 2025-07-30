"""
Base Redis tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.redis.service import RedisServiceManager
from utils.logging import setup_logger
from utils.formatting import format_json_response, format_error_response


class RedisBaseTools:
    """Base class for Redis tools."""
    
    def __init__(self, mcp: FastMCP, redis_service: Optional[RedisServiceManager] = None):
        """
        Initialize Redis base tools.
        
        Args:
            mcp: The MCP server instance
            redis_service: The Redis service manager instance (optional)
        """
        self.mcp = mcp
        self.redis_service = redis_service or RedisServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.redis.base")
    
    def _check_service_available(self) -> bool:
        """
        Check if the Redis service is available.
        
        Returns:
            True if available, False otherwise
        """
        if not self.redis_service:
            self.logger.error("Redis service is not available")
            return False
        
        if not self.redis_service.is_available():
            self.logger.error("Redis server is not available")
            return False
        
        return True
    
    def _format_response(self, result: Any) -> str:
        """
        Format a response from the Redis server.
        
        Args:
            result: The result from the Redis server
            
        Returns:
            Formatted response
        """
        return format_json_response(result)
    
    def _format_error(self, message: str) -> str:
        """
        Format an error message.
        
        Args:
            message: The error message
            
        Returns:
            Formatted error response
        """
        return format_error_response(message)