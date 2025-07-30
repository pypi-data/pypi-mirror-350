"""
GitHub repository tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.github.service import GitHubServiceManager
from tools.github.base_tools import GitHubBaseTools
from utils.logging import setup_logger


class GitHubRepoTools(GitHubBaseTools):
    """Tools for GitHub repository operations."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub repository tools.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        super().__init__(mcp, github_service)
        self.logger = setup_logger("devops_mcp_server.tools.github.repo")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register GitHub repository tools with the MCP server."""
        
        @self.mcp.tool()
        def list_github_repositories(username: str = None, org_name: str = None, 
                                  type: str = "all") -> str:
            """
            List GitHub repositories.
            
            This tool lists GitHub repositories for a user or organization.
            
            Args:
                username: GitHub username (optional)
                org_name: GitHub organization name (optional)
                type: Repository type (all, owner, public, private, member) (default: all)
                
            Returns:
                List of repositories in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate type
            valid_types = ["all", "owner", "public", "private", "member"]
            if type not in valid_types:
                return self._format_error(f"Invalid type. Must be one of: {', '.join(valid_types)}")
            
            try:
                repos = self.github_service.repo.list_repositories(username, org_name, type)
                # Check if repos is None before trying to get its length
                if repos is None:
                    return self._format_error("Failed to retrieve repositories")
                return self._format_response({"repositories": repos, "count": len(repos)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub repositories: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_repository(repo_name: str) -> str:
            """
            Get details of a GitHub repository.
            
            This tool retrieves details of a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                
            Returns:
                Repository details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                repo = self.github_service.repo.get_repository(repo_name)
                return self._format_response(repo)
            except Exception as e:
                self.logger.error(f"Error getting GitHub repository: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_branches(repo_name: str) -> str:
            """
            List branches in a GitHub repository.
            
            This tool lists branches in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                
            Returns:
                List of branches in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                branches = self.github_service.repo.list_branches(repo_name)
                # Check if branches is None before trying to get its length
                if branches is None:
                    return self._format_error("Failed to retrieve branches")
                return self._format_response({"branches": branches, "count": len(branches)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub branches: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_branch(repo_name: str, branch_name: str) -> str:
            """
            Get details of a branch in a GitHub repository.
            
            This tool retrieves details of a branch in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                branch_name: Branch name
                
            Returns:
                Branch details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                branch = self.github_service.repo.get_branch(repo_name, branch_name)
                return self._format_response(branch)
            except Exception as e:
                self.logger.error(f"Error getting GitHub branch: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_commits(repo_name: str, branch: str = None, path: str = None, 
                             author: str = None, since: str = None, until: str = None,
                             max_results: int = 100) -> str:
            """
            List commits in a GitHub repository.
            
            This tool lists commits in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                branch: Branch name (optional)
                path: File path (optional)
                author: Author name (optional)
                since: Start date (ISO format) (optional)
                until: End date (ISO format) (optional)
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of commits in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                commits = self.github_service.repo.list_commits(
                    repo_name, branch, path, author, since, until, max_results
                )
                # Check if commits is None before trying to get its length
                if commits is None:
                    return self._format_error("Failed to retrieve commits")
                return self._format_response({"commits": commits, "count": len(commits)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub commits: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_commit(repo_name: str, commit_sha: str) -> str:
            """
            Get details of a commit in a GitHub repository.
            
            This tool retrieves details of a commit in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                commit_sha: Commit SHA
                
            Returns:
                Commit details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                commit = self.github_service.repo.get_commit(repo_name, commit_sha)
                return self._format_response(commit)
            except Exception as e:
                self.logger.error(f"Error getting GitHub commit: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_contents(repo_name: str, path: str = "", ref: str = None) -> str:
            """
            List contents of a GitHub repository.
            
            This tool lists contents of a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                path: Directory path (default: root)
                ref: Branch, tag, or commit SHA (optional)
                
            Returns:
                List of contents in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                contents = self.github_service.repo.list_contents(repo_name, path, ref)
                return self._format_response({"contents": contents, "count": len(contents)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub contents: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_content(repo_name: str, path: str, ref: str = None) -> str:
            """
            Get content of a file in a GitHub repository.
            
            This tool retrieves content of a file in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                path: File path
                ref: Branch, tag, or commit SHA (optional)
                
            Returns:
                File content in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                content = self.github_service.repo.get_content(repo_name, path, ref)
                return self._format_response(content)
            except Exception as e:
                self.logger.error(f"Error getting GitHub content: {e}")
                return self._format_error(str(e))