"""
Base Vault tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.vault.service import VaultServiceManager
from utils.logging import setup_logger
from utils.formatting import format_json_response, format_error_response


class VaultBaseTools:
    """Base class for Vault tools."""
    
    def __init__(self, mcp: FastMCP, vault_service: Optional[VaultServiceManager] = None):
        """
        Initialize Vault base tools.
        
        Args:
            mcp: The MCP server instance
            vault_service: The Vault service manager instance (optional)
        """
        self.mcp = mcp
        self.vault_service = vault_service or VaultServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.vault.base")
    
    def _check_service_available(self) -> bool:
        """
        Check if the Vault service is available.
        
        Returns:
            True if available, False otherwise
        """
        if not self.vault_service:
            self.logger.error("Vault service is not available")
            return False
        
        if not self.vault_service.is_available():
            self.logger.error("Vault API is not available")
            return False
        
        return True
    
    def _format_response(self, result: Dict[str, Any]) -> str:
        """
        Format a response from the Vault API.
        
        Args:
            result: The result from the Vault API
            
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