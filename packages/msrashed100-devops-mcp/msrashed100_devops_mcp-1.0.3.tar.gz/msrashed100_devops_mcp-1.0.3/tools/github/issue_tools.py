"""
GitHub issues tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.github.service import GitHubServiceManager
from tools.github.base_tools import GitHubBaseTools
from utils.logging import setup_logger


class GitHubIssueTools(GitHubBaseTools):
    """Tools for GitHub issues operations."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub issues tools.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        super().__init__(mcp, github_service)
        self.logger = setup_logger("devops_mcp_server.tools.github.issue")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register GitHub issues tools with the MCP server."""
        
        @self.mcp.tool()
        def list_github_issues(repo_name: str, state: str = "open", 
                            labels: str = None, sort: str = "created", 
                            direction: str = "desc", since: str = None,
                            max_results: int = 100) -> str:
            """
            List issues in a GitHub repository.
            
            This tool lists issues in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                state: Issue state (open, closed, all) (default: open)
                labels: Comma-separated list of label names (optional)
                sort: Sort field (created, updated, comments) (default: created)
                direction: Sort direction (asc, desc) (default: desc)
                since: Only issues updated after this time (ISO format) (optional)
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of issues in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate state
            valid_states = ["open", "closed", "all"]
            if state not in valid_states:
                return self._format_error(f"Invalid state. Must be one of: {', '.join(valid_states)}")
            
            # Validate sort
            valid_sorts = ["created", "updated", "comments"]
            if sort not in valid_sorts:
                return self._format_error(f"Invalid sort. Must be one of: {', '.join(valid_sorts)}")
            
            # Validate direction
            valid_directions = ["asc", "desc"]
            if direction not in valid_directions:
                return self._format_error(f"Invalid direction. Must be one of: {', '.join(valid_directions)}")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            # Parse labels
            label_list = None
            if labels:
                label_list = [label.strip() for label in labels.split(",")]
            
            try:
                issues = self.github_service.issue.list_issues(
                    repo_name, state, label_list, sort, direction, since, max_results
                )
                return self._format_response({"issues": issues, "count": len(issues)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub issues: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_issue(repo_name: str, issue_number: int) -> str:
            """
            Get details of an issue in a GitHub repository.
            
            This tool retrieves details of an issue in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                issue_number: Issue number
                
            Returns:
                Issue details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                issue = self.github_service.issue.get_issue(repo_name, issue_number)
                return self._format_response(issue)
            except Exception as e:
                self.logger.error(f"Error getting GitHub issue: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_issue_comments(repo_name: str, issue_number: int, 
                                    max_results: int = 100) -> str:
            """
            List comments on an issue in a GitHub repository.
            
            This tool lists comments on an issue in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                issue_number: Issue number
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of comments in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                comments = self.github_service.issue.list_issue_comments(
                    repo_name, issue_number, max_results
                )
                return self._format_response({"comments": comments, "count": len(comments)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub issue comments: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_issue_events(repo_name: str, issue_number: int, 
                                  max_results: int = 100) -> str:
            """
            List events on an issue in a GitHub repository.
            
            This tool lists events on an issue in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                issue_number: Issue number
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of events in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                events = self.github_service.issue.list_issue_events(
                    repo_name, issue_number, max_results
                )
                return self._format_response({"events": events, "count": len(events)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub issue events: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_labels(repo_name: str) -> str:
            """
            List labels in a GitHub repository.
            
            This tool lists labels in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                
            Returns:
                List of labels in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                labels = self.github_service.issue.list_labels(repo_name)
                return self._format_response({"labels": labels, "count": len(labels)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub labels: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_label(repo_name: str, label_name: str) -> str:
            """
            Get details of a label in a GitHub repository.
            
            This tool retrieves details of a label in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                label_name: Label name
                
            Returns:
                Label details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                label = self.github_service.issue.get_label(repo_name, label_name)
                return self._format_response(label)
            except Exception as e:
                self.logger.error(f"Error getting GitHub label: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_milestones(repo_name: str, state: str = "open", 
                                sort: str = "due_on", direction: str = "asc") -> str:
            """
            List milestones in a GitHub repository.
            
            This tool lists milestones in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                state: Milestone state (open, closed, all) (default: open)
                sort: Sort field (due_on, completeness) (default: due_on)
                direction: Sort direction (asc, desc) (default: asc)
                
            Returns:
                List of milestones in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate state
            valid_states = ["open", "closed", "all"]
            if state not in valid_states:
                return self._format_error(f"Invalid state. Must be one of: {', '.join(valid_states)}")
            
            # Validate sort
            valid_sorts = ["due_on", "completeness"]
            if sort not in valid_sorts:
                return self._format_error(f"Invalid sort. Must be one of: {', '.join(valid_sorts)}")
            
            # Validate direction
            valid_directions = ["asc", "desc"]
            if direction not in valid_directions:
                return self._format_error(f"Invalid direction. Must be one of: {', '.join(valid_directions)}")
            
            try:
                milestones = self.github_service.issue.list_milestones(
                    repo_name, state, sort, direction
                )
                return self._format_response({"milestones": milestones, "count": len(milestones)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub milestones: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_milestone(repo_name: str, milestone_number: int) -> str:
            """
            Get details of a milestone in a GitHub repository.
            
            This tool retrieves details of a milestone in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                milestone_number: Milestone number
                
            Returns:
                Milestone details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                milestone = self.github_service.issue.get_milestone(repo_name, milestone_number)
                return self._format_response(milestone)
            except Exception as e:
                self.logger.error(f"Error getting GitHub milestone: {e}")
                return self._format_error(str(e))