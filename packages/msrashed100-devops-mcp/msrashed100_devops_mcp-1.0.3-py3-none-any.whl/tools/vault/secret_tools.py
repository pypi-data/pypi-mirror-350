"""
Vault secret tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.vault.service import VaultServiceManager
from tools.vault.base_tools import VaultBaseTools
from utils.logging import setup_logger


class VaultSecretTools(VaultBaseTools):
    """Tools for Vault secret operations."""
    
    def __init__(self, mcp: FastMCP, vault_service: Optional[VaultServiceManager] = None):
        """
        Initialize Vault secret tools.
        
        Args:
            mcp: The MCP server instance
            vault_service: The Vault service manager instance (optional)
        """
        super().__init__(mcp, vault_service)
        self.logger = setup_logger("devops_mcp_server.tools.vault.secret")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Vault secret tools with the MCP server."""
        
        @self.mcp.tool()
        def list_vault_secrets(path: str, mount_point: str = "secret", limit: int = 100) -> str:
            """
            List secrets at a path in Vault.
            
            This tool lists secrets at the specified path in the Vault server.
            
            Args:
                path: Path to list secrets from (e.g., "my-app")
                mount_point: The secret engine mount point (default: "secret")
                limit: Maximum number of secrets to return (default: 100, max: 500)
                
            Returns:
                List of secrets in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Vault service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                response = self.vault_service.secret.list_secrets(path, mount_point, limit)
                # Ensure the response is JSON serializable
                if hasattr(response, 'json'):
                    result = response.json()
                elif isinstance(response, dict):
                    result = response
                else:
                    self.logger.warning(f"Unexpected response type for list secrets: {type(response)}")
                    result = {"keys": [], "error": "Unexpected response type", "details": str(response)}
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error listing Vault secrets: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_vault_secret(path: str, mount_point: str = "secret", version: int = None) -> str:
            """
            Get a secret from Vault.
            
            This tool retrieves a secret from the specified path in the Vault server.
            
            Args:
                path: Path to the secret (e.g., "my-app/database")
                mount_point: The secret engine mount point (default: "secret")
                version: Specific version to retrieve (optional)
                
            Returns:
                Secret data in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Vault service is not available")
            
            try:
                response = self.vault_service.secret.get_secret(path, mount_point, version)
                # Ensure the response is JSON serializable
                if hasattr(response, 'json'):
                    result = response.json()
                elif isinstance(response, dict):
                    result = response
                else:
                    self.logger.warning(f"Unexpected response type for get secret: {type(response)}")
                    result = {"data": None, "error": "Unexpected response type", "details": str(response)}
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Vault secret: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_vault_secret_metadata(path: str, mount_point: str = "secret") -> str:
            """
            Get metadata for a secret in Vault.
            
            This tool retrieves metadata for a secret from the specified path in the Vault server.
            
            Args:
                path: Path to the secret (e.g., "my-app/database")
                mount_point: The secret engine mount point (default: "secret")
                
            Returns:
                Secret metadata in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Vault service is not available")
            
            try:
                result = self.vault_service.secret.get_secret_metadata(path, mount_point)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Vault secret metadata: {e}")
                return self._format_error(str(e))