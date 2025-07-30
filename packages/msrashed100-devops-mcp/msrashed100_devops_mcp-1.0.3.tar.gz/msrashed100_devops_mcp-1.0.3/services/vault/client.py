"""
Base Vault client for the DevOps MCP Server.
"""
import os
import importlib
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

from services.base import BaseService
from core.exceptions import ServiceConnectionError, ServiceOperationError
from config.settings import VAULT_URL, VAULT_TOKEN, VAULT_TIMEOUT

# Check if hvac is available
try:
    hvac = importlib.import_module('hvac')
    HVAC_AVAILABLE = True
except ImportError:
    HVAC_AVAILABLE = False


class VaultService(BaseService):
    """Base service for interacting with Vault."""
    
    def __init__(self, vault_url: Optional[str] = None, vault_token: Optional[str] = None,
                timeout: Optional[int] = None):
        """
        Initialize the Vault service.
        
        Args:
            vault_url: URL of the Vault server (default: from settings)
            vault_token: Vault authentication token (default: from settings)
            timeout: Timeout for API calls in seconds (default: from settings)
        """
        super().__init__("vault", {
            "vault_url": vault_url or VAULT_URL,
            "vault_token": vault_token or VAULT_TOKEN,
            "timeout": timeout or VAULT_TIMEOUT
        })
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize the Vault client."""
        try:
            self.url = self.config.get("vault_url")
            self.token = self.config.get("vault_token")
            self.timeout = self.config.get("timeout")
            
            self.logger.info(f"Initializing Vault client with URL: {self.url}")
            
            if not HVAC_AVAILABLE:
                self.logger.error("hvac module is not installed. Please install it with 'pip install hvac'")
                self.client = None
                return
            
            # Initialize hvac client
            self.client = hvac.Client(
                url=self.url,
                token=self.token,
                timeout=self.timeout
            )
            
            # Test connection
            self.is_available()
            
            self.logger.info("Vault client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Vault client: {e}")
            raise ServiceConnectionError("vault", str(e))
    
    def is_available(self) -> bool:
        """
        Check if the Vault API is available.
        
        Returns:
            True if the API is available, False otherwise
        """
        if not HVAC_AVAILABLE:
            self.logger.warning("hvac module is not installed. Vault service is not available.")
            return False
            
        if self.client is None:
            return False
            
        try:
            # Check if client is authenticated
            is_authenticated = self.client.is_authenticated()
            if not is_authenticated:
                self.logger.warning("Vault client is not authenticated")
                return False
            
            return True
        except Exception as e:
            self.logger.warning(f"Vault API is not available: {e}")
            return False
    
    def _handle_error(self, operation: str, error: Exception) -> None:
        """
        Handle an error from the Vault API.
        
        Args:
            operation: The operation that failed
            error: The exception that was raised
            
        Raises:
            ServiceOperationError: With details about the failure
        """
        self.logger.error(f"Error during Vault {operation}: {error}")
        raise ServiceOperationError("vault", f"{operation} failed: {str(error)}")