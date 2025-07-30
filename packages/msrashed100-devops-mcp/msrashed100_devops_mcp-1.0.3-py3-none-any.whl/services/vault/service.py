"""
Vault service manager for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from services.vault.client import VaultService
from services.vault.secret_client import VaultSecretClient
from services.vault.auth_client import VaultAuthClient
from services.vault.system_client import VaultSystemClient


class VaultServiceManager:
    """Manager for all Vault services."""
    
    def __init__(self, vault_url: Optional[str] = None, vault_token: Optional[str] = None,
                timeout: Optional[int] = None):
        """
        Initialize the Vault service manager.
        
        Args:
            vault_url: URL of the Vault server
            vault_token: Vault authentication token
            timeout: Timeout for API calls in seconds
        """
        # Initialize the base service
        self.base_service = VaultService(vault_url, vault_token, timeout)
        
        # Initialize specialized clients
        self.secret = VaultSecretClient(self.base_service)
        self.auth = VaultAuthClient(self.base_service)
        self.system = VaultSystemClient(self.base_service)
        
        self.logger = self.base_service.logger
        self.logger.info("Vault service manager initialized")
    
    def is_available(self) -> bool:
        """
        Check if the Vault API is available.
        
        Returns:
            True if the API is available, False otherwise
        """
        return self.base_service.is_available()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the service status.
        
        Returns:
            A dictionary with the service status
        """
        return self.base_service.get_status()