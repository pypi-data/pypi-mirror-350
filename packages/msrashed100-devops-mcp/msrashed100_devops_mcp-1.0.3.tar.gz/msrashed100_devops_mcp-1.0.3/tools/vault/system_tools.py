"""
Vault system tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.vault.service import VaultServiceManager
from tools.vault.base_tools import VaultBaseTools
from utils.logging import setup_logger


class VaultSystemTools(VaultBaseTools):
    """Tools for Vault system operations."""
    
    def __init__(self, mcp: FastMCP, vault_service: Optional[VaultServiceManager] = None):
        """
        Initialize Vault system tools.
        
        Args:
            mcp: The MCP server instance
            vault_service: The Vault service manager instance (optional)
        """
        super().__init__(mcp, vault_service)
        self.logger = setup_logger("devops_mcp_server.tools.vault.system")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Vault system tools with the MCP server."""
        
        @self.mcp.tool()
        def get_vault_health_status() -> str:
            """
            Get Vault health status.
            
            This tool retrieves the health status of the Vault server.
            
            Returns:
                Health status information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Vault service is not available")
            
            try:
                response = self.vault_service.system.get_health_status()
                # Ensure the response is JSON serializable
                if hasattr(response, 'json'):
                    result = response.json()
                elif isinstance(response, dict):
                    result = response
                else:
                    # If it's not a dict or doesn't have .json(),
                    # it might be an error or unexpected response type.
                    # Try to convert to string, or handle as an error.
                    self.logger.warning(f"Unexpected response type for health status: {type(response)}")
                    result = {"status": "unknown", "details": str(response)}
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Vault health status: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_vault_seal_status() -> str:
            """
            Get Vault seal status.
            
            This tool retrieves the seal status of the Vault server.
            
            Returns:
                Seal status information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Vault service is not available")
            
            try:
                result = self.vault_service.system.get_seal_status()
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Vault seal status: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_vault_policies(limit: int = 100) -> str:
            """
            List policies in Vault.
            
            This tool lists all policies in the Vault server.
            
            Args:
                limit: Maximum number of policies to return (default: 100, max: 500)
                
            Returns:
                List of policies in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Vault service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.vault_service.system.list_policies(limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error listing Vault policies: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_vault_policy(name: str) -> str:
            """
            Get a policy from Vault.
            
            This tool retrieves a policy from the Vault server.
            
            Args:
                name: Policy name
                
            Returns:
                Policy details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Vault service is not available")
            
            try:
                result = self.vault_service.system.get_policy(name)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting Vault policy: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_vault_audit_devices(limit: int = 100) -> str:
            """
            List audit devices in Vault.
            
            This tool lists all audit devices in the Vault server.
            
            Args:
                limit: Maximum number of devices to return (default: 100, max: 500)
                
            Returns:
                List of audit devices in JSON format
            """
            if not self._check_service_available():
                return self._format_error("Vault service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                result = self.vault_service.system.list_audit_devices(limit)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error listing Vault audit devices: {e}")
                return self._format_error(str(e))