"""
Kubernetes service for interacting with Kubernetes clusters.
"""
import os
from typing import Dict, List, Optional, Any
from kubernetes import client, config
from kubernetes.client.rest import ApiException


class KubernetesService:
    """Service for interacting with Kubernetes clusters."""
    
    def __init__(self, kubeconfig_path: Optional[str] = None, timeout: int = 5):
        """
        Initialize the Kubernetes service.
        
        Args:
            kubeconfig_path: Path to kubeconfig file. If None, uses the value from
                             KUBECONFIG environment variable or default location.
            timeout: Timeout in seconds for Kubernetes API calls (default: 5 seconds)
        """
        self.kubeconfig_path = kubeconfig_path or os.environ.get("KUBECONFIG")
        self.timeout = timeout
        print(f"Kubernetes service initialized with timeout: {self.timeout} seconds")
        self._load_config()
        
        # Initialize API clients
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.batch_v1 = client.BatchV1Api()
        self.networking_v1 = client.NetworkingV1Api()
        
        # Set timeout for API clients
        self.core_v1.api_client.configuration.timeout = self.timeout
        self.apps_v1.api_client.configuration.timeout = self.timeout
        self.batch_v1.api_client.configuration.timeout = self.timeout
        self.networking_v1.api_client.configuration.timeout = self.timeout
        print(f"API client timeout set to {self.timeout} seconds")
        
        # Set additional debugging options
        for api_client in [self.core_v1.api_client, self.apps_v1.api_client,
                          self.batch_v1.api_client, self.networking_v1.api_client]:
            api_client.configuration.debug = True
            api_client.configuration.verify_ssl = False
            print(f"API client debug mode enabled, SSL verification disabled")
    
    def _load_config(self) -> None:
        """Load Kubernetes configuration from kubeconfig file."""
        try:
            if self.kubeconfig_path:
                config.load_kube_config(config_file=self.kubeconfig_path)
            else:
                # Try loading from default locations
                config.load_kube_config()
        except Exception as e:
            raise RuntimeError(f"Failed to load Kubernetes config: {str(e)}")
    
    def list_resources(self, resource_type: str, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List Kubernetes resources of a specific type in a namespace.
        
        Args:
            resource_type: Type of resource to list (pods, deployments, services, etc.)
            namespace: Namespace to list resources from. If None, uses all namespaces.
            
        Returns:
            List of resources as dictionaries
        """
        import time
        start_time = time.time()
        print(f"Starting Kubernetes API call for {resource_type} with timeout {self.timeout} seconds...")
        print(f"Using kubeconfig: {self.kubeconfig_path}")
        try:
            # Set a timeout for this specific operation
            timeout_seconds = self.timeout
            if resource_type == "pods":
                if namespace:
                    response = self.core_v1.list_namespaced_pod(namespace=namespace, _request_timeout=timeout_seconds)
                else:
                    response = self.core_v1.list_pod_for_all_namespaces(_request_timeout=timeout_seconds)
                
                return [self._pod_to_dict(item) for item in response.items]
                
            elif resource_type == "deployments":
                if namespace:
                    response = self.apps_v1.list_namespaced_deployment(namespace=namespace, _request_timeout=timeout_seconds)
                else:
                    response = self.apps_v1.list_deployment_for_all_namespaces(_request_timeout=timeout_seconds)
                
                return [self._deployment_to_dict(item) for item in response.items]
                
            elif resource_type == "services":
                if namespace:
                    response = self.core_v1.list_namespaced_service(namespace=namespace, _request_timeout=timeout_seconds)
                else:
                    response = self.core_v1.list_service_for_all_namespaces(_request_timeout=timeout_seconds)
                
                return [self._service_to_dict(item) for item in response.items]
                
            elif resource_type == "configmaps":
                if namespace:
                    response = self.core_v1.list_namespaced_config_map(namespace=namespace, _request_timeout=timeout_seconds)
                else:
                    response = self.core_v1.list_config_map_for_all_namespaces(_request_timeout=timeout_seconds)
                
                return [self._configmap_to_dict(item) for item in response.items]
                
            elif resource_type == "secrets":
                if namespace:
                    response = self.core_v1.list_namespaced_secret(namespace=namespace, _request_timeout=timeout_seconds)
                else:
                    response = self.core_v1.list_secret_for_all_namespaces(_request_timeout=timeout_seconds)
                
                return [self._secret_to_dict(item) for item in response.items]
                
            elif resource_type == "ingresses":
                if namespace:
                    response = self.networking_v1.list_namespaced_ingress(namespace=namespace, _request_timeout=timeout_seconds)
                else:
                    response = self.networking_v1.list_ingress_for_all_namespaces(_request_timeout=timeout_seconds)
                
                return [self._ingress_to_dict(item) for item in response.items]
                
            elif resource_type == "jobs":
                if namespace:
                    response = self.batch_v1.list_namespaced_job(namespace=namespace, _request_timeout=timeout_seconds)
                else:
                    response = self.batch_v1.list_job_for_all_namespaces(_request_timeout=timeout_seconds)
                
                return [self._job_to_dict(item) for item in response.items]
                
            elif resource_type == "namespaces":
                response = self.core_v1.list_namespace(_request_timeout=timeout_seconds)
                return [self._namespace_to_dict(item) for item in response.items]
                
            else:
                raise ValueError(f"Unsupported resource type: {resource_type}")
                
            elapsed_time = time.time() - start_time
            print(f"Kubernetes API call completed in {elapsed_time:.2f} seconds")
            return [self._namespace_to_dict(item) for item in response.items]
                
        except ApiException as e:
            elapsed_time = time.time() - start_time
            print(f"Kubernetes API error after {elapsed_time:.2f} seconds: {str(e)}")
            raise RuntimeError(f"Kubernetes API error: {str(e)}")
        except Exception as e:
            elapsed_time = time.time() - start_time
            error_message = f"Timeout or other error after {elapsed_time:.2f} seconds: {str(e)}"
            print(error_message)
            print(f"Exception type: {type(e).__name__}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
            if elapsed_time >= timeout_seconds:
                error_message = f"Kubernetes API call timed out after {timeout_seconds} seconds"
                print(error_message)
                raise RuntimeError(error_message)
            else:
                error_message = f"Error accessing Kubernetes API: {str(e)}"
                print(error_message)
                raise RuntimeError(error_message)
    
    def _pod_to_dict(self, pod) -> Dict[str, Any]:
        """Convert Pod object to dictionary."""
        return {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
            "ip": pod.status.pod_ip,
            "node": pod.spec.node_name if pod.spec.node_name else "None",
            "containers": [
                {
                    "name": container.name,
                    "image": container.image,
                    "ready": any(
                        status.name == container.name and status.ready
                        for status in pod.status.container_statuses
                    ) if pod.status.container_statuses else False
                }
                for container in pod.spec.containers
            ],
            "created_at": pod.metadata.creation_timestamp.isoformat() if pod.metadata.creation_timestamp else None,
        }
    
    def _deployment_to_dict(self, deployment) -> Dict[str, Any]:
        """Convert Deployment object to dictionary."""
        return {
            "name": deployment.metadata.name,
            "namespace": deployment.metadata.namespace,
            "replicas": {
                "desired": deployment.spec.replicas,
                "available": deployment.status.available_replicas if deployment.status.available_replicas else 0,
                "ready": deployment.status.ready_replicas if deployment.status.ready_replicas else 0,
            },
            "containers": [
                {
                    "name": container.name,
                    "image": container.image,
                }
                for container in deployment.spec.template.spec.containers
            ],
            "created_at": deployment.metadata.creation_timestamp.isoformat() if deployment.metadata.creation_timestamp else None,
        }
    
    def _service_to_dict(self, service) -> Dict[str, Any]:
        """Convert Service object to dictionary."""
        return {
            "name": service.metadata.name,
            "namespace": service.metadata.namespace,
            "type": service.spec.type,
            "cluster_ip": service.spec.cluster_ip,
            "ports": [
                {
                    "name": port.name if port.name else str(port.port),
                    "port": port.port,
                    "target_port": port.target_port,
                    "protocol": port.protocol,
                }
                for port in service.spec.ports
            ] if service.spec.ports else [],
            "created_at": service.metadata.creation_timestamp.isoformat() if service.metadata.creation_timestamp else None,
        }
    
    def _configmap_to_dict(self, configmap) -> Dict[str, Any]:
        """Convert ConfigMap object to dictionary."""
        return {
            "name": configmap.metadata.name,
            "namespace": configmap.metadata.namespace,
            "data_keys": list(configmap.data.keys()) if configmap.data else [],
            "created_at": configmap.metadata.creation_timestamp.isoformat() if configmap.metadata.creation_timestamp else None,
        }
    
    def _secret_to_dict(self, secret) -> Dict[str, Any]:
        """Convert Secret object to dictionary."""
        return {
            "name": secret.metadata.name,
            "namespace": secret.metadata.namespace,
            "type": secret.type,
            "data_keys": list(secret.data.keys()) if secret.data else [],
            "created_at": secret.metadata.creation_timestamp.isoformat() if secret.metadata.creation_timestamp else None,
        }
    
    def _ingress_to_dict(self, ingress) -> Dict[str, Any]:
        """Convert Ingress object to dictionary."""
        return {
            "name": ingress.metadata.name,
            "namespace": ingress.metadata.namespace,
            "hosts": [
                {
                    "host": rule.host if rule.host else "*",
                    "paths": [
                        {
                            "path": path.path if path.path else "/",
                            "path_type": path.path_type,
                            "backend": {
                                "service": path.backend.service.name if path.backend.service else None,
                                "port": path.backend.service.port.number if path.backend.service and path.backend.service.port else None,
                            }
                        }
                        for path in rule.http.paths
                    ] if rule.http and rule.http.paths else []
                }
                for rule in ingress.spec.rules
            ] if ingress.spec.rules else [],
            "created_at": ingress.metadata.creation_timestamp.isoformat() if ingress.metadata.creation_timestamp else None,
        }
    
    def _job_to_dict(self, job) -> Dict[str, Any]:
        """Convert Job object to dictionary."""
        return {
            "name": job.metadata.name,
            "namespace": job.metadata.namespace,
            "status": {
                "active": job.status.active if job.status.active else 0,
                "succeeded": job.status.succeeded if job.status.succeeded else 0,
                "failed": job.status.failed if job.status.failed else 0,
            },
            "containers": [
                {
                    "name": container.name,
                    "image": container.image,
                }
                for container in job.spec.template.spec.containers
            ],
            "created_at": job.metadata.creation_timestamp.isoformat() if job.metadata.creation_timestamp else None,
        }
    
    def _namespace_to_dict(self, namespace) -> Dict[str, Any]:
        """Convert Namespace object to dictionary."""
        return {
            "name": namespace.metadata.name,
            "status": namespace.status.phase,
            "created_at": namespace.metadata.creation_timestamp.isoformat() if namespace.metadata.creation_timestamp else None,
        }