"""
GitHub pull request resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.github.service import GitHubServiceManager
from resources.github.base_resources import GitHubBaseResources
from utils.logging import setup_logger


class GitHubPRResources(GitHubBaseResources):
    """GitHub pull request resources."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub pull request resources.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        super().__init__(mcp, github_service)
        self.logger = setup_logger("devops_mcp_server.resources.github.pr")
    
    def get_resource_templates(self) -> List[Dict[str, str]]:
        """
        Get pull request resource templates.
        
        Returns:
            List of resource templates
        """
        templates = []
        
        # Pull request templates
        templates.append({
            "uriTemplate": "github://pulls/{owner}/{repo}",
            "name": "GitHub Pull Requests",
            "mimeType": "application/json",
            "description": "List pull requests in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://pulls/{owner}/{repo}/{pr_number}",
            "name": "GitHub Pull Request",
            "mimeType": "application/json",
            "description": "Get details of a pull request in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://pulls/{owner}/{repo}/{pr_number}/commits",
            "name": "GitHub Pull Request Commits",
            "mimeType": "application/json",
            "description": "List commits in a pull request"
        })
        
        templates.append({
            "uriTemplate": "github://pulls/{owner}/{repo}/{pr_number}/files",
            "name": "GitHub Pull Request Files",
            "mimeType": "application/json",
            "description": "List files in a pull request"
        })
        
        templates.append({
            "uriTemplate": "github://pulls/{owner}/{repo}/{pr_number}/comments",
            "name": "GitHub Pull Request Comments",
            "mimeType": "application/json",
            "description": "List comments on a pull request"
        })
        
        templates.append({
            "uriTemplate": "github://pulls/{owner}/{repo}/{pr_number}/reviews",
            "name": "GitHub Pull Request Reviews",
            "mimeType": "application/json",
            "description": "List reviews on a pull request"
        })
        
        return templates
    
    def handle_resource(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Handle pull request resources.
        
        Args:
            path: Resource path
            
        Returns:
            Resource response or None if not handled
        """
        if path.startswith("pulls/"):
            repo_path = path[len("pulls/"):]
            if "/" not in repo_path:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid repository path: {repo_path}. Format should be 'owner/repo'"
                )
            
            if "/" not in repo_path[repo_path.find("/")+1:]:
                # List pull requests
                return self._handle_pulls_resource(repo_path)
            else:
                parts = repo_path.split("/", 3)
                owner = parts[0]
                repo = parts[1]
                
                if len(parts) > 2 and parts[2].isdigit():
                    pr_number = int(parts[2])
                    if len(parts) > 3:
                        if parts[3] == "commits":
                            return self._handle_pull_commits_resource(f"{owner}/{repo}", pr_number)
                        elif parts[3] == "files":
                            return self._handle_pull_files_resource(f"{owner}/{repo}", pr_number)
                        elif parts[3] == "comments":
                            return self._handle_pull_comments_resource(f"{owner}/{repo}", pr_number)
                        elif parts[3] == "reviews":
                            return self._handle_pull_reviews_resource(f"{owner}/{repo}", pr_number)
                    else:
                        return self._handle_pull_resource(f"{owner}/{repo}", pr_number)
        
        return None
    
    def _handle_pulls_resource(self, repo_name: str) -> Dict[str, Any]:
        """
        Handle GitHub pull requests resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Resource response
        """
        pulls = self.github_service.pr.list_pull_requests(repo_name)
        
        return {
            "contents": [
                {
                    "uri": f"github://pulls/{repo_name}",
                    "mimeType": "application/json",
                    "text": self._format_json({"pullRequests": pulls, "count": len(pulls)})
                }
            ]
        }
    
    def _handle_pull_resource(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """
        Handle GitHub pull request resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            pr_number: Pull request number
            
        Returns:
            Resource response
        """
        pull = self.github_service.pr.get_pull_request(repo_name, pr_number)
        
        return {
            "contents": [
                {
                    "uri": f"github://pulls/{repo_name}/{pr_number}",
                    "mimeType": "application/json",
                    "text": self._format_json(pull)
                }
            ]
        }
    
    def _handle_pull_commits_resource(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """
        Handle GitHub pull request commits resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            pr_number: Pull request number
            
        Returns:
            Resource response
        """
        commits = self.github_service.pr.list_pull_request_commits(repo_name, pr_number)
        
        return {
            "contents": [
                {
                    "uri": f"github://pulls/{repo_name}/{pr_number}/commits",
                    "mimeType": "application/json",
                    "text": self._format_json({"commits": commits, "count": len(commits)})
                }
            ]
        }
    
    def _handle_pull_files_resource(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """
        Handle GitHub pull request files resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            pr_number: Pull request number
            
        Returns:
            Resource response
        """
        files = self.github_service.pr.list_pull_request_files(repo_name, pr_number)
        
        return {
            "contents": [
                {
                    "uri": f"github://pulls/{repo_name}/{pr_number}/files",
                    "mimeType": "application/json",
                    "text": self._format_json({"files": files, "count": len(files)})
                }
            ]
        }
    
    def _handle_pull_comments_resource(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """
        Handle GitHub pull request comments resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            pr_number: Pull request number
            
        Returns:
            Resource response
        """
        comments = self.github_service.pr.list_pull_request_comments(repo_name, pr_number)
        
        return {
            "contents": [
                {
                    "uri": f"github://pulls/{repo_name}/{pr_number}/comments",
                    "mimeType": "application/json",
                    "text": self._format_json({"comments": comments, "count": len(comments)})
                }
            ]
        }
    
    def _handle_pull_reviews_resource(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """
        Handle GitHub pull request reviews resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            pr_number: Pull request number
            
        Returns:
            Resource response
        """
        comments = self.github_service.pr.list_pull_request_review_comments(repo_name, pr_number)
        
        return {
            "contents": [
                {
                    "uri": f"github://pulls/{repo_name}/{pr_number}/reviews",
                    "mimeType": "application/json",
                    "text": self._format_json({"reviewComments": comments, "count": len(comments)})
                }
            ]
        }