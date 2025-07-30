"""
MongoDB information tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.mongodb.service import MongoDBServiceManager
from tools.mongodb.base_tools import MongoDBBaseTools
from utils.logging import setup_logger


class MongoDBInfoTools(MongoDBBaseTools):
    """Tools for MongoDB server information operations."""
    
    def __init__(self, mcp: FastMCP, mongodb_service: Optional[MongoDBServiceManager] = None):
        """
        Initialize MongoDB information tools.
        
        Args:
            mcp: The MCP server instance
            mongodb_service: The MongoDB service manager instance (optional)
        """
        super().__init__(mcp, mongodb_service)
        self.logger = setup_logger("devops_mcp_server.tools.mongodb.info")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register MongoDB information tools with the MCP server."""
        
        @self.mcp.tool()
        def get_mongodb_server_info() -> str:
            """
            Get MongoDB server information.
            
            This tool retrieves information about the MongoDB server.
            
            Returns:
                Server information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                info = self.mongodb_service.info.get_server_info()
                return self._format_response(info)
            except Exception as e:
                self.logger.error(f"Error getting MongoDB server info: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_server_status() -> str:
            """
            Get MongoDB server status.
            
            This tool retrieves the status of the MongoDB server.
            
            Returns:
                Server status in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                status = self.mongodb_service.info.get_server_status()
                return self._format_response(status)
            except Exception as e:
                self.logger.error(f"Error getting MongoDB server status: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_build_info() -> str:
            """
            Get MongoDB build information.
            
            This tool retrieves build information about the MongoDB server.
            
            Returns:
                Build information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                build_info = self.mongodb_service.info.get_build_info()
                return self._format_response(build_info)
            except Exception as e:
                self.logger.error(f"Error getting MongoDB build info: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_host_info() -> str:
            """
            Get MongoDB host information.
            
            This tool retrieves information about the host running the MongoDB server.
            
            Returns:
                Host information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                host_info = self.mongodb_service.info.get_host_info()
                return self._format_response(host_info)
            except Exception as e:
                self.logger.error(f"Error getting MongoDB host info: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_server_parameters() -> str:
            """
            Get MongoDB server parameters.
            
            This tool retrieves the parameters of the MongoDB server.
            
            Returns:
                Server parameters in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                parameters = self.mongodb_service.info.get_server_parameters()
                return self._format_response(parameters)
            except Exception as e:
                self.logger.error(f"Error getting MongoDB server parameters: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_replica_set_status() -> str:
            """
            Get MongoDB replica set status.
            
            This tool retrieves the status of the MongoDB replica set.
            
            Returns:
                Replica set status in JSON format, or an error if not a replica set
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                status = self.mongodb_service.info.get_replica_set_status()
                
                if status is None:
                    return self._format_error("Not a replica set or failed to get status")
                
                return self._format_response(status)
            except Exception as e:
                self.logger.error(f"Error getting MongoDB replica set status: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_sharding_status() -> str:
            """
            Get MongoDB sharding status.
            
            This tool retrieves the status of the MongoDB sharded cluster.
            
            Returns:
                Sharding status in JSON format, or an error if not a sharded cluster
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                status = self.mongodb_service.info.get_sharding_status()
                
                if status is None:
                    return self._format_error("Not a sharded cluster or failed to get status")
                
                return self._format_response(status)
            except Exception as e:
                self.logger.error(f"Error getting MongoDB sharding status: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_current_operations(limit: int = 100) -> str:
            """
            Get MongoDB current operations.
            
            This tool retrieves the current operations running on the MongoDB server.
            
            Args:
                limit: Maximum number of operations to return (default: 100, max: 500)
                
            Returns:
                List of current operations in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                operations = self.mongodb_service.info.get_current_operations(limit)
                return self._format_response({"operations": operations, "count": len(operations)})
            except Exception as e:
                self.logger.error(f"Error getting MongoDB current operations: {e}")
                return self._format_error(str(e))