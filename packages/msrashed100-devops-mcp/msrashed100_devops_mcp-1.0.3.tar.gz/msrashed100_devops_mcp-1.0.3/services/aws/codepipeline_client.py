"""
AWS CodePipeline Client.
"""
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError

from utils.logging import setup_logger
from services.aws.client import AWSService

class AWSCodePipelineClient:
    """Client for interacting with AWS CodePipeline."""

    def __init__(self, base_service: AWSService):
        """
        Initialize CodePipeline client.

        Args:
            base_service: The base AWSService instance.
        """
        self.service_name = "codepipeline"
        self.client = base_service.get_client(self.service_name)
        self.logger = setup_logger(f"devops_mcp_server.services.aws.{self.service_name}")

    def list_pipelines(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Lists all pipelines in AWS CodePipeline.

        Args:
            max_results: The maximum number of pipelines to return.

        Returns:
            A list of pipelines.
        """
        self.logger.info(f"Listing CodePipelines with max_results: {max_results}")
        try:
            pipelines = []
            paginator = self.client.get_paginator('list_pipelines')
            page_iterator = paginator.paginate(PaginationConfig={'MaxItems': max_results})
            for page in page_iterator:
                pipelines.extend(page.get("pipelines", []))
            self.logger.info(f"Successfully listed {len(pipelines)} CodePipelines.")
            return pipelines
        except ClientError as e:
            self.logger.error(f"Error listing CodePipelines: {e}")
            raise

    def get_pipeline(self, name: str) -> Dict[str, Any]:
        """
        Returns the summary of a pipeline.

        Args:
            name: The name of the pipeline to retrieve.

        Returns:
            A dictionary containing the pipeline structure and metadata.
        """
        self.logger.info(f"Getting CodePipeline: {name}")
        try:
            response = self.client.get_pipeline(name=name)
            self.logger.info(f"Successfully retrieved CodePipeline: {name}")
            return response # Contains 'pipeline' and 'metadata'
        except ClientError as e:
            self.logger.error(f"Error getting CodePipeline {name}: {e}")
            raise

    def list_pipeline_executions(self, pipeline_name: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Gets a summary of the most recent executions for a pipeline.

        Args:
            pipeline_name: The name of the pipeline.
            max_results: The maximum number of executions to return.

        Returns:
            A list of pipeline execution summaries.
        """
        self.logger.info(f"Listing executions for CodePipeline: {pipeline_name}")
        try:
            executions = []
            paginator = self.client.get_paginator('list_pipeline_executions')
            page_iterator = paginator.paginate(pipelineName=pipeline_name, PaginationConfig={'MaxItems': max_results})
            for page in page_iterator:
                executions.extend(page.get("pipelineExecutionSummaries", []))
            self.logger.info(f"Successfully listed {len(executions)} executions for CodePipeline: {pipeline_name}")
            return executions
        except ClientError as e:
            self.logger.error(f"Error listing executions for CodePipeline {pipeline_name}: {e}")
            raise

    def get_pipeline_execution(self, pipeline_name: str, pipeline_execution_id: str) -> Dict[str, Any]:
        """
        Returns information about an execution of a pipeline.

        Args:
            pipeline_name: The name of the pipeline.
            pipeline_execution_id: The ID of the pipeline execution.

        Returns:
            A dictionary containing the pipeline execution details.
        """
        self.logger.info(f"Getting execution {pipeline_execution_id} for CodePipeline: {pipeline_name}")
        try:
            response = self.client.get_pipeline_execution(
                pipelineName=pipeline_name,
                pipelineExecutionId=pipeline_execution_id
            )
            self.logger.info(f"Successfully retrieved execution {pipeline_execution_id}")
            return response.get("pipelineExecution", {})
        except ClientError as e:
            self.logger.error(f"Error getting execution {pipeline_execution_id} for CodePipeline {pipeline_name}: {e}")
            raise

    def list_action_executions(self, pipeline_name: str, pipeline_execution_id: Optional[str] = None, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Lists the action executions that have occurred in a pipeline.

        Args:
            pipeline_name: The name of the pipeline.
            pipeline_execution_id: Filter by pipeline execution ID (optional).
            max_results: The maximum number of results to return.

        Returns:
            A list of action execution details.
        """
        self.logger.info(f"Listing action executions for pipeline: {pipeline_name}")
        try:
            action_executions = []
            paginator = self.client.get_paginator('list_action_executions')
            filter_params = {}
            if pipeline_execution_id:
                filter_params['pipelineExecutionId'] = pipeline_execution_id

            page_iterator = paginator.paginate(
                pipelineName=pipeline_name,
                filter=filter_params if filter_params else None, # API expects filter or it errors
                PaginationConfig={'MaxItems': max_results}
            )
            for page in page_iterator:
                action_executions.extend(page.get("actionExecutionDetails", []))
            self.logger.info(f"Successfully listed {len(action_executions)} action executions for pipeline: {pipeline_name}")
            return action_executions
        except ClientError as e:
            self.logger.error(f"Error listing action executions for pipeline {pipeline_name}: {e}")
            raise