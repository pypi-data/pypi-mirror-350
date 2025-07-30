"""
Generic Kubernetes resource tools for the DevOps MCP Server.

This module provides tools for dynamically retrieving any Kubernetes resource type
without having to create specific tools for each resource type.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.kubernetes.client import KubernetesService
from utils.logging import setup_logger
from utils.kubernetes_formatting import format_k8s_resources, format_k8s_resource_detail, format_error_response


class KubernetesGenericResourceTools:
    """Tools for dynamically retrieving any Kubernetes resource type."""
    
    def __init__(self, mcp: FastMCP, k8s_service: Optional[KubernetesService] = None):
        """
        Initialize Kubernetes generic resource tools.
        
        Args:
            mcp: The MCP server instance
            k8s_service: The Kubernetes service instance (optional)
        """
        self.mcp = mcp
        self.k8s_service = k8s_service
        self.logger = setup_logger("devops_mcp_server.tools.kubernetes.generic")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Kubernetes generic resource tools with the MCP server."""
        
        @self.mcp.tool()
        def get_k8s_api_resources() -> str:
            """
            Get all available API resources in the cluster.
            
            Returns:
                A string listing all API resources in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get API resources
                api_resources = self.k8s_service.get_api_resources()
                
                # Format response as YAML
                return format_k8s_resources(api_resources, "apiResources")
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes API resources: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def list_k8s_resources(resource_type: str, namespace: str = "default",
                              selector: str = "", field_selector: str = "",
                              limit: int = 100, all_namespaces: bool = False) -> str:
            """
            List Kubernetes resources of a specific type.
            
            This is a generic tool that can list any Kubernetes resource type.
            
            Args:
                resource_type: Type of resource to list (e.g., pods, deployments, services, etc.)
                namespace: Namespace to list resources from (default: "default")
                selector: Label selector to filter resources (optional, e.g., "app=nginx,tier=frontend")
                field_selector: Field selector to filter resources (optional, e.g., "status.phase=Running")
                limit: Maximum number of resources to return (default: 100)
                all_namespaces: Whether to list resources across all namespaces (similar to kubectl's -A flag)
                
            Returns:
                A string with resources in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get resource info to determine if it's namespaced and its API version
                resource_info = self._get_resource_info(resource_type)
                if not resource_info:
                    return format_error_response(f"Resource type not found: {resource_type}")
                
                is_namespaced = resource_info.get("namespaced", False)
                api_version = resource_info.get("apiVersion")
                
                # Determine namespace based on all_namespaces flag and resource type
                actual_namespace = None
                if is_namespaced:
                    if all_namespaces:
                        actual_namespace = None  # List across all namespaces
                    else:
                        actual_namespace = namespace
                
                # Get minimal resource information (just names and basic metadata)
                resources = self.k8s_service.get_resource_names(
                    resource_type=resource_type,
                    namespace=actual_namespace,
                    api_version=api_version,
                    label_selector=selector if selector else None,
                    field_selector=field_selector if field_selector else None,
                    limit=limit if limit != 100 else None
                )
                
                # Format response as YAML (with minimal information)
                return format_k8s_resources(resources, resource_type, namespace if is_namespaced else None)
            
            except Exception as e:
                self.logger.error(f"Error listing Kubernetes resources: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_resource(resource_type: str, name: str, namespace: str = "default") -> str:
            """
            Get a specific Kubernetes resource by name (similar to 'kubectl get <resource_type> <name> -o yaml').
            
            This is a generic tool that can retrieve any Kubernetes resource type.
            
            Args:
                resource_type: Type of resource to get (e.g., pod, deployment, service, etc.)
                name: Name of the resource
                namespace: Namespace of the resource (default: "default")
                
            Returns:
                A string with resource details in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get resource info to determine if it's namespaced and its API version
                resource_info = self._get_resource_info(resource_type)
                if not resource_info:
                    return format_error_response(f"Resource type not found: {resource_type}")
                
                is_namespaced = resource_info.get("namespaced", False)
                api_version = resource_info.get("apiVersion")
                actual_kind = resource_info.get("kind")

                if not actual_kind:
                    return format_error_response(f"Could not determine Kind for resource type: {resource_type}")
                
                # If the resource is namespaced but no namespace is provided, return an error
                if is_namespaced and not namespace:
                    return format_error_response(f"Namespace is required for namespaced resource: {resource_type}")
                
                # Get the resource
                resource = self.k8s_service.get_resource(
                    kind=actual_kind, # Pass the discovered kind
                    name=name,
                    namespace=namespace if is_namespaced else None,
                    api_version=api_version,
                    resource_type_for_error_reporting=resource_type # Pass original for errors
                )
                
                # Format response as YAML
                return format_k8s_resource_detail(resource, resource_type, namespace if is_namespaced else None)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes resource: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_resource_events(resource_type: str, name: str, namespace: str = None) -> str:
            """
            Get events related to a specific Kubernetes resource.
            
            Args:
                resource_type: Type of resource (e.g., pods, deployments, services, etc.)
                name: Name of the resource
                namespace: Namespace of the resource (optional for cluster-scoped resources)
                
            Returns:
                A string with events related to the resource in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get resource info to determine if it's namespaced and its API version
                resource_info = self._get_resource_info(resource_type)
                if not resource_info:
                    return format_error_response(f"Resource type not found: {resource_type}")
                
                is_namespaced = resource_info.get("namespaced", False)
                
                # If the resource is namespaced but no namespace is provided, return an error
                if is_namespaced and not namespace:
                    return format_error_response(f"Namespace is required for namespaced resource: {resource_type}")
                
                # Get the events
                events = self.k8s_service.get_resource_events(
                    resource_type=resource_type,
                    name=name,
                    namespace=namespace if is_namespaced else None
                )
                
                # Format response as YAML
                return format_k8s_resources(events, "events", namespace if is_namespaced else None)
            
            except Exception as e:
                self.logger.error(f"Error getting resource events: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_logs(pod_name: str, namespace: str, container: str = None,
                        tail_lines: int = 100, previous: bool = False,
                        since_seconds: int = None, timestamps: bool = False,
                        grep: str = None) -> str:
            """
            Get logs from a Kubernetes pod with advanced filtering options.
            
            Args:
                pod_name: Name of the pod
                namespace: Namespace where the pod is located
                container: Container name (optional, if not provided gets logs from the first container)
                tail_lines: Number of lines to return from the end of the logs (default: 100)
                previous: Get logs from previous instance of the container if it exists (default: False)
                since_seconds: Only return logs newer than a relative duration in seconds (optional)
                timestamps: Include timestamps on each line in the log output (default: False)
                grep: Filter logs using a regular expression pattern (optional)
                
            Returns:
                The pod logs
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # This would need to be implemented in the KubernetesService class
                logs = self.k8s_service.get_pod_logs(
                    pod_name=pod_name,
                    namespace=namespace,
                    container=container,
                    tail_lines=tail_lines,
                    previous=previous,
                    since_seconds=since_seconds,
                    timestamps=timestamps
                )
                
                # Apply grep filter if provided
                if grep and logs:
                    import re
                    pattern = re.compile(grep)
                    filtered_logs = []
                    for line in logs.splitlines():
                        if pattern.search(line):
                            filtered_logs.append(line)
                    logs = "\n".join(filtered_logs)
                
                # Format response
                if container:
                    header = f"Logs for pod {pod_name} container {container} in namespace '{namespace}':"
                else:
                    header = f"Logs for pod {pod_name} in namespace '{namespace}':"
                
                # Add filter information to header
                filters = []
                if tail_lines:
                    filters.append(f"last {tail_lines} lines")
                if previous:
                    filters.append("previous container instance")
                if since_seconds:
                    filters.append(f"since {since_seconds} seconds ago")
                if grep:
                    filters.append(f"filtered by '{grep}'")
                
                if filters:
                    header += f" ({', '.join(filters)})"
                
                return format_text_response(f"{header}\n\n{logs}")
            
            except Exception as e:
                self.logger.error(f"Error getting pod logs: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_version() -> str:
            """
            Get the Kubernetes version information for the cluster.
            
            Returns:
                A string with the Kubernetes version information in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get version information
                version_info = self.k8s_service.get_version()
                
                # Format response as YAML
                return format_k8s_version(version_info)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes version: {e}")
                return format_error_response(str(e))
    
    def _get_resource_info(self, resource_type: str) -> Dict[str, Any]:
        """
        Get information about a resource type.
        
        Args:
            resource_type: Type of resource to get information about
            
        Returns:
            A dictionary with resource information, or None if not found
        """
        try:
            # Get all API resources
            api_resources = self.k8s_service.get_api_resources()
            
            # Normalize resource type (handle singular/plural forms)
            resource_type_lower = resource_type.lower()
            
            # First try exact match
            for resource in api_resources:
                if resource["name"].lower() == resource_type_lower:
                    return resource
            
            # Try matching by short names
            for resource in api_resources:
                if "shortNames" in resource and resource["shortNames"]:
                    for short_name in resource["shortNames"]:
                        if short_name.lower() == resource_type_lower:
                            return resource
            
            # Try matching by singular name
            for resource in api_resources:
                if "singularName" in resource and resource["singularName"]:
                    if resource["singularName"].lower() == resource_type_lower:
                        return resource
            
            # Try matching by kind
            for resource in api_resources:
                if "kind" in resource and resource["kind"].lower() == resource_type_lower:
                    return resource
            
            # No match found
            return None
        
        except Exception as e:
            self.logger.error(f"Error getting resource info: {e}")
            return None
    
    def _is_resource_namespaced(self, resource_type: str, api_version: str = None) -> bool:
        """
        Check if a resource type is namespaced.
        
        Args:
            resource_type: Type of resource to check
            api_version: API version to check (optional)
            
        Returns:
            True if the resource is namespaced, False otherwise
        """
        # Get resource info
        resource_info = self._get_resource_info(resource_type)
        
        # If resource info is found, use the namespaced field
        if resource_info and "namespaced" in resource_info:
            return resource_info["namespaced"]
        
        # Fallback to a list of common cluster-scoped resources
        cluster_scoped_resources = [
            "nodes", "namespaces", "persistentvolumes", "clusterroles", "clusterrolebindings",
            "customresourcedefinitions", "storageclasses", "volumeattachments", "priorityclasses",
            "csidrivers", "csinodes", "volumesnapshotclasses", "volumesnapshotcontents",
            "ingressclasses", "runtimeclasses", "apiservices", "componentstatuses",
            "mutatingwebhookconfigurations", "validatingwebhookconfigurations", "flowschemas",
            "prioritylevelconfigurations", "certificatesigningrequests"
        ]
        
        # Check if the resource type is in the list of cluster-scoped resources
        return resource_type.lower() not in cluster_scoped_resources