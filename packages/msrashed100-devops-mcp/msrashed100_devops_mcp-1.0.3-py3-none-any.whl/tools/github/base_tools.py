"""
Base GitHub tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.github.service import GitHubServiceManager
from utils.logging import setup_logger
from utils.formatting import format_json_response, format_error_response


class GitHubBaseTools:
    """Base class for GitHub tools."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub base tools.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        self.mcp = mcp
        self.github_service = github_service or GitHubServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.github.base")
    
    def _check_service_available(self) -> bool:
        """
        Check if the GitHub service is available.
        
        Returns:
            True if available, False otherwise
        """
        if not self.github_service:
            self.logger.error("GitHub service is not available")
            return False
        
        if not self.github_service.is_available():
            self.logger.error("GitHub API is not available")
            return False
        
        return True
    
    def _format_response(self, result: Any) -> str:
        """
        Format a response from the GitHub API.
        
        Args:
            result: The result from the GitHub API
            
        Returns:
            Formatted response
        """
        return format_json_response(result)
    
    def _format_error(self, message: str) -> str:
        """
        Format an error message.
        
        Args:
            message: The error message
            
        Returns:
            Formatted error response
        """
        return format_error_response(message)