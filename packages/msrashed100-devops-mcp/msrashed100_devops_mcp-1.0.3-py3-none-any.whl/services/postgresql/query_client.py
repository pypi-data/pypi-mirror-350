"""
PostgreSQL query client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from psycopg2 import sql

from services.postgresql.client import PostgreSQLService


class PostgreSQLQueryClient:
    """Client for PostgreSQL query operations."""
    
    def __init__(self, postgresql_service: PostgreSQLService):
        """
        Initialize the PostgreSQL query client.
        
        Args:
            postgresql_service: The base PostgreSQL service
        """
        self.postgresql = postgresql_service
        self.logger = postgresql_service.logger
    
    def execute_query(self, query: str, params: Optional[List[Any]] = None, 
                     database: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Execute a SQL query.
        
        Args:
            query: SQL query to execute
            params: Query parameters (optional)
            database: Database name (optional, uses the current connection if not specified)
            limit: Maximum number of rows to return
            
        Returns:
            Query results
        """
        try:
            # Create a new service instance if a different database is specified
            service = self._get_service_for_database(database)
            
            # Add LIMIT clause if not present
            if "LIMIT" not in query.upper() and "limit" not in query.lower():
                query = f"{query} LIMIT {limit}"
            
            # Execute the query
            results = service._execute_query(query, params)
            
            # Apply limit if needed
            if results and len(results) > limit:
                results = results[:limit]
            
            return {
                "rows": results,
                "count": len(results) if results else 0
            }
        except Exception as e:
            self.postgresql._handle_error("execute_query", e)
    
    def get_table_data(self, table: str, columns: Optional[List[str]] = None,
                      where: Optional[str] = None, params: Optional[List[Any]] = None,
                      order_by: Optional[str] = None, limit: int = 100,
                      database: Optional[str] = None, schema: str = "public") -> Dict[str, Any]:
        """
        Get data from a table.
        
        Args:
            table: Table name
            columns: Columns to select (optional, selects all columns if not specified)
            where: WHERE clause (optional)
            params: Query parameters for WHERE clause (optional)
            order_by: ORDER BY clause (optional)
            limit: Maximum number of rows to return
            database: Database name (optional, uses the current connection if not specified)
            schema: Schema name (default: public)
            
        Returns:
            Table data
        """
        try:
            # Create a new service instance if a different database is specified
            service = self._get_service_for_database(database)
            
            # Build the query
            query_parts = []
            
            # SELECT clause
            if columns:
                columns_str = ", ".join(columns)
                query_parts.append(f"SELECT {columns_str}")
            else:
                query_parts.append("SELECT *")
            
            # FROM clause
            query_parts.append(f"FROM {schema}.{table}")
            
            # WHERE clause
            if where:
                query_parts.append(f"WHERE {where}")
            
            # ORDER BY clause
            if order_by:
                query_parts.append(f"ORDER BY {order_by}")
            
            # LIMIT clause
            query_parts.append(f"LIMIT {limit}")
            
            # Join the query parts
            query = " ".join(query_parts)
            
            # Execute the query
            results = service._execute_query(query, params)
            
            return {
                "rows": results,
                "count": len(results) if results else 0
            }
        except Exception as e:
            self.postgresql._handle_error("get_table_data", e)
    
    def get_query_columns(self, query: str, params: Optional[List[Any]] = None,
                         database: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get column information for a query.
        
        Args:
            query: SQL query
            params: Query parameters (optional)
            database: Database name (optional, uses the current connection if not specified)
            
        Returns:
            Column information
        """
        try:
            # Create a new service instance if a different database is specified
            service = self._get_service_for_database(database)
            
            # Create a connection
            with service._get_connection() as conn:
                # Create a cursor
                with conn.cursor() as cursor:
                    # Prepare the query
                    cursor.execute(f"PREPARE stmt AS {query}")
                    
                    # Get column information
                    cursor.execute("""
                    SELECT name, pg_catalog.format_type(type, NULL) as type
                    FROM pg_prepared_statement
                    JOIN pg_catalog.pg_type ON type = pg_type.oid
                    WHERE name = 'stmt'
                    """)
                    
                    columns = cursor.fetchall()
                    
                    # Deallocate the prepared statement
                    cursor.execute("DEALLOCATE stmt")
                    
                    return columns
        except Exception as e:
            self.postgresql._handle_error("get_query_columns", e)
    
    def explain_query(self, query: str, params: Optional[List[Any]] = None,
                     database: Optional[str] = None) -> Dict[str, Any]:
        """
        Explain a SQL query.
        
        Args:
            query: SQL query to explain
            params: Query parameters (optional)
            database: Database name (optional, uses the current connection if not specified)
            
        Returns:
            Query explanation
        """
        try:
            # Create a new service instance if a different database is specified
            service = self._get_service_for_database(database)
            
            # Execute the EXPLAIN query
            explain_query = f"EXPLAIN (FORMAT JSON) {query}"
            result = service._execute_query(explain_query, params, fetch_all=False)
            
            # Extract the plan
            if result and len(result) > 0:
                return result[0]
            else:
                return {}
        except Exception as e:
            self.postgresql._handle_error("explain_query", e)
    
    def _get_service_for_database(self, database: Optional[str] = None) -> PostgreSQLService:
        """
        Get a PostgreSQL service for a specific database.
        
        Args:
            database: Database name (optional, uses the current connection if not specified)
            
        Returns:
            PostgreSQL service
        """
        if database and database != self.postgresql.database:
            # Create a new service instance for the specified database
            return PostgreSQLService(
                host=self.postgresql.host,
                port=self.postgresql.port,
                user=self.postgresql.user,
                password=self.postgresql.password,
                database=database,
                timeout=self.postgresql.timeout
            )
        else:
            # Use the current service
            return self.postgresql