"""
GitHub tools for the DevOps MCP Server.
"""
from typing import Optional
from mcp.server.fastmcp import FastMCP

from services.github.service import GitHubServiceManager
from tools.github.base_tools import GitHubBaseTools
from tools.github.repo_tools import GitHubRepoTools
from tools.github.issue_tools import GitHubIssueTools
from tools.github.pr_tools import GitHubPRTools
from tools.github.actions_tools import GitHubActionsTools
from utils.logging import setup_logger


class GitHubTools(GitHubBaseTools):
    """Tools for interacting with GitHub."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub tools.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        super().__init__(mcp, github_service)
        self.logger = setup_logger("devops_mcp_server.tools.github")
        
        # Initialize specialized tools
        self.repo_tools = GitHubRepoTools(mcp, self.github_service)
        self.issue_tools = GitHubIssueTools(mcp, self.github_service)
        self.pr_tools = GitHubPRTools(mcp, self.github_service)
        self.actions_tools = GitHubActionsTools(mcp, self.github_service)
        
        self._register_tools()
        
        self.logger.info("GitHub tools initialized successfully")
    
    def _register_tools(self) -> None:
        """Register GitHub tools with the MCP server."""
        
        @self.mcp.tool()
        def get_github_rate_limit() -> str:
            """
            Get GitHub API rate limit information.
            
            This tool retrieves GitHub API rate limit information.
            
            Returns:
                Rate limit information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
                
            try:
                rate_limit = self.github_service.get_rate_limit()
                return self._format_response(rate_limit)
            except Exception as e:
                self.logger.error(f"Error getting GitHub rate limit: {e}")
                return self._format_error(str(e))