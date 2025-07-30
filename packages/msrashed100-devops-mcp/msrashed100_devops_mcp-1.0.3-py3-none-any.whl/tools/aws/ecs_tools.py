"""
AWS ECS tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.base_tools import AWSBaseTools
from utils.logging import setup_logger


class AWSECSTools(AWSBaseTools):
    """Tools for AWS ECS operations."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS ECS tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.ecs")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register AWS ECS tools with the MCP server."""
        
        @self.mcp.tool()
        def list_ecs_clusters(max_results: int = 100) -> str:
            """
            List ECS clusters.
            
            This tool lists all ECS clusters in your AWS account.
            
            Args:
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of ECS clusters in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                clusters = self.aws_service.ecs.list_clusters(max_results)
                return self._format_response({"clusters": clusters, "count": len(clusters)})
            except Exception as e:
                self.logger.error(f"Error listing ECS clusters: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_ecs_cluster(cluster: str) -> str:
            """
            Get details of an ECS cluster.
            
            This tool retrieves details of an ECS cluster.
            
            Args:
                cluster: Cluster name or ARN
                
            Returns:
                Cluster details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                cluster_details = self.aws_service.ecs.get_cluster(cluster)
                return self._format_response(cluster_details)
            except Exception as e:
                self.logger.error(f"Error getting ECS cluster: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_ecs_services(cluster: str, max_results: int = 100) -> str:
            """
            List ECS services in a cluster.
            
            This tool lists all ECS services in a cluster.
            
            Args:
                cluster: Cluster name or ARN
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of ECS services in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                services = self.aws_service.ecs.list_services(cluster, max_results)
                return self._format_response({"services": services, "count": len(services)})
            except Exception as e:
                self.logger.error(f"Error listing ECS services: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_ecs_service(cluster: str, service: str) -> str:
            """
            Get details of an ECS service.
            
            This tool retrieves details of an ECS service.
            
            Args:
                cluster: Cluster name or ARN
                service: Service name or ARN
                
            Returns:
                Service details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                service_details = self.aws_service.ecs.get_service(cluster, service)
                return self._format_response(service_details)
            except Exception as e:
                self.logger.error(f"Error getting ECS service: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_ecs_tasks(cluster: str, service: str = None, max_results: int = 100) -> str:
            """
            List ECS tasks in a cluster.
            
            This tool lists all ECS tasks in a cluster, optionally filtered by service.
            
            Args:
                cluster: Cluster name or ARN
                service: Service name or ARN (optional)
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of ECS tasks in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                tasks = self.aws_service.ecs.list_tasks(cluster, service, max_results)
                return self._format_response({"tasks": tasks, "count": len(tasks)})
            except Exception as e:
                self.logger.error(f"Error listing ECS tasks: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_ecs_task(cluster: str, task: str) -> str:
            """
            Get details of an ECS task.
            
            This tool retrieves details of an ECS task.
            
            Args:
                cluster: Cluster name or ARN
                task: Task name or ARN
                
            Returns:
                Task details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                task_details = self.aws_service.ecs.get_task(cluster, task)
                return self._format_response(task_details)
            except Exception as e:
                self.logger.error(f"Error getting ECS task: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_ecs_task_definitions(family_prefix: str = None, max_results: int = 100) -> str:
            """
            List ECS task definitions.
            
            This tool lists all ECS task definitions, optionally filtered by family prefix.
            
            Args:
                family_prefix: Family prefix to filter by (optional)
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of task definition ARNs in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                task_definitions = self.aws_service.ecs.list_task_definitions(family_prefix, max_results)
                return self._format_response({"taskDefinitions": task_definitions, "count": len(task_definitions)})
            except Exception as e:
                self.logger.error(f"Error listing ECS task definitions: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_ecs_task_definition(task_definition: str) -> str:
            """
            Get details of an ECS task definition.
            
            This tool retrieves details of an ECS task definition.
            
            Args:
                task_definition: Task definition name or ARN
                
            Returns:
                Task definition details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                task_definition_details = self.aws_service.ecs.get_task_definition(task_definition)
                return self._format_response(task_definition_details)
            except Exception as e:
                self.logger.error(f"Error getting ECS task definition: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def list_ecs_container_instances(cluster: str, max_results: int = 100) -> str:
            """
            List container instances registered to an ECS cluster.

            Args:
                cluster: Cluster name or ARN.
                max_results: Maximum number of results to return (default: 100, max: 100).
            
            Returns:
                List of container instance ARNs in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            max_results = min(max(1, max_results), 100)
            
            try:
                instance_arns = self.aws_service.ecs.list_container_instances(cluster, max_results)
                return self._format_response({"containerInstanceArns": instance_arns, "count": len(instance_arns)})
            except Exception as e:
                self.logger.error(f"Error listing ECS container instances for cluster {cluster}: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def describe_ecs_container_instance(cluster: str, container_instance_id: str) -> str:
            """
            Get details of a specific container instance.

            Args:
                cluster: Cluster name or ARN.
                container_instance_id: The ID or ARN of the container instance.
            
            Returns:
                Dictionary containing container instance details in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                instance_details = self.aws_service.ecs.describe_container_instance(cluster, container_instance_id)
                return self._format_response(instance_details)
            except Exception as e:
                self.logger.error(f"Error describing ECS container instance {container_instance_id} in cluster {cluster}: {e}")
                return self._format_error(str(e))