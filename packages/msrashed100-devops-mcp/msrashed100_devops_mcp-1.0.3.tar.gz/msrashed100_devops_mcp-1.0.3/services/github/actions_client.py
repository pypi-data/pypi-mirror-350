"""
GitHub Actions client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.github.client import GitHubService


class GitHubActionsClient:
    """Client for GitHub Actions operations."""
    
    def __init__(self, github_service: GitHubService):
        """
        Initialize the GitHub Actions client.
        
        Args:
            github_service: The base GitHub service
        """
        self.github = github_service
        self.logger = github_service.logger
    
    def list_workflows(self, repo_name: str) -> List[Dict[str, Any]]:
        """
        List workflows in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            List of workflows
        """
        try:
            repo = self.github.get_repo(repo_name)
            workflows = list(repo.get_workflows())
            
            # Convert to dictionaries
            workflow_list = []
            for workflow in workflows:
                workflow_list.append({
                    "id": workflow.id,
                    "name": workflow.name,
                    "path": workflow.path,
                    "state": workflow.state,
                    "created_at": workflow.created_at.isoformat() if workflow.created_at else None,
                    "updated_at": workflow.updated_at.isoformat() if workflow.updated_at else None,
                    "url": workflow.url,
                    "html_url": workflow.html_url,
                    "badge_url": workflow.badge_url
                })
            
            return workflow_list
        except Exception as e:
            self.github._handle_error(f"list_workflows({repo_name})", e)
    
    def get_workflow(self, repo_name: str, workflow_id: int) -> Dict[str, Any]:
        """
        Get details of a workflow in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            workflow_id: Workflow ID
            
        Returns:
            Workflow details
        """
        try:
            repo = self.github.get_repo(repo_name)
            workflow = repo.get_workflow(workflow_id)
            
            return {
                "id": workflow.id,
                "name": workflow.name,
                "path": workflow.path,
                "state": workflow.state,
                "created_at": workflow.created_at.isoformat() if workflow.created_at else None,
                "updated_at": workflow.updated_at.isoformat() if workflow.updated_at else None,
                "url": workflow.url,
                "html_url": workflow.html_url,
                "badge_url": workflow.badge_url
            }
        except Exception as e:
            self.github._handle_error(f"get_workflow({repo_name}, {workflow_id})", e)
    
    def list_workflow_runs(self, repo_name: str, workflow_id: Optional[int] = None, 
                         actor: Optional[str] = None, branch: Optional[str] = None,
                         event: Optional[str] = None, status: Optional[str] = None,
                         max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List workflow runs in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            workflow_id: Workflow ID (optional)
            actor: Filter by actor login (optional)
            branch: Filter by branch (optional)
            event: Filter by event type (optional)
            status: Filter by status (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of workflow runs
        """
        try:
            repo = self.github.get_repo(repo_name)
            
            # Get workflow runs
            if workflow_id:
                workflow = repo.get_workflow(workflow_id)
                runs = list(workflow.get_runs(actor=actor, branch=branch, event=event, status=status)[:max_results])
            else:
                runs = list(repo.get_workflow_runs(actor=actor, branch=branch, event=event, status=status)[:max_results])
            
            # Convert to dictionaries
            run_list = []
            for run in runs:
                run_list.append({
                    "id": run.id,
                    "name": run.name,
                    "head_branch": run.head_branch,
                    "head_sha": run.head_sha,
                    "run_number": run.run_number,
                    "event": run.event,
                    "status": run.status,
                    "conclusion": run.conclusion,
                    "workflow_id": run.workflow_id,
                    "url": run.url,
                    "html_url": run.html_url,
                    "created_at": run.created_at.isoformat() if run.created_at else None,
                    "updated_at": run.updated_at.isoformat() if run.updated_at else None,
                    "run_started_at": run.run_started_at.isoformat() if run.run_started_at else None
                })
            
            return run_list
        except Exception as e:
            self.github._handle_error(f"list_workflow_runs({repo_name})", e)
    
    def get_workflow_run(self, repo_name: str, run_id: int) -> Dict[str, Any]:
        """
        Get details of a workflow run in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            run_id: Run ID
            
        Returns:
            Workflow run details
        """
        try:
            repo = self.github.get_repo(repo_name)
            run = repo.get_workflow_run(run_id)
            
            return {
                "id": run.id,
                "name": run.name,
                "head_branch": run.head_branch,
                "head_sha": run.head_sha,
                "run_number": run.run_number,
                "event": run.event,
                "status": run.status,
                "conclusion": run.conclusion,
                "workflow_id": run.workflow_id,
                "url": run.url,
                "html_url": run.html_url,
                "created_at": run.created_at.isoformat() if run.created_at else None,
                "updated_at": run.updated_at.isoformat() if run.updated_at else None,
                "run_started_at": run.run_started_at.isoformat() if run.run_started_at else None,
                "jobs_url": run.jobs_url,
                "logs_url": run.logs_url,
                "check_suite_url": run.check_suite_url,
                "artifacts_url": run.artifacts_url,
                "cancel_url": run.cancel_url,
                "rerun_url": run.rerun_url,
                "workflow_url": run.workflow_url
            }
        except Exception as e:
            self.github._handle_error(f"get_workflow_run({repo_name}, {run_id})", e)
    
    def list_workflow_run_jobs(self, repo_name: str, run_id: int, 
                             max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List jobs for a workflow run in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            run_id: Run ID
            max_results: Maximum number of results to return
            
        Returns:
            List of workflow run jobs
        """
        try:
            repo = self.github.get_repo(repo_name)
            run = repo.get_workflow_run(run_id)
            jobs = list(run.get_jobs()[:max_results])
            
            # Convert to dictionaries
            job_list = []
            for job in jobs:
                job_list.append({
                    "id": job.id,
                    "name": job.name,
                    "status": job.status,
                    "conclusion": job.conclusion,
                    "started_at": job.started_at.isoformat() if job.started_at else None,
                    "completed_at": job.completed_at.isoformat() if job.completed_at else None,
                    "url": job.url,
                    "html_url": job.html_url,
                    "steps": [
                        {
                            "name": step.name,
                            "status": step.status,
                            "conclusion": step.conclusion,
                            "number": step.number,
                            "started_at": step.started_at.isoformat() if step.started_at else None,
                            "completed_at": step.completed_at.isoformat() if step.completed_at else None
                        } for step in job.get_steps()
                    ] if hasattr(job, "get_steps") else []
                })
            
            return job_list
        except Exception as e:
            self.github._handle_error(f"list_workflow_run_jobs({repo_name}, {run_id})", e)
    
    def list_workflow_run_artifacts(self, repo_name: str, run_id: int, 
                                  max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List artifacts for a workflow run in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            run_id: Run ID
            max_results: Maximum number of results to return
            
        Returns:
            List of workflow run artifacts
        """
        try:
            repo = self.github.get_repo(repo_name)
            run = repo.get_workflow_run(run_id)
            artifacts = list(run.get_artifacts()[:max_results])
            
            # Convert to dictionaries
            artifact_list = []
            for artifact in artifacts:
                artifact_list.append({
                    "id": artifact.id,
                    "name": artifact.name,
                    "size_in_bytes": artifact.size_in_bytes,
                    "url": artifact.url,
                    "archive_download_url": artifact.archive_download_url,
                    "expired": artifact.expired,
                    "created_at": artifact.created_at.isoformat() if artifact.created_at else None,
                    "updated_at": artifact.updated_at.isoformat() if artifact.updated_at else None
                })
            
            return artifact_list
        except Exception as e:
            self.github._handle_error(f"list_workflow_run_artifacts({repo_name}, {run_id})", e)
    
    def get_workflow_content(self, repo_name: str, workflow_id: int) -> Dict[str, Any]:
        """
        Get content of a workflow file in a GitHub repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            workflow_id: Workflow ID
            
        Returns:
            Workflow file content
        """
        try:
            repo = self.github.get_repo(repo_name)
            workflow = repo.get_workflow(workflow_id)
            content = repo.get_contents(workflow.path)
            
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
            self.github._handle_error(f"get_workflow_content({repo_name}, {workflow_id})", e)
    
    def trigger_workflow_dispatch(self, repo_name: str, workflow_id: int,
                               ref: str, inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Trigger a workflow dispatch event.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            workflow_id: Workflow ID
            ref: The git reference (branch or tag) to run the workflow on
            inputs: Optional inputs to the workflow
            
        Returns:
            Response data
        """
        try:
            repo = self.github.get_repo(repo_name)
            workflow = repo.get_workflow(workflow_id)
            
            # Create workflow dispatch event
            response = workflow.create_dispatch(ref, inputs or {})
            
            return {
                "status": "success",
                "message": f"Workflow dispatch event created for workflow {workflow_id} on {ref}",
                "workflow_id": workflow_id,
                "ref": ref,
                "inputs": inputs or {}
            }
        except Exception as e:
            self.github._handle_error(f"trigger_workflow_dispatch({repo_name}, {workflow_id}, {ref})", e)
    
    def cancel_workflow_run(self, repo_name: str, run_id: int) -> Dict[str, Any]:
        """
        Cancel a workflow run.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            run_id: Run ID
            
        Returns:
            Response data
        """
        try:
            repo = self.github.get_repo(repo_name)
            run = repo.get_workflow_run(run_id)
            
            # Cancel the workflow run
            response = run.cancel()
            
            return {
                "status": "success",
                "message": f"Workflow run {run_id} cancelled",
                "run_id": run_id
            }
        except Exception as e:
            self.github._handle_error(f"cancel_workflow_run({repo_name}, {run_id})", e)
    
    def rerun_workflow_run(self, repo_name: str, run_id: int) -> Dict[str, Any]:
        """
        Rerun a workflow run.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            run_id: Run ID
            
        Returns:
            Response data
        """
        try:
            repo = self.github.get_repo(repo_name)
            run = repo.get_workflow_run(run_id)
            
            # Rerun the workflow run
            response = run.rerun()
            
            return {
                "status": "success",
                "message": f"Workflow run {run_id} rerun initiated",
                "run_id": run_id
            }
        except Exception as e:
            self.github._handle_error(f"rerun_workflow_run({repo_name}, {run_id})", e)
    
    def download_workflow_run_logs(self, repo_name: str, run_id: int, output_path: str) -> Dict[str, Any]:
        """
        Download logs for a workflow run.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            run_id: Run ID
            output_path: Path to save the logs
            
        Returns:
            Response data
        """
        try:
            repo = self.github.get_repo(repo_name)
            run = repo.get_workflow_run(run_id)
            
            # Download the logs
            run.download_logs(output_path)
            
            return {
                "status": "success",
                "message": f"Workflow run {run_id} logs downloaded to {output_path}",
                "run_id": run_id,
                "output_path": output_path
            }
        except Exception as e:
            self.github._handle_error(f"download_workflow_run_logs({repo_name}, {run_id}, {output_path})", e)
    
    def download_workflow_run_artifact(self, repo_name: str, run_id: int,
                                    artifact_id: int, output_path: str) -> Dict[str, Any]:
        """
        Download an artifact from a workflow run.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            run_id: Run ID
            artifact_id: Artifact ID
            output_path: Path to save the artifact
            
        Returns:
            Response data
        """
        try:
            repo = self.github.get_repo(repo_name)
            run = repo.get_workflow_run(run_id)
            
            # Get the artifact
            artifacts = list(run.get_artifacts())
            artifact = next((a for a in artifacts if a.id == artifact_id), None)
            
            if not artifact:
                raise ValueError(f"Artifact {artifact_id} not found in workflow run {run_id}")
            
            # Download the artifact
            artifact.download(output_path)
            
            return {
                "status": "success",
                "message": f"Artifact {artifact_id} downloaded to {output_path}",
                "run_id": run_id,
                "artifact_id": artifact_id,
                "artifact_name": artifact.name,
                "output_path": output_path
            }
        except Exception as e:
            self.github._handle_error(f"download_workflow_run_artifact({repo_name}, {run_id}, {artifact_id}, {output_path})", e)
    
    def get_repository_secrets(self, repo_name: str) -> Dict[str, Any]:
        """
        Get repository secrets.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Repository secrets information
        """
        try:
            repo = self.github.get_repo(repo_name)
            secrets = repo.get_secrets()
            
            # Convert to dictionary
            secrets_list = []
            for secret in secrets:
                secrets_list.append({
                    "name": secret.name,
                    "created_at": secret.created_at.isoformat() if secret.created_at else None,
                    "updated_at": secret.updated_at.isoformat() if secret.updated_at else None
                })
            
            return {
                "secrets": secrets_list,
                "count": len(secrets_list)
            }
        except Exception as e:
            self.github._handle_error(f"get_repository_secrets({repo_name})", e)
    
    def get_repository_environments(self, repo_name: str) -> Dict[str, Any]:
        """
        Get repository environments.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Repository environments information
        """
        try:
            repo = self.github.get_repo(repo_name)
            environments = repo.get_environments()
            
            # Convert to dictionary
            env_list = []
            for env in environments:
                env_list.append({
                    "name": env.name,
                    "id": env.id,
                    "html_url": env.html_url,
                    "created_at": env.created_at.isoformat() if env.created_at else None,
                    "updated_at": env.updated_at.isoformat() if env.updated_at else None
                })
            
            return {
                "environments": env_list,
                "count": len(env_list)
            }
        except Exception as e:
            self.github._handle_error(f"get_repository_environments({repo_name})", e)
    
    def get_environment_secrets(self, repo_name: str, environment_name: str) -> Dict[str, Any]:
        """
        Get environment secrets.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            environment_name: Environment name
            
        Returns:
            Environment secrets information
        """
        try:
            repo = self.github.get_repo(repo_name)
            environment = repo.get_environment(environment_name)
            secrets = environment.get_secrets()
            
            # Convert to dictionary
            secrets_list = []
            for secret in secrets:
                secrets_list.append({
                    "name": secret.name,
                    "created_at": secret.created_at.isoformat() if secret.created_at else None,
                    "updated_at": secret.updated_at.isoformat() if secret.updated_at else None
                })
            
            return {
                "environment": environment_name,
                "secrets": secrets_list,
                "count": len(secrets_list)
            }
        except Exception as e:
            self.github._handle_error(f"get_environment_secrets({repo_name}, {environment_name})", e)
    
    def get_repository_variables(self, repo_name: str) -> Dict[str, Any]:
        """
        Get repository variables.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Repository variables information
        """
        try:
            repo = self.github.get_repo(repo_name)
            variables = repo.get_variables()
            
            # Convert to dictionary
            variables_list = []
            for variable in variables:
                variables_list.append({
                    "name": variable.name,
                    "value": variable.value,
                    "created_at": variable.created_at.isoformat() if variable.created_at else None,
                    "updated_at": variable.updated_at.isoformat() if variable.updated_at else None
                })
            
            return {
                "variables": variables_list,
                "count": len(variables_list)
            }
        except Exception as e:
            self.github._handle_error(f"get_repository_variables({repo_name})", e)
    
    def get_environment_variables(self, repo_name: str, environment_name: str) -> Dict[str, Any]:
        """
        Get environment variables.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            environment_name: Environment name
            
        Returns:
            Environment variables information
        """
        try:
            repo = self.github.get_repo(repo_name)
            environment = repo.get_environment(environment_name)
            variables = environment.get_variables()
            
            # Convert to dictionary
            variables_list = []
            for variable in variables:
                variables_list.append({
                    "name": variable.name,
                    "value": variable.value,
                    "created_at": variable.created_at.isoformat() if variable.created_at else None,
                    "updated_at": variable.updated_at.isoformat() if variable.updated_at else None
                })
            
            return {
                "environment": environment_name,
                "variables": variables_list,
                "count": len(variables_list)
            }
        except Exception as e:
            self.github._handle_error(f"get_environment_variables({repo_name}, {environment_name})", e)
    
    def get_workflow_usage(self, repo_name: str, workflow_id: int) -> Dict[str, Any]:
        """
        Get workflow usage.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            workflow_id: Workflow ID
            
        Returns:
            Workflow usage information
        """
        try:
            repo = self.github.get_repo(repo_name)
            workflow = repo.get_workflow(workflow_id)
            usage = workflow.get_timing()
            
            return {
                "workflow_id": workflow_id,
                "billable": {
                    "ubuntu": usage.billable.get("UBUNTU", {}).get("total_ms", 0),
                    "macos": usage.billable.get("MACOS", {}).get("total_ms", 0),
                    "windows": usage.billable.get("WINDOWS", {}).get("total_ms", 0)
                },
                "run_duration_ms": usage.run_duration_ms
            }
        except Exception as e:
            self.github._handle_error(f"get_workflow_usage({repo_name}, {workflow_id})", e)
    
    def list_self_hosted_runners(self, repo_name: str) -> Dict[str, Any]:
        """
        List self-hosted runners for a repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            List of self-hosted runners
        """
        try:
            repo = self.github.get_repo(repo_name)
            runners = repo.get_self_hosted_runners()
            
            # Convert to dictionary
            runner_list = []
            for runner in runners:
                runner_list.append({
                    "id": runner.id,
                    "name": runner.name,
                    "os": runner.os,
                    "status": runner.status,
                    "busy": runner.busy,
                    "labels": [label.name for label in runner.labels]
                })
            
            return {
                "runners": runner_list,
                "count": len(runner_list)
            }
        except Exception as e:
            self.github._handle_error(f"list_self_hosted_runners({repo_name})", e)
    
    def get_self_hosted_runner(self, repo_name: str, runner_id: int) -> Dict[str, Any]:
        """
        Get a self-hosted runner for a repository.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            runner_id: Runner ID
            
        Returns:
            Self-hosted runner details
        """
        try:
            repo = self.github.get_repo(repo_name)
            runner = repo.get_self_hosted_runner(runner_id)
            
            return {
                "id": runner.id,
                "name": runner.name,
                "os": runner.os,
                "status": runner.status,
                "busy": runner.busy,
                "labels": [label.name for label in runner.labels]
            }
        except Exception as e:
            self.github._handle_error(f"get_self_hosted_runner({repo_name}, {runner_id})", e)
    
    def create_self_hosted_runner_registration_token(self, repo_name: str) -> Dict[str, Any]:
        """
        Create a registration token for a self-hosted runner.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Registration token
        """
        try:
            repo = self.github.get_repo(repo_name)
            token = repo.create_self_hosted_runner_registration_token()
            
            return {
                "token": token.token,
                "expires_at": token.expires_at.isoformat() if token.expires_at else None
            }
        except Exception as e:
            self.github._handle_error(f"create_self_hosted_runner_registration_token({repo_name})", e)
    
    def create_self_hosted_runner_removal_token(self, repo_name: str) -> Dict[str, Any]:
        """
        Create a removal token for a self-hosted runner.
        
        Args:
            repo_name: Repository name (format: "owner/repo")
            
        Returns:
            Removal token
        """
        try:
            repo = self.github.get_repo(repo_name)
            token = repo.create_self_hosted_runner_removal_token()
            
            return {
                "token": token.token,
                "expires_at": token.expires_at.isoformat() if token.expires_at else None
            }
        except Exception as e:
            self.github._handle_error(f"create_self_hosted_runner_removal_token({repo_name})", e)