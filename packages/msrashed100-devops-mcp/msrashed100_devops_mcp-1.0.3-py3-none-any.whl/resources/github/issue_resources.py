"""
GitHub issue resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.github.service import GitHubServiceManager
from resources.github.base_resources import GitHubBaseResources
from utils.logging import setup_logger


class GitHubIssueResources(GitHubBaseResources):
    """GitHub issue resources."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub issue resources.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        super().__init__(mcp, github_service)
        self.logger = setup_logger("devops_mcp_server.resources.github.issue")
    
    def get_resource_templates(self) -> List[Dict[str, str]]:
        """
        Get issue resource templates.
        
        Returns:
            List of resource templates
        """
        templates = []
        
        # Issue templates
        templates.append({
            "uriTemplate": "github://issues/{owner}/{repo}",
            "name": "GitHub Issues",
            "mimeType": "application/json",
            "description": "List issues in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://issues/{owner}/{repo}/{issue_number}",
            "name": "GitHub Issue",
            "mimeType": "application/json",
            "description": "Get details of an issue in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://issues/{owner}/{repo}/{issue_number}/comments",
            "name": "GitHub Issue Comments",
            "mimeType": "application/json",
            "description": "List comments on an issue in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://issues/{owner}/{repo}/{issue_number}/events",
            "name": "GitHub Issue Events",
            "mimeType": "application/json",
            "description": "List events on an issue in a GitHub repository"
        })
        
        # Label templates
        templates.append({
            "uriTemplate": "github://labels/{owner}/{repo}",
            "name": "GitHub Labels",
            "mimeType": "application/json",
            "description": "List labels in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://labels/{owner}/{repo}/{label_name}",
            "name": "GitHub Label",
            "mimeType": "application/json",
            "description": "Get details of a label in a GitHub repository"
        })
        
        # Milestone templates
        templates.append({
            "uriTemplate": "github://milestones/{owner}/{repo}",
            "name": "GitHub Milestones",
            "mimeType": "application/json",
            "description": "List milestones in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://milestones/{owner}/{repo}/{milestone_number}",
            "name": "GitHub Milestone",
            "mimeType": "application/json",
            "description": "Get details of a milestone in a GitHub repository"
        })
        
        return templates
    
    def handle_resource(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Handle issue resources.
        
        Args:
            path: Resource path
            
        Returns:
            Resource response or None if not handled
        """
        # Issue resources
        if path.startswith("issues/"):
            repo_path = path[len("issues/"):]
            if "/" not in repo_path:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid repository path: {repo_path}. Format should be 'owner/repo'"
                )
            
            if "/" not in repo_path[repo_path.find("/")+1:]:
                # List issues
                return self._handle_issues_resource(repo_path)
            else:
                parts = repo_path.split("/", 3)
                owner = parts[0]
                repo = parts[1]
                
                if len(parts) > 2 and parts[2].isdigit():
                    issue_number = int(parts[2])
                    if len(parts) > 3:
                        if parts[3] == "comments":
                            return self._handle_issue_comments_resource(f"{owner}/{repo}", issue_number)
                        elif parts[3] == "events":
                            return self._handle_issue_events_resource(f"{owner}/{repo}", issue_number)
                    else:
                        return self._handle_issue_resource(f"{owner}/{repo}", issue_number)
        
        # Label resources
        elif path.startswith("labels/"):
            repo_path = path[len("labels/"):]
            if "/" not in repo_path:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid repository path: {repo_path}. Format should be 'owner/repo'"
                )
            
            parts = repo_path.split("/", 2)
            owner = parts[0]
            repo = parts[1]
            
            if len(parts) > 2:
                label_name = parts[2]
                return self._handle_label_resource(f"{owner}/{repo}", label_name)
            else:
                return self._handle_labels_resource(f"{owner}/{repo}")
        
        # Milestone resources
        elif path.startswith("milestones/"):
            repo_path = path[len("milestones/"):]
            if "/" not in repo_path:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid repository path: {repo_path}. Format should be 'owner/repo'"
                )
            
            parts = repo_path.split("/", 2)
            owner = parts[0]
            repo = parts[1]
            
            if len(parts) > 2 and parts[2].isdigit():
                milestone_number = int(parts[2])
                return self._handle_milestone_resource(f"{owner}/{repo}", milestone_number)
            else:
                return self._handle_milestones_resource(f"{owner}/{repo}")
        
        return None
    
    def _handle_issues_resource(self, repo_name: str) -> Dict[str, Any]:
        """
        Handle GitHub issues resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Resource response
        """
        issues = self.github_service.issue.list_issues(repo_name)
        
        return {
            "contents": [
                {
                    "uri": f"github://issues/{repo_name}",
                    "mimeType": "application/json",
                    "text": self._format_json({"issues": issues, "count": len(issues)})
                }
            ]
        }
    
    def _handle_issue_resource(self, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """
        Handle GitHub issue resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            issue_number: Issue number
            
        Returns:
            Resource response
        """
        issue = self.github_service.issue.get_issue(repo_name, issue_number)
        
        return {
            "contents": [
                {
                    "uri": f"github://issues/{repo_name}/{issue_number}",
                    "mimeType": "application/json",
                    "text": self._format_json(issue)
                }
            ]
        }
    
    def _handle_issue_comments_resource(self, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """
        Handle GitHub issue comments resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            issue_number: Issue number
            
        Returns:
            Resource response
        """
        comments = self.github_service.issue.list_issue_comments(repo_name, issue_number)
        
        return {
            "contents": [
                {
                    "uri": f"github://issues/{repo_name}/{issue_number}/comments",
                    "mimeType": "application/json",
                    "text": self._format_json({"comments": comments, "count": len(comments)})
                }
            ]
        }
    
    def _handle_issue_events_resource(self, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """
        Handle GitHub issue events resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            issue_number: Issue number
            
        Returns:
            Resource response
        """
        events = self.github_service.issue.list_issue_events(repo_name, issue_number)
        
        return {
            "contents": [
                {
                    "uri": f"github://issues/{repo_name}/{issue_number}/events",
                    "mimeType": "application/json",
                    "text": self._format_json({"events": events, "count": len(events)})
                }
            ]
        }
    
    def _handle_labels_resource(self, repo_name: str) -> Dict[str, Any]:
        """
        Handle GitHub labels resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Resource response
        """
        labels = self.github_service.issue.list_labels(repo_name)
        
        return {
            "contents": [
                {
                    "uri": f"github://labels/{repo_name}",
                    "mimeType": "application/json",
                    "text": self._format_json({"labels": labels, "count": len(labels)})
                }
            ]
        }
    
    def _handle_label_resource(self, repo_name: str, label_name: str) -> Dict[str, Any]:
        """
        Handle GitHub label resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            label_name: Label name
            
        Returns:
            Resource response
        """
        label = self.github_service.issue.get_label(repo_name, label_name)
        
        return {
            "contents": [
                {
                    "uri": f"github://labels/{repo_name}/{label_name}",
                    "mimeType": "application/json",
                    "text": self._format_json(label)
                }
            ]
        }
    
    def _handle_milestones_resource(self, repo_name: str) -> Dict[str, Any]:
        """
        Handle GitHub milestones resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Resource response
        """
        milestones = self.github_service.issue.list_milestones(repo_name)
        
        return {
            "contents": [
                {
                    "uri": f"github://milestones/{repo_name}",
                    "mimeType": "application/json",
                    "text": self._format_json({"milestones": milestones, "count": len(milestones)})
                }
            ]
        }
    
    def _handle_milestone_resource(self, repo_name: str, milestone_number: int) -> Dict[str, Any]:
        """
        Handle GitHub milestone resource.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            milestone_number: Milestone number
            
        Returns:
            Resource response
        """
        milestone = self.github_service.issue.get_milestone(repo_name, milestone_number)
        
        return {
            "contents": [
                {
                    "uri": f"github://milestones/{repo_name}/{milestone_number}",
                    "mimeType": "application/json",
                    "text": self._format_json(milestone)
                }
            ]
        }