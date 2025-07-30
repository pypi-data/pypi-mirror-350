"""
Kubernetes formatting utilities for the DevOps MCP Server.
"""
import yaml
from typing import Dict, Any, List, Optional
from utils.formatting import format_text_response, format_error_response


def format_as_yaml(data: Any) -> Dict[str, Any]:
    """
    Format data as YAML.
    
    Args:
        data: The data to format
        
    Returns:
        Formatted response with YAML content
    """
    yaml_content = yaml.dump(data, default_flow_style=False)
    return format_text_response(yaml_content)


def format_k8s_version(version_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format Kubernetes version information as YAML.
    
    Args:
        version_info: Dictionary with version information
        
    Returns:
        Formatted response with YAML content
    """
    return format_as_yaml(version_info)


def format_k8s_resources(resources: List[Dict[str, Any]], resource_type: str, namespace: Optional[str] = None) -> Dict[str, Any]:
    """
    Format Kubernetes resources list as YAML.
    
    Args:
        resources: List of resources
        resource_type: Type of resources
        namespace: Namespace of resources (optional)
        
    Returns:
        Formatted response with YAML content
    """
    # Add metadata about the request
    result = {
        "kind": f"{resource_type.capitalize()}List",
        "apiVersion": "v1",
        "metadata": {
            "resourceType": resource_type
        },
        "items": resources
    }
    
    if namespace:
        result["metadata"]["namespace"] = namespace
    
    return format_as_yaml(result)


def format_k8s_resource_detail(resource: Dict[str, Any], resource_type: str, namespace: Optional[str] = None) -> Dict[str, Any]:
    """
    Format detailed information about a Kubernetes resource as YAML.
    
    Args:
        resource: Resource details
        resource_type: Type of resource
        namespace: Namespace of resource (optional)
        
    Returns:
        Formatted response with YAML content
    """
    return format_as_yaml(resource)


def format_k8s_logs(logs: str, pod_name: str, namespace: str, container: Optional[str] = None, tail_lines: int = 100) -> Dict[str, Any]:
    """
    Format Kubernetes pod logs.
    
    Args:
        logs: Pod logs
        pod_name: Name of the pod
        namespace: Namespace of the pod
        container: Container name (optional)
        tail_lines: Number of lines from the end of the logs
        
    Returns:
        Formatted response with logs
    """
    if container:
        header = f"Logs for pod {pod_name} container {container} in namespace '{namespace}' (last {tail_lines} lines):\n\n"
    else:
        header = f"Logs for pod {pod_name} in namespace '{namespace}' (last {tail_lines} lines):\n\n"
    
    return format_text_response(header + logs)