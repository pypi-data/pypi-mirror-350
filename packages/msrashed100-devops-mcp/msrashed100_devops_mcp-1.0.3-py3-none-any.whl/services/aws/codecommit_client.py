"""
AWS CodeCommit Client.
"""
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError

from utils.logging import setup_logger
from services.aws.client import AWSService

class AWSCodeCommitClient:
    """Client for interacting with AWS CodeCommit."""

    def __init__(self, base_service: AWSService):
        """
        Initialize CodeCommit client.

        Args:
            base_service: The base AWSService instance.
        """
        self.service_name = "codecommit"
        self.client = base_service.get_client(self.service_name)
        self.logger = setup_logger(f"devops_mcp_server.services.aws.{self.service_name}")

    def list_repositories(self, sort_by: Optional[str] = None, order: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Gets information about one or more repositories.

        Args:
            sort_by: The criterion to use to sort the results. Valid values include: repositoryName, lastModifiedDate.
            order: The order in which to sort the results. Valid values include: ascending, descending.
        
        Returns:
            A list of repository metadata objects.
        """
        self.logger.info(f"Listing CodeCommit repositories with sort_by: {sort_by}, order: {order}")
        try:
            params = {}
            if sort_by:
                params['sortBy'] = sort_by
            if order:
                params['order'] = order
            
            repositories = []
            paginator = self.client.get_paginator('list_repositories')
            page_iterator = paginator.paginate(**params)
            for page in page_iterator:
                repositories.extend(page.get("repositories", []))
            self.logger.info(f"Successfully listed {len(repositories)} CodeCommit repositories.")
            return repositories
        except ClientError as e:
            self.logger.error(f"Error listing CodeCommit repositories: {e}")
            raise

    def get_repository(self, repository_name: str) -> Dict[str, Any]:
        """
        Returns information about a repository.

        Args:
            repository_name: The name of the repository to get information about.

        Returns:
            A dictionary containing the repository metadata.
        """
        self.logger.info(f"Getting CodeCommit repository: {repository_name}")
        try:
            response = self.client.get_repository(repositoryName=repository_name)
            self.logger.info(f"Successfully retrieved CodeCommit repository: {repository_name}")
            return response.get("repositoryMetadata", {})
        except ClientError as e:
            self.logger.error(f"Error getting CodeCommit repository {repository_name}: {e}")
            raise

    def list_branches(self, repository_name: str) -> List[str]:
        """
        Gets information about one or more branches in a repository.

        Args:
            repository_name: The name of the repository that contains the branches.

        Returns:
            A list of branch names.
        """
        self.logger.info(f"Listing branches for CodeCommit repository: {repository_name}")
        try:
            branches = []
            paginator = self.client.get_paginator('list_branches')
            page_iterator = paginator.paginate(repositoryName=repository_name)
            for page in page_iterator:
                branches.extend(page.get("branches", []))
            self.logger.info(f"Successfully listed {len(branches)} branches for repository: {repository_name}")
            return branches
        except ClientError as e:
            self.logger.error(f"Error listing branches for CodeCommit repository {repository_name}: {e}")
            raise

    def get_branch(self, repository_name: str, branch_name: str) -> Dict[str, Any]:
        """
        Returns information about a branch.

        Args:
            repository_name: The name of the repository that contains the branch.
            branch_name: The name of the branch to retrieve.

        Returns:
            A dictionary containing the branch information.
        """
        self.logger.info(f"Getting branch {branch_name} for CodeCommit repository: {repository_name}")
        try:
            response = self.client.get_branch(repositoryName=repository_name, branchName=branch_name)
            self.logger.info(f"Successfully retrieved branch {branch_name} for repository: {repository_name}")
            return response.get("branch", {})
        except ClientError as e:
            self.logger.error(f"Error getting branch {branch_name} for CodeCommit repository {repository_name}: {e}")
            raise