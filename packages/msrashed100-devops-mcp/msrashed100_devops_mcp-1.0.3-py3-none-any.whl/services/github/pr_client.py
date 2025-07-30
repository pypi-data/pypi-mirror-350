"""
GitHub pull requests client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.github.client import GitHubService


class GitHubPRClient:
    """Client for GitHub pull requests operations."""
    
    def __init__(self, github_service: GitHubService):
        """
        Initialize the GitHub pull requests client.
        
        Args:
            github_service: The base GitHub service
        """
        self.github = github_service
        self.logger = github_service.logger
    
    def list_pull_requests(self, repo_name: str, state: str = "open", 
                         sort: str = "created", direction: str = "desc",
                         base: Optional[str] = None, head: Optional[str] = None,
                         max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List pull requests in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            state: Pull request state (open, closed, all)
            sort: Sort field (created, updated, popularity, long-running)
            direction: Sort direction (asc, desc)
            base: Base branch filter
            head: Head branch filter
            max_results: Maximum number of results to return
            
        Returns:
            List of pull requests
        """
        try:
            repo = self.github.get_repo(repo_name)
            
            # Get pull requests
            pulls = list(repo.get_pulls(state=state, sort=sort, direction=direction, 
                                      base=base, head=head)[:max_results])
            
            # Convert to dictionaries
            pr_list = []
            for pr in pulls:
                pr_list.append({
                    "id": pr.id,
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "locked": pr.locked,
                    "html_url": pr.html_url,
                    "created_at": pr.created_at.isoformat() if pr.created_at else None,
                    "updated_at": pr.updated_at.isoformat() if pr.updated_at else None,
                    "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                    "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                    "labels": [label.name for label in pr.labels],
                    "user": {
                        "login": pr.user.login,
                        "id": pr.user.id,
                        "avatar_url": pr.user.avatar_url
                    } if pr.user else None,
                    "assignees": [
                        {
                            "login": assignee.login,
                            "id": assignee.id,
                            "avatar_url": assignee.avatar_url
                        } for assignee in pr.assignees
                    ],
                    "milestone": {
                        "id": pr.milestone.id,
                        "number": pr.milestone.number,
                        "title": pr.milestone.title,
                        "state": pr.milestone.state,
                        "due_on": pr.milestone.due_on.isoformat() if pr.milestone.due_on else None
                    } if pr.milestone else None,
                    "draft": pr.draft,
                    "merged": pr.merged,
                    "mergeable": pr.mergeable,
                    "mergeable_state": pr.mergeable_state,
                    "merged_by": {
                        "login": pr.merged_by.login,
                        "id": pr.merged_by.id,
                        "avatar_url": pr.merged_by.avatar_url
                    } if pr.merged_by else None,
                    "comments": pr.comments,
                    "commits": pr.commits,
                    "additions": pr.additions,
                    "deletions": pr.deletions,
                    "changed_files": pr.changed_files,
                    "base": {
                        "ref": pr.base.ref,
                        "sha": pr.base.sha,
                        "label": pr.base.label
                    },
                    "head": {
                        "ref": pr.head.ref,
                        "sha": pr.head.sha,
                        "label": pr.head.label
                    },
                    "body": pr.body
                })
            
            return pr_list
        except Exception as e:
            self.github._handle_error(f"list_pull_requests({repo_name})", e)
    
    def get_pull_request(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """
        Get details of a pull request in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            pr_number: Pull request number
            
        Returns:
            Pull request details
        """
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            
            return {
                "id": pr.id,
                "number": pr.number,
                "title": pr.title,
                "state": pr.state,
                "locked": pr.locked,
                "html_url": pr.html_url,
                "created_at": pr.created_at.isoformat() if pr.created_at else None,
                "updated_at": pr.updated_at.isoformat() if pr.updated_at else None,
                "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                "labels": [label.name for label in pr.labels],
                "user": {
                    "login": pr.user.login,
                    "id": pr.user.id,
                    "avatar_url": pr.user.avatar_url
                } if pr.user else None,
                "assignees": [
                    {
                        "login": assignee.login,
                        "id": assignee.id,
                        "avatar_url": assignee.avatar_url
                    } for assignee in pr.assignees
                ],
                "milestone": {
                    "id": pr.milestone.id,
                    "number": pr.milestone.number,
                    "title": pr.milestone.title,
                    "state": pr.milestone.state,
                    "due_on": pr.milestone.due_on.isoformat() if pr.milestone.due_on else None
                } if pr.milestone else None,
                "draft": pr.draft,
                "merged": pr.merged,
                "mergeable": pr.mergeable,
                "mergeable_state": pr.mergeable_state,
                "merged_by": {
                    "login": pr.merged_by.login,
                    "id": pr.merged_by.id,
                    "avatar_url": pr.merged_by.avatar_url
                } if pr.merged_by else None,
                "comments": pr.comments,
                "commits": pr.commits,
                "additions": pr.additions,
                "deletions": pr.deletions,
                "changed_files": pr.changed_files,
                "base": {
                    "ref": pr.base.ref,
                    "sha": pr.base.sha,
                    "label": pr.base.label
                },
                "head": {
                    "ref": pr.head.ref,
                    "sha": pr.head.sha,
                    "label": pr.head.label
                },
                "body": pr.body
            }
        except Exception as e:
            self.github._handle_error(f"get_pull_request({repo_name}, {pr_number})", e)
    
    def list_pull_request_commits(self, repo_name: str, pr_number: int, 
                                max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List commits in a pull request.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            pr_number: Pull request number
            max_results: Maximum number of results to return
            
        Returns:
            List of commits
        """
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            commits = list(pr.get_commits()[:max_results])
            
            # Convert to dictionaries
            commit_list = []
            for commit in commits:
                commit_list.append({
                    "sha": commit.sha,
                    "html_url": commit.html_url,
                    "commit": {
                        "message": commit.commit.message,
                        "author": {
                            "name": commit.commit.author.name,
                            "email": commit.commit.author.email,
                            "date": commit.commit.author.date.isoformat() if commit.commit.author.date else None
                        },
                        "committer": {
                            "name": commit.commit.committer.name,
                            "email": commit.commit.committer.email,
                            "date": commit.commit.committer.date.isoformat() if commit.commit.committer.date else None
                        }
                    },
                    "author": {
                        "login": commit.author.login if commit.author else None,
                        "id": commit.author.id if commit.author else None,
                        "avatar_url": commit.author.avatar_url if commit.author else None
                    } if commit.author else None,
                    "committer": {
                        "login": commit.committer.login if commit.committer else None,
                        "id": commit.committer.id if commit.committer else None,
                        "avatar_url": commit.committer.avatar_url if commit.committer else None
                    } if commit.committer else None
                })
            
            return commit_list
        except Exception as e:
            self.github._handle_error(f"list_pull_request_commits({repo_name}, {pr_number})", e)
    
    def list_pull_request_files(self, repo_name: str, pr_number: int, 
                              max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List files in a pull request.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            pr_number: Pull request number
            max_results: Maximum number of results to return
            
        Returns:
            List of files
        """
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            files = list(pr.get_files()[:max_results])
            
            # Convert to dictionaries
            file_list = []
            for file in files:
                file_list.append({
                    "filename": file.filename,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "status": file.status,
                    "raw_url": file.raw_url,
                    "blob_url": file.blob_url,
                    "patch": file.patch
                })
            
            return file_list
        except Exception as e:
            self.github._handle_error(f"list_pull_request_files({repo_name}, {pr_number})", e)
    
    def list_pull_request_comments(self, repo_name: str, pr_number: int, 
                                 max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List comments on a pull request.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            pr_number: Pull request number
            max_results: Maximum number of results to return
            
        Returns:
            List of comments
        """
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            comments = list(pr.get_issue_comments()[:max_results])
            
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
            self.github._handle_error(f"list_pull_request_comments({repo_name}, {pr_number})", e)
    
    def list_pull_request_review_comments(self, repo_name: str, pr_number: int, 
                                        max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List review comments on a pull request.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            pr_number: Pull request number
            max_results: Maximum number of results to return
            
        Returns:
            List of review comments
        """
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            comments = list(pr.get_comments()[:max_results])
            
            # Convert to dictionaries
            comment_list = []
            for comment in comments:
                comment_list.append({
                    "id": comment.id,
                    "html_url": comment.html_url,
                    "diff_hunk": comment.diff_hunk,
                    "path": comment.path,
                    "position": comment.position,
                    "original_position": comment.original_position,
                    "commit_id": comment.commit_id,
                    "original_commit_id": comment.original_commit_id,
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
            self.github._handle_error(f"list_pull_request_review_comments({repo_name}, {pr_number})", e)