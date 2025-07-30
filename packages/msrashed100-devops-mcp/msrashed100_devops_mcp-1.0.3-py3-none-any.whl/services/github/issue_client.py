"""
GitHub issues client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.github.client import GitHubService


class GitHubIssueClient:
    """Client for GitHub issues operations."""
    
    def __init__(self, github_service: GitHubService):
        """
        Initialize the GitHub issues client.
        
        Args:
            github_service: The base GitHub service
        """
        self.github = github_service
        self.logger = github_service.logger
    
    def list_issues(self, repo_name: str, state: str = "open", 
                  labels: Optional[List[str]] = None, 
                  sort: str = "created", direction: str = "desc",
                  since: Optional[str] = None,
                  max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List issues in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            state: Issue state (open, closed, all)
            labels: List of label names
            sort: Sort field (created, updated, comments)
            direction: Sort direction (asc, desc)
            since: Only issues updated after this time (ISO format)
            max_results: Maximum number of results to return
            
        Returns:
            List of issues
        """
        try:
            repo = self.github.get_repo(repo_name)
            
            # Convert ISO date to datetime object
            since_date = None
            if since:
                from datetime import datetime
                since_date = datetime.fromisoformat(since.replace('Z', '+00:00'))
            
            # Get issues
            issues = list(repo.get_issues(state=state, labels=labels, sort=sort, 
                                       direction=direction, since=since_date)[:max_results])
            
            # Convert to dictionaries
            issue_list = []
            for issue in issues:
                # Skip pull requests
                if issue.pull_request is not None:
                    continue
                
                issue_list.append({
                    "id": issue.id,
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "locked": issue.locked,
                    "html_url": issue.html_url,
                    "created_at": issue.created_at.isoformat() if issue.created_at else None,
                    "updated_at": issue.updated_at.isoformat() if issue.updated_at else None,
                    "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                    "labels": [label.name for label in issue.labels],
                    "user": {
                        "login": issue.user.login,
                        "id": issue.user.id,
                        "avatar_url": issue.user.avatar_url
                    } if issue.user else None,
                    "assignees": [
                        {
                            "login": assignee.login,
                            "id": assignee.id,
                            "avatar_url": assignee.avatar_url
                        } for assignee in issue.assignees
                    ],
                    "milestone": {
                        "id": issue.milestone.id,
                        "number": issue.milestone.number,
                        "title": issue.milestone.title,
                        "state": issue.milestone.state,
                        "due_on": issue.milestone.due_on.isoformat() if issue.milestone.due_on else None
                    } if issue.milestone else None,
                    "comments": issue.comments,
                    "body": issue.body
                })
            
            return issue_list
        except Exception as e:
            self.github._handle_error(f"list_issues({repo_name})", e)
    
    def get_issue(self, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """
        Get details of an issue in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            issue_number: Issue number
            
        Returns:
            Issue details
        """
        try:
            repo = self.github.get_repo(repo_name)
            issue = repo.get_issue(issue_number)
            
            # Skip pull requests
            if issue.pull_request is not None:
                raise ValueError(f"Issue #{issue_number} is a pull request")
            
            return {
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "state": issue.state,
                "locked": issue.locked,
                "html_url": issue.html_url,
                "created_at": issue.created_at.isoformat() if issue.created_at else None,
                "updated_at": issue.updated_at.isoformat() if issue.updated_at else None,
                "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                "labels": [label.name for label in issue.labels],
                "user": {
                    "login": issue.user.login,
                    "id": issue.user.id,
                    "avatar_url": issue.user.avatar_url
                } if issue.user else None,
                "assignees": [
                    {
                        "login": assignee.login,
                        "id": assignee.id,
                        "avatar_url": assignee.avatar_url
                    } for assignee in issue.assignees
                ],
                "milestone": {
                    "id": issue.milestone.id,
                    "number": issue.milestone.number,
                    "title": issue.milestone.title,
                    "state": issue.milestone.state,
                    "due_on": issue.milestone.due_on.isoformat() if issue.milestone.due_on else None
                } if issue.milestone else None,
                "comments": issue.comments,
                "body": issue.body
            }
        except Exception as e:
            self.github._handle_error(f"get_issue({repo_name}, {issue_number})", e)
    
    def list_issue_comments(self, repo_name: str, issue_number: int, 
                          max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List comments on an issue in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            issue_number: Issue number
            max_results: Maximum number of results to return
            
        Returns:
            List of comments
        """
        try:
            repo = self.github.get_repo(repo_name)
            issue = repo.get_issue(issue_number)
            comments = list(issue.get_comments()[:max_results])
            
            # Convert to dictionaries
            comment_list = []
            for comment in comments:
                comment_list.append({
                    "id": comment.id,
                    "html_url": comment.html_url,
                    "created_at": comment.created_at.isoformat() if comment.created_at else None,
                    "updated_at": comment.updated_at.isoformat() if comment.updated_at else None,
                    "user": {
                        "login": comment.user.login,
                        "id": comment.user.id,
                        "avatar_url": comment.user.avatar_url
                    } if comment.user else None,
                    "body": comment.body
                })
            
            return comment_list
        except Exception as e:
            self.github._handle_error(f"list_issue_comments({repo_name}, {issue_number})", e)
    
    def list_issue_events(self, repo_name: str, issue_number: int, 
                        max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List events on an issue in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            issue_number: Issue number
            max_results: Maximum number of results to return
            
        Returns:
            List of events
        """
        try:
            repo = self.github.get_repo(repo_name)
            issue = repo.get_issue(issue_number)
            events = list(issue.get_events()[:max_results])
            
            # Convert to dictionaries
            event_list = []
            for event in events:
                event_list.append({
                    "id": event.id,
                    "event": event.event,
                    "created_at": event.created_at.isoformat() if event.created_at else None,
                    "actor": {
                        "login": event.actor.login,
                        "id": event.actor.id,
                        "avatar_url": event.actor.avatar_url
                    } if event.actor else None,
                    "commit_id": event.commit_id,
                    "commit_url": event.commit_url,
                    "label": {
                        "name": event.label.name,
                        "color": event.label.color
                    } if event.label else None
                })
            
            return event_list
        except Exception as e:
            self.github._handle_error(f"list_issue_events({repo_name}, {issue_number})", e)
    
    def list_labels(self, repo_name: str) -> List[Dict[str, Any]]:
        """
        List labels in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            List of labels
        """
        try:
            repo = self.github.get_repo(repo_name)
            labels = list(repo.get_labels())
            
            # Convert to dictionaries
            label_list = []
            for label in labels:
                label_list.append({
                    "id": label.id,
                    "name": label.name,
                    "color": label.color,
                    "description": label.description,
                    "url": label.url
                })
            
            return label_list
        except Exception as e:
            self.github._handle_error(f"list_labels({repo_name})", e)
    
    def get_label(self, repo_name: str, label_name: str) -> Dict[str, Any]:
        """
        Get details of a label in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            label_name: Label name
            
        Returns:
            Label details
        """
        try:
            repo = self.github.get_repo(repo_name)
            label = repo.get_label(label_name)
            
            return {
                "id": label.id,
                "name": label.name,
                "color": label.color,
                "description": label.description,
                "url": label.url
            }
        except Exception as e:
            self.github._handle_error(f"get_label({repo_name}, {label_name})", e)
    
    def list_milestones(self, repo_name: str, state: str = "open", 
                      sort: str = "due_on", direction: str = "asc") -> List[Dict[str, Any]]:
        """
        List milestones in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            state: Milestone state (open, closed, all)
            sort: Sort field (due_on, completeness)
            direction: Sort direction (asc, desc)
            
        Returns:
            List of milestones
        """
        try:
            repo = self.github.get_repo(repo_name)
            milestones = list(repo.get_milestones(state=state, sort=sort, direction=direction))
            
            # Convert to dictionaries
            milestone_list = []
            for milestone in milestones:
                milestone_list.append({
                    "id": milestone.id,
                    "number": milestone.number,
                    "title": milestone.title,
                    "description": milestone.description,
                    "state": milestone.state,
                    "created_at": milestone.created_at.isoformat() if milestone.created_at else None,
                    "updated_at": milestone.updated_at.isoformat() if milestone.updated_at else None,
                    "due_on": milestone.due_on.isoformat() if milestone.due_on else None,
                    "closed_at": milestone.closed_at.isoformat() if milestone.closed_at else None,
                    "html_url": milestone.html_url,
                    "open_issues": milestone.open_issues,
                    "closed_issues": milestone.closed_issues
                })
            
            return milestone_list
        except Exception as e:
            self.github._handle_error(f"list_milestones({repo_name})", e)
    
    def get_milestone(self, repo_name: str, milestone_number: int) -> Dict[str, Any]:
        """
        Get details of a milestone in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            milestone_number: Milestone number
            
        Returns:
            Milestone details
        """
        try:
            repo = self.github.get_repo(repo_name)
            milestone = repo.get_milestone(milestone_number)
            
            return {
                "id": milestone.id,
                "number": milestone.number,
                "title": milestone.title,
                "description": milestone.description,
                "state": milestone.state,
                "created_at": milestone.created_at.isoformat() if milestone.created_at else None,
                "updated_at": milestone.updated_at.isoformat() if milestone.updated_at else None,
                "due_on": milestone.due_on.isoformat() if milestone.due_on else None,
                "closed_at": milestone.closed_at.isoformat() if milestone.closed_at else None,
                "html_url": milestone.html_url,
                "open_issues": milestone.open_issues,
                "closed_issues": milestone.closed_issues
            }
        except Exception as e:
            self.github._handle_error(f"get_milestone({repo_name}, {milestone_number})", e)