"""
GitHub repository resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.github.service import GitHubServiceManager
from resources.github.base_resources import GitHubBaseResources
from utils.logging import setup_logger


class GitHubRepoResources(GitHubBaseResources):
    """GitHub repository resources."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub repository resources.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        super().__init__(mcp, github_service)
        self.logger = setup_logger("devops_mcp_server.resources.github.repo")
    
    def get_resource_templates(self) -> List[Dict[str, str]]:
        """
        Get repository resource templates.
        
        Returns:
            List of resource templates
        """
        templates = []
        
        # Repository templates
        templates.append({
            "uriTemplate": "github://repos",
            "name": "GitHub Repositories",
            "mimeType": "application/json",
            "description": "List GitHub repositories for the authenticated user"
        })
        
        templates.append({
            "uriTemplate": "github://repo/{owner}/{repo}",
            "name": "GitHub Repository",
            "mimeType": "application/json",
            "description": "Get details of a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://repo/{owner}/{repo}/branches",
            "name": "GitHub Branches",
            "mimeType": "application/json",
            "description": "List branches in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://repo/{owner}/{repo}/branch/{branch}",
            "name": "GitHub Branch",
            "mimeType": "application/json",
            "description": "Get details of a branch in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://repo/{owner}/{repo}/commits",
            "name": "GitHub Commits",
            "mimeType": "application/json",
            "description": "List commits in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://repo/{owner}/{repo}/commit/{sha}",
            "name": "GitHub Commit",
            "mimeType": "application/json",
            "description": "Get details of a commit in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://repo/{owner}/{repo}/contents/{path}",
            "name": "GitHub Contents",
            "mimeType": "application/json",
            "description": "Get contents of a file or directory in a GitHub repository"
        })
        
        return templates
    
    def handle_resource(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Handle repository resources.
        
        Args:
            path: Resource path
            
        Returns:
            Resource response or None if not handled
        """
        if path == "repos":
            return self._handle_repos_resource()
        elif path.startswith("repo/"):
            repo_path = path[len("repo/"):]
            if "/" not in repo_path:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid repository path: {repo_path}. Format should be 'owner/repo'"
                )
            
            if "/" not in repo_path[repo_path.find("/")+1:]:
                # Repository details
                return self._handle_repo_resource(repo_path)
            else:
                parts = repo_path.split("/", 3)
                owner = parts[0]
                repo = parts[1]
                resource_type = parts[2]
                
                if resource_type == "branches":
                    return self._handle_branches_resource(f"{owner}/{repo}")
                elif resource_type == "branch" and len(parts) > 3:
                    branch_name = parts[3]
                    return self._handle_branch_resource(f"{owner}/{repo}", branch_name)
                elif resource_type == "commits":
                    return self._handle_commits_resource(f"{owner}/{repo}")
                elif resource_type == "commit" and len(parts) > 3:
                    commit_sha = parts[3]
                    return self._handle_commit_resource(f"{owner}/{repo}", commit_sha)
                elif resource_type == "contents":
                    path_parts = repo_path.split("/", 3)
                    if len(path_parts) > 3:
                        file_path = path_parts[3]
                        return self._handle_contents_resource(f"{owner}/{repo}", file_path)
                    else:
                        return self._handle_contents_resource(f"{owner}/{repo}")
        
        return None
    
    def _handle_repos_resource(self) -> Dict[str, Any]:
        """
        Handle GitHub repositories resource.
        
        Returns:
            Resource response
        """
        repos = self.github_service.repo.list_repositories()
        
        return {
            "contents": [
                {
                    "uri": "github://repos",
                    "mimeType": "application/json",
                    "text": self._format_json({"repositories": repos, "count": len(repos)})
                }
            ]
        }
    
    def _handle_repo_resource(self, repo_name: str) -> Dict[str, Any]:
        """
        Handle GitHub repository resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Resource response
        """
        repo = self.github_service.repo.get_repository(repo_name)
        
        return {
            "contents": [
                {
                    "uri": f"github://repo/{repo_name}",
                    "mimeType": "application/json",
                    "text": self._format_json(repo)
                }
            ]
        }
    
    def _handle_branches_resource(self, repo_name: str) -> Dict[str, Any]:
        """
        Handle GitHub branches resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Resource response
        """
        branches = self.github_service.repo.list_branches(repo_name)
        
        return {
            "contents": [
                {
                    "uri": f"github://repo/{repo_name}/branches",
                    "mimeType": "application/json",
                    "text": self._format_json({"branches": branches, "count": len(branches)})
                }
            ]
        }
    
    def _handle_branch_resource(self, repo_name: str, branch_name: str) -> Dict[str, Any]:
        """
        Handle GitHub branch resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            branch_name: Branch name
            
        Returns:
            Resource response
        """
        branch = self.github_service.repo.get_branch(repo_name, branch_name)
        
        return {
            "contents": [
                {
                    "uri": f"github://repo/{repo_name}/branch/{branch_name}",
                    "mimeType": "application/json",
                    "text": self._format_json(branch)
                }
            ]
        }
    
    def _handle_commits_resource(self, repo_name: str) -> Dict[str, Any]:
        """
        Handle GitHub commits resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Resource response
        """
        commits = self.github_service.repo.list_commits(repo_name)
        
        return {
            "contents": [
                {
                    "uri": f"github://repo/{repo_name}/commits",
                    "mimeType": "application/json",
                    "text": self._format_json({"commits": commits, "count": len(commits)})
                }
            ]
        }
    
    def _handle_commit_resource(self, repo_name: str, commit_sha: str) -> Dict[str, Any]:
        """
        Handle GitHub commit resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            commit_sha: Commit SHA
            
        Returns:
            Resource response
        """
        commit = self.github_service.repo.get_commit(repo_name, commit_sha)
        
        return {
            "contents": [
                {
                    "uri": f"github://repo/{repo_name}/commit/{commit_sha}",
                    "mimeType": "application/json",
                    "text": self._format_json(commit)
                }
            ]
        }
    
    def _handle_contents_resource(self, repo_name: str, path: str = "") -> Dict[str, Any]:
        """
        Handle GitHub contents resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            path: File or directory path
            
        Returns:
            Resource response
        """
        try:
            # Try to get file content
            content = self.github_service.repo.get_content(repo_name, path)
            return {
                "contents": [
                    {
                        "uri": f"github://repo/{repo_name}/contents/{path}",
                        "mimeType": "application/json",
                        "text": self._format_json(content)
                    }
                ]
            }
        except ValueError:
            # If path is a directory, list contents
            contents = self.github_service.repo.list_contents(repo_name, path)
            return {
                "contents": [
                    {
                        "uri": f"github://repo/{repo_name}/contents/{path}",
                        "mimeType": "application/json",
                        "text": self._format_json({"contents": contents, "count": len(contents)})
                    }
                ]
            }