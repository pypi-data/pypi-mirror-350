"""
Vault tools for the DevOps MCP Server.
"""
from typing import Optional
from mcp.server.fastmcp import FastMCP

from services.vault.service import VaultServiceManager
from tools.vault.secret_tools import VaultSecretTools
from tools.vault.auth_tools import VaultAuthTools
from tools.vault.system_tools import VaultSystemTools
from utils.logging import setup_logger


class VaultTools:
    """Tools for interacting with Vault."""
    
    def __init__(self, mcp: FastMCP, vault_service: Optional[VaultServiceManager] = None):
        """
        Initialize Vault tools.
        
        Args:
            mcp: The MCP server instance
            vault_service: The Vault service manager instance (optional)
        """
        self.mcp = mcp
        self.vault_service = vault_service or VaultServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.vault")
        
        # Initialize specialized tools
        self.secret_tools = VaultSecretTools(mcp, self.vault_service)
        self.auth_tools = VaultAuthTools(mcp, self.vault_service)
        self.system_tools = VaultSystemTools(mcp, self.vault_service)
        
        self.logger.info("Vault tools initialized successfully")