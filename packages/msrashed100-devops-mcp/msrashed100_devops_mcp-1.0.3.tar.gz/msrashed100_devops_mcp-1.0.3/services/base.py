"""
Base service class for the DevOps MCP Server.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from utils.logging import setup_logger


class BaseService(ABC):
    """Base class for all services."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the service.
        
        Args:
            name: The service name
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.logger = setup_logger(f"devops_mcp_server.services.{name}")
        self.client = None
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the service client.
        This method should be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the service is available.
        This method should be implemented by subclasses.
        
        Returns:
            True if the service is available, False otherwise
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the service status.
        
        Returns:
            A dictionary with the service status
        """
        return {
            "name": self.name,
            "available": self.is_available(),
            "config": {k: v for k, v in self.config.items() if k != "password" and k != "api_key"}
        }
    
    def __str__(self) -> str:
        """String representation of the service."""
        return f"{self.name} Service"
    
    def __repr__(self) -> str:
        """Detailed string representation of the service."""
        return f"{self.__class__.__name__}(name='{self.name}', config={self.config})"


class ServiceRegistry:
    """Registry for all services."""
    
    def __init__(self):
        """Initialize the service registry."""
        self.services = {}
        self.logger = setup_logger("devops_mcp_server.services.registry")
    
    def register(self, service: BaseService) -> None:
        """
        Register a service.
        
        Args:
            service: The service to register
        """
        self.services[service.name] = service
        self.logger.info(f"Registered service: {service.name}")
    
    def get(self, name: str) -> Optional[BaseService]:
        """
        Get a service by name.
        
        Args:
            name: The service name
            
        Returns:
            The service instance or None if not found
        """
        return self.services.get(name)
    
    def get_all(self) -> Dict[str, BaseService]:
        """
        Get all registered services.
        
        Returns:
            A dictionary of service instances
        """
        return self.services
    
    def get_available(self) -> Dict[str, BaseService]:
        """
        Get all available services.
        
        Returns:
            A dictionary of available service instances
        """
        return {name: service for name, service in self.services.items() if service.is_available()}
    
    def get_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the status of all services.
        
        Returns:
            A dictionary with the status of all services
        """
        return {name: service.get_status() for name, service in self.services.items()}


# Create a global service registry
service_registry = ServiceRegistry()