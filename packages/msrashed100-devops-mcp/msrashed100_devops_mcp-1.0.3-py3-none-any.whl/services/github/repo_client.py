"""
GitHub repository client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.github.client import GitHubService


class GitHubRepoClient:
    """Client for GitHub repository operations."""
    
    def __init__(self, github_service: GitHubService):
        """
        Initialize the GitHub repository client.
        
        Args:
            github_service: The base GitHub service
        """
        self.github = github_service
        self.logger = github_service.logger
    
    def list_repositories(self, username: Optional[str] = None, 
                        org_name: Optional[str] = None,
                        type: str = "all") -> List[Dict[str, Any]]:
        """
        List GitHub repositories.
        
        Args:
            username: Username (optional)
            org_name: Organization name (optional)
            type: Repository type (all, owner, public, private, member)
            
        Returns:
            List of repositories
        """
        try:
            if org_name:
                # Get organization repositories
                org = self.github.get_organization(org_name)
                repos = list(org.get_repos(type=type))
            elif username:
                # Get user repositories
                user = self.github.get_user(username)
                repos = list(user.get_repos(type=type))
            else:
                # Get authenticated user repositories
                user = self.github.get_user()
                repos = list(user.get_repos(type=type))
            
            # Convert to dictionaries
            repo_list = []
            for repo in repos:
                repo_list.append({
                    "id": repo.id,
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "html_url": repo.html_url,
                    "language": repo.language,
                    "stargazers_count": repo.stargazers_count,
                    "forks_count": repo.forks_count,
                    "open_issues_count": repo.open_issues_count,
                    "private": repo.private,
                    "created_at": repo.created_at.isoformat() if repo.created_at else None,
                    "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                    "pushed_at": repo.pushed_at.isoformat() if repo.pushed_at else None,
                    "default_branch": repo.default_branch
                })
            
            return repo_list
        except Exception as e:
            self.github._handle_error("list_repositories", e)
            return None  # Add a return statement to avoid None being returned implicitly
    
    def get_repository(self, repo_name: str) -> Dict[str, Any]:
        """
        Get details of a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Repository details
        """
        try:
            repo = self.github.get_repo(repo_name)
            
            return {
                "id": repo.id,
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "html_url": repo.html_url,
                "language": repo.language,
                "stargazers_count": repo.stargazers_count,
                "forks_count": repo.forks_count,
                "open_issues_count": repo.open_issues_count,
                "private": repo.private,
                "created_at": repo.created_at.isoformat() if repo.created_at else None,
                "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                "pushed_at": repo.pushed_at.isoformat() if repo.pushed_at else None,
                "default_branch": repo.default_branch,
                "topics": repo.get_topics(),
                "license": repo.license.name if repo.license else None,
                "subscribers_count": repo.subscribers_count,
                "network_count": repo.network_count,
                "size": repo.size,
                "archived": repo.archived,
                "disabled": repo.disabled,
                "fork": repo.fork,
                "has_issues": repo.has_issues,
                "has_projects": repo.has_projects,
                "has_wiki": repo.has_wiki,
                "has_pages": repo.has_pages,
                "has_downloads": repo.has_downloads
            }
        except Exception as e:
            self.github._handle_error(f"get_repository({repo_name})", e)
            return None  # Add a return statement to avoid None being returned implicitly
    
    def list_branches(self, repo_name: str) -> List[Dict[str, Any]]:
        """
        List branches in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            List of branches
        """
        try:
            repo = self.github.get_repo(repo_name)
            branches = list(repo.get_branches())
            
            # Convert to dictionaries
            branch_list = []
            for branch in branches:
                branch_list.append({
                    "name": branch.name,
                    "protected": branch.protected,
                    "commit": {
                        "sha": branch.commit.sha,
                        "url": branch.commit.url
                    }
                })
            
            return branch_list
        except Exception as e:
            self.github._handle_error(f"list_branches({repo_name})", e)
            return None  # Add a return statement to avoid None being returned implicitly
    
    def get_branch(self, repo_name: str, branch_name: str) -> Dict[str, Any]:
        """
        Get details of a branch in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            branch_name: Branch name
            
        Returns:
            Branch details
        """
        try:
            repo = self.github.get_repo(repo_name)
            branch = repo.get_branch(branch_name)
            
            return {
                "name": branch.name,
                "protected": branch.protected,
                "commit": {
                    "sha": branch.commit.sha,
                    "url": branch.commit.url
                }
            }
        except Exception as e:
            self.github._handle_error(f"get_branch({repo_name}, {branch_name})", e)
            return None  # Add a return statement to avoid None being returned implicitly
    
    def list_commits(self, repo_name: str, branch: Optional[str] = None,
                   path: Optional[str] = None, author: Optional[str] = None,
                   since: Optional[str] = None, until: Optional[str] = None,
                   max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List commits in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            branch: Branch name (optional)
            path: File path (optional)
            author: Author name (optional)
            since: Start date (ISO format) (optional)
            until: End date (ISO format) (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of commits
        """
        try:
            # Get the repository owner and name
            parts = repo_name.split('/')
            if len(parts) != 2:
                raise ValueError(f"Invalid repository name format: {repo_name}. Expected format: owner/repo")
            
            owner, repo = parts
            
            # Build the API URL
            url = f"repos/{owner}/{repo}/commits"
            
            # Build query parameters
            params = {}
            if branch:
                params['sha'] = branch
            if path:
                params['path'] = path
            if author:
                params['author'] = author
            if since:
                params['since'] = since
            if until:
                params['until'] = until
            if max_results:
                params['per_page'] = min(max_results, 100)  # GitHub API limit is 100 per page
            
            # Make the API request
            self.github.logger.info(f"Getting commits for {repo_name} with params: {params}")
            
            # Use the GitHub API directly
            response = self.github.session.get(
                f"{self.github.base_url}/{url}",
                params=params,
                headers=self.github.headers
            )
            
            # Check for errors
            if response.status_code != 200:
                self.github.logger.error(f"Error getting commits: {response.status_code} {response.text}")
                return None
            
            # Parse the response
            commits_data = response.json()
            
            # Limit the number of results
            if max_results and len(commits_data) > max_results:
                commits_data = commits_data[:max_results]
            
            # Convert to our format
            commit_list = []
            for commit in commits_data:
                commit_list.append({
                    "sha": commit.get("sha"),
                    "html_url": commit.get("html_url"),
                    "commit": {
                        "message": commit.get("commit", {}).get("message"),
                        "author": {
                            "name": commit.get("commit", {}).get("author", {}).get("name"),
                            "email": commit.get("commit", {}).get("author", {}).get("email"),
                            "date": commit.get("commit", {}).get("author", {}).get("date")
                        },
                        "committer": {
                            "name": commit.get("commit", {}).get("committer", {}).get("name"),
                            "email": commit.get("commit", {}).get("committer", {}).get("email"),
                            "date": commit.get("commit", {}).get("committer", {}).get("date")
                        }
                    },
                    "author": {
                        "login": commit.get("author", {}).get("login") if commit.get("author") else None,
                        "id": commit.get("author", {}).get("id") if commit.get("author") else None,
                        "avatar_url": commit.get("author", {}).get("avatar_url") if commit.get("author") else None
                    } if commit.get("author") else None,
                    "committer": {
                        "login": commit.get("committer", {}).get("login") if commit.get("committer") else None,
                        "id": commit.get("committer", {}).get("id") if commit.get("committer") else None,
                        "avatar_url": commit.get("committer", {}).get("avatar_url") if commit.get("committer") else None
                    } if commit.get("committer") else None
                })
            
            self.github.logger.info(f"Successfully got {len(commit_list)} commits")
            return commit_list
        except Exception as e:
            self.github.logger.error(f"Error in list_commits({repo_name}): {str(e)}")
            return []  # Return empty list instead of None to avoid NoneType errors
    
    def get_commit(self, repo_name: str, commit_sha: str) -> Dict[str, Any]:
        """
        Get details of a commit in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            commit_sha: Commit SHA
            
        Returns:
            Commit details
        """
        try:
            repo = self.github.get_repo(repo_name)
            commit = repo.get_commit(commit_sha)
            
            return {
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
                } if commit.committer else None,
                "stats": {
                    "additions": commit.stats.additions,
                    "deletions": commit.stats.deletions,
                    "total": commit.stats.total
                },
                "files": [
                    {
                        "filename": file.filename,
                        "additions": file.additions,
                        "deletions": file.deletions,
                        "changes": file.changes,
                        "status": file.status,
                        "raw_url": file.raw_url,
                        "blob_url": file.blob_url,
                        "patch": file.patch
                    } for file in commit.files
                ]
            }
        except Exception as e:
            self.github._handle_error(f"get_commit({repo_name}, {commit_sha})", e)
    
    def list_contents(self, repo_name: str, path: str = "", ref: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List contents of a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            path: Directory path (default: root)
            ref: Branch, tag, or commit SHA (optional)
            
        Returns:
            List of contents
        """
        try:
            repo = self.github.get_repo(repo_name)
            contents = repo.get_contents(path, ref=ref)
            
            # Handle case where contents is a single file
            if not isinstance(contents, list):
                contents = [contents]
            
            # Convert to dictionaries
            content_list = []
            for content in contents:
                content_list.append({
                    "name": content.name,
                    "path": content.path,
                    "sha": content.sha,
                    "size": content.size,
                    "type": content.type,
                    "download_url": content.download_url,
                    "html_url": content.html_url,
                    "git_url": content.git_url,
                    "url": content.url
                })
            
            return content_list
        except Exception as e:
            self.github._handle_error(f"list_contents({repo_name}, {path})", e)
    
    def get_content(self, repo_name: str, path: str, ref: Optional[str] = None) -> Dict[str, Any]:
        """
        Get content of a file in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            path: File path
            ref: Branch, tag, or commit SHA (optional)
            
        Returns:
            File content
        """
        try:
            repo = self.github.get_repo(repo_name)
            content = repo.get_contents(path, ref=ref)
            
            # Handle case where content is a directory
            if isinstance(content, list):
                raise ValueError(f"Path '{path}' is a directory, not a file")
            
            return {
                "name": content.name,
                "path": content.path,
                "sha": content.sha,
                "size": content.size,
                "type": content.type,
                "encoding": content.encoding,
                "content": content.decoded_content.decode('utf-8') if content.encoding == 'base64' else None,
                "download_url": content.download_url,
                "html_url": content.html_url,
                "git_url": content.git_url,
                "url": content.url
            }
        except Exception as e:
            self.github._handle_error(f"get_content({repo_name}, {path})", e)