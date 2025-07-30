"""
Tool handlers for the MCP server.
"""
from typing import Dict, Any, List, Optional
from mcp.types import JSONRPCError as McpError
from mcp.types import INVALID_REQUEST as ErrorCode

from services.kubernetes_service import KubernetesService
from utils.config import Config


class ToolHandlers:
    """Handlers for MCP tools."""
    
    def __init__(self):
        """Initialize tool handlers."""
        # Initialize services
        kubeconfig_path = Config.get_kubeconfig_path()
        self.k8s_service = KubernetesService(kubeconfig_path)
    
    async def handle_call_tool(self, request) -> Dict[str, Any]:
        """
        Handle tool call requests.
        
        Args:
            request: MCP tool call request
            
        Returns:
            Tool response
            
        Raises:
            McpError: If the tool is not found or if there's an error
        """
        tool_name = request.params.name
        arguments = request.params.arguments
        
        # Kubernetes tools
        if tool_name == "list_k8s_resources":
            return await self.list_k8s_resources(arguments)
        
        # Add more tools here
        
        # Tool not found
        raise McpError(
            ErrorCode.MethodNotFound,
            f"Unknown tool: {tool_name}"
        )
    
    async def list_k8s_resources(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        List Kubernetes resources of a specific type in a namespace.
        
        Args:
            arguments: Tool arguments
                - resource_type: Type of resource to list (pods, deployments, services, etc.)
                - namespace: Namespace to list resources from (optional)
                
        Returns:
            Tool response with the list of resources
        """
        # Validate arguments
        if not isinstance(arguments, dict):
            return self._create_error_response("Invalid arguments: must be a dictionary")
        
        if "resource_type" not in arguments:
            return self._create_error_response("Missing required argument: resource_type")
        
        resource_type = arguments["resource_type"]
        namespace = arguments.get("namespace")
        
        try:
            # Get resources from Kubernetes
            resources = self.k8s_service.list_resources(resource_type, namespace)
            
            # Format response
            namespace_info = f" in namespace '{namespace}'" if namespace else ""
            formatted_response = f"Kubernetes {resource_type}{namespace_info}:\n\n"
            
            if not resources:
                formatted_response += f"No {resource_type} found{namespace_info}."
            else:
                for i, resource in enumerate(resources, 1):
                    formatted_response += f"{i}. {resource['name']}\n"
                    
                    # Add resource-specific details
                    if resource_type == "pods":
                        formatted_response += f"   Status: {resource['status']}\n"
                        formatted_response += f"   Node: {resource['node']}\n"
                        formatted_response += f"   IP: {resource['ip']}\n"
                        formatted_response += "   Containers:\n"
                        for container in resource["containers"]:
                            ready_status = "Ready" if container["ready"] else "Not Ready"
                            formatted_response += f"     - {container['name']} ({container['image']}) - {ready_status}\n"
                    
                    elif resource_type == "deployments":
                        replicas = resource["replicas"]
                        formatted_response += f"   Replicas: {replicas['available']}/{replicas['desired']} ready\n"
                        formatted_response += "   Containers:\n"
                        for container in resource["containers"]:
                            formatted_response += f"     - {container['name']} ({container['image']})\n"
                    
                    elif resource_type == "services":
                        formatted_response += f"   Type: {resource['type']}\n"
                        formatted_response += f"   Cluster IP: {resource['cluster_ip']}\n"
                        if resource["ports"]:
                            formatted_response += "   Ports:\n"
                            for port in resource["ports"]:
                                formatted_response += f"     - {port['port']} → {port['target_port']} ({port['protocol']})\n"
                    
                    formatted_response += "\n"
            
            # Return formatted response
            return {
                "content": [
                    {
                        "type": "text",
                        "text": formatted_response,
                    }
                ]
            }
            
        except ValueError as e:
            return self._create_error_response(str(e))
        except RuntimeError as e:
            return self._create_error_response(str(e))
        except Exception as e:
            return self._create_error_response(f"Error listing Kubernetes resources: {str(e)}")
    
    def _create_error_response(self, message: str) -> Dict[str, Any]:
        """
        Create an error response.
        
        Args:
            message: Error message
            
        Returns:
            Error response
        """
        return {
            "content": [
                {
                    "type": "text",
                    "text": message,
                }
            ],
            "isError": True,
        }