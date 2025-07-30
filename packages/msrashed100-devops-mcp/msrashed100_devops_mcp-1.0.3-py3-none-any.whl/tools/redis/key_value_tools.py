"""
Redis key-value tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.redis.service import RedisServiceManager
from tools.redis.base_tools import RedisBaseTools
from utils.logging import setup_logger


class RedisKeyValueTools(RedisBaseTools):
    """Tools for Redis key-value operations."""
    
    def __init__(self, mcp: FastMCP, redis_service: Optional[RedisServiceManager] = None):
        """
        Initialize Redis key-value tools.
        
        Args:
            mcp: The MCP server instance
            redis_service: The Redis service manager instance (optional)
        """
        super().__init__(mcp, redis_service)
        self.logger = setup_logger("devops_mcp_server.tools.redis.key_value")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Redis key-value tools with the MCP server."""
        
        @self.mcp.tool()
        def get_redis_keys(pattern: str = "*", limit: int = 100) -> str:
            """
            Get Redis keys matching a pattern.
            
            This tool lists all keys in the Redis server that match the specified pattern.
            
            Args:
                pattern: Pattern to match keys against (default: "*" for all keys)
                limit: Maximum number of keys to return (default: 100, max: 500)
                
            Returns:
                List of matching keys in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Redis service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                keys = self.redis_service.key_value.get_keys(pattern, limit)
                return self._format_response({"keys": keys, "count": len(keys)})
            except Exception as e:
                self.logger.error(f"Error getting Redis keys: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_redis_value(key: str) -> str:
            """
            Get the value of a Redis key.
            
            This tool retrieves the value of a key from the Redis server.
            The value can be a string, list, set, hash, or sorted set.
            
            Args:
                key: Key to get the value of
                
            Returns:
                Value of the key in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Redis service is not available")
            
            try:
                value = self.redis_service.key_value.get_value(key)
                
                if value is None:
                    return self._format_error(f"Key '{key}' does not exist")
                
                return self._format_response({"key": key, "value": value})
            except Exception as e:
                self.logger.error(f"Error getting Redis value: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_redis_key_info(key: str) -> str:
            """
            Get information about a Redis key.
            
            This tool retrieves information about a key from the Redis server,
            including its type, TTL, and size.
            
            Args:
                key: Key to get information about
                
            Returns:
                Information about the key in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Redis service is not available")
            
            try:
                info = self.redis_service.key_value.get_key_info(key)
                
                if not info["exists"]:
                    return self._format_error(f"Key '{key}' does not exist")
                
                return self._format_response({"key": key, "info": info})
            except Exception as e:
                self.logger.error(f"Error getting Redis key info: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def scan_redis_keys(pattern: str = "*", count: int = 10, cursor: int = 0, limit: int = 100) -> str:
            """
            Scan Redis keys matching a pattern.
            
            This tool scans keys in the Redis server that match the specified pattern.
            It uses the SCAN command, which is more efficient for large databases than KEYS.
            
            Args:
                pattern: Pattern to match keys against (default: "*" for all keys)
                count: Number of keys to scan per iteration (default: 10)
                cursor: Cursor position to start scanning from (default: 0)
                limit: Maximum number of keys to return (default: 100, max: 500)
                
            Returns:
                List of matching keys and the next cursor position in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Redis service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                # Use the SCAN command
                next_cursor, keys = self.redis_service.base_service.client.scan(cursor, pattern, count)
                
                # Apply limit
                if len(keys) > limit:
                    keys = keys[:limit]
                
                return self._format_response({
                    "cursor": next_cursor,
                    "keys": keys,
                    "count": len(keys)
                })
            except Exception as e:
                self.logger.error(f"Error scanning Redis keys: {e}")
                return self._format_error(str(e))