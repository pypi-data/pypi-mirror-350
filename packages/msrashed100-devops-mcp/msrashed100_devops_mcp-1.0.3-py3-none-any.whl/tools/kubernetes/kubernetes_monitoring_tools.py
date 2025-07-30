"""
Kubernetes monitoring tools for the DevOps MCP Server.

This module provides read-only tools for monitoring and inspecting Kubernetes resources
without making any changes to the cluster.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.kubernetes.client import KubernetesService
from utils.logging import setup_logger
from utils.kubernetes_formatting import format_k8s_resources, format_k8s_resource_detail, format_error_response, format_as_yaml


class KubernetesMonitoringTools:
    """Tools for monitoring and inspecting Kubernetes resources."""
    
    def __init__(self, mcp: FastMCP, k8s_service: Optional[KubernetesService] = None):
        """
        Initialize Kubernetes monitoring tools.
        
        Args:
            mcp: The MCP server instance
            k8s_service: The Kubernetes service instance (optional)
        """
        self.mcp = mcp
        self.k8s_service = k8s_service
        self.logger = setup_logger("devops_mcp_server.tools.kubernetes.monitoring")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Kubernetes monitoring tools with the MCP server."""
        
        @self.mcp.tool()
        def get_k8s_node_status() -> str:
            """
            Get the status of all nodes in the cluster.
            
            Returns:
                A string with node status information in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get nodes using the list_resources method
                nodes = self.k8s_service.list_resources("nodes")
                
                # Format response as YAML
                return format_k8s_resources(nodes, "nodes")
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes node status: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_component_status() -> str:
            """
            Get the status of Kubernetes cluster components.
            
            Returns:
                A string with component status information in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get component status using the list_resources method
                components = self.k8s_service.list_resources("componentstatuses")
                
                # Format response as YAML
                return format_k8s_resources(components, "componentstatuses")
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes component status: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_namespace_events(namespace: str) -> str:
            """
            Get all events in a namespace.
            
            Args:
                namespace: The namespace to get events for
                
            Returns:
                A string with events in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get events using the list_resources method
                events = self.k8s_service.list_resources("events", namespace)
                
                # Format response as YAML
                return format_k8s_resources(events, "events", namespace)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes namespace events: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_resource_quota(namespace: str) -> str:
            """
            Get resource quotas in a namespace.
            
            Args:
                namespace: The namespace to get resource quotas for
                
            Returns:
                A string with resource quotas in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get resource quotas using the list_resources method
                quotas = self.k8s_service.list_resources("resourcequotas", namespace)
                
                # Format response as YAML
                return format_k8s_resources(quotas, "resourcequotas", namespace)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes resource quotas: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_pod_distribution() -> str:
            """
            Get the distribution of pods across nodes.
            
            Returns:
                A string with pod distribution information in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get all pods across all namespaces
                pods = self.k8s_service.list_resources("pods")
                
                # Group pods by node
                pod_distribution = {}
                for pod in pods:
                    node = pod.get("node", "unknown")
                    if node not in pod_distribution:
                        pod_distribution[node] = []
                    
                    pod_distribution[node].append({
                        "name": pod.get("name"),
                        "namespace": pod.get("namespace"),
                        "status": pod.get("status")
                    })
                
                # Count pods per node
                node_summary = {}
                for node, node_pods in pod_distribution.items():
                    node_summary[node] = {
                        "total_pods": len(node_pods),
                        "running_pods": sum(1 for p in node_pods if p.get("status") == "Running"),
                        "pods": node_pods
                    }
                
                # Format response as YAML
                result = {
                    "kind": "PodDistribution",
                    "apiVersion": "v1",
                    "metadata": {},
                    "nodes": node_summary
                }
                
                return format_as_yaml(result)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes pod distribution: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_network_policies(namespace: str = None) -> str:
            """
            Get network policies in a namespace or across all namespaces.
            
            Args:
                namespace: The namespace to get network policies for (optional)
                
            Returns:
                A string with network policies in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get network policies using the list_resources method
                policies = self.k8s_service.list_resources("networkpolicies", namespace)
                
                # Format response as YAML
                return format_k8s_resources(policies, "networkpolicies", namespace)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes network policies: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_service_endpoints(service_name: str, namespace: str) -> str:
            """
            Get endpoints for a service.
            
            Args:
                service_name: The name of the service
                namespace: The namespace of the service
                
            Returns:
                A string with service endpoints in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get the endpoint resource
                endpoint = self.k8s_service.describe_resource("endpoint", service_name, namespace)
                
                # Format response as YAML
                return format_k8s_resource_detail(endpoint, "endpoint", namespace)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes service endpoints: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_persistent_volumes() -> str:
            """
            Get all persistent volumes in the cluster.
            
            Returns:
                A string with persistent volumes in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get persistent volumes using the list_resources method
                pvs = self.k8s_service.list_resources("persistentvolumes")
                
                # Format response as YAML
                return format_k8s_resources(pvs, "persistentvolumes")
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes persistent volumes: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_storage_classes() -> str:
            """
            Get all storage classes in the cluster.
            
            Returns:
                A string with storage classes in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get storage classes using the list_resources method
                storage_classes = self.k8s_service.list_resources("storageclasses")
                
                # Format response as YAML
                return format_k8s_resources(storage_classes, "storageclasses")
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes storage classes: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_rbac_info(namespace: str = None) -> str:
            """
            Get RBAC information (roles, role bindings) in a namespace or across all namespaces.
            
            Args:
                namespace: The namespace to get RBAC information for (optional)
                
            Returns:
                A string with RBAC information in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get roles and role bindings
                roles = self.k8s_service.list_resources("roles", namespace)
                role_bindings = self.k8s_service.list_resources("rolebindings", namespace)
                
                # If no namespace is specified, also get cluster roles and cluster role bindings
                cluster_roles = []
                cluster_role_bindings = []
                if not namespace:
                    cluster_roles = self.k8s_service.list_resources("clusterroles")
                    cluster_role_bindings = self.k8s_service.list_resources("clusterrolebindings")
                
                # Format response as YAML
                result = {
                    "kind": "RBACInfo",
                    "apiVersion": "v1",
                    "metadata": {},
                    "roles": roles,
                    "roleBindings": role_bindings
                }
                
                if not namespace:
                    result["clusterRoles"] = cluster_roles
                    result["clusterRoleBindings"] = cluster_role_bindings
                
                return format_as_yaml(result)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes RBAC information: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_crds() -> str:
            """
            Get all Custom Resource Definitions in the cluster.
            
            Returns:
                A string with CRDs in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get CRDs using the list_resources method
                crds = self.k8s_service.list_resources("customresourcedefinitions")
                
                # Format response as YAML
                return format_k8s_resources(crds, "customresourcedefinitions")
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes CRDs: {e}")
                return format_error_response(str(e))
        
        self.logger.info("Kubernetes monitoring tools registered successfully")