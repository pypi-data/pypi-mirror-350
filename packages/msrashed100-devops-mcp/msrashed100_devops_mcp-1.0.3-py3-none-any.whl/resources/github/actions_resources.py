"""
GitHub Actions resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.github.service import GitHubServiceManager
from resources.github.base_resources import GitHubBaseResources
from utils.logging import setup_logger


class GitHubActionsResources(GitHubBaseResources):
    """GitHub Actions resources."""
    
    def __init__(self, mcp: FastMCP, github_service: Optional[GitHubServiceManager] = None):
        """
        Initialize GitHub Actions resources.
        
        Args:
            mcp: The MCP server instance
            github_service: The GitHub service manager instance (optional)
        """
        super().__init__(mcp, github_service)
        self.logger = setup_logger("devops_mcp_server.resources.github.actions")
    
    def get_resource_templates(self) -> List[Dict[str, str]]:
        """
        Get Actions resource templates.
        
        Returns:
            List of resource templates
        """
        templates = []
        
        # Actions templates
        templates.append({
            "uriTemplate": "github://workflows",
            "name": "GitHub Workflows",
            "mimeType": "application/json",
            "description": "List workflows in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://workflow/{workflow_id}",
            "name": "GitHub Workflow",
            "mimeType": "application/json",
            "description": "Get details of a workflow in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://workflow/{workflow_id}/runs",
            "name": "GitHub Workflow Runs",
            "mimeType": "application/json",
            "description": "List runs for a workflow in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://workflow/{workflow_id}/content",
            "name": "GitHub Workflow Content",
            "mimeType": "application/json",
            "description": "Get content of a workflow file in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://runs/{run_id}",
            "name": "GitHub Workflow Run",
            "mimeType": "application/json",
            "description": "Get details of a workflow run in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://runs/{run_id}/jobs",
            "name": "GitHub Workflow Run Jobs",
            "mimeType": "application/json",
            "description": "List jobs for a workflow run in a GitHub repository"
        })
        
        templates.append({
            "uriTemplate": "github://runs/{run_id}/artifacts",
            "name": "GitHub Workflow Run Artifacts",
            "mimeType": "application/json",
            "description": "List artifacts for a workflow run in a GitHub repository"
        })
        
        return templates
    
    def handle_resource(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Handle Actions resources.
        
        Args:
            path: Resource path
            
        Returns:
            Resource response or None if not handled
        """
        if path == "workflows":
            return self._handle_workflows_resource()
        elif path.startswith("workflow/"):
            workflow_path = path[len("workflow/"):]
            if "/" not in workflow_path:
                try:
                    workflow_id = int(workflow_path)
                    return self._handle_workflow_resource(workflow_id)
                except ValueError:
                    raise JSONRPCError(
                        code=INVALID_REQUEST,
                        message=f"Invalid workflow ID: {workflow_path}"
                    )
            else:
                parts = workflow_path.split("/", 2)
                try:
                    workflow_id = int(parts[0])
                    if parts[1] == "runs":
                        return self._handle_workflow_runs_resource(workflow_id)
                    elif parts[1] == "content":
                        return self._handle_workflow_content_resource(workflow_id)
                except ValueError:
                    raise JSONRPCError(
                        code=INVALID_REQUEST,
                        message=f"Invalid workflow ID: {parts[0]}"
                    )
        
        elif path.startswith("runs/"):
            run_path = path[len("runs/"):]
            if "/" not in run_path:
                try:
                    run_id = int(run_path)
                    return self._handle_run_resource(run_id)
                except ValueError:
                    raise JSONRPCError(
                        code=INVALID_REQUEST,
                        message=f"Invalid run ID: {run_path}"
                    )
            else:
                parts = run_path.split("/", 2)
                try:
                    run_id = int(parts[0])
                    if parts[1] == "jobs":
                        return self._handle_run_jobs_resource(run_id)
                    elif parts[1] == "artifacts":
                        return self._handle_run_artifacts_resource(run_id)
                except ValueError:
                    raise JSONRPCError(
                        code=INVALID_REQUEST,
                        message=f"Invalid run ID: {parts[0]}"
                    )
        
        return None
    
    def _handle_workflows_resource(self) -> Dict[str, Any]:
        """
        Handle GitHub workflows resource.
        
        Returns:
            Resource response
        """
        workflows = self.github_service.actions.list_workflows("owner/repo")
        
        return {
            "contents": [
                {
                    "uri": "github://workflows",
                    "mimeType": "application/json",
                    "text": self._format_json({"workflows": workflows, "count": len(workflows)})
                }
            ]
        }
    
    def _handle_workflow_resource(self, workflow_id: int) -> Dict[str, Any]:
        """
        Handle GitHub workflow resource.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Resource response
        """
        workflow = self.github_service.actions.get_workflow("owner/repo", workflow_id)
        
        return {
            "contents": [
                {
                    "uri": f"github://workflow/{workflow_id}",
                    "mimeType": "application/json",
                    "text": self._format_json(workflow)
                }
            ]
        }
    
    def _handle_workflow_runs_resource(self, workflow_id: int) -> Dict[str, Any]:
        """
        Handle GitHub workflow runs resource.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Resource response
        """
        runs = self.github_service.actions.list_workflow_runs("owner/repo", workflow_id)
        
        return {
            "contents": [
                {
                    "uri": f"github://workflow/{workflow_id}/runs",
                    "mimeType": "application/json",
                    "text": self._format_json({"workflowRuns": runs, "count": len(runs)})
                }
            ]
        }
    
    def _handle_workflow_content_resource(self, workflow_id: int) -> Dict[str, Any]:
        """
        Handle GitHub workflow content resource.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Resource response
        """
        content = self.github_service.actions.get_workflow_content("owner/repo", workflow_id)
        
        return {
            "contents": [
                {
                    "uri": f"github://workflow/{workflow_id}/content",
                    "mimeType": "application/json",
                    "text": self._format_json(content)
                }
            ]
        }
    
    def _handle_run_resource(self, run_id: int) -> Dict[str, Any]:
        """
        Handle GitHub workflow run resource.
        
        Args:
            run_id: Run ID
            
        Returns:
            Resource response
        """
        run = self.github_service.actions.get_workflow_run("owner/repo", run_id)
        
        return {
            "contents": [
                {
                    "uri": f"github://runs/{run_id}",
                    "mimeType": "application/json",
                    "text": self._format_json(run)
                }
            ]
        }
    
    def _handle_run_jobs_resource(self, run_id: int) -> Dict[str, Any]:
        """
        Handle GitHub workflow run jobs resource.
        
        Args:
            run_id: Run ID
            
        Returns:
            Resource response
        """
        jobs = self.github_service.actions.list_workflow_run_jobs("owner/repo", run_id)
        
        return {
            "contents": [
                {
                    "uri": f"github://runs/{run_id}/jobs",
                    "mimeType": "application/json",
                    "text": self._format_json({"jobs": jobs, "count": len(jobs)})
                }
            ]
        }
    
    def _handle_run_artifacts_resource(self, run_id: int) -> Dict[str, Any]:
        """
        Handle GitHub workflow run artifacts resource.
        
        Args:
            run_id: Run ID
            
        Returns:
            Resource response
        """
        artifacts = self.github_service.actions.list_workflow_run_artifacts("owner/repo", run_id)
        
        return {
            "contents": [
                {
                    "uri": f"github://runs/{run_id}/artifacts",
                    "mimeType": "application/json",
                    "text": self._format_json({"artifacts": artifacts, "count": len(artifacts)})
                }
            ]
        }