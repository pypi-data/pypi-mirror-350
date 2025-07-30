"""
GitHub Actions tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.github.service import GitHubServiceManager
from tools.github.base_tools import GitHubBaseTools
from utils.logging import setup_logger


class GitHubActionsTools(GitHubBaseTools):
    """Tools for GitHub Actions operations."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub Actions tools.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        super().__init__(mcp, github_service)
        self.logger = setup_logger("devops_mcp_server.tools.github.actions")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register GitHub Actions tools with the MCP server."""
        
        @self.mcp.tool()
        def list_github_workflows(repo_name: str) -> str:
            """
            List workflows in a GitHub repository.
            
            This tool lists workflows in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                
            Returns:
                List of workflows in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                workflows = self.github_service.actions.list_workflows(repo_name)
                return self._format_response({"workflows": workflows, "count": len(workflows)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub workflows: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_workflow(repo_name: str, workflow_id: int) -> str:
            """
            Get details of a workflow in a GitHub repository.
            
            This tool retrieves details of a workflow in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                workflow_id: Workflow ID
                
            Returns:
                Workflow details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                workflow = self.github_service.actions.get_workflow(repo_name, workflow_id)
                return self._format_response(workflow)
            except Exception as e:
                self.logger.error(f"Error getting GitHub workflow: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_workflow_runs(repo_name: str, workflow_id: int = None, 
                                   actor: str = None, branch: str = None,
                                   event: str = None, status: str = None,
                                   max_results: int = 100) -> str:
            """
            List workflow runs in a GitHub repository.
            
            This tool lists workflow runs in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                workflow_id: Workflow ID (optional)
                actor: Filter by actor login (optional)
                branch: Filter by branch (optional)
                event: Filter by event type (optional)
                status: Filter by status (optional)
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of workflow runs in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                runs = self.github_service.actions.list_workflow_runs(
                    repo_name, workflow_id, actor, branch, event, status, max_results
                )
                return self._format_response({"workflowRuns": runs, "count": len(runs)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub workflow runs: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_workflow_run(repo_name: str, run_id: int) -> str:
            """
            Get details of a workflow run in a GitHub repository.
            
            This tool retrieves details of a workflow run in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                run_id: Run ID
                
            Returns:
                Workflow run details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                run = self.github_service.actions.get_workflow_run(repo_name, run_id)
                return self._format_response(run)
            except Exception as e:
                self.logger.error(f"Error getting GitHub workflow run: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_workflow_run_jobs(repo_name: str, run_id: int, 
                                       max_results: int = 100) -> str:
            """
            List jobs for a workflow run in a GitHub repository.
            
            This tool lists jobs for a workflow run in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                run_id: Run ID
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of workflow run jobs in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                jobs = self.github_service.actions.list_workflow_run_jobs(
                    repo_name, run_id, max_results
                )
                return self._format_response({"jobs": jobs, "count": len(jobs)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub workflow run jobs: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_workflow_run_artifacts(repo_name: str, run_id: int, 
                                            max_results: int = 100) -> str:
            """
            List artifacts for a workflow run in a GitHub repository.
            
            This tool lists artifacts for a workflow run in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                run_id: Run ID
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of workflow run artifacts in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                artifacts = self.github_service.actions.list_workflow_run_artifacts(
                    repo_name, run_id, max_results
                )
                return self._format_response({"artifacts": artifacts, "count": len(artifacts)})
            except Exception as e:
                self.logger.error(f"Error listing GitHub workflow run artifacts: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_workflow_content(repo_name: str, workflow_id: int) -> str:
            """
            Get content of a workflow file in a GitHub repository.
            
            This tool retrieves content of a workflow file in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                workflow_id: Workflow ID
                
            Returns:
                Workflow file content in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                content = self.github_service.actions.get_workflow_content(repo_name, workflow_id)
                return self._format_response(content)
            except Exception as e:
                self.logger.error(f"Error getting GitHub workflow content: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_repository_secrets(repo_name: str) -> str:
            """
            Get repository secrets.
            
            This tool retrieves secrets from a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                
            Returns:
                Repository secrets in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.get_repository_secrets(repo_name)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting GitHub repository secrets: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_repository_environments(repo_name: str) -> str:
            """
            Get repository environments.
            
            This tool retrieves environments from a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                
            Returns:
                Repository environments in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.get_repository_environments(repo_name)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting GitHub repository environments: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_environment_secrets(repo_name: str, environment_name: str) -> str:
            """
            Get environment secrets.
            
            This tool retrieves secrets from a GitHub repository environment.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                environment_name: Environment name
                
            Returns:
                Environment secrets in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.get_environment_secrets(repo_name, environment_name)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting GitHub environment secrets: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_repository_variables(repo_name: str) -> str:
            """
            Get repository variables.
            
            This tool retrieves variables from a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                
            Returns:
                Repository variables in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.get_repository_variables(repo_name)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting GitHub repository variables: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_environment_variables(repo_name: str, environment_name: str) -> str:
            """
            Get environment variables.
            
            This tool retrieves variables from a GitHub repository environment.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                environment_name: Environment name
                
            Returns:
                Environment variables in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.get_environment_variables(repo_name, environment_name)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting GitHub environment variables: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_workflow_usage(repo_name: str, workflow_id: int) -> str:
            """
            Get workflow usage.
            
            This tool retrieves usage information for a workflow in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                workflow_id: Workflow ID
                
            Returns:
                Workflow usage in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.get_workflow_usage(repo_name, workflow_id)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting GitHub workflow usage: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_github_self_hosted_runners(repo_name: str) -> str:
            """
            List self-hosted runners for a repository.
            
            This tool lists self-hosted runners for a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                
            Returns:
                List of self-hosted runners in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.list_self_hosted_runners(repo_name)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error listing GitHub self-hosted runners: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_github_self_hosted_runner(repo_name: str, runner_id: int) -> str:
            """
            Get a self-hosted runner for a repository.
            
            This tool retrieves details of a self-hosted runner for a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                runner_id: Runner ID
                
            Returns:
                Self-hosted runner details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.get_self_hosted_runner(repo_name, runner_id)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error getting GitHub self-hosted runner: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def create_github_self_hosted_runner_registration_token(repo_name: str) -> str:
            """
            Create a registration token for a self-hosted runner.
            
            This tool creates a registration token for a self-hosted runner for a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                
            Returns:
                Registration token in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.create_self_hosted_runner_registration_token(repo_name)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error creating GitHub self-hosted runner registration token: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def create_github_self_hosted_runner_removal_token(repo_name: str) -> str:
            """
            Create a removal token for a self-hosted runner.
            
            This tool creates a removal token for a self-hosted runner for a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                
            Returns:
                Removal token in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.create_self_hosted_runner_removal_token(repo_name)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error creating GitHub self-hosted runner removal token: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def trigger_github_workflow_dispatch(repo_name: str, workflow_id: int,
                                         ref: str, inputs: str = None) -> str:
            """
            Trigger a workflow dispatch event.
            
            This tool triggers a workflow dispatch event for a workflow in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                workflow_id: Workflow ID
                ref: The git reference (branch or tag) to run the workflow on
                inputs: Optional JSON string of inputs to the workflow
                
            Returns:
                Response data in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                # Parse inputs if provided
                input_dict = None
                if inputs:
                    import json
                    try:
                        input_dict = json.loads(inputs)
                    except json.JSONDecodeError:
                        return self._format_error("Invalid JSON in inputs parameter")
                
                result = self.github_service.actions.trigger_workflow_dispatch(
                    repo_name, workflow_id, ref, input_dict
                )
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error triggering GitHub workflow dispatch: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def cancel_github_workflow_run(repo_name: str, run_id: int) -> str:
            """
            Cancel a workflow run.
            
            This tool cancels a workflow run in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                run_id: Run ID
                
            Returns:
                Response data in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.cancel_workflow_run(repo_name, run_id)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error cancelling GitHub workflow run: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def rerun_github_workflow_run(repo_name: str, run_id: int) -> str:
            """
            Rerun a workflow run.
            
            This tool reruns a workflow run in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                run_id: Run ID
                
            Returns:
                Response data in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.rerun_workflow_run(repo_name, run_id)
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error rerunning GitHub workflow run: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def download_github_workflow_run_logs(repo_name: str, run_id: int, output_path: str) -> str:
            """
            Download logs for a workflow run.
            
            This tool downloads logs for a workflow run in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                run_id: Run ID
                output_path: Path to save the logs
                
            Returns:
                Response data in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.download_workflow_run_logs(
                    repo_name, run_id, output_path
                )
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error downloading GitHub workflow run logs: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def download_github_workflow_run_artifact(repo_name: str, run_id: int,
                                              artifact_id: int, output_path: str) -> str:
            """
            Download an artifact from a workflow run.
            
            This tool downloads an artifact from a workflow run in a GitHub repository.
            
            Args:
                repo_name: Repository name (format: "owner/repo")
                run_id: Run ID
                artifact_id: Artifact ID
                output_path: Path to save the artifact
                
            Returns:
                Response data in JSON format
            """
            if not self._check_service_available():
                return self._format_error("GitHub service is not available")
            
            try:
                result = self.github_service.actions.download_workflow_run_artifact(
                    repo_name, run_id, artifact_id, output_path
                )
                return self._format_response(result)
            except Exception as e:
                self.logger.error(f"Error downloading GitHub workflow run artifact: {e}")
                return self._format_error(str(e))