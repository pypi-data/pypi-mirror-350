"""
Kubernetes resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.kubernetes.client import KubernetesService
from utils.logging import setup_logger


class KubernetesResources:
    """Kubernetes resources for the MCP server."""
    
    def __init__(self, mcp: FastMCP, kubeconfig_path: Optional[str] = None):
        """
        Initialize Kubernetes resources.
        
        Args:
            mcp: The MCP server instance
            kubeconfig_path: Path to the kubeconfig file (optional)
        """
        self.mcp = mcp
        self.logger = setup_logger("devops_mcp_server.resources.kubernetes")
        
        # Initialize Kubernetes service
        try:
            self.k8s_service = KubernetesService(kubeconfig_path)
            self.logger.info("Kubernetes service initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Kubernetes service: {e}")
            self.k8s_service = None
        
        # Register resources
        self._register_resources()
    
    def _register_resources(self) -> None:
        """Register Kubernetes resources with the MCP server."""
        
        @self.mcp.resource("k8s://.*")
        def list_k8s_resources(uri: str):
            """List Kubernetes resources handler."""
            if not self.k8s_service:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message="Kubernetes service is not available"
                )
            
            # Parse URI
            if not uri.startswith("k8s://"):
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid URI format: {uri}"
                )
            
            parts = uri[len("k8s://"):].split("/")
            
            try:
                if len(parts) == 1 and parts[0] == "namespaces":
                    # List all namespaces
                    resources = self.k8s_service.list_resources("namespaces")
                    return {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": "application/json",
                                "text": self._format_json(resources)
                            }
                        ]
                    }
                
                elif len(parts) == 2:
                    # List resources in namespace
                    namespace = parts[0]
                    resource_type = parts[1]
                    resources = self.k8s_service.list_resources(resource_type, namespace)
                    return {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": "application/json",
                                "text": self._format_json(resources)
                            }
                        ]
                    }
                
                elif len(parts) == 3:
                    # Get specific resource in namespace
                    namespace = parts[0]
                    resource_type = parts[1]
                    name = parts[2]
                    
                    # Convert plural resource type to singular for the describe method
                    singular_type = self._plural_to_singular(resource_type)
                    
                    resource = self.k8s_service.describe_resource(singular_type, name, namespace)
                    return {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": "application/json",
                                "text": self._format_json(resource)
                            }
                        ]
                    }
                
                else:
                    raise JSONRPCError(
                        code=INVALID_REQUEST,
                        message=f"Invalid Kubernetes URI format: {uri}"
                    )
            
            except Exception as e:
                self.logger.error(f"Error handling Kubernetes resource: {e}")
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Error handling Kubernetes resource: {str(e)}"
                )
        
        @self.mcp.list_resource_templates()
        def list_k8s_resource_templates():
            """List Kubernetes resource templates."""
            templates = []
            
            # Add template for listing all namespaces
            templates.append({
                "uriTemplate": "k8s://namespaces",
                "name": "Kubernetes namespaces",
                "mimeType": "application/json",
                "description": "List of all Kubernetes namespaces"
            })
            
            # Add template for listing resources in a namespace
            templates.append({
                "uriTemplate": "k8s://{namespace}/{resource_type}",
                "name": "Kubernetes resources in namespace",
                "mimeType": "application/json",
                "description": "List of Kubernetes resources of a specific type in a namespace"
            })
            
            # Add template for getting a specific resource
            templates.append({
                "uriTemplate": "k8s://{namespace}/{resource_type}/{name}",
                "name": "Specific Kubernetes resource",
                "mimeType": "application/json",
                "description": "Details of a specific Kubernetes resource"
            })
            
            return templates
            return {
                "uriTemplate": "k8s://namespaces",
                "name": "Kubernetes namespaces",
                "mimeType": "application/json",
                "description": "List of all Kubernetes namespaces"
            }
        
    
    def _format_json(self, data: Any) -> str:
        """Format data as JSON string."""
        import json
        return json.dumps(data, indent=2)
    
    def _plural_to_singular(self, resource_type: str) -> str:
        """Convert plural resource type to singular."""
        mapping = {
            "pods": "pod",
            "deployments": "deployment",
            "services": "service",
            "configmaps": "configmap",
            "secrets": "secret",
            "ingresses": "ingress",
            "jobs": "job",
            "namespaces": "namespace"
        }
        return mapping.get(resource_type, resource_type)