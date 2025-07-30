"""
Base PostgreSQL client for the DevOps MCP Server.
"""
import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from typing import Dict, Any, Optional, List, Tuple

from services.base import BaseService
from core.exceptions import ServiceConnectionError, ServiceOperationError
from config.settings import DATABASE_SETTINGS


class PostgreSQLService(BaseService):
    """Base service for interacting with PostgreSQL."""
    
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None,
                user: Optional[str] = None, password: Optional[str] = None,
                database: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the PostgreSQL service.
        
        Args:
            host: PostgreSQL server host (default: from settings)
            port: PostgreSQL server port (default: from settings)
            user: PostgreSQL username (default: from settings)
            password: PostgreSQL password (default: from settings)
            database: PostgreSQL database name (default: from settings)
            timeout: Timeout for API calls in seconds (default: from settings)
        """
        postgres_settings = DATABASE_SETTINGS.get("postgres", {})
        super().__init__("postgresql", {
            "host": host or postgres_settings.get("host", "localhost"),
            "port": port or postgres_settings.get("port", 5432),
            "user": user or postgres_settings.get("user", "postgres"),
            "password": password or postgres_settings.get("password", ""),
            "database": database,  # Can be None to connect to the default database
            "timeout": timeout or postgres_settings.get("timeout", 10)
        })
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize the PostgreSQL client."""
        try:
            self.host = self.config.get("host")
            self.port = self.config.get("port")
            self.user = self.config.get("user")
            self.password = self.config.get("password")
            self.database = self.config.get("database")
            self.timeout = self.config.get("timeout")
            
            self.logger.info(f"Initializing PostgreSQL client with host: {self.host}, port: {self.port}, database: {self.database or 'default'}")
            
            # Initialize connection parameters
            self.connection_params = {
                "host": self.host,
                "port": self.port,
                "user": self.user,
                "password": self.password,
                "connect_timeout": self.timeout
            }
            
            # Add database if specified
            if self.database:
                self.connection_params["dbname"] = self.database
            
            # Test connection
            self.is_available()
            
            self.logger.info("PostgreSQL client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize PostgreSQL client: {e}")
            raise ServiceConnectionError("postgresql", str(e))
    
    def is_available(self) -> bool:
        """
        Check if the PostgreSQL server is available.
        
        Returns:
            True if the server is available, False otherwise
        """
        try:
            # Create a connection
            with self._get_connection() as conn:
                # Test the connection
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    cursor.fetchone()
            return True
        except Exception as e:
            self.logger.warning(f"PostgreSQL server is not available: {e}")
            return False
    
    def _get_connection(self):
        """
        Get a PostgreSQL connection.
        
        Returns:
            A PostgreSQL connection
        """
        try:
            return psycopg2.connect(**self.connection_params)
        except Exception as e:
            self.logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise ServiceConnectionError("postgresql", str(e))
    
    def _execute_query(self, query: str, params: Optional[Tuple] = None, 
                      fetch_all: bool = True, as_dict: bool = True) -> Any:
        """
        Execute a SQL query.
        
        Args:
            query: SQL query to execute
            params: Query parameters (optional)
            fetch_all: Whether to fetch all results (default: True)
            as_dict: Whether to return results as dictionaries (default: True)
            
        Returns:
            Query results
        """
        try:
            # Create a connection
            with self._get_connection() as conn:
                # Create a cursor
                cursor_factory = RealDictCursor if as_dict else None
                with conn.cursor(cursor_factory=cursor_factory) as cursor:
                    # Execute the query
                    cursor.execute(query, params)
                    
                    # Fetch results if needed
                    if fetch_all:
                        return cursor.fetchall()
                    elif cursor.description:
                        return cursor.fetchone()
                    else:
                        return None
        except Exception as e:
            self.logger.error(f"Failed to execute query: {e}")
            raise ServiceOperationError("postgresql", f"Query execution failed: {str(e)}")
    
    def _handle_error(self, operation: str, error: Exception) -> None:
        """
        Handle an error from the PostgreSQL server.
        
        Args:
            operation: The operation that failed
            error: The exception that was raised
            
        Raises:
            ServiceOperationError: With details about the failure
        """
        self.logger.error(f"Error during PostgreSQL {operation}: {error}")
        raise ServiceOperationError("postgresql", f"{operation} failed: {str(error)}")