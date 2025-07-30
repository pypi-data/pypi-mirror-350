"""
Redis resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.redis.service import RedisServiceManager
from utils.logging import setup_logger


class RedisResources:
    """Redis resources for the MCP server."""
    
    def __init__(self, mcp: FastMCP, redis_service: Optional[RedisServiceManager] = None):
        """
        Initialize Redis resources.
        
        Args:
            mcp: The MCP server instance
            redis_service: The Redis service manager instance (optional)
        """
        self.mcp = mcp
        self.redis_service = redis_service or RedisServiceManager()
        self.logger = setup_logger("devops_mcp_server.resources.redis")
        self._register_resources()
    
    def _register_resources(self) -> None:
        """Register Redis resources with the MCP server."""
        
        @self.mcp.resource("redis://.*")
        def handle_redis_resource(uri: str):
            """Handle Redis resource requests."""
            if not self.redis_service:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message="Redis service is not available"
                )
            
            # Parse URI
            if not uri.startswith("redis://"):
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid URI format: {uri}"
                )
            
            path = uri[len("redis://"):]
            
            try:
                if path == "info":
                    # Handle info resource
                    return self._handle_info_resource()
                elif path == "stats":
                    # Handle stats resource
                    return self._handle_stats_resource()
                elif path == "config":
                    # Handle config resource
                    return self._handle_config_resource()
                elif path == "clients":
                    # Handle clients resource
                    return self._handle_clients_resource()
                elif path.startswith("key/"):
                    # Handle key resource
                    key = path[len("key/"):]
                    return self._handle_key_resource(key)
                elif path.startswith("keys/"):
                    # Handle keys resource
                    pattern = path[len("keys/"):]
                    return self._handle_keys_resource(pattern)
                else:
                    raise JSONRPCError(
                        code=INVALID_REQUEST,
                        message=f"Invalid Redis resource: {uri}"
                    )
            except Exception as e:
                self.logger.error(f"Error handling Redis resource: {e}")
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Error handling Redis resource: {str(e)}"
                )
        
        @self.mcp.list_resource_templates()
        def list_redis_resource_templates():
            """List Redis resource templates."""
            templates = []
            
            # Add template for info
            templates.append({
                "uriTemplate": "redis://info",
                "name": "Redis server information",
                "mimeType": "application/json",
                "description": "Get Redis server information"
            })
            
            # Add template for stats
            templates.append({
                "uriTemplate": "redis://stats",
                "name": "Redis server statistics",
                "mimeType": "application/json",
                "description": "Get Redis server statistics"
            })
            
            # Add template for config
            templates.append({
                "uriTemplate": "redis://config",
                "name": "Redis server configuration",
                "mimeType": "application/json",
                "description": "Get Redis server configuration"
            })
            
            # Add template for clients
            templates.append({
                "uriTemplate": "redis://clients",
                "name": "Redis client list",
                "mimeType": "application/json",
                "description": "Get Redis client list"
            })
            
            # Add template for key
            templates.append({
                "uriTemplate": "redis://key/{key}",
                "name": "Redis key value",
                "mimeType": "application/json",
                "description": "Get the value of a Redis key"
            })
            
            # Add template for keys
            templates.append({
                "uriTemplate": "redis://keys/{pattern}",
                "name": "Redis keys",
                "mimeType": "application/json",
                "description": "Get Redis keys matching a pattern"
            })
            
            return templates
    
    def _handle_info_resource(self) -> Dict[str, Any]:
        """
        Handle info resource.
        
        Returns:
            Resource response
        """
        info = self.redis_service.info.get_server_info()
        
        return {
            "contents": [
                {
                    "uri": "redis://info",
                    "mimeType": "application/json",
                    "text": self._format_json(info)
                }
            ]
        }
    
    def _handle_stats_resource(self) -> Dict[str, Any]:
        """
        Handle stats resource.
        
        Returns:
            Resource response
        """
        stats = self.redis_service.info.get_server_stats()
        
        return {
            "contents": [
                {
                    "uri": "redis://stats",
                    "mimeType": "application/json",
                    "text": self._format_json(stats)
                }
            ]
        }
    
    def _handle_config_resource(self) -> Dict[str, Any]:
        """
        Handle config resource.
        
        Returns:
            Resource response
        """
        config = self.redis_service.info.get_server_config()
        
        return {
            "contents": [
                {
                    "uri": "redis://config",
                    "mimeType": "application/json",
                    "text": self._format_json(config)
                }
            ]
        }
    
    def _handle_clients_resource(self) -> Dict[str, Any]:
        """
        Handle clients resource.
        
        Returns:
            Resource response
        """
        clients = self.redis_service.info.get_client_list()
        
        return {
            "contents": [
                {
                    "uri": "redis://clients",
                    "mimeType": "application/json",
                    "text": self._format_json({"clients": clients, "count": len(clients)})
                }
            ]
        }
    
    def _handle_key_resource(self, key: str) -> Dict[str, Any]:
        """
        Handle key resource.
        
        Args:
            key: Key to get the value of
            
        Returns:
            Resource response
        """
        value = self.redis_service.key_value.get_value(key)
        
        if value is None:
            raise JSONRPCError(
                code=INVALID_REQUEST,
                message=f"Key '{key}' does not exist"
            )
        
        return {
            "contents": [
                {
                    "uri": f"redis://key/{key}",
                    "mimeType": "application/json",
                    "text": self._format_json({"key": key, "value": value})
                }
            ]
        }
    
    def _handle_keys_resource(self, pattern: str) -> Dict[str, Any]:
        """
        Handle keys resource.
        
        Args:
            pattern: Pattern to match keys against
            
        Returns:
            Resource response
        """
        keys = self.redis_service.key_value.get_keys(pattern)
        
        return {
            "contents": [
                {
                    "uri": f"redis://keys/{pattern}",
                    "mimeType": "application/json",
                    "text": self._format_json({"keys": keys, "count": len(keys)})
                }
            ]
        }
    
    def _format_json(self, data: Any) -> str:
        """Format data as JSON string."""
        import json
        return json.dumps(data, indent=2)