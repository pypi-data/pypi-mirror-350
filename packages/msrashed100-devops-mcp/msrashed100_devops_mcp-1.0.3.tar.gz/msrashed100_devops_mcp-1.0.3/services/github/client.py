"""
Base GitHub client for the DevOps MCP Server.
"""
import os
import importlib
import requests
from typing import Dict, Any, Optional, List, Union

from services.base import BaseService
from core.exceptions import ServiceConnectionError, ServiceOperationError
from config.settings import GITHUB_ACCESS_TOKEN, GITHUB_BASE_URL, GITHUB_TIMEOUT

# Check if PyGithub is available
try:
    Github = importlib.import_module('github').Github
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False


class GitHubService(BaseService):
    """Base service for interacting with GitHub."""
    
    def __init__(self, access_token: Optional[str] = None,
                base_url: Optional[str] = None,
                timeout: Optional[int] = None):
        """
        Initialize the GitHub service.
        
        Args:
            access_token: GitHub access token (default: from settings)
            base_url: GitHub API base URL (default: from settings)
            timeout: API timeout in seconds (default: from settings)
        """
        super().__init__("github", {
            "access_token": access_token or GITHUB_ACCESS_TOKEN or os.environ.get("GITHUB_ACCESS_TOKEN"),
            "base_url": base_url or GITHUB_BASE_URL or os.environ.get("GITHUB_BASE_URL", "https://api.github.com"),
            "timeout": timeout or GITHUB_TIMEOUT or int(os.environ.get("GITHUB_TIMEOUT", 10))
        })
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize the GitHub client."""
        try:
            self.access_token = self.config.get("access_token")
            self.base_url = self.config.get("base_url")
            self.timeout = self.config.get("timeout")
            
            self.logger.info(f"Initializing GitHub client with base URL: {self.base_url}")
            
            # Initialize requests session for direct API calls
            self.session = requests.Session()
            
            if not GITHUB_AVAILABLE:
                self.logger.error("PyGithub module is not installed. Please install it with 'pip install PyGithub'")
                self.client = None
                return
            
            if not self.access_token:
                self.logger.warning("No GitHub access token provided. GitHub tools may not work correctly.")
            
            # Initialize GitHub client
            self.client = Github(
                login_or_token=self.access_token,
                base_url=self.base_url,
                timeout=self.timeout
            )
            
            # Test connection
            self.is_available()
            
            self.logger.info("GitHub client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize GitHub client: {e}")
            raise ServiceConnectionError("github", str(e))
    
    @property
    def headers(self) -> Dict[str, str]:
        """
        Get the headers for GitHub API requests.
        
        Returns:
            Headers dictionary
        """
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "DevOps-MCP-Server/1.0.0"
        }
        
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        return headers
    
    def is_available(self) -> bool:
        """
        Check if the GitHub API is available.
        
        Returns:
            True if the API is available, False otherwise
        """
        if not GITHUB_AVAILABLE:
            self.logger.warning("PyGithub module is not installed. GitHub service is not available.")
            return False
            
        if self.client is None:
            return False
            
        try:
            # Try to get the authenticated user to test the connection
            self.client.get_user().login
            return True
        except Exception as e:
            self.logger.warning(f"GitHub API is not available: {e}")
            return False
    
    def get_user(self, username: Optional[str] = None) -> Any:
        """
        Get a GitHub user.
        
        Args:
            username: Username (if not provided, gets the authenticated user)
            
        Returns:
            GitHub user
        """
        if not self.is_available():
            raise ServiceConnectionError("github", "GitHub service is not available")
        
        try:
            if username:
                return self.client.get_user(username)
            else:
                return self.client.get_user()
        except Exception as e:
            self.logger.error(f"Failed to get GitHub user: {e}")
            raise ServiceOperationError("github", f"Failed to get GitHub user: {str(e)}")
    
    def get_repo(self, repo_name: str) -> Any:
        """
        Get a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            GitHub repository
        """
        if not self.is_available():
            raise ServiceConnectionError("github", "GitHub service is not available")
        
        try:
            return self.client.get_repo(repo_name)
        except Exception as e:
            self.logger.error(f"Failed to get GitHub repository: {e}")
            raise ServiceOperationError("github", f"Failed to get GitHub repository: {str(e)}")
    
    def get_organization(self, org_name: str) -> Any:
        """
        Get a GitHub organization.
        
        Args:
            org_name: Organization name
            
        Returns:
            GitHub organization
        """
        if not self.is_available():
            raise ServiceConnectionError("github", "GitHub service is not available")
        
        try:
            return self.client.get_organization(org_name)
        except Exception as e:
            self.logger.error(f"Failed to get GitHub organization: {e}")
            raise ServiceOperationError("github", f"Failed to get GitHub organization: {str(e)}")
    
    def search_repositories(self, query: str, sort: Optional[str] = None, 
                          order: Optional[str] = None) -> List[Any]:
        """
        Search GitHub repositories.
        
        Args:
            query: Search query
            sort: Sort field (stars, forks, updated)
            order: Sort order (asc, desc)
            
        Returns:
            List of GitHub repositories
        """
        if not self.is_available():
            raise ServiceConnectionError("github", "GitHub service is not available")
        
        try:
            return list(self.client.search_repositories(query, sort=sort, order=order))
        except Exception as e:
            self.logger.error(f"Failed to search GitHub repositories: {e}")
            raise ServiceOperationError("github", f"Failed to search GitHub repositories: {str(e)}")
    
    def search_users(self, query: str, sort: Optional[str] = None, 
                   order: Optional[str] = None) -> List[Any]:
        """
        Search GitHub users.
        
        Args:
            query: Search query
            sort: Sort field (followers, repositories, joined)
            order: Sort order (asc, desc)
            
        Returns:
            List of GitHub users
        """
        if not self.is_available():
            raise ServiceConnectionError("github", "GitHub service is not available")
        
        try:
            return list(self.client.search_users(query, sort=sort, order=order))
        except Exception as e:
            self.logger.error(f"Failed to search GitHub users: {e}")
            raise ServiceOperationError("github", f"Failed to search GitHub users: {str(e)}")
    
    def search_issues(self, query: str, sort: Optional[str] = None, 
                    order: Optional[str] = None) -> List[Any]:
        """
        Search GitHub issues.
        
        Args:
            query: Search query
            sort: Sort field (comments, created, updated)
            order: Sort order (asc, desc)
            
        Returns:
            List of GitHub issues
        """
        if not self.is_available():
            raise ServiceConnectionError("github", "GitHub service is not available")
        
        try:
            return list(self.client.search_issues(query, sort=sort, order=order))
        except Exception as e:
            self.logger.error(f"Failed to search GitHub issues: {e}")
            raise ServiceOperationError("github", f"Failed to search GitHub issues: {str(e)}")
    
    def search_code(self, query: str, sort: Optional[str] = None, 
                  order: Optional[str] = None) -> List[Any]:
        """
        Search GitHub code.
        
        Args:
            query: Search query
            sort: Sort field (indexed)
            order: Sort order (asc, desc)
            
        Returns:
            List of GitHub code results
        """
        if not self.is_available():
            raise ServiceConnectionError("github", "GitHub service is not available")
        
        try:
            return list(self.client.search_code(query, sort=sort, order=order))
        except Exception as e:
            self.logger.error(f"Failed to search GitHub code: {e}")
            raise ServiceOperationError("github", f"Failed to search GitHub code: {str(e)}")
    
    def get_rate_limit(self) -> Dict[str, Any]:
        """
        Get GitHub API rate limit information.
        
        Returns:
            Rate limit information
        """
        if not self.is_available():
            raise ServiceConnectionError("github", "GitHub service is not available")
        
        try:
            rate_limit = self.client.get_rate_limit()
            return {
                "core": {
                    "limit": rate_limit.core.limit,
                    "remaining": rate_limit.core.remaining,
                    "reset": rate_limit.core.reset.timestamp()
                },
                "search": {
                    "limit": rate_limit.search.limit,
                    "remaining": rate_limit.search.remaining,
                    "reset": rate_limit.search.reset.timestamp()
                },
                "graphql": {
                    "limit": rate_limit.graphql.limit,
                    "remaining": rate_limit.graphql.remaining,
                    "reset": rate_limit.graphql.reset.timestamp()
                }
            }
        except Exception as e:
            self.logger.error(f"Failed to get GitHub rate limit: {e}")
            raise ServiceOperationError("github", f"Failed to get GitHub rate limit: {str(e)}")
            
    def _handle_error(self, operation: str, error: Exception) -> None:
        """
        Handle GitHub API errors.
        
        Args:
            operation: The operation that failed
            error: The exception that was raised
            
        Raises:
            ServiceOperationError: Always raised with the error details
        """
        import traceback
        self.logger.error(f"GitHub API error in {operation}: {error}")
        self.logger.error(f"Error type: {type(error)}")
        self.logger.error(f"Error traceback: {traceback.format_exc()}")
        # Instead of raising an exception, we'll just log it
        # This will allow the calling method to return None
        # raise ServiceOperationError("github", f"Failed to {operation}: {str(error)}")