"""
AWS CodeBuild tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from mcp.server.fastmcp import FastMCP
from services.aws.service import AWSServiceManager
from utils.logging import setup_logger
from tools.aws.base_tools import AWSBaseTools


class AWSCodeBuildTools(AWSBaseTools):
    """Tools for interacting with AWS CodeBuild."""

    def __init__(self, mcp: FastMCP, aws_service: AWSServiceManager):
        """
        Initialize AWS CodeBuild tools.

        Args:
            mcp: The MCP server instance.
            aws_service: The AWS service manager instance.
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.codebuild")
        self._register_tools()

    def _register_tools(self) -> None:
        """Register CodeBuild tools with the MCP server."""

        @self.mcp.tool()
        def list_codebuild_projects(sort_by: Optional[str] = None, sort_order: Optional[str] = None) -> str:
            """
            Gets a list of build project names, with optional sorting.

            Args:
                sort_by: The criterion to list build project names (NAME, CREATED_TIME, LAST_MODIFIED_TIME).
                sort_order: The order to list results (ASCENDING, DESCENDING).
            
            Returns:
                A list of build project names in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            valid_sort_by = ["NAME", "CREATED_TIME", "LAST_MODIFIED_TIME"]
            valid_sort_order = ["ASCENDING", "DESCENDING"]

            if sort_by and sort_by not in valid_sort_by:
                return self._format_error(f"Invalid sort_by value. Must be one of {valid_sort_by}")
            if sort_order and sort_order not in valid_sort_order:
                return self._format_error(f"Invalid sort_order value. Must be one of {valid_sort_order}")

            try:
                project_names = self.aws_service.codebuild.list_projects(sort_by=sort_by, sort_order=sort_order)
                return self._format_response({"project_names": project_names, "count": len(project_names)})
            except Exception as e:
                self.logger.error(f"Error listing CodeBuild projects: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_codebuild_projects_details(names: str) -> str: # Expect comma-separated string for names
            """
            Gets information about one or more build projects.

            Args:
                names: A comma-separated string of build project names or ARNs.
            
            Returns:
                A list of build projects in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                name_list = [name.strip() for name in names.split(',')]
                if not name_list or not all(name_list):
                     return self._format_error("Project names cannot be empty.")
                projects = self.aws_service.codebuild.batch_get_projects(names=name_list)
                return self._format_response({"projects": projects, "count": len(projects)})
            except Exception as e:
                self.logger.error(f"Error getting CodeBuild projects details: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def list_codebuild_project_builds(project_name: str, sort_order: Optional[str] = None) -> str:
            """
            Gets a list of build IDs for the specified build project, with optional sorting.

            Args:
                project_name: The name of the CodeBuild project.
                sort_order: The order to list results (ASCENDING, DESCENDING).
            
            Returns:
                A list of build IDs in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")

            valid_sort_order = ["ASCENDING", "DESCENDING"]
            if sort_order and sort_order not in valid_sort_order:
                return self._format_error(f"Invalid sort_order value. Must be one of {valid_sort_order}")

            try:
                build_ids = self.aws_service.codebuild.list_builds_for_project(project_name=project_name, sort_order=sort_order)
                return self._format_response({"build_ids": build_ids, "count": len(build_ids)})
            except Exception as e:
                self.logger.error(f"Error listing builds for CodeBuild project {project_name}: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_codebuild_builds_details(ids: str) -> str: # Expect comma-separated string for ids
            """
            Gets information about one or more builds.

            Args:
                ids: A comma-separated string of build IDs.
            
            Returns:
                A list of builds in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                id_list = [id.strip() for id in ids.split(',')]
                if not id_list or not all(id_list):
                     return self._format_error("Build IDs cannot be empty.")
                builds = self.aws_service.codebuild.batch_get_builds(ids=id_list)
                return self._format_response({"builds": builds, "count": len(builds)})
            except Exception as e:
                self.logger.error(f"Error getting CodeBuild builds details: {e}")
                return self._format_error(str(e))

        self.logger.info("AWS CodeBuild tools registered successfully")