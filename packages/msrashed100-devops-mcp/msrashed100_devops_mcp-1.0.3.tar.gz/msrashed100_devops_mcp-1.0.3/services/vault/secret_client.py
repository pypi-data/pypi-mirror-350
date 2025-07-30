"""
Vault secret client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.vault.client import VaultService


class VaultSecretClient:
    """Client for Vault secret operations."""
    
    def __init__(self, vault_service: VaultService):
        """
        Initialize the Vault secret client.
        
        Args:
            vault_service: The base Vault service
        """
        self.vault = vault_service
        self.logger = vault_service.logger
    
    def list_secrets(self, path: str, mount_point: str = "secret", limit: int = 100) -> Dict[str, Any]:
        """
        List secrets at a path.
        
        Args:
            path: Path to list secrets from
            mount_point: The secret engine mount point
            limit: Maximum number of secrets to return
            
        Returns:
            List of secrets
        """
        try:
            # List secrets at the specified path
            response = self.vault.client.secrets.kv.v2.list_secrets(
                path=path,
                mount_point=mount_point
            )
            
            # Extract keys from response
            result = {
                "request_id": response.get("request_id", ""),
                "lease_id": response.get("lease_id", ""),
                "renewable": response.get("renewable", False),
                "lease_duration": response.get("lease_duration", 0),
                "data": {}
            }
            
            # Extract keys and apply limit
            if "data" in response and "keys" in response["data"]:
                keys = response["data"]["keys"]
                if len(keys) > limit:
                    keys = keys[:limit]
                    result["resultLimited"] = True
                
                result["data"]["keys"] = keys
            
            return result
        except Exception as e:
            self.vault._handle_error(f"list_secrets({path})", e)
    
    def get_secret(self, path: str, mount_point: str = "secret", version: Optional[int] = None) -> Dict[str, Any]:
        """
        Get a secret.
        
        Args:
            path: Path to the secret
            mount_point: The secret engine mount point
            version: Specific version to retrieve (optional)
            
        Returns:
            Secret data
        """
        try:
            # Get the secret
            kwargs = {"path": path, "mount_point": mount_point}
            if version is not None:
                kwargs["version"] = version
            
            response = self.vault.client.secrets.kv.v2.read_secret_version(**kwargs)
            
            # Extract data from response
            result = {
                "request_id": response.get("request_id", ""),
                "lease_id": response.get("lease_id", ""),
                "renewable": response.get("renewable", False),
                "lease_duration": response.get("lease_duration", 0),
                "data": {}
            }
            
            # Extract metadata and data
            if "data" in response:
                if "metadata" in response["data"]:
                    result["metadata"] = response["data"]["metadata"]
                
                if "data" in response["data"]:
                    result["data"] = response["data"]["data"]
            
            return result
        except Exception as e:
            self.vault._handle_error(f"get_secret({path})", e)
    
    def get_secret_metadata(self, path: str, mount_point: str = "secret") -> Dict[str, Any]:
        """
        Get metadata for a secret.
        
        Args:
            path: Path to the secret
            mount_point: The secret engine mount point
            
        Returns:
            Secret metadata
        """
        try:
            # Get the secret metadata
            response = self.vault.client.secrets.kv.v2.read_secret_metadata(
                path=path,
                mount_point=mount_point
            )
            
            # Extract metadata from response
            result = {
                "request_id": response.get("request_id", ""),
                "lease_id": response.get("lease_id", ""),
                "renewable": response.get("renewable", False),
                "lease_duration": response.get("lease_duration", 0),
                "data": {}
            }
            
            # Extract metadata
            if "data" in response:
                result["data"] = response["data"]
            
            return result
        except Exception as e:
            self.vault._handle_error(f"get_secret_metadata({path})", e)