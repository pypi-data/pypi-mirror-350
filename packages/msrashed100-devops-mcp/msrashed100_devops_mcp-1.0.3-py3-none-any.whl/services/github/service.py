"""
GitHub service manager for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from services.github.client import GitHubService
from services.github.repo_client import GitHubRepoClient
from services.github.issue_client import GitHubIssueClient
from services.github.pr_client import GitHubPRClient
from services.github.actions_client import GitHubActionsClient


class GitHubServiceManager:
    """Manager for all GitHub services."""
    
    def __init__(self, access_token: Optional[str] = None,
                base_url: Optional[str] = None,
                timeout: Optional[int] = None):
        """
        Initialize the GitHub service manager.
        
        Args:
            access_token: GitHub access token
            base_url: GitHub API base URL
            timeout: API timeout in seconds
        """
        # Initialize the base service
        self.base_service = GitHubService(access_token, base_url, timeout)
        
        # Initialize specialized clients
        self.repo = GitHubRepoClient(self.base_service)
        self.issue = GitHubIssueClient(self.base_service)
        self.pr = GitHubPRClient(self.base_service)
        self.actions = GitHubActionsClient(self.base_service)
        
        self.logger = self.base_service.logger
        self.logger.info("GitHub service manager initialized")
    
    def is_available(self) -> bool:
        """
        Check if the GitHub API is available.
        
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
    
    def get_rate_limit(self) -> Dict[str, Any]:
        """
        Get GitHub API rate limit information.
        
        Returns:
            Rate limit information
        """
        return self.base_service.get_rate_limit()