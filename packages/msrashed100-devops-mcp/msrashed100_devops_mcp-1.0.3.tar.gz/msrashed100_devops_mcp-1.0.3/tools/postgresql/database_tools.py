"""
PostgreSQL database tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.postgresql.service import PostgreSQLServiceManager
from tools.postgresql.base_tools import PostgreSQLBaseTools
from utils.logging import setup_logger


class PostgreSQLDatabaseTools(PostgreSQLBaseTools):
    """Tools for PostgreSQL database operations."""
    
    def __init__(self, mcp: FastMCP, postgresql_service: Optional[PostgreSQLServiceManager] = None):
        """
        Initialize PostgreSQL database tools.
        
        Args:
            mcp: The MCP server instance
            postgresql_service: The PostgreSQL service manager instance (optional)
        """
        super().__init__(mcp, postgresql_service)
        self.logger = setup_logger("devops_mcp_server.tools.postgresql.database")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register PostgreSQL database tools with the MCP server."""
        
        @self.mcp.tool()
        def list_postgresql_databases(limit: int = 100) -> str:
            """
            List all PostgreSQL databases.
            
            This tool lists all databases in the PostgreSQL server.
            
            Args:
                limit: Maximum number of databases to return (default: 100, max: 500)
                
            Returns:
                List of databases in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                databases = self.postgresql_service.database.list_databases(limit)
                return self._format_response({"databases": databases, "count": len(databases)})
            except Exception as e:
                self.logger.error(f"Error listing PostgreSQL databases: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_postgresql_database_info(database: str) -> str:
            """
            Get information about a PostgreSQL database.
            
            This tool retrieves information about a database in the PostgreSQL server.
            
            Args:
                database: Database name
                
            Returns:
                Database information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            try:
                info = self.postgresql_service.database.get_database_info(database)
                return self._format_response(info)
            except Exception as e:
                self.logger.error(f"Error getting PostgreSQL database info: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_postgresql_schemas(database: str = None, limit: int = 100) -> str:
            """
            List all schemas in a PostgreSQL database.
            
            This tool lists all schemas in a database in the PostgreSQL server.
            
            Args:
                database: Database name (optional, uses the current connection if not specified)
                limit: Maximum number of schemas to return (default: 100, max: 500)
                
            Returns:
                List of schemas in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                schemas = self.postgresql_service.database.list_schemas(database, limit)
                return self._format_response({"schemas": schemas, "count": len(schemas)})
            except Exception as e:
                self.logger.error(f"Error listing PostgreSQL schemas: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_postgresql_tables(database: str = None, schema: str = "public", limit: int = 100) -> str:
            """
            List all tables in a PostgreSQL schema.
            
            This tool lists all tables in a schema in a database in the PostgreSQL server.
            
            Args:
                database: Database name (optional, uses the current connection if not specified)
                schema: Schema name (default: public)
                limit: Maximum number of tables to return (default: 100, max: 500)
                
            Returns:
                List of tables in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                tables = self.postgresql_service.database.list_tables(database, schema, limit)
                return self._format_response({"tables": tables, "count": len(tables)})
            except Exception as e:
                self.logger.error(f"Error listing PostgreSQL tables: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_postgresql_table_info(table: str, database: str = None, schema: str = "public") -> str:
            """
            Get information about a PostgreSQL table.
            
            This tool retrieves information about a table in a schema in a database in the PostgreSQL server.
            
            Args:
                table: Table name
                database: Database name (optional, uses the current connection if not specified)
                schema: Schema name (default: public)
                
            Returns:
                Table information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            try:
                info = self.postgresql_service.database.get_table_info(table, database, schema)
                return self._format_response(info)
            except Exception as e:
                self.logger.error(f"Error getting PostgreSQL table info: {e}")
                return self._format_error(str(e))