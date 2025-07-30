"""
AWS CodePipeline tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from services.aws.service import AWSServiceManager
from utils.logging import setup_logger
from tools.aws.base_tools import AWSBaseTools


class AWSCodePipelineTools(AWSBaseTools):
    """Tools for interacting with AWS CodePipeline."""

    def __init__(self, mcp: FastMCP, aws_service: AWSServiceManager):
        """
        Initialize AWS CodePipeline tools.

        Args:
            mcp: The MCP server instance.
            aws_service: The AWS service manager instance.
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.codepipeline")
        self._register_tools()

    def _register_tools(self) -> None:
        """Register CodePipeline tools with the MCP server."""

        @self.mcp.tool()
        def list_codepipelines(max_results: int = 50) -> str:
            """
            Lists all pipelines in AWS CodePipeline.

            Args:
                max_results: The maximum number of pipelines to return (default: 50).
            
            Returns:
                A list of pipelines in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                pipelines = self.aws_service.codepipeline.list_pipelines(max_results=max_results)
                return self._format_response({"pipelines": pipelines, "count": len(pipelines)})
            except Exception as e:
                self.logger.error(f"Error listing CodePipelines: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_codepipeline(name: str) -> str:
            """
            Returns the summary of a pipeline.

            Args:
                name: The name of the pipeline to retrieve.
            
            Returns:
                A dictionary containing the pipeline structure and metadata in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                pipeline_data = self.aws_service.codepipeline.get_pipeline(name=name)
                return self._format_response(pipeline_data)
            except Exception as e:
                self.logger.error(f"Error getting CodePipeline {name}: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def list_codepipeline_executions(pipeline_name: str, max_results: int = 50) -> str:
            """
            Gets a summary of the most recent executions for a pipeline.

            Args:
                pipeline_name: The name of the pipeline.
                max_results: The maximum number of executions to return (default: 50).
            
            Returns:
                A list of pipeline execution summaries in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                executions = self.aws_service.codepipeline.list_pipeline_executions(pipeline_name=pipeline_name, max_results=max_results)
                return self._format_response({"pipeline_execution_summaries": executions, "count": len(executions)})
            except Exception as e:
                self.logger.error(f"Error listing executions for CodePipeline {pipeline_name}: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_codepipeline_execution(pipeline_name: str, pipeline_execution_id: str) -> str:
            """
            Returns information about an execution of a pipeline.

            Args:
                pipeline_name: The name of the pipeline.
                pipeline_execution_id: The ID of the pipeline execution.

            Returns:
                A dictionary containing the pipeline execution details in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")

            try:
                execution_details = self.aws_service.codepipeline.get_pipeline_execution(
                    pipeline_name=pipeline_name,
                    pipeline_execution_id=pipeline_execution_id
                )
                return self._format_response(execution_details)
            except Exception as e:
                self.logger.error(f"Error getting execution {pipeline_execution_id} for CodePipeline {pipeline_name}: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def list_codepipeline_action_executions(pipeline_name: str, pipeline_execution_id: Optional[str] = None, max_results: int = 50) -> str:
            """
            Lists the action executions that have occurred in a pipeline.

            Args:
                pipeline_name: The name of the pipeline.
                pipeline_execution_id: Filter by pipeline execution ID (optional).
                max_results: The maximum number of results to return (default: 50).

            Returns:
                A list of action execution details in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")

            try:
                action_executions = self.aws_service.codepipeline.list_action_executions(
                    pipeline_name=pipeline_name,
                    pipeline_execution_id=pipeline_execution_id,
                    max_results=max_results
                )
                return self._format_response({"action_execution_details": action_executions, "count": len(action_executions)})
            except Exception as e:
                self.logger.error(f"Error listing action executions for CodePipeline {pipeline_name}: {e}")
                return self._format_error(str(e))

        self.logger.info("AWS CodePipeline tools registered successfully")