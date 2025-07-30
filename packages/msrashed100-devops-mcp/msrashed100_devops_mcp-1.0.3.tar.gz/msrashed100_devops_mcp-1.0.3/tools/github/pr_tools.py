"""
GitHub pull requests tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.github.service import GitHubServiceManager
from tools.github.base_tools import GitHubBaseTools
from utils.logging import setup_logger


class GitHubPRTools(GitHubBaseTools):
    """Tools for GitHub pull requests operations."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub pull requests tools.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        super().__init__(mcp, github_service)
        self.logger = setup_logger("devops_mcp_server.tools.github.pr")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register GitHub pull requests tools with the MCP server."""
        
        @self.mcp.tool()
        def list_github_pull_requests(repo_name: str, state: str = "open", 
                                   sort: str = "created", direction: str = "desc",
                                   base: str = None, head: str = None,
                                   max_results: int = 100) -> str:
            """
            List pull requests in a GitHub repository.
            
            This tool lists pull requests in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                state: Pull request state (open, closed, all) (default: open)
                sort: Sort field (created, updated, popularity, long-running) (default: created)
                direction: Sort direction (asc, desc) (default: desc)
                base: Base branch filter (optional)
                head: Head branch filter (optional)
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of pull requests in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate state
            valid_states = ["open", "closed", "all"]
            if state not in valid_states:
                return self._format_error(f"Invalid state. Must be one of: {', '.join(valid_states)}")
            
            # Validate sort
            valid_sorts = ["created", "updated", "popularity", "long-running"]
            if sort not in valid_sorts:
                return self._format_error(f"Invalid sort. Must be one of: {', '.join(valid_sorts)}")
            
            # Validate direction
            valid_directions = ["asc", "desc"]
            if direction not in valid_directions:
                return self._format_error(f"Invalid direction. Must be one of: {', '.join(valid_directions)}")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                pull_requests = self.github_service.pr.list_pull_requests(
                    repo_name, state, sort, direction, base, head, max_results
                )
                return self._format_response({"pullRequests": pull_requests, "count": len(pull_requests)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub pull requests: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_pull_request(repo_name: str, pr_number: int) -> str:
            """
            Get details of a pull request in a GitHub repository.
            
            This tool retrieves details of a pull request in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                pr_number: Pull request number
                
            Returns:
                Pull request details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                pull_request = self.github_service.pr.get_pull_request(repo_name, pr_number)
                return self._format_response(pull_request)
            except Exception as e:
                self.logger.error(f"Error getting GitHub pull request: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_pull_request_commits(repo_name: str, pr_number: int, 
                                          max_results: int = 100) -> str:
            """
            List commits in a pull request.
            
            This tool lists commits in a pull request.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                pr_number: Pull request number
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of commits in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                commits = self.github_service.pr.list_pull_request_commits(
                    repo_name, pr_number, max_results
                )
                return self._format_response({"commits": commits, "count": len(commits)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub pull request commits: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_pull_request_files(repo_name: str, pr_number: int, 
                                        max_results: int = 100) -> str:
            """
            List files in a pull request.
            
            This tool lists files in a pull request.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                pr_number: Pull request number
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of files in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                files = self.github_service.pr.list_pull_request_files(
                    repo_name, pr_number, max_results
                )
                return self._format_response({"files": files, "count": len(files)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub pull request files: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_pull_request_comments(repo_name: str, pr_number: int, 
                                           max_results: int = 100) -> str:
            """
            List comments on a pull request.
            
            This tool lists comments on a pull request.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                pr_number: Pull request number
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of comments in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                comments = self.github_service.pr.list_pull_request_comments(
                    repo_name, pr_number, max_results
                )
                return self._format_response({"comments": comments, "count": len(comments)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub pull request comments: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_pull_request_review_comments(repo_name: str, pr_number: int, 
                                                  max_results: int = 100) -> str:
            """
            List review comments on a pull request.
            
            This tool lists review comments on a pull request.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                pr_number: Pull request number
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of review comments in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                comments = self.github_service.pr.list_pull_request_review_comments(
                    repo_name, pr_number, max_results
                )
                return self._format_response({"reviewComments": comments, "count": len(comments)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub pull request review comments: {e}")
                return self._format_error(str(e))