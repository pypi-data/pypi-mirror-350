"""
Base PostgreSQL tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.postgresql.service import PostgreSQLServiceManager
from utils.logging import setup_logger
from utils.formatting import format_json_response, format_error_response


class PostgreSQLBaseTools:
    """Base class for PostgreSQL tools."""
    
    def __init__(self, mcp: FastMCP, postgresql_service: Optional[PostgreSQLServiceManager] = None):
        """
        Initialize PostgreSQL base tools.
        
        Args:
            mcp: The MCP server instance
            postgresql_service: The PostgreSQL service manager instance (optional)
        """
        self.mcp = mcp
        self.postgresql_service = postgresql_service or PostgreSQLServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.postgresql.base")
    
    def _check_service_available(self) -> bool:
        """
        Check if the PostgreSQL service is available.
        
        Returns:
            True if available, False otherwise
        """
        if not self.postgresql_service:
            self.logger.error("PostgreSQL service is not available")
            return False
        
        if not self.postgresql_service.is_available():
            self.logger.error("PostgreSQL server is not available")
            return False
        
        return True
    
    def _format_response(self, result: Any) -> str:
        """
        Format a response from the PostgreSQL server.
        
        Args:
            result: The result from the PostgreSQL server
            
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