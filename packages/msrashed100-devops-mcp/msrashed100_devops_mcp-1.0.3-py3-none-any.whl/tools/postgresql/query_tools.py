"""
PostgreSQL query tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.postgresql.service import PostgreSQLServiceManager
from tools.postgresql.base_tools import PostgreSQLBaseTools
from utils.logging import setup_logger


class PostgreSQLQueryTools(PostgreSQLBaseTools):
    """Tools for PostgreSQL query operations."""
    
    def __init__(self, mcp: FastMCP, postgresql_service: Optional[PostgreSQLServiceManager] = None):
        """
        Initialize PostgreSQL query tools.
        
        Args:
            mcp: The MCP server instance
            postgresql_service: The PostgreSQL service manager instance (optional)
        """
        super().__init__(mcp, postgresql_service)
        self.logger = setup_logger("devops_mcp_server.tools.postgresql.query")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register PostgreSQL query tools with the MCP server."""
        
        @self.mcp.tool()
        def execute_postgresql_query(query: str, params: str = None, database: str = None, limit: int = 100) -> str:
            """
            Execute a SQL query on a PostgreSQL database.
            
            This tool executes a SQL query on a database in the PostgreSQL server.
            
            Args:
                query: SQL query to execute
                params: Query parameters in JSON format (optional)
                database: Database name (optional, uses the current connection if not specified)
                limit: Maximum number of rows to return (default: 100, max: 500)
                
            Returns:
                Query results in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                # Parse parameters if provided
                params_list = None
                if params:
                    import json
                    params_list = json.loads(params)
                
                results = self.postgresql_service.query.execute_query(query, params_list, database, limit)
                return self._format_response(results)
            except Exception as e:
                self.logger.error(f"Error executing PostgreSQL query: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_postgresql_table_data(table: str, columns: str = None, where: str = None,
                                    params: str = None, order_by: str = None, limit: int = 100,
                                    database: str = None, schema: str = "public") -> str:
            """
            Get data from a PostgreSQL table.
            
            This tool retrieves data from a table in a schema in a database in the PostgreSQL server.
            
            Args:
                table: Table name
                columns: Comma-separated list of columns to select (optional)
                where: WHERE clause (optional)
                params: Query parameters for WHERE clause in JSON format (optional)
                order_by: ORDER BY clause (optional)
                limit: Maximum number of rows to return (default: 100, max: 500)
                database: Database name (optional, uses the current connection if not specified)
                schema: Schema name (default: public)
                
            Returns:
                Table data in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                # Parse columns if provided
                columns_list = None
                if columns:
                    columns_list = [col.strip() for col in columns.split(",")]
                
                # Parse parameters if provided
                params_list = None
                if params:
                    import json
                    params_list = json.loads(params)
                
                results = self.postgresql_service.query.get_table_data(
                    table, columns_list, where, params_list, order_by, limit, database, schema
                )
                return self._format_response(results)
            except Exception as e:
                self.logger.error(f"Error getting PostgreSQL table data: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def explain_postgresql_query(query: str, params: str = None, database: str = None) -> str:
            """
            Explain a SQL query on a PostgreSQL database.
            
            This tool explains a SQL query on a database in the PostgreSQL server.
            
            Args:
                query: SQL query to explain
                params: Query parameters in JSON format (optional)
                database: Database name (optional, uses the current connection if not specified)
                
            Returns:
                Query explanation in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            try:
                # Parse parameters if provided
                params_list = None
                if params:
                    import json
                    params_list = json.loads(params)
                
                explanation = self.postgresql_service.query.explain_query(query, params_list, database)
                return self._format_response(explanation)
            except Exception as e:
                self.logger.error(f"Error explaining PostgreSQL query: {e}")
                return self._format_error(str(e))