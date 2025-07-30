"""
Redis tools for the DevOps MCP Server.
"""
from typing import Optional
from mcp.server.fastmcp import FastMCP

from services.redis.service import RedisServiceManager
from tools.redis.key_value_tools import RedisKeyValueTools
from tools.redis.info_tools import RedisInfoTools
from utils.logging import setup_logger


class RedisTools:
    """Tools for interacting with Redis."""
    
    def __init__(self, mcp: FastMCP, redis_service: Optional[RedisServiceManager] = None):
        """
        Initialize Redis tools.
        
        Args:
            mcp: The MCP server instance
            redis_service: The Redis service manager instance (optional)
        """
        self.mcp = mcp
        self.redis_service = redis_service or RedisServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.redis")
        
        # Initialize specialized tools
        self.key_value_tools = RedisKeyValueTools(mcp, self.redis_service)
        self.info_tools = RedisInfoTools(mcp, self.redis_service)
        
        self.logger.info("Redis tools initialized successfully")