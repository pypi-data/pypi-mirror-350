"""
Redis information tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.redis.service import RedisServiceManager
from tools.redis.base_tools import RedisBaseTools
from utils.logging import setup_logger


class RedisInfoTools(RedisBaseTools):
    """Tools for Redis server information operations."""
    
    def __init__(self, mcp: FastMCP, redis_service: Optional[RedisServiceManager] = None):
        """
        Initialize Redis information tools.
        
        Args:
            mcp: The MCP server instance
            redis_service: The Redis service manager instance (optional)
        """
        super().__init__(mcp, redis_service)
        self.logger = setup_logger("devops_mcp_server.tools.redis.info")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Redis information tools with the MCP server."""
        
        @self.mcp.tool()
        def get_redis_info(section: str = None) -> str:
            """
            Get Redis server information.
            
            This tool retrieves information about the Redis server.
            
            Args:
                section: Specific section of information to retrieve (optional)
                         Valid sections include: server, clients, memory, persistence,
                         stats, replication, cpu, commandstats, cluster, keyspace
                
            Returns:
                Server information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Redis service is not available")
            
            try:
                info = self.redis_service.info.get_server_info(section)
                return self._format_response(info)
            except Exception as e:
                self.logger.error(f"Error getting Redis info: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_redis_stats() -> str:
            """
            Get Redis server statistics.
            
            This tool retrieves statistics about the Redis server,
            including memory usage, connections, and operations.
            
            Returns:
                Server statistics in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Redis service is not available")
            
            try:
                stats = self.redis_service.info.get_server_stats()
                return self._format_response(stats)
            except Exception as e:
                self.logger.error(f"Error getting Redis stats: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_redis_config(parameter: str = None) -> str:
            """
            Get Redis server configuration.
            
            This tool retrieves the configuration of the Redis server.
            
            Args:
                parameter: Specific configuration parameter to retrieve (optional)
                           If not provided, all configuration parameters are returned
                
            Returns:
                Server configuration in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Redis service is not available")
            
            try:
                config = self.redis_service.info.get_server_config(parameter)
                return self._format_response(config)
            except Exception as e:
                self.logger.error(f"Error getting Redis config: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_redis_slow_log(count: int = 10) -> str:
            """
            Get Redis slow log.
            
            This tool retrieves the slow log from the Redis server.
            
            Args:
                count: Maximum number of entries to return (default: 10, max: 100)
                
            Returns:
                Slow log entries in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Redis service is not available")
            
            # Validate count
            count = min(max(1, count), 100)
            
            try:
                slow_log = self.redis_service.info.get_slow_log(count)
                return self._format_response({"entries": slow_log, "count": len(slow_log)})
            except Exception as e:
                self.logger.error(f"Error getting Redis slow log: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_redis_client_list(limit: int = 100) -> str:
            """
            Get Redis client list.
            
            This tool retrieves the list of clients connected to the Redis server.
            
            Args:
                limit: Maximum number of clients to return (default: 100, max: 500)
                
            Returns:
                List of connected clients in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Redis service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                client_list = self.redis_service.info.get_client_list(limit)
                return self._format_response({"clients": client_list, "count": len(client_list)})
            except Exception as e:
                self.logger.error(f"Error getting Redis client list: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_redis_memory_stats() -> str:
            """
            Get Redis memory statistics.
            
            This tool retrieves memory statistics from the Redis server.
            
            Returns:
                Memory statistics in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Redis service is not available")
            
            try:
                # Get memory info
                memory_info = self.redis_service.info.get_server_info("memory")
                
                # Extract relevant memory statistics
                memory_stats = {
                    "used_memory": memory_info.get("used_memory", 0),
                    "used_memory_human": memory_info.get("used_memory_human", "0B"),
                    "used_memory_rss": memory_info.get("used_memory_rss", 0),
                    "used_memory_rss_human": memory_info.get("used_memory_rss_human", "0B"),
                    "used_memory_peak": memory_info.get("used_memory_peak", 0),
                    "used_memory_peak_human": memory_info.get("used_memory_peak_human", "0B"),
                    "used_memory_lua": memory_info.get("used_memory_lua", 0),
                    "used_memory_lua_human": memory_info.get("used_memory_lua_human", "0B"),
                    "maxmemory": memory_info.get("maxmemory", 0),
                    "maxmemory_human": memory_info.get("maxmemory_human", "0B"),
                    "maxmemory_policy": memory_info.get("maxmemory_policy", ""),
                    "mem_fragmentation_ratio": memory_info.get("mem_fragmentation_ratio", 0),
                    "mem_allocator": memory_info.get("mem_allocator", "")
                }
                
                return self._format_response(memory_stats)
            except Exception as e:
                self.logger.error(f"Error getting Redis memory stats: {e}")
                return self._format_error(str(e))