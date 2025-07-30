"""
Vault auth client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.vault.client import VaultService


class VaultAuthClient:
    """Client for Vault authentication operations."""
    
    def __init__(self, vault_service: VaultService):
        """
        Initialize the Vault auth client.
        
        Args:
            vault_service: The base Vault service
        """
        self.vault = vault_service
        self.logger = vault_service.logger
    
    def list_auth_methods(self, limit: int = 100) -> Dict[str, Any]:
        """
        List authentication methods.
        
        Args:
            limit: Maximum number of methods to return
            
        Returns:
            List of authentication methods
        """
        try:
            # List auth methods
            response = self.vault.client.sys.list_auth_methods()
            
            # Extract data from response
            result = {
                "request_id": response.get("request_id", ""),
                "lease_id": response.get("lease_id", ""),
                "renewable": response.get("renewable", False),
                "lease_duration": response.get("lease_duration", 0),
                "data": {}
            }
            
            # Extract auth methods and apply limit
            if "data" in response:
                auth_methods = response["data"]
                if len(auth_methods) > limit:
                    # Convert to list of tuples, limit, and convert back to dict
                    items = list(auth_methods.items())[:limit]
                    auth_methods = dict(items)
                    result["resultLimited"] = True
                
                result["data"] = auth_methods
            
            return result
        except Exception as e:
            self.vault._handle_error("list_auth_methods", e)
    
    def get_token_info(self) -> Dict[str, Any]:
        """
        Get information about the current token.
        
        Returns:
            Token information
        """
        try:
            # Get token info
            response = self.vault.client.auth.token.lookup_self()
            
            # Extract data from response
            result = {
                "request_id": response.get("request_id", ""),
                "lease_id": response.get("lease_id", ""),
                "renewable": response.get("renewable", False),
                "lease_duration": response.get("lease_duration", 0),
                "data": {}
            }
            
            # Extract token data
            if "data" in response:
                # Remove sensitive fields
                data = response["data"].copy()
                if "id" in data:
                    data["id"] = "********"  # Redact token ID
                
                result["data"] = data
            
            return result
        except Exception as e:
            self.vault._handle_error("get_token_info", e)
    
    def list_token_accessors(self, limit: int = 100) -> Dict[str, Any]:
        """
        List token accessors.
        
        Args:
            limit: Maximum number of accessors to return
            
        Returns:
            List of token accessors
        """
        try:
            # List token accessors
            response = self.vault.client.auth.token.list_accessors()
            
            # Extract data from response
            result = {
                "request_id": response.get("request_id", ""),
                "lease_id": response.get("lease_id", ""),
                "renewable": response.get("renewable", False),
                "lease_duration": response.get("lease_duration", 0),
                "data": {}
            }
            
            # Extract accessors and apply limit
            if "data" in response and "keys" in response["data"]:
                accessors = response["data"]["keys"]
                if len(accessors) > limit:
                    accessors = accessors[:limit]
                    result["resultLimited"] = True
                
                result["data"]["keys"] = accessors
            
            return result
        except Exception as e:
            self.vault._handle_error("list_token_accessors", e)