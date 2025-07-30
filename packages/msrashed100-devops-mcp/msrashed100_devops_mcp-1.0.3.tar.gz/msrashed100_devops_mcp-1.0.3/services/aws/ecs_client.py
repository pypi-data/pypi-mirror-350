"""
AWS ECS client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.aws.client import AWSService


class AWSECSClient:
    """Client for AWS ECS operations."""
    
    def __init__(self, aws_service: AWSService):
        """
        Initialize the AWS ECS client.
        
        Args:
            aws_service: The base AWS service
        """
        self.aws = aws_service
        self.logger = aws_service.logger
        self.client = None
    
    def _get_client(self):
        """Get the ECS client."""
        if self.client is None:
            self.client = self.aws.get_client('ecs')
        return self.client
    
    def list_clusters(self, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List ECS clusters.
        
        Args:
            max_results: Maximum number of results to return
            
        Returns:
            List of ECS clusters
        """
        try:
            client = self._get_client()
            
            # Get cluster ARNs
            response = client.list_clusters(maxResults=min(max_results, 100))
            cluster_arns = response.get('clusterArns', [])
            
            if not cluster_arns:
                return []
            
            # Get cluster details
            clusters_response = client.describe_clusters(clusters=cluster_arns)
            clusters = clusters_response.get('clusters', [])
            
            return clusters
        except Exception as e:
            self.aws._handle_error("list_clusters", e)
    
    def get_cluster(self, cluster: str) -> Dict[str, Any]:
        """
        Get details of an ECS cluster.
        
        Args:
            cluster: Cluster name or ARN
            
        Returns:
            Cluster details
        """
        try:
            client = self._get_client()
            
            response = client.describe_clusters(clusters=[cluster])
            clusters = response.get('clusters', [])
            
            if not clusters:
                raise ValueError(f"Cluster '{cluster}' not found")
            
            return clusters[0]
        except Exception as e:
            self.aws._handle_error(f"get_cluster({cluster})", e)
    
    def list_services(self, cluster: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List ECS services in a cluster.
        
        Args:
            cluster: Cluster name or ARN
            max_results: Maximum number of results to return
            
        Returns:
            List of ECS services
        """
        try:
            client = self._get_client()
            
            # Get service ARNs
            response = client.list_services(cluster=cluster, maxResults=min(max_results, 100))
            service_arns = response.get('serviceArns', [])
            
            if not service_arns:
                return []
            
            # Get service details
            services_response = client.describe_services(cluster=cluster, services=service_arns)
            services = services_response.get('services', [])
            
            return services
        except Exception as e:
            self.aws._handle_error(f"list_services({cluster})", e)
    
    def get_service(self, cluster: str, service: str) -> Dict[str, Any]:
        """
        Get details of an ECS service.
        
        Args:
            cluster: Cluster name or ARN
            service: Service name or ARN
            
        Returns:
            Service details
        """
        try:
            client = self._get_client()
            
            response = client.describe_services(cluster=cluster, services=[service])
            services = response.get('services', [])
            
            if not services:
                raise ValueError(f"Service '{service}' not found in cluster '{cluster}'")
            
            return services[0]
        except Exception as e:
            self.aws._handle_error(f"get_service({cluster}, {service})", e)
    
    def list_tasks(self, cluster: str, service: Optional[str] = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List ECS tasks in a cluster.
        
        Args:
            cluster: Cluster name or ARN
            service: Service name or ARN (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of ECS tasks
        """
        try:
            client = self._get_client()
            
            # Get task ARNs
            params = {'cluster': cluster, 'maxResults': min(max_results, 100)}
            if service:
                params['serviceName'] = service
            
            response = client.list_tasks(**params)
            task_arns = response.get('taskArns', [])
            
            if not task_arns:
                return []
            
            # Get task details
            tasks_response = client.describe_tasks(cluster=cluster, tasks=task_arns)
            tasks = tasks_response.get('tasks', [])
            
            return tasks
        except Exception as e:
            self.aws._handle_error(f"list_tasks({cluster})", e)
    
    def get_task(self, cluster: str, task: str) -> Dict[str, Any]:
        """
        Get details of an ECS task.
        
        Args:
            cluster: Cluster name or ARN
            task: Task name or ARN
            
        Returns:
            Task details
        """
        try:
            client = self._get_client()
            
            response = client.describe_tasks(cluster=cluster, tasks=[task])
            tasks = response.get('tasks', [])
            
            if not tasks:
                raise ValueError(f"Task '{task}' not found in cluster '{cluster}'")
            
            return tasks[0]
        except Exception as e:
            self.aws._handle_error(f"get_task({cluster}, {task})", e)
    
    def list_task_definitions(self, family_prefix: Optional[str] = None, max_results: int = 100) -> List[str]:
        """
        List ECS task definitions.
        
        Args:
            family_prefix: Family prefix to filter by (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of task definition ARNs
        """
        try:
            client = self._get_client()
            
            params = {'maxResults': min(max_results, 100)}
            if family_prefix:
                params['familyPrefix'] = family_prefix
            
            response = client.list_task_definitions(**params)
            task_definition_arns = response.get('taskDefinitionArns', [])
            
            return task_definition_arns
        except Exception as e:
            self.aws._handle_error("list_task_definitions", e)
    
    def get_task_definition(self, task_definition: str) -> Dict[str, Any]:
        """
        Get details of an ECS task definition.
        
        Args:
            task_definition: Task definition name or ARN
            
        Returns:
            Task definition details
        """
        try:
            client = self._get_client()
            
            response = client.describe_task_definition(taskDefinition=task_definition)
            task_definition = response.get('taskDefinition', {})
            
            return task_definition
        except Exception as e:
            self.aws._handle_error(f"get_task_definition({task_definition})", e)

    def list_container_instances(self, cluster: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List container instances registered to an ECS cluster.

        Args:
            cluster: Cluster name or ARN.
            max_results: Maximum number of results to return.

        Returns:
            List of container instance ARNs.
        """
        self.logger.info(f"Listing container instances for cluster: {cluster}")
        try:
            client = self._get_client()
            container_instance_arns = []
            paginator = client.get_paginator('list_container_instances')
            page_iterator = paginator.paginate(cluster=cluster, maxResults=min(max_results, 100))
            for page in page_iterator:
                container_instance_arns.extend(page.get('containerInstanceArns', []))
            
            self.logger.info(f"Successfully listed {len(container_instance_arns)} container instances for cluster: {cluster}")
            return container_instance_arns
        except Exception as e:
            self.aws._handle_error(f"list_container_instances({cluster})", e)

    def describe_container_instance(self, cluster: str, container_instance_id: str) -> Dict[str, Any]:
        """
        Get details of a specific container instance.

        Args:
            cluster: Cluster name or ARN.
            container_instance_id: The ID or ARN of the container instance.

        Returns:
            Dictionary containing container instance details.
        """
        self.logger.info(f"Describing container instance {container_instance_id} in cluster {cluster}")
        try:
            client = self._get_client()
            response = client.describe_container_instances(
                cluster=cluster,
                containerInstances=[container_instance_id]
            )
            container_instances = response.get('containerInstances', [])
            if not container_instances:
                self.logger.warning(f"Container instance {container_instance_id} not found in cluster {cluster}")
                return {"error": "Container instance not found"}
            self.logger.info(f"Successfully described container instance {container_instance_id}")
            return container_instances[0]
        except Exception as e:
            self.aws._handle_error(f"describe_container_instance({cluster}, {container_instance_id})", e)