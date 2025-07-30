"""
AWS CodeCommit tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from services.aws.service import AWSServiceManager
from utils.logging import setup_logger
from tools.aws.base_tools import AWSBaseTools


class AWSCodeCommitTools(AWSBaseTools):
    """Tools for interacting with AWS CodeCommit."""

    def __init__(self, mcp: FastMCP, aws_service: AWSServiceManager):
        """
        Initialize AWS CodeCommit tools.

        Args:
            mcp: The MCP server instance.
            aws_service: The AWS service manager instance.
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.codecommit")
        self._register_tools()

    def _register_tools(self) -> None:
        """Register CodeCommit tools with the MCP server."""

        @self.mcp.tool()
        def list_codecommit_repositories(sort_by: Optional[str] = None, order: Optional[str] = None) -> str:
            """
            Gets information about one or more repositories.

            Args:
                sort_by: The criterion to sort results (repositoryName, lastModifiedDate).
                order: The order to sort results (ascending, descending).
            
            Returns:
                A list of repository metadata objects in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            valid_sort_by = ["repositoryName", "lastModifiedDate"]
            valid_order = ["ascending", "descending"]

            if sort_by and sort_by not in valid_sort_by:
                return self._format_error(f"Invalid sort_by value. Must be one of {valid_sort_by}")
            if order and order not in valid_order:
                return self._format_error(f"Invalid order value. Must be one of {valid_order}")

            try:
                repositories = self.aws_service.codecommit.list_repositories(sort_by=sort_by, order=order)
                return self._format_response({"repositories": repositories, "count": len(repositories)})
            except Exception as e:
                self.logger.error(f"Error listing CodeCommit repositories: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_codecommit_repository(repository_name: str) -> str:
            """
            Returns information about a repository.

            Args:
                repository_name: The name of the repository.
            
            Returns:
                A dictionary containing repository metadata in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                repo_details = self.aws_service.codecommit.get_repository(repository_name=repository_name)
                return self._format_response(repo_details)
            except Exception as e:
                self.logger.error(f"Error getting CodeCommit repository {repository_name}: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def list_codecommit_branches(repository_name: str) -> str:
            """
            Gets information about one or more branches in a repository.

            Args:
                repository_name: The name of the repository.
            
            Returns:
                A list of branch names in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                branches = self.aws_service.codecommit.list_branches(repository_name=repository_name)
                return self._format_response({"branches": branches, "count": len(branches)})
            except Exception as e:
                self.logger.error(f"Error listing branches for CodeCommit repository {repository_name}: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_codecommit_branch(repository_name: str, branch_name: str) -> str:
            """
            Returns information about a branch.

            Args:
                repository_name: The name of the repository.
                branch_name: The name of the branch.
            
            Returns:
                A dictionary containing branch information in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                branch_details = self.aws_service.codecommit.get_branch(repository_name=repository_name, branch_name=branch_name)
                return self._format_response(branch_details)
            except Exception as e:
                self.logger.error(f"Error getting branch {branch_name} for CodeCommit repository {repository_name}: {e}")
                return self._format_error(str(e))

        self.logger.info("AWS CodeCommit tools registered successfully")