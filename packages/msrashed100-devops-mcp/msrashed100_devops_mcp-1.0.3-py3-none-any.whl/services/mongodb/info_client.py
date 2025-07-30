"""
MongoDB information client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.mongodb.client import MongoDBService


class MongoDBInfoClient:
    """Client for MongoDB server information operations."""
    
    def __init__(self, mongodb_service: MongoDBService):
        """
        Initialize the MongoDB information client.
        
        Args:
            mongodb_service: The base MongoDB service
        """
        self.mongodb = mongodb_service
        self.logger = mongodb_service.logger
    
    def get_server_info(self) -> Dict[str, Any]:
        """
        Get MongoDB server information.
        
        Returns:
            Server information
        """
        try:
            # Get server information
            server_info = self.mongodb.client.server_info()
            
            return server_info
        except Exception as e:
            self.mongodb._handle_error("get_server_info", e)
    
    def get_server_status(self) -> Dict[str, Any]:
        """
        Get MongoDB server status.
        
        Returns:
            Server status
        """
        try:
            # Get server status
            status = self.mongodb.client.admin.command("serverStatus")
            
            return status
        except Exception as e:
            self.mongodb._handle_error("get_server_status", e)
    
    def get_build_info(self) -> Dict[str, Any]:
        """
        Get MongoDB build information.
        
        Returns:
            Build information
        """
        try:
            # Get build information
            build_info = self.mongodb.client.admin.command("buildInfo")
            
            return build_info
        except Exception as e:
            self.mongodb._handle_error("get_build_info", e)
    
    def get_host_info(self) -> Dict[str, Any]:
        """
        Get MongoDB host information.
        
        Returns:
            Host information
        """
        try:
            # Get host information
            host_info = self.mongodb.client.admin.command("hostInfo")
            
            return host_info
        except Exception as e:
            self.mongodb._handle_error("get_host_info", e)
    
    def get_server_parameters(self) -> Dict[str, Any]:
        """
        Get MongoDB server parameters.
        
        Returns:
            Server parameters
        """
        try:
            # Get server parameters
            parameters = self.mongodb.client.admin.command("getParameter", "*")
            
            return parameters
        except Exception as e:
            self.mongodb._handle_error("get_server_parameters", e)
    
    def get_replica_set_status(self) -> Optional[Dict[str, Any]]:
        """
        Get MongoDB replica set status.
        
        Returns:
            Replica set status or None if not a replica set
        """
        try:
            # Get replica set status
            status = self.mongodb.client.admin.command("replSetGetStatus")
            
            return status
        except Exception as e:
            # Not a replica set or other error
            self.logger.warning(f"Failed to get replica set status: {e}")
            return None
    
    def get_sharding_status(self) -> Optional[Dict[str, Any]]:
        """
        Get MongoDB sharding status.
        
        Returns:
            Sharding status or None if not a sharded cluster
        """
        try:
            # Get sharding status
            status = self.mongodb.client.admin.command("listShards")
            
            return status
        except Exception as e:
            # Not a sharded cluster or other error
            self.logger.warning(f"Failed to get sharding status: {e}")
            return None
    
    def get_current_operations(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get current operations.
        
        Args:
            limit: Maximum number of operations to return
            
        Returns:
            List of current operations
        """
        try:
            # Get current operations
            operations = self.mongodb.client.admin.current_op()
            
            # Extract operations
            if "inprog" in operations:
                ops = operations["inprog"]
                
                # Apply limit
                if len(ops) > limit:
                    ops = ops[:limit]
                
                return ops
            
            return []
        except Exception as e:
            self.mongodb._handle_error("get_current_operations", e)