"""
AWS CodeBuild Client.
"""
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError

from utils.logging import setup_logger
from services.aws.client import AWSService

class AWSCodeBuildClient:
    """Client for interacting with AWS CodeBuild."""

    def __init__(self, base_service: AWSService):
        """
        Initialize CodeBuild client.

        Args:
            base_service: The base AWSService instance.
        """
        self.service_name = "codebuild"
        self.client = base_service.get_client(self.service_name)
        self.logger = setup_logger(f"devops_mcp_server.services.aws.{self.service_name}")

    def list_projects(self, sort_by: Optional[str] = None, sort_order: Optional[str] = None) -> List[str]:
        """
        Gets a list of build project names, with optional sorting.

        Args:
            sort_by: The criterion to be used to list build project names. Valid values include: NAME, CREATED_TIME, LAST_MODIFIED_TIME.
            sort_order: The order in which to list results. Valid values include: ASCENDING, DESCENDING.

        Returns:
            A list of build project names.
        """
        self.logger.info(f"Listing CodeBuild projects with sort_by: {sort_by}, sort_order: {sort_order}")
        try:
            params = {}
            if sort_by:
                params['sortBy'] = sort_by
            if sort_order:
                params['sortOrder'] = sort_order
            
            project_names = []
            paginator = self.client.get_paginator('list_projects')
            page_iterator = paginator.paginate(**params)
            for page in page_iterator:
                project_names.extend(page.get("projects", []))
            self.logger.info(f"Successfully listed {len(project_names)} CodeBuild projects.")
            return project_names
        except ClientError as e:
            self.logger.error(f"Error listing CodeBuild projects: {e}")
            raise

    def batch_get_projects(self, names: List[str]) -> List[Dict[str, Any]]:
        """
        Gets information about one or more build projects.

        Args:
            names: A list of build project names or ARNs.

        Returns:
            A list of build projects.
        """
        self.logger.info(f"Getting CodeBuild projects by names: {names}")
        if not names:
            return []
        try:
            # batch_get_projects can take up to 100 names
            projects_data = []
            for i in range(0, len(names), 100):
                chunk = names[i:i + 100]
                response = self.client.batch_get_projects(names=chunk)
                projects_data.extend(response.get("projects", []))
            
            self.logger.info(f"Successfully retrieved {len(projects_data)} CodeBuild projects.")
            return projects_data
        except ClientError as e:
            self.logger.error(f"Error getting CodeBuild projects by names: {e}")
            raise

    def list_builds_for_project(self, project_name: str, sort_order: Optional[str] = None) -> List[str]:
        """
        Gets a list of build IDs for the specified build project, with optional sorting.

        Args:
            project_name: The name of the CodeBuild project.
            sort_order: The order in which to list results. Valid values include: ASCENDING, DESCENDING.

        Returns:
            A list of build IDs.
        """
        self.logger.info(f"Listing builds for CodeBuild project: {project_name}")
        try:
            params = {'projectName': project_name}
            if sort_order:
                params['sortOrder'] = sort_order

            build_ids = []
            paginator = self.client.get_paginator('list_builds_for_project')
            page_iterator = paginator.paginate(**params)
            for page in page_iterator:
                build_ids.extend(page.get("ids", []))
            self.logger.info(f"Successfully listed {len(build_ids)} builds for project: {project_name}")
            return build_ids
        except ClientError as e:
            self.logger.error(f"Error listing builds for CodeBuild project {project_name}: {e}")
            raise

    def batch_get_builds(self, ids: List[str]) -> List[Dict[str, Any]]:
        """
        Gets information about one or more builds.

        Args:
            ids: A list of build IDs.

        Returns:
            A list of builds.
        """
        self.logger.info(f"Getting CodeBuild builds by IDs: {ids}")
        if not ids:
            return []
        try:
            # batch_get_builds can take up to 100 ids
            builds_data = []
            for i in range(0, len(ids), 100):
                chunk = ids[i:i + 100]
                response = self.client.batch_get_builds(ids=chunk)
                builds_data.extend(response.get("builds", []))

            self.logger.info(f"Successfully retrieved {len(builds_data)} CodeBuild builds.")
            return builds_data
        except ClientError as e:
            self.logger.error(f"Error getting CodeBuild builds by IDs: {e}")
            raise