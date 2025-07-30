"""
Vault system client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.vault.client import VaultService


class VaultSystemClient:
    """Client for Vault system operations."""
    
    def __init__(self, vault_service: VaultService):
        """
        Initialize the Vault system client.
        
        Args:
            vault_service: The base Vault service
        """
        self.vault = vault_service
        self.logger = vault_service.logger
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get Vault health status.
        
        Returns:
            Health status information
        """
        try:
            # Get health status
            response = self.vault.client.sys.read_health_status(method="GET")
            
            # Return the health status
            return response
        except Exception as e:
            self.vault._handle_error("get_health_status", e)
    
    def get_seal_status(self) -> Dict[str, Any]:
        """
        Get Vault seal status.
        
        Returns:
            Seal status information
        """
        try:
            # Get seal status
            response = self.vault.client.sys.read_seal_status()
            
            # Return the seal status
            return response
        except Exception as e:
            self.vault._handle_error("get_seal_status", e)
    
    def list_policies(self, limit: int = 100) -> Dict[str, Any]:
        """
        List policies.
        
        Args:
            limit: Maximum number of policies to return
            
        Returns:
            List of policies
        """
        try:
            # List policies
            response = self.vault.client.sys.list_policies()
            
            # Extract data from response
            result = {
                "request_id": response.get("request_id", ""),
                "lease_id": response.get("lease_id", ""),
                "renewable": response.get("renewable", False),
                "lease_duration": response.get("lease_duration", 0),
                "data": {}
            }
            
            # Extract policies and apply limit
            if "data" in response and "policies" in response["data"]:
                policies = response["data"]["policies"]
                if len(policies) > limit:
                    policies = policies[:limit]
                    result["resultLimited"] = True
                
                result["data"]["policies"] = policies
            
            return result
        except Exception as e:
            self.vault._handle_error("list_policies", e)
    
    def get_policy(self, name: str) -> Dict[str, Any]:
        """
        Get a policy.
        
        Args:
            name: Policy name
            
        Returns:
            Policy details
        """
        try:
            # Get policy
            response = self.vault.client.sys.read_policy(name=name)
            
            # Return the policy
            return response
        except Exception as e:
            self.vault._handle_error(f"get_policy({name})", e)
    
    def list_audit_devices(self, limit: int = 100) -> Dict[str, Any]:
        """
        List audit devices.
        
        Args:
            limit: Maximum number of devices to return
            
        Returns:
            List of audit devices
        """
        try:
            # List audit devices
            response = self.vault.client.sys.list_enabled_audit_devices()
            
            # Extract data from response
            result = {
                "request_id": response.get("request_id", ""),
                "lease_id": response.get("lease_id", ""),
                "renewable": response.get("renewable", False),
                "lease_duration": response.get("lease_duration", 0),
                "data": {}
            }
            
            # Extract audit devices and apply limit
            if "data" in response:
                audit_devices = response["data"]
                if len(audit_devices) > limit:
                    # Convert to list of tuples, limit, and convert back to dict
                    items = list(audit_devices.items())[:limit]
                    audit_devices = dict(items)
                    result["resultLimited"] = True
                
                result["data"] = audit_devices
            
            return result
        except Exception as e:
            self.vault._handle_error("list_audit_devices", e)