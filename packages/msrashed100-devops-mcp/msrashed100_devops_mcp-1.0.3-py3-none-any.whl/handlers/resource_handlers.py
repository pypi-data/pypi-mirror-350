"""
Resource handlers for the MCP server.
"""
from typing import Dict, Any, List
from mcp.types import JSONRPCError as McpError
from mcp.types import INVALID_REQUEST as ErrorCode

from services.kubernetes_service import KubernetesService
from utils.config import Config


class ResourceHandlers:
    """Handlers for MCP resources."""
    
    def __init__(self):
        """Initialize resource handlers."""
        # Initialize services
        kubeconfig_path = Config.get_kubeconfig_path()
        self.k8s_service = KubernetesService(kubeconfig_path)
    
    async def handle_list_resources(self, request) -> Dict[str, Any]:
        """
        Handle list resources requests.
        
        Args:
            request: MCP list resources request
            
        Returns:
            List of available resources
        """
        resources = []
        
        # Add Kubernetes resources
        resources.append({
            "uri": "k8s://namespaces",
            "name": "Kubernetes namespaces",
            "mimeType": "application/json",
            "description": "List of all Kubernetes namespaces in the current context",
        })
        
        resources.append({
            "uri": "k8s://default/pods",
            "name": "Kubernetes pods in default namespace",
            "mimeType": "application/json",
            "description": "List of all pods in the default namespace",
        })
        
        return {"resources": resources}
    
    async def handle_list_resource_templates(self, request) -> Dict[str, Any]:
        """
        Handle list resource templates requests.
        
        Args:
            request: MCP list resource templates request
            
        Returns:
            List of available resource templates
        """
        templates = []
        
        # Add Kubernetes templates
        templates.append({
            "uriTemplate": "k8s://{namespace}/pods",
            "name": "Kubernetes pods in namespace",
            "mimeType": "application/json",
            "description": "List of all pods in the specified Kubernetes namespace",
        })
        
        templates.append({
            "uriTemplate": "k8s://{namespace}/deployments",
            "name": "Kubernetes deployments in namespace",
            "mimeType": "application/json",
            "description": "List of all deployments in the specified Kubernetes namespace",
        })
        
        templates.append({
            "uriTemplate": "k8s://{namespace}/services",
            "name": "Kubernetes services in namespace",
            "mimeType": "application/json",
            "description": "List of all services in the specified Kubernetes namespace",
        })
        
        return {"resourceTemplates": templates}
    
    async def handle_read_resource(self, request) -> Dict[str, Any]:
        """
        Handle read resource requests.
        
        Args:
            request: MCP read resource request
            
        Returns:
            Resource content
            
        Raises:
            McpError: If the resource is not found or if there's an error
        """
        uri = request.params.uri
        
        # Handle Kubernetes resources
        uri_str = str(uri)
        if uri_str.startswith("k8s://"):
            return await self._handle_k8s_resource(uri_str)
        
        # Resource not found
        raise McpError(
            ErrorCode.InvalidRequest,
            f"Invalid URI format: {uri_str}"
        )
    
    async def _handle_k8s_resource(self, uri: str) -> Dict[str, Any]:
        """
        Handle Kubernetes resource requests.
        
        Args:
            uri: Resource URI as a string
            
        Returns:
            Resource content
            
        Raises:
            McpError: If there's an error
        """
        try:
            # Parse URI
            parts = uri[len("k8s://"):].split("/")
            
            if len(parts) == 1 and parts[0] == "namespaces":
                # List all namespaces
                resources = self.k8s_service.list_resources("namespaces")
                return self._create_json_response(uri, resources)
            
            elif len(parts) == 2:
                # List resources in namespace
                namespace = parts[0]
                resource_type = parts[1]
                resources = self.k8s_service.list_resources(resource_type, namespace)
                return self._create_json_response(uri, resources)
            
            else:
                raise McpError(
                    ErrorCode.InvalidRequest,
                    f"Invalid Kubernetes URI format: {uri}"
                )
                
        except ValueError as e:
            raise McpError(
                ErrorCode.InvalidRequest,
                str(e)
            )
        except RuntimeError as e:
            raise McpError(
                ErrorCode.InternalError,
                str(e)
            )
        except Exception as e:
            raise McpError(
                ErrorCode.InternalError,
                f"Error handling Kubernetes resource: {str(e)}"
            )
    
    def _create_json_response(self, uri: str, data: Any) -> Dict[str, Any]:
        """
        Create a JSON response.
        
        Args:
            uri: Resource URI
            data: Response data
            
        Returns:
            JSON response
        """
        import json
        
        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "application/json",
                    "text": json.dumps(data, indent=2),
                }
            ]
        }