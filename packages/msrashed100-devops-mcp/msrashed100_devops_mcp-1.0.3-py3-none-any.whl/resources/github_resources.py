"""
GitHub resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.github.service import GitHubServiceManager
from resources.github.repo_resources import GitHubRepoResources
from resources.github.issue_resources import GitHubIssueResources
from resources.github.pr_resources import GitHubPRResources
from resources.github.actions_resources import GitHubActionsResources
from utils.logging import setup_logger


class GitHubResources:
    """GitHub resources for the MCP server."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub resources.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        self.mcp = mcp
        self.github_service = github_service or GitHubServiceManager()
        self.logger = setup_logger("devops_mcp_server.resources.github")
        
        # Initialize specialized resources
        self.repo_resources = GitHubRepoResources(mcp, self.github_service)
        self.issue_resources = GitHubIssueResources(mcp, self.github_service)
        self.pr_resources = GitHubPRResources(mcp, self.github_service)
        self.actions_resources = GitHubActionsResources(mcp, self.github_service)
        
        self._register_resources()
        self._register_resource_templates()
    
    def _register_resources(self) -> None:
        """Register GitHub resources with the MCP server."""
        
        @self.mcp.resource("github://.*")
        def handle_github_resource(uri: str):
            """Handle GitHub resource requests."""
            if not self.github_service:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message="GitHub service is not available"
                )
            
            # Parse URI
            if not uri.startswith("github://"):
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid URI format: {uri}"
                )
            
            path = uri[len("github://"):]
            
            try:
                # Try each resource handler in turn
                response = None
                
                # Repository resources
                response = self.repo_resources.handle_resource(path)
                if response:
                    return response
                
                # Issue resources
                response = self.issue_resources.handle_resource(path)
                if response:
                    return response
                
                # Pull request resources
                response = self.pr_resources.handle_resource(path)
                if response:
                    return response
                
                # Actions resources
                response = self.actions_resources.handle_resource(path)
                if response:
                    return response
                
                # If no handler matched
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid GitHub resource: {uri}"
                )
            except Exception as e:
                self.logger.error(f"Error handling GitHub resource: {e}")
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Error handling GitHub resource: {str(e)}"
                )
    
    def _register_resource_templates(self) -> None:
        """Register GitHub resource templates with the MCP server."""
        
        @self.mcp.list_resource_templates()
        def list_github_resource_templates():
            """List GitHub resource templates."""
            templates = []
            
            # Collect templates from all resource handlers
            templates.extend(self.repo_resources.get_resource_templates())
            templates.extend(self.issue_resources.get_resource_templates())
            templates.extend(self.pr_resources.get_resource_templates())
            templates.extend(self.actions_resources.get_resource_templates())
            
            return templates