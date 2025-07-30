"""
Kubernetes client for the DevOps MCP Server.
"""
import os
from typing import Dict, Any, Optional, List
from kubernetes import client, config
from kubernetes.client.rest import ApiException

from services.base import BaseService
from core.exceptions import ServiceConnectionError, ServiceOperationError
from config.settings import KUBECONFIG_PATH, KUBERNETES_TIMEOUT


class KubernetesService(BaseService):
    """Service for interacting with Kubernetes."""
    
    def __init__(self, kubeconfig_path: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the Kubernetes service.
        
        Args:
            kubeconfig_path: Path to the kubeconfig file (default: from settings)
            timeout: Timeout for API calls in seconds (default: from settings)
        """
        super().__init__("kubernetes", {
            "kubeconfig_path": kubeconfig_path or KUBECONFIG_PATH,
            "timeout": timeout or KUBERNETES_TIMEOUT
        })
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize the Kubernetes client."""
        try:
            kubeconfig_path = self.config.get("kubeconfig_path")
            if kubeconfig_path and os.path.exists(kubeconfig_path):
                self.logger.info(f"Loading kubeconfig from {kubeconfig_path}")
                config.load_kube_config(config_file=kubeconfig_path)
            else:
                self.logger.info("Loading in-cluster config")
                config.load_incluster_config()
            
            # Create the API client
            self.client = client.ApiClient()
            
            # Create API clients
            self.core_api = client.CoreV1Api(self.client)
            self.apps_api = client.AppsV1Api(self.client)
            self.batch_api = client.BatchV1Api(self.client)
            self.networking_api = client.NetworkingV1Api(self.client)
            self.rbac_api = client.RbacAuthorizationV1Api(self.client)
            self.custom_objects_api = client.CustomObjectsApi(self.client)
            
            # Set timeout for API calls
            timeout = self.config.get("timeout")
            if timeout:
                client.Configuration.get_default_copy().connection_pool_maxsize = 32
                client.Configuration.get_default_copy().retries = 3
                client.Configuration.get_default_copy().timeout = timeout
            
            self.logger.info("Kubernetes client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Kubernetes client: {e}")
            raise ServiceConnectionError("kubernetes", str(e))
    
    def is_available(self) -> bool:
        """
        Check if the Kubernetes API is available.
        
        Returns:
            True if the API is available, False otherwise
        """
        try:
            # Try to list namespaces as a simple availability check
            self.core_api.list_namespace(limit=1)
            return True
        except Exception:
            return False
    
    def list_resources(self, resource_type: str, namespace: Optional[str] = None,
                      api_version: Optional[str] = None, label_selector: Optional[str] = None,
                      field_selector: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List Kubernetes resources of a specific type.
        
        Args:
            resource_type: Type of resource to list (pods, deployments, services, etc.)
            namespace: Namespace to list resources from (optional)
            api_version: API version to use (optional, defaults to the preferred version)
            label_selector: Label selector to filter resources (optional)
            field_selector: Field selector to filter resources (optional)
            limit: Maximum number of resources to return (optional)
            
        Returns:
            A list of resources
            
        Raises:
            ServiceOperationError: If the operation fails
        """
        try:
            resources = []
            
            if resource_type == "namespaces":
                # List namespaces
                namespaces = self.core_api.list_namespace()
                for ns in namespaces.items:
                    resources.append({
                        "name": ns.metadata.name,
                        "status": ns.status.phase,
                        "labels": ns.metadata.labels or {},
                        "creation_time": ns.metadata.creation_timestamp.isoformat() if ns.metadata.creation_timestamp else None
                    })
            
            elif resource_type == "pods":
                # List pods
                if namespace:
                    pods = self.core_api.list_namespaced_pod(namespace)
                else:
                    pods = self.core_api.list_pod_for_all_namespaces()
                
                for pod in pods.items:
                    containers = []
                    for container in pod.spec.containers:
                        container_status = next((cs for cs in pod.status.container_statuses if cs.name == container.name), None) if pod.status.container_statuses else None
                        containers.append({
                            "name": container.name,
                            "image": container.image,
                            "ready": container_status.ready if container_status else False
                        })
                    
                    resources.append({
                        "name": pod.metadata.name,
                        "namespace": pod.metadata.namespace,
                        "status": pod.status.phase,
                        "node": pod.spec.node_name,
                        "ip": pod.status.pod_ip,
                        "containers": containers,
                        "labels": pod.metadata.labels or {},
                        "creation_time": pod.metadata.creation_timestamp.isoformat() if pod.metadata.creation_timestamp else None
                    })
            
            elif resource_type == "deployments":
                # List deployments
                if namespace:
                    deployments = self.apps_api.list_namespaced_deployment(namespace)
                else:
                    deployments = self.apps_api.list_deployment_for_all_namespaces()
                
                for deployment in deployments.items:
                    containers = []
                    for container in deployment.spec.template.spec.containers:
                        containers.append({
                            "name": container.name,
                            "image": container.image
                        })
                    
                    resources.append({
                        "name": deployment.metadata.name,
                        "namespace": deployment.metadata.namespace,
                        "replicas": {
                            "desired": deployment.spec.replicas,
                            "available": deployment.status.available_replicas or 0,
                            "ready": deployment.status.ready_replicas or 0
                        },
                        "containers": containers,
                        "labels": deployment.metadata.labels or {},
                        "creation_time": deployment.metadata.creation_timestamp.isoformat() if deployment.metadata.creation_timestamp else None
                    })
            
            elif resource_type == "services":
                # List services
                if namespace:
                    services = self.core_api.list_namespaced_service(namespace)
                else:
                    services = self.core_api.list_service_for_all_namespaces()
                
                for service in services.items:
                    ports = []
                    for port in service.spec.ports:
                        ports.append({
                            "name": port.name,
                            "port": port.port,
                            "target_port": port.target_port,
                            "protocol": port.protocol
                        })
                    
                    resources.append({
                        "name": service.metadata.name,
                        "namespace": service.metadata.namespace,
                        "type": service.spec.type,
                        "cluster_ip": service.spec.cluster_ip,
                        "external_ip": service.spec.external_i_ps[0] if service.spec.external_i_ps else None,
                        "ports": ports,
                        "labels": service.metadata.labels or {},
                        "creation_time": service.metadata.creation_timestamp.isoformat() if service.metadata.creation_timestamp else None
                    })
            
            elif resource_type == "configmaps":
                # List configmaps
                if namespace:
                    configmaps = self.core_api.list_namespaced_config_map(namespace)
                else:
                    configmaps = self.core_api.list_config_map_for_all_namespaces()
                
                for configmap in configmaps.items:
                    resources.append({
                        "name": configmap.metadata.name,
                        "namespace": configmap.metadata.namespace,
                        "data_keys": list(configmap.data.keys()) if configmap.data else [],
                        "labels": configmap.metadata.labels or {},
                        "creation_time": configmap.metadata.creation_timestamp.isoformat() if configmap.metadata.creation_timestamp else None
                    })
            
            elif resource_type == "secrets":
                # List secrets
                if namespace:
                    secrets = self.core_api.list_namespaced_secret(namespace)
                else:
                    secrets = self.core_api.list_secret_for_all_namespaces()
                
                for secret in secrets.items:
                    resources.append({
                        "name": secret.metadata.name,
                        "namespace": secret.metadata.namespace,
                        "type": secret.type,
                        "data_keys": list(secret.data.keys()) if secret.data else [],
                        "labels": secret.metadata.labels or {},
                        "creation_time": secret.metadata.creation_timestamp.isoformat() if secret.metadata.creation_timestamp else None
                    })
            
            elif resource_type == "ingresses":
                # List ingresses
                if namespace:
                    ingresses = self.networking_api.list_namespaced_ingress(namespace)
                else:
                    ingresses = self.networking_api.list_ingress_for_all_namespaces()
                
                for ingress in ingresses.items:
                    hosts = []
                    for rule in ingress.spec.rules:
                        hosts.append(rule.host)
                    
                    resources.append({
                        "name": ingress.metadata.name,
                        "namespace": ingress.metadata.namespace,
                        "hosts": hosts,
                        "labels": ingress.metadata.labels or {},
                        "creation_time": ingress.metadata.creation_timestamp.isoformat() if ingress.metadata.creation_timestamp else None
                    })
            
            elif resource_type == "jobs":
                # List jobs
                if namespace:
                    jobs = self.batch_api.list_namespaced_job(namespace)
                else:
                    jobs = self.batch_api.list_job_for_all_namespaces()
                
                for job in jobs.items:
                    resources.append({
                        "name": job.metadata.name,
                        "namespace": job.metadata.namespace,
                        "status": {
                            "active": job.status.active or 0,
                            "succeeded": job.status.succeeded or 0,
                            "failed": job.status.failed or 0
                        },
                        "labels": job.metadata.labels or {},
                        "creation_time": job.metadata.creation_timestamp.isoformat() if job.metadata.creation_timestamp else None
                    })
            
            else:
                raise ValueError(f"Unsupported resource type: {resource_type}")
            
            return resources
        
        except ApiException as e:
            self.logger.error(f"Kubernetes API error: {e}")
            raise ServiceOperationError("kubernetes", f"list_{resource_type}", str(e))
        except ValueError as e:
            self.logger.error(f"Value error: {e}")
            raise ServiceOperationError("kubernetes", f"list_{resource_type}", str(e))
        except Exception as e:
            self.logger.error(f"Error listing {resource_type}: {e}")
            raise ServiceOperationError("kubernetes", f"list_{resource_type}", str(e))
    
    def describe_resource(self, resource_type: str, name: str, namespace: Optional[str] = None) -> Dict[str, Any]:
        """
        Describe a Kubernetes resource.
        
        Args:
            resource_type: Type of resource to describe
            name: Name of the resource
            namespace: Namespace of the resource (optional for cluster-wide resources)
            
        Returns:
            A dictionary with the resource details
            
        Raises:
            ServiceOperationError: If the operation fails
        """
        try:
            if resource_type == "pod":
                if not namespace:
                    raise ValueError("Namespace is required for pod resources")
                pod = self.core_api.read_namespaced_pod(name, namespace)
                return self._format_pod(pod)
            
            elif resource_type == "deployment":
                if not namespace:
                    raise ValueError("Namespace is required for deployment resources")
                deployment = self.apps_api.read_namespaced_deployment(name, namespace)
                return self._format_deployment(deployment)
            
            elif resource_type == "service":
                if not namespace:
                    raise ValueError("Namespace is required for service resources")
                service = self.core_api.read_namespaced_service(name, namespace)
                return self._format_service(service)
            
            elif resource_type == "namespace":
                namespace_obj = self.core_api.read_namespace(name)
                return self._format_namespace(namespace_obj)
            
            else:
                raise ValueError(f"Unsupported resource type: {resource_type}")
        
        except ApiException as e:
            self.logger.error(f"Kubernetes API error: {e}")
            raise ServiceOperationError("kubernetes", f"describe_{resource_type}", str(e))
        except ValueError as e:
            self.logger.error(f"Value error: {e}")
            raise ServiceOperationError("kubernetes", f"describe_{resource_type}", str(e))
        except Exception as e:
            self.logger.error(f"Error describing {resource_type}/{name}: {e}")
            raise ServiceOperationError("kubernetes", f"describe_{resource_type}", str(e))
    
    def get_pod_logs(self, pod_name: str, namespace: str, container: Optional[str] = None,
                    tail_lines: int = 100, previous: bool = False,
                    since_seconds: Optional[int] = None, timestamps: bool = False) -> str:
        """
        Get logs from a pod with advanced filtering options.
        
        Args:
            pod_name: Name of the pod
            namespace: Namespace of the pod
            container: Container name (optional)
            tail_lines: Number of lines to return from the end of the logs
            previous: Get logs from previous instance of the container if it exists
            since_seconds: Only return logs newer than a relative duration in seconds
            timestamps: Include timestamps on each line in the log output
            
        Returns:
            The pod logs
            
        Raises:
            ServiceOperationError: If the operation fails
        """
        try:
            return self.core_api.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                container=container,
                tail_lines=tail_lines,
                previous=previous,
                since_seconds=since_seconds,
                timestamps=timestamps
            )
        except ApiException as e:
            self.logger.error(f"Kubernetes API error: {e}")
            raise ServiceOperationError("kubernetes", "get_pod_logs", str(e))
        except Exception as e:
            self.logger.error(f"Error getting logs for pod {pod_name}: {e}")
            raise ServiceOperationError("kubernetes", "get_pod_logs", str(e))
    
    def _format_pod(self, pod) -> Dict[str, Any]:
        """Format a pod object for display."""
        containers = []
        for container in pod.spec.containers:
            container_status = next((cs for cs in pod.status.container_statuses if cs.name == container.name), None) if pod.status.container_statuses else None
            containers.append({
                "name": container.name,
                "image": container.image,
                "ready": container_status.ready if container_status else False,
                "restart_count": container_status.restart_count if container_status else 0,
                "state": self._format_container_state(container_status.state) if container_status and container_status.state else None
            })
        
        return {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
            "node": pod.spec.node_name,
            "ip": pod.status.pod_ip,
            "containers": containers,
            "labels": pod.metadata.labels or {},
            "annotations": pod.metadata.annotations or {},
            "creation_time": pod.metadata.creation_timestamp.isoformat() if pod.metadata.creation_timestamp else None,
            "volumes": [v.name for v in pod.spec.volumes] if pod.spec.volumes else []
        }
    
    def _format_deployment(self, deployment) -> Dict[str, Any]:
        """Format a deployment object for display."""
        containers = []
        for container in deployment.spec.template.spec.containers:
            containers.append({
                "name": container.name,
                "image": container.image,
                "resources": self._format_resources(container.resources) if container.resources else None
            })
        
        return {
            "name": deployment.metadata.name,
            "namespace": deployment.metadata.namespace,
            "replicas": {
                "desired": deployment.spec.replicas,
                "available": deployment.status.available_replicas or 0,
                "ready": deployment.status.ready_replicas or 0
            },
            "containers": containers,
            "labels": deployment.metadata.labels or {},
            "annotations": deployment.metadata.annotations or {},
            "creation_time": deployment.metadata.creation_timestamp.isoformat() if deployment.metadata.creation_timestamp else None,
            "strategy": deployment.spec.strategy.type if deployment.spec.strategy else None
        }
    
    def _format_service(self, service) -> Dict[str, Any]:
        """Format a service object for display."""
        ports = []
        for port in service.spec.ports:
            ports.append({
                "name": port.name,
                "port": port.port,
                "target_port": port.target_port,
                "protocol": port.protocol
            })
        
        return {
            "name": service.metadata.name,
            "namespace": service.metadata.namespace,
            "type": service.spec.type,
            "cluster_ip": service.spec.cluster_ip,
            "external_ip": service.spec.external_i_ps[0] if service.spec.external_i_ps else None,
            "ports": ports,
            "selector": service.spec.selector or {},
            "labels": service.metadata.labels or {},
            "annotations": service.metadata.annotations or {},
            "creation_time": service.metadata.creation_timestamp.isoformat() if service.metadata.creation_timestamp else None
        }
    
    def _format_namespace(self, namespace) -> Dict[str, Any]:
        """Format a namespace object for display."""
        return {
            "name": namespace.metadata.name,
            "status": namespace.status.phase,
            "labels": namespace.metadata.labels or {},
            "annotations": namespace.metadata.annotations or {},
            "creation_time": namespace.metadata.creation_timestamp.isoformat() if namespace.metadata.creation_timestamp else None
        }
    
    def _format_container_state(self, state) -> Dict[str, Any]:
        """Format a container state for display."""
        if state.running:
            return {
                "status": "running",
                "started_at": state.running.started_at.isoformat() if state.running.started_at else None
            }
        elif state.waiting:
            return {
                "status": "waiting",
                "reason": state.waiting.reason,
                "message": state.waiting.message
            }
        elif state.terminated:
            return {
                "status": "terminated",
                "reason": state.terminated.reason,
                "exit_code": state.terminated.exit_code,
                "started_at": state.terminated.started_at.isoformat() if state.terminated.started_at else None,
                "finished_at": state.terminated.finished_at.isoformat() if state.terminated.finished_at else None
            }
        return {"status": "unknown"}
    
    def _format_resources(self, resources) -> Dict[str, Dict[str, str]]:
        """Format container resources for display."""
        result = {}
        if resources.requests:
            result["requests"] = {k: v for k, v in resources.requests.items()}
        if resources.limits:
            result["limits"] = {k: v for k, v in resources.limits.items()}
        return result
    
    def get_version(self) -> Dict[str, Any]:
        """
        Get the Kubernetes version information.
        
        Returns:
            A dictionary with the version information
            
        Raises:
            ServiceOperationError: If the operation fails
        """
        try:
            version = self.core_api.get_code()
            return {
                "gitVersion": version.git_version,
                "buildDate": version.build_date,
                "goVersion": version.go_version,
                "platform": version.platform,
                "gitCommit": version.git_commit,
                "compiler": version.compiler,
                "major": version.major,
                "minor": version.minor
            }
        except ApiException as e:
            self.logger.error(f"Kubernetes API error: {e}")
            raise ServiceOperationError("kubernetes", "get_version", str(e))
        except Exception as e:
            self.logger.error(f"Error getting Kubernetes version: {e}")
            raise ServiceOperationError("kubernetes", "get_version", str(e))
    
    def get_api_resources(self) -> List[Dict[str, Any]]:
        """
        Get all available API resources in the cluster.
        
        Returns:
            A list of API resources
            
        Raises:
            ServiceOperationError: If the operation fails
        """
        try:
            api_resources = []
            
            # Create API client for discovery
            api_client = client.ApiClient()
            
            # Get API groups using the discovery API
            api_groups_response = api_client.call_api(
                '/apis', 'GET',
                auth_settings=['BearerToken'],
                response_type='object'
            )
            api_groups_data = api_groups_response[0]
            
            # Add core API resources (v1)
            core_api_resources_response = api_client.call_api(
                '/api/v1', 'GET',
                auth_settings=['BearerToken'],
                response_type='object'
            )
            core_api_data = core_api_resources_response[0]
            
            if 'resources' in core_api_data:
                for resource in core_api_data['resources']:
                    # Skip subresources like pods/log, pods/exec, etc.
                    if "/" in resource['name']:
                        continue
                    
                    api_resources.append({
                        "name": resource['name'],
                        "singularName": resource.get('singularName', ''),
                        "namespaced": resource.get('namespaced', False),
                        "kind": resource.get('kind', ''),
                        "verbs": resource.get('verbs', []),
                        "shortNames": resource.get('shortNames', []),
                        "apiVersion": "v1",
                        "group": ""
                    })
            
            # Add API resources from each group
            if 'groups' in api_groups_data:
                for group in api_groups_data['groups']:
                    group_name = group['name']
                    for version in group['versions']:
                        version_name = version['groupVersion']
                        try:
                            # Get resources for this API group version
                            group_resources_response = api_client.call_api(
                                f'/apis/{version_name}', 'GET',
                                auth_settings=['BearerToken'],
                                response_type='object'
                            )
                            group_data = group_resources_response[0]
                            
                            if 'resources' in group_data:
                                for resource in group_data['resources']:
                                    # Skip subresources like deployments/scale, etc.
                                    if "/" in resource['name']:
                                        continue
                                    
                                    api_resources.append({
                                        "name": resource['name'],
                                        "singularName": resource.get('singularName', ''),
                                        "namespaced": resource.get('namespaced', False),
                                        "kind": resource.get('kind', ''),
                                        "verbs": resource.get('verbs', []),
                                        "shortNames": resource.get('shortNames', []),
                                        "apiVersion": version_name,
                                        "group": group_name
                                    })
                        except Exception:
                            # Skip if we can't get resources for this group/version
                            pass
            
            return api_resources
        
        except ApiException as e:
            self.logger.error(f"Kubernetes API error: {e}")
            raise ServiceOperationError("kubernetes", "get_api_resources", str(e))
        except Exception as e:
            self.logger.error(f"Error getting API resources: {e}")
            raise ServiceOperationError("kubernetes", "get_api_resources", str(e))
    
    def get_resource(self, kind: str, name: str, api_version: str, namespace: str = None,
                     resource_type_for_error_reporting: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a specific Kubernetes resource using its discovered kind and api_version.
        
        Args:
            kind: The exact Kind of the resource (e.g., "ConfigMap", "Deployment").
            name: Name of the resource.
            api_version: API version of the resource (e.g., "v1", "apps/v1").
            namespace: Namespace of the resource (required for namespaced resources).
            resource_type_for_error_reporting: Original resource type string for error messages.
            
        Returns:
            A dictionary with the resource details.
            
        Raises:
            ServiceOperationError: If the operation fails.
            ValueError: If kind or api_version is not provided.
        """
        error_resource_name = resource_type_for_error_reporting or kind
        if not kind or not api_version:
            msg = "Both 'kind' and 'api_version' must be provided to get_resource."
            self.logger.error(msg)
            raise ValueError(msg)
            
        try:
            # Get the resource using the dynamic client
            import kubernetes.dynamic as dynamic
            
            # Create a dynamic client
            dynamic_client = dynamic.DynamicClient(self.client)
            
            # Get the API resource handle from the dynamic client
            api_resource = dynamic_client.resources.get(api_version=api_version, kind=kind)
            
            # Get the specific resource instance
            if namespace:
                resource = api_resource.get(name=name, namespace=namespace)
            else:
                resource = api_resource.get(name=name)
            
            if resource is None:
                 raise ServiceOperationError("kubernetes", f"get_{error_resource_name}", f"Resource {name} not found.")

            # Convert to dictionary
            return self._convert_to_dict(resource)
        
        except ApiException as e:
            self.logger.error(f"Kubernetes API error getting {error_resource_name}/{name}: {e}")
            raise ServiceOperationError("kubernetes", f"get_{error_resource_name}", str(e))
        except ValueError as e: # Catch ValueErrors from this method or dynamic client
            self.logger.error(f"Value error getting {error_resource_name}/{name}: {e}")
            raise ServiceOperationError("kubernetes", f"get_{error_resource_name}", str(e))
        except Exception as e: # Catch any other unexpected errors
            self.logger.error(f"Unexpected error getting {error_resource_name}/{name}: {e}")
            raise ServiceOperationError("kubernetes", f"get_{error_resource_name}", str(e))
    
    def get_resource_yaml(self, resource_type: str, name: str, namespace: str = None,
                         api_version: str = None) -> str:
        """
        Get the YAML definition of a Kubernetes resource.
        
        Args:
            resource_type: Type of resource to get
            name: Name of the resource
            namespace: Namespace of the resource (optional for cluster-scoped resources)
            api_version: API version to use (optional, defaults to the preferred version)
            
        Returns:
            A string with the YAML definition of the resource
            
        Raises:
            ServiceOperationError: If the operation fails
        """
        try:
            # Get the resource
            resource = self.get_resource(resource_type, name, namespace, api_version)
            
            # Convert to YAML
            import yaml
            return yaml.dump(resource, default_flow_style=False)
        
        except Exception as e:
            self.logger.error(f"Error getting YAML for {resource_type}/{name}: {e}")
            raise ServiceOperationError("kubernetes", f"get_{resource_type}_yaml", str(e))
    
    def get_resource_events(self, resource_type: str, name: str, namespace: str = None) -> List[Dict[str, Any]]:
        """
        Get events related to a specific Kubernetes resource.
        
        Args:
            resource_type: Type of resource
            name: Name of the resource
            namespace: Namespace of the resource (optional for cluster-scoped resources)
            
        Returns:
            A list of events related to the resource
            
        Raises:
            ServiceOperationError: If the operation fails
        """
        try:
            # Get the resource to get its UID
            resource = self.get_resource(resource_type, name, namespace)
            
            # Get events for the resource
            field_selector = f"involvedObject.uid={resource['metadata']['uid']}"
            
            if namespace:
                events = self.core_api.list_namespaced_event(
                    namespace=namespace,
                    field_selector=field_selector
                )
            else:
                events = self.core_api.list_event_for_all_namespaces(
                    field_selector=field_selector
                )
            
            # Convert to list of dictionaries
            return [self._convert_to_dict(event) for event in events.items]
        
        except ApiException as e:
            self.logger.error(f"Kubernetes API error: {e}")
            raise ServiceOperationError("kubernetes", f"get_{resource_type}_events", str(e))
        except Exception as e:
            self.logger.error(f"Error getting events for {resource_type}/{name}: {e}")
            raise ServiceOperationError("kubernetes", f"get_{resource_type}_events", str(e))
    
    def _convert_to_dict(self, obj) -> Dict[str, Any]:
        """Convert a Kubernetes object to a dictionary."""
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif isinstance(obj, dict):
            return obj
        elif isinstance(obj, list):
            return [self._convert_to_dict(item) for item in obj]
        else:
            return obj
    
    def get_resource_names(self, resource_type: str, namespace: Optional[str] = None,
                          api_version: Optional[str] = None, label_selector: Optional[str] = None,
                          field_selector: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get minimal information about resources (just names and basic metadata).
        
        Args:
            resource_type: Type of resource to list
            namespace: Namespace to list resources from (optional)
            api_version: API version to use (optional)
            label_selector: Label selector to filter resources (optional)
            field_selector: Field selector to filter resources (optional)
            limit: Maximum number of resources to return (optional)
            
        Returns:
            A list of minimal resource information
        """
        try:
            # Get the resources
            resources = self.list_resources(
                resource_type=resource_type,
                namespace=namespace,
                api_version=api_version,
                label_selector=label_selector,
                field_selector=field_selector,
                limit=limit
            )
            
            # Extract minimal information
            minimal_resources = []
            for resource in resources:
                minimal_info = {
                    "name": resource.get("name", ""),
                    "namespace": resource.get("namespace", "")
                }
                
                # Add a few key fields based on resource type
                if resource_type.lower() == "pods":
                    minimal_info["status"] = resource.get("status", "")
                    minimal_info["node"] = resource.get("node", "")
                elif resource_type.lower() in ["deployments", "statefulsets", "daemonsets"]:
                    if "replicas" in resource:
                        minimal_info["ready"] = f"{resource['replicas'].get('ready', 0)}/{resource['replicas'].get('desired', 0)}"
                elif resource_type.lower() == "services":
                    minimal_info["type"] = resource.get("type", "")
                    minimal_info["cluster_ip"] = resource.get("cluster_ip", "")
                
                minimal_resources.append(minimal_info)
            
            return minimal_resources
        
        except Exception as e:
            self.logger.error(f"Error getting resource names: {e}")
            raise ServiceOperationError("kubernetes", f"get_resource_names", str(e))