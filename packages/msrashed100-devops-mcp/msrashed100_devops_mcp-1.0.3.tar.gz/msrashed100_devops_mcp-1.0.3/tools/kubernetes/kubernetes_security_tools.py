"""
Kubernetes security and configuration tools for the DevOps MCP Server.

This module provides read-only tools for inspecting Kubernetes security and configuration
without making any changes to the cluster.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.kubernetes.client import KubernetesService
from utils.logging import setup_logger
from utils.kubernetes_formatting import format_k8s_resources, format_k8s_resource_detail, format_error_response, format_as_yaml


class KubernetesSecurityTools:
    """Tools for inspecting Kubernetes security and configuration."""
    
    def __init__(self, mcp: FastMCP, k8s_service: Optional[KubernetesService] = None):
        """
        Initialize Kubernetes security tools.
        
        Args:
            mcp: The MCP server instance
            k8s_service: The Kubernetes service instance (optional)
        """
        self.mcp = mcp
        self.k8s_service = k8s_service
        self.logger = setup_logger("devops_mcp_server.tools.kubernetes.security")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register Kubernetes security tools with the MCP server."""
        
        @self.mcp.tool()
        def get_k8s_service_accounts(namespace: str = None) -> str:
            """
            Get service accounts in a namespace or across all namespaces.
            
            Args:
                namespace: The namespace to get service accounts for (optional)
                
            Returns:
                A string with service accounts in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get service accounts using the list_resources method
                service_accounts = self.k8s_service.list_resources("serviceaccounts", namespace)
                
                # Format response as YAML
                return format_k8s_resources(service_accounts, "serviceaccounts", namespace)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes service accounts: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_pod_security_policies() -> str:
            """
            Get all pod security policies in the cluster.
            
            Returns:
                A string with pod security policies in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get pod security policies using the list_resources method
                policies = self.k8s_service.list_resources("podsecuritypolicies")
                
                # Format response as YAML
                return format_k8s_resources(policies, "podsecuritypolicies")
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes pod security policies: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_secrets_metadata(namespace: str = None) -> str:
            """
            Get metadata about secrets in a namespace or across all namespaces.
            This does not expose the actual secret values.
            
            Args:
                namespace: The namespace to get secrets for (optional)
                
            Returns:
                A string with secrets metadata in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get secrets using the list_resources method
                secrets = self.k8s_service.list_resources("secrets", namespace)
                
                # Remove the actual secret data to avoid exposing sensitive information
                for secret in secrets:
                    if "data" in secret:
                        # Replace actual data with just the keys
                        secret["data_keys"] = list(secret.get("data", {}).keys())
                        del secret["data"]
                
                # Format response as YAML
                return format_k8s_resources(secrets, "secrets", namespace)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes secrets metadata: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_admission_controllers() -> str:
            """
            Get information about configured admission controllers.
            
            Returns:
                A string with admission controller information in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get the API server pod to extract admission controller configuration
                # This assumes the API server is running as a pod in the kube-system namespace
                api_server_pods = self.k8s_service.list_resources("pods", "kube-system")
                
                # Filter for the API server pod
                api_server_pod = None
                for pod in api_server_pods:
                    if pod.get("name", "").startswith("kube-apiserver-"):
                        api_server_pod = pod
                        break
                
                if not api_server_pod:
                    return format_error_response("Could not find API server pod")
                
                # Extract admission controller configuration from command line arguments
                admission_controllers = []
                for container in api_server_pod.get("containers", []):
                    for arg in container.get("args", []):
                        if arg.startswith("--enable-admission-plugins="):
                            controllers = arg.split("=")[1].split(",")
                            admission_controllers.extend(controllers)
                
                # Format response as YAML
                result = {
                    "kind": "AdmissionControllers",
                    "apiVersion": "v1",
                    "metadata": {},
                    "enabledAdmissionControllers": admission_controllers
                }
                
                return format_as_yaml(result)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes admission controllers: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_config_maps(namespace: str = None) -> str:
            """
            Get config maps in a namespace or across all namespaces.
            
            Args:
                namespace: The namespace to get config maps for (optional)
                
            Returns:
                A string with config maps in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # Get config maps using the list_resources method
                config_maps = self.k8s_service.list_resources("configmaps", namespace)
                
                # Format response as YAML
                return format_k8s_resources(config_maps, "configmaps", namespace)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes config maps: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_contexts() -> str:
            """
            Get all available Kubernetes contexts.
            
            Returns:
                A string with contexts in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # This requires accessing the kubeconfig file
                # We'll use the kubernetes.config module to get contexts
                from kubernetes import config
                
                # Get contexts from kubeconfig
                _, active_context = config.list_kube_config_contexts()
                contexts, _ = config.list_kube_config_contexts()
                
                # Format contexts
                formatted_contexts = []
                for context in contexts:
                    context_info = {
                        "name": context["name"],
                        "cluster": context["context"]["cluster"],
                        "user": context["context"]["user"],
                        "namespace": context["context"].get("namespace", "default"),
                        "active": context["name"] == active_context["name"]
                    }
                    formatted_contexts.append(context_info)
                
                # Format response as YAML
                result = {
                    "kind": "ContextList",
                    "apiVersion": "v1",
                    "metadata": {},
                    "contexts": formatted_contexts
                }
                
                return format_as_yaml(result)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes contexts: {e}")
                return format_error_response(str(e))
        
        @self.mcp.tool()
        def get_k8s_resource_dependencies(resource_type: str, name: str, namespace: str) -> str:
            """
            Get dependencies between resources (e.g., which pods use which configmaps).
            
            Args:
                resource_type: Type of resource to check dependencies for
                name: Name of the resource
                namespace: Namespace of the resource
                
            Returns:
                A string with resource dependencies in YAML format
            """
            if not self.k8s_service:
                return format_error_response("Kubernetes service is not available")
            
            try:
                # This is a complex operation that depends on the resource type
                # For now, we'll implement it for configmaps and secrets
                
                if resource_type not in ["configmap", "secret"]:
                    return format_error_response(f"Resource dependencies not supported for {resource_type}")
                
                # Get all pods in the namespace
                pods = self.k8s_service.list_resources("pods", namespace)
                
                # Find pods that use the specified resource
                dependent_pods = []
                
                for pod in pods:
                    uses_resource = False
                    
                    # Check volume mounts
                    for volume in pod.get("volumes", []):
                        if resource_type == "configmap" and volume.get("configMap", {}).get("name") == name:
                            uses_resource = True
                            break
                        elif resource_type == "secret" and volume.get("secret", {}).get("secretName") == name:
                            uses_resource = True
                            break
                    
                    # Check environment variables
                    for container in pod.get("containers", []):
                        for env in container.get("env", []):
                            if "valueFrom" in env:
                                if resource_type == "configmap" and env.get("valueFrom", {}).get("configMapKeyRef", {}).get("name") == name:
                                    uses_resource = True
                                    break
                                elif resource_type == "secret" and env.get("valueFrom", {}).get("secretKeyRef", {}).get("name") == name:
                                    uses_resource = True
                                    break
                    
                    if uses_resource:
                        dependent_pods.append({
                            "name": pod.get("name"),
                            "namespace": pod.get("namespace"),
                            "status": pod.get("status")
                        })
                
                # Format response as YAML
                result = {
                    "kind": "ResourceDependencies",
                    "apiVersion": "v1",
                    "metadata": {
                        "resourceType": resource_type,
                        "resourceName": name,
                        "namespace": namespace
                    },
                    "dependentPods": dependent_pods,
                    "dependentPodsCount": len(dependent_pods)
                }
                
                return format_as_yaml(result)
            
            except Exception as e:
                self.logger.error(f"Error getting Kubernetes resource dependencies: {e}")
                return format_error_response(str(e))
        
        self.logger.info("Kubernetes security tools registered successfully")