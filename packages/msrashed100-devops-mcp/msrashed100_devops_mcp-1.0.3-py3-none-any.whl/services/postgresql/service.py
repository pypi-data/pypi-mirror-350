"""
PostgreSQL service manager for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from services.postgresql.client import PostgreSQLService
from services.postgresql.database_client import PostgreSQLDatabaseClient
from services.postgresql.query_client import PostgreSQLQueryClient
from services.postgresql.info_client import PostgreSQLInfoClient


class PostgreSQLServiceManager:
    """Manager for all PostgreSQL services."""
    
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None,
                user: Optional[str] = None, password: Optional[str] = None,
                database: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the PostgreSQL service manager.
        
        Args:
            host: PostgreSQL server host
            port: PostgreSQL server port
            user: PostgreSQL username
            password: PostgreSQL password
            database: PostgreSQL database name
            timeout: Timeout for API calls in seconds
        """
        # Initialize the base service
        self.base_service = PostgreSQLService(host, port, user, password, database, timeout)
        
        # Initialize specialized clients
        self.database = PostgreSQLDatabaseClient(self.base_service)
        self.query = PostgreSQLQueryClient(self.base_service)
        self.info = PostgreSQLInfoClient(self.base_service)
        
        self.logger = self.base_service.logger
        self.logger.info("PostgreSQL service manager initialized")
    
    def is_available(self) -> bool:
        """
        Check if the PostgreSQL server is available.
        
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