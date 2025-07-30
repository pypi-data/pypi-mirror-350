"""
Base GitHub resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.github.service import GitHubServiceManager
from utils.logging import setup_logger


class GitHubBaseResources:
    """Base class for GitHub resources."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub base resources.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        self.mcp = mcp
        self.github_service = github_service or GitHubServiceManager()
        self.logger = setup_logger("devops_mcp_server.resources.github.base")
    
    def _format_json(self, data: Any) -> str:
        """Format data as JSON string."""
        import json
        return json.dumps(data, indent=2)
    
    def register_resource_templates(self, templates: List[Dict[str, str]]) -> None:
        """
        Register resource templates with the MCP server.
        
        Args:
            templates: List of resource templates
        """
        @self.mcp.list_resource_templates()
        def list_github_resource_templates():
            """List GitHub resource templates."""
            return templates