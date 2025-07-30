"""
Vault auth tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.vault.service import VaultServiceManager
from tools.vault.base_tools import VaultBaseTools
from utils.logging import setup_logger


class VaultAuthTools(VaultBaseTools):
    """Tools for Vault authentication operations."""
    
    def __init__(self, mcp: FastMCP, vault_service: Optional[VaultServiceManager] = None):
        """
        Initialize Vault auth tools.
        
        Args:
            mcp: The MCP server instance
            vault_service: The Vault service manager instance (optional)
        """
        super().__init__(mcp, vault_service)
        self.logger = setup_logger("devops_mcp_server.tools.vault.auth")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Vault auth tools with the MCP server."""
        
        @self.mcp.tool()
        def list_vault_auth_methods(limit: int = 100) -> str:
            """
            List authentication methods in Vault.
            
            This tool lists all authentication methods enabled in the Vault server.
            
            Args:
                limit: Maximum number of methods to return (default: 100, max: 500)
                
            Returns:
                List of authentication methods in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Vault service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.vault_service.auth.list_auth_methods(limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error listing Vault auth methods: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_vault_token_info() -> str:
            """
            Get information about the current token.
            
            This tool retrieves information about the token currently being used to authenticate with Vault.
            
            Returns:
                Token information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Vault service is not available")
            
            try:
                result = self.vault_service.auth.get_token_info()
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Vault token info: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_vault_token_accessors(limit: int = 100) -> str:
            """
            List token accessors in Vault.
            
            This tool lists all token accessors in the Vault server.
            
            Args:
                limit: Maximum number of accessors to return (default: 100, max: 500)
                
            Returns:
                List of token accessors in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Vault service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.vault_service.auth.list_token_accessors(limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error listing Vault token accessors: {e}")
                return self._format_error(str(e))