"""
MongoDB service manager for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from services.mongodb.client import MongoDBService
from services.mongodb.database_client import MongoDBDatabaseClient
from services.mongodb.collection_client import MongoDBCollectionClient
from services.mongodb.info_client import MongoDBInfoClient


class MongoDBServiceManager:
    """Manager for all MongoDB services."""
    
    def __init__(self, uri: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the MongoDB service manager.
        
        Args:
            uri: MongoDB connection URI
            timeout: Timeout for API calls in seconds
        """
        # Initialize the base service
        self.base_service = MongoDBService(uri, timeout)
        
        # Initialize specialized clients
        self.database = MongoDBDatabaseClient(self.base_service)
        self.collection = MongoDBCollectionClient(self.base_service)
        self.info = MongoDBInfoClient(self.base_service)
        
        self.logger = self.base_service.logger
        self.logger.info("MongoDB service manager initialized")
    
    def is_available(self) -> bool:
        """
        Check if the MongoDB server is available.
        
        Returns:
            True if the server is available, False otherwise
        """
        return self.base_service.is_available()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the service status.
        
        Returns:
            A dictionary with the service status
        """
        return self.base_service.get_status()