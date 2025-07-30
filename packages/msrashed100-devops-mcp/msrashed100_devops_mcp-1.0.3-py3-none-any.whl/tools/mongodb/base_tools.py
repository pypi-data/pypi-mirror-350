"""
Base MongoDB tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.mongodb.service import MongoDBServiceManager
from utils.logging import setup_logger
from utils.formatting import format_json_response, format_error_response


class MongoDBBaseTools:
    """Base class for MongoDB tools."""
    
    def __init__(self, mcp: FastMCP, mongodb_service: Optional[MongoDBServiceManager] = None):
        """
        Initialize MongoDB base tools.
        
        Args:
            mcp: The MCP server instance
            mongodb_service: The MongoDB service manager instance (optional)
        """
        self.mcp = mcp
        self.mongodb_service = mongodb_service or MongoDBServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.mongodb.base")
    
    def _check_service_available(self) -> bool:
        """
        Check if the MongoDB service is available.
        
        Returns:
            True if available, False otherwise
        """
        if not self.mongodb_service:
            self.logger.error("MongoDB service is not available")
            return False
        
        if not self.mongodb_service.is_available():
            self.logger.error("MongoDB server is not available")
            return False
        
        return True
    
    def _format_response(self, result: Any) -> str:
        """
        Format a response from the MongoDB server.
        
        Args:
            result: The result from the MongoDB server
            
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