"""
Base AWS client for the DevOps MCP Server.
"""
import os
import importlib
from typing import Dict, Any, Optional, List

from services.base import BaseService
from core.exceptions import ServiceConnectionError, ServiceOperationError
from config.settings import AWS_PROFILE, AWS_REGION

# Check if boto3 is available
try:
    boto3 = importlib.import_module('boto3')
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False


class AWSService(BaseService):
    """Base service for interacting with AWS."""
    
    def __init__(self, region: Optional[str] = None, profile: Optional[str] = None):
        """
        Initialize the AWS service.
        
        Args:
            region: AWS region (default: from settings)
            profile: AWS profile name (default: from settings)
        """
        super().__init__("aws", {
            "profile": profile or AWS_PROFILE or os.environ.get("AWS_PROFILE", "default"),
            "region": region or AWS_REGION or os.environ.get("AWS_REGION", "us-east-1")
        })
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize the AWS client."""
        try:
            self.profile = self.config.get("profile")
            self.region = self.config.get("region")
            
            self.logger.info(f"Initializing AWS client with profile: {self.profile} and region: {self.region}")
            
            if not BOTO3_AVAILABLE:
                self.logger.error("boto3 module is not installed. Please install it with 'pip install boto3'")
                self.session = None
                return
            
            # Initialize AWS session
            self.session = boto3.Session(
                profile_name=self.profile,
                region_name=self.region
            )
            
            # Test connection
            self.is_available()
            
            self.logger.info("AWS client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize AWS client: {e}")
            raise ServiceConnectionError("aws", str(e))
    
    def is_available(self) -> bool:
        """
        Check if the AWS API is available.
        
        Returns:
            True if the API is available, False otherwise
        """
        if not BOTO3_AVAILABLE:
            self.logger.warning("boto3 module is not installed. AWS service is not available.")
            return False
            
        if self.session is None:
            return False
            
        try:
            # Try to use STS to validate credentials
            sts = self.session.client('sts')
            sts.get_caller_identity()
            return True
        except Exception as e:
            self.logger.warning(f"AWS API is not available: {e}")
            return False
    
    def get_client(self, service_name: str) -> Any:
        """
        Get an AWS service client.
        
        Args:
            service_name: AWS service name (e.g., 's3', 'ec2', 'ecs')
            
        Returns:
            AWS service client
        """
        if not self.is_available():
            raise ServiceConnectionError("aws", "AWS service is not available")
        
        try:
            return self.session.client(service_name)
        except Exception as e:
            self.logger.error(f"Failed to get AWS client for {service_name}: {e}")
            raise ServiceConnectionError("aws", f"Failed to get AWS client for {service_name}: {str(e)}")
    
    def get_resource(self, service_name: str) -> Any:
        """
        Get an AWS service resource.
        
        Args:
            service_name: AWS service name (e.g., 's3', 'ec2', 'dynamodb')
            
        Returns:
            AWS service resource
        """
        if not self.is_available():
            raise ServiceConnectionError("aws", "AWS service is not available")
        
        try:
            return self.session.resource(service_name)
        except Exception as e:
            self.logger.error(f"Failed to get AWS resource for {service_name}: {e}")
            raise ServiceConnectionError("aws", f"Failed to get AWS resource for {service_name}: {str(e)}")
    
    def _handle_error(self, operation: str, error: Exception) -> None:
        """
        Handle an error from the AWS API.
        
        Args:
            operation: The operation that failed
            error: The exception that was raised
            
        Raises:
            ServiceOperationError: With details about the failure
        """
        self.logger.error(f"Error during AWS {operation}: {error}")
        raise ServiceOperationError("aws", f"{operation} failed: {str(error)}")