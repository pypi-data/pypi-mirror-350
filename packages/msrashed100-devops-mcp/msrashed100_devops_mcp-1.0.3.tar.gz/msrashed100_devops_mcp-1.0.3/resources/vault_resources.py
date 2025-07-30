"""
Vault resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.vault.service import VaultServiceManager
from utils.logging import setup_logger


class VaultResources:
    """Vault resources for the MCP server."""
    
    def __init__(self, mcp: FastMCP, vault_service: Optional[VaultServiceManager] = None):
        """
        Initialize Vault resources.
        
        Args:
            mcp: The MCP server instance
            vault_service: The Vault service manager instance (optional)
        """
        self.mcp = mcp
        self.vault_service = vault_service or VaultServiceManager()
        self.logger = setup_logger("devops_mcp_server.resources.vault")
        self._register_resources()
    
    def _register_resources(self) -> None:
        """Register Vault resources with the MCP server."""
        
        @self.mcp.resource("vault://.*")
        def handle_vault_resource(uri: str):
            """Handle Vault resource requests."""
            if not self.vault_service:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message="Vault service is not available"
                )
            
            # Parse URI
            if not uri.startswith("vault://"):
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid URI format: {uri}"
                )
            
            path = uri[len("vault://"):]
            
            try:
                if path == "status":
                    # Handle status resource
                    return self._handle_status_resource()
                elif path == "auth":
                    # Handle auth resource
                    return self._handle_auth_resource()
                elif path.startswith("secret/"):
                    # Handle secret resource
                    secret_path = path[len("secret/"):]
                    return self._handle_secret_resource(secret_path)
                elif path == "policies":
                    # Handle policies resource
                    return self._handle_policies_resource()
                else:
                    raise JSONRPCError(
                        code=INVALID_REQUEST,
                        message=f"Invalid Vault resource: {uri}"
                    )
            except Exception as e:
                self.logger.error(f"Error handling Vault resource: {e}")
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Error handling Vault resource: {str(e)}"
                )
        
        @self.mcp.list_resource_templates()
        def list_vault_resource_templates():
            """List Vault resource templates."""
            templates = []
            
            # Add template for status
            templates.append({
                "uriTemplate": "vault://status",
                "name": "Vault status",
                "mimeType": "application/json",
                "description": "Get Vault server status"
            })
            
            # Add template for auth
            templates.append({
                "uriTemplate": "vault://auth",
                "name": "Vault authentication",
                "mimeType": "application/json",
                "description": "Get Vault authentication information"
            })
            
            # Add template for secret
            templates.append({
                "uriTemplate": "vault://secret/{path}",
                "name": "Vault secret",
                "mimeType": "application/json",
                "description": "Get a secret from Vault"
            })
            
            # Add template for policies
            templates.append({
                "uriTemplate": "vault://policies",
                "name": "Vault policies",
                "mimeType": "application/json",
                "description": "List Vault policies"
            })
            
            return templates
    
    def _handle_status_resource(self) -> Dict[str, Any]:
        """
        Handle status resource.
        
        Returns:
            Resource response
        """
        health_status = self.vault_service.system.get_health_status()
        seal_status = self.vault_service.system.get_seal_status()
        
        result = {
            "health": health_status,
            "seal": seal_status
        }
        
        return {
            "contents": [
                {
                    "uri": "vault://status",
                    "mimeType": "application/json",
                    "text": self._format_json(result)
                }
            ]
        }
    
    def _handle_auth_resource(self) -> Dict[str, Any]:
        """
        Handle auth resource.
        
        Returns:
            Resource response
        """
        auth_methods = self.vault_service.auth.list_auth_methods()
        token_info = self.vault_service.auth.get_token_info()
        
        result = {
            "auth_methods": auth_methods,
            "token_info": token_info
        }
        
        return {
            "contents": [
                {
                    "uri": "vault://auth",
                    "mimeType": "application/json",
                    "text": self._format_json(result)
                }
            ]
        }
    
    def _handle_secret_resource(self, path: str) -> Dict[str, Any]:
        """
        Handle secret resource.
        
        Args:
            path: Secret path
            
        Returns:
            Resource response
        """
        try:
            secret = self.vault_service.secret.get_secret(path)
            
            return {
                "contents": [
                    {
                        "uri": f"vault://secret/{path}",
                        "mimeType": "application/json",
                        "text": self._format_json(secret)
                    }
                ]
            }
        except Exception as e:
            self.logger.error(f"Error getting secret: {e}")
            
            # Try to list secrets if path is a directory
            try:
                secrets = self.vault_service.secret.list_secrets(path)
                
                return {
                    "contents": [
                        {
                            "uri": f"vault://secret/{path}",
                            "mimeType": "application/json",
                            "text": self._format_json(secrets)
                        }
                    ]
                }
            except Exception:
                # Re-raise the original exception
                raise
    
    def _handle_policies_resource(self) -> Dict[str, Any]:
        """
        Handle policies resource.
        
        Returns:
            Resource response
        """
        policies = self.vault_service.system.list_policies()
        
        return {
            "contents": [
                {
                    "uri": "vault://policies",
                    "mimeType": "application/json",
                    "text": self._format_json(policies)
                }
            ]
        }
    
    def _format_json(self, data: Any) -> str:
        """Format data as JSON string."""
        import json
        return json.dumps(data, indent=2)