"""
Base MongoDB client for the DevOps MCP Server.
"""
import os
from typing import Dict, Any, Optional, List
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

from services.base import BaseService
from core.exceptions import ServiceConnectionError, ServiceOperationError
from config.settings import DATABASE_SETTINGS


class MongoDBService(BaseService):
    """Base service for interacting with MongoDB."""
    
    def __init__(self, uri: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the MongoDB service.
        
        Args:
            uri: MongoDB connection URI (default: from settings)
            timeout: Timeout for API calls in seconds (default: from settings)
        """
        mongodb_settings = DATABASE_SETTINGS.get("mongodb", {})
        super().__init__("mongodb", {
            "uri": uri or mongodb_settings.get("uri"),
            "timeout": timeout or mongodb_settings.get("timeout", 10)
        })
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize the MongoDB client."""
        try:
            self.uri = self.config.get("uri")
            self.timeout = self.config.get("timeout")
            
            self.logger.info(f"Initializing MongoDB client with URI: {self.uri}")
            
            # Initialize MongoDB client
            self.client = MongoClient(
                self.uri,
                serverSelectionTimeoutMS=self.timeout * 1000,  # Convert to milliseconds
                connectTimeoutMS=self.timeout * 1000,
                socketTimeoutMS=self.timeout * 1000
            )
            
            # Test connection
            self.is_available()
            
            self.logger.info("MongoDB client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize MongoDB client: {e}")
            raise ServiceConnectionError("mongodb", str(e))
    
    def is_available(self) -> bool:
        """
        Check if the MongoDB server is available.
        
        Returns:
            True if the server is available, False otherwise
        """
        try:
            # Ping the MongoDB server
            self.client.admin.command('ping')
            return True
        except Exception as e:
            self.logger.warning(f"MongoDB server is not available: {e}")
            return False
    
    def _handle_error(self, operation: str, error: Exception) -> None:
        """
        Handle an error from the MongoDB server.
        
        Args:
            operation: The operation that failed
            error: The exception that was raised
            
        Raises:
            ServiceOperationError: With details about the failure
        """
        self.logger.error(f"Error during MongoDB {operation}: {error}")
        raise ServiceOperationError("mongodb", f"{operation} failed: {str(error)}")