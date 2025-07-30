"""
Redis information client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.redis.client import RedisService


class RedisInfoClient:
    """Client for Redis server information operations."""
    
    def __init__(self, redis_service: RedisService):
        """
        Initialize the Redis information client.
        
        Args:
            redis_service: The base Redis service
        """
        self.redis = redis_service
        self.logger = redis_service.logger
    
    def get_server_info(self, section: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Redis server information.
        
        Args:
            section: Specific section of information to retrieve (optional)
            
        Returns:
            Server information
        """
        try:
            # Get server information
            if section:
                info = self.redis.client.info(section)
            else:
                info = self.redis.client.info()
            
            return info
        except Exception as e:
            self.redis._handle_error("get_server_info", e)
    
    def get_server_stats(self) -> Dict[str, Any]:
        """
        Get Redis server statistics.
        
        Returns:
            Server statistics
        """
        try:
            # Get server information
            info = self.redis.client.info()
            
            # Extract relevant statistics
            stats = {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "used_memory_peak_human": info.get("used_memory_peak_human", "0B"),
                "total_connections_received": info.get("total_connections_received", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "instantaneous_ops_per_sec": info.get("instantaneous_ops_per_sec", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "uptime_in_seconds": info.get("uptime_in_seconds", 0),
                "uptime_in_days": info.get("uptime_in_days", 0)
            }
            
            # Add keyspace information
            keyspace = {}
            for key, value in info.items():
                if key.startswith("db"):
                    keyspace[key] = value
            
            stats["keyspace"] = keyspace
            
            return stats
        except Exception as e:
            self.redis._handle_error("get_server_stats", e)
    
    def get_server_config(self, parameter: Optional[str] = None) -> Dict[str, str]:
        """
        Get Redis server configuration.
        
        Args:
            parameter: Specific configuration parameter to retrieve (optional)
            
        Returns:
            Server configuration
        """
        try:
            # Get server configuration
            if parameter:
                config = self.redis.client.config_get(parameter)
            else:
                config = self.redis.client.config_get("*")
            
            return config
        except Exception as e:
            self.redis._handle_error("get_server_config", e)
    
    def get_slow_log(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get Redis slow log.
        
        Args:
            count: Maximum number of entries to return
            
        Returns:
            Slow log entries
        """
        try:
            # Get slow log
            slow_log = self.redis.client.slowlog_get(count)
            
            # Format slow log entries
            formatted_log = []
            for entry in slow_log:
                formatted_entry = {
                    "id": entry["id"],
                    "timestamp": entry["start_time"],
                    "duration": entry["duration"],
                    "command": " ".join(entry["command"]),
                    "client_address": entry.get("client_address", ""),
                    "client_name": entry.get("client_name", "")
                }
                formatted_log.append(formatted_entry)
            
            return formatted_log
        except Exception as e:
            self.redis._handle_error("get_slow_log", e)
    
    def get_client_list(self, limit: int = 100) -> List[Dict[str, str]]:
        """
        Get Redis client list.
        
        Args:
            limit: Maximum number of clients to return
            
        Returns:
            List of connected clients
        """
        try:
            # Get client list
            client_list = self.redis.client.client_list()
            
            # Apply limit
            if len(client_list) > limit:
                client_list = client_list[:limit]
            
            return client_list
        except Exception as e:
            self.redis._handle_error("get_client_list", e)