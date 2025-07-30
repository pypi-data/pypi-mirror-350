"""
PostgreSQL database client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from psycopg2 import sql

from services.postgresql.client import PostgreSQLService


class PostgreSQLDatabaseClient:
    """Client for PostgreSQL database operations."""
    
    def __init__(self, postgresql_service: PostgreSQLService):
        """
        Initialize the PostgreSQL database client.
        
        Args:
            postgresql_service: The base PostgreSQL service
        """
        self.postgresql = postgresql_service
        self.logger = postgresql_service.logger
    
    def list_databases(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all databases.
        
        Args:
            limit: Maximum number of databases to return
            
        Returns:
            List of databases
        """
        try:
            query = """
            SELECT d.datname as name, 
                   pg_catalog.pg_get_userbyid(d.datdba) as owner,
                   pg_catalog.pg_encoding_to_char(d.encoding) as encoding,
                   d.datcollate as collate,
                   d.datctype as ctype,
                   pg_catalog.array_to_string(d.datacl, E'\n') as access_privileges,
                   CASE WHEN pg_catalog.has_database_privilege(d.datname, 'CONNECT')
                        THEN pg_catalog.pg_database_size(d.datname)
                        ELSE NULL
                   END as size_bytes
            FROM pg_catalog.pg_database d
            WHERE d.datname != 'template0'
            ORDER BY 1
            LIMIT %s
            """
            
            databases = self.postgresql._execute_query(query, (limit,))
            
            # Format size
            for db in databases:
                if db.get("size_bytes") is not None:
                    db["size_human"] = self._format_size(db["size_bytes"])
            
            return databases
        except Exception as e:
            self.postgresql._handle_error("list_databases", e)
    
    def get_database_info(self, database: str) -> Dict[str, Any]:
        """
        Get information about a database.
        
        Args:
            database: Database name
            
        Returns:
            Database information
        """
        try:
            query = """
            SELECT d.datname as name, 
                   pg_catalog.pg_get_userbyid(d.datdba) as owner,
                   pg_catalog.pg_encoding_to_char(d.encoding) as encoding,
                   d.datcollate as collate,
                   d.datctype as ctype,
                   pg_catalog.array_to_string(d.datacl, E'\n') as access_privileges,
                   CASE WHEN pg_catalog.has_database_privilege(d.datname, 'CONNECT')
                        THEN pg_catalog.pg_database_size(d.datname)
                        ELSE NULL
                   END as size_bytes
            FROM pg_catalog.pg_database d
            WHERE d.datname = %s
            """
            
            db_info = self.postgresql._execute_query(query, (database,), fetch_all=False)
            
            if not db_info:
                raise ValueError(f"Database '{database}' not found")
            
            # Format size
            if db_info.get("size_bytes") is not None:
                db_info["size_human"] = self._format_size(db_info["size_bytes"])
            
            return db_info
        except Exception as e:
            self.postgresql._handle_error(f"get_database_info({database})", e)
    
    def list_schemas(self, database: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all schemas in a database.
        
        Args:
            database: Database name (optional, uses the current connection if not specified)
            limit: Maximum number of schemas to return
            
        Returns:
            List of schemas
        """
        try:
            # Create a new service instance if a different database is specified
            service = self._get_service_for_database(database)
            
            query = """
            SELECT n.nspname as name,
                   pg_catalog.pg_get_userbyid(n.nspowner) as owner,
                   pg_catalog.array_to_string(n.nspacl, E'\n') as access_privileges,
                   pg_catalog.obj_description(n.oid, 'pg_namespace') as description
            FROM pg_catalog.pg_namespace n
            WHERE n.nspname !~ '^pg_' AND n.nspname <> 'information_schema'
            ORDER BY 1
            LIMIT %s
            """
            
            schemas = service._execute_query(query, (limit,))
            
            return schemas
        except Exception as e:
            self.postgresql._handle_error("list_schemas", e)
    
    def list_tables(self, database: Optional[str] = None, schema: str = "public", limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all tables in a schema.
        
        Args:
            database: Database name (optional, uses the current connection if not specified)
            schema: Schema name (default: public)
            limit: Maximum number of tables to return
            
        Returns:
            List of tables
        """
        try:
            # Create a new service instance if a different database is specified
            service = self._get_service_for_database(database)
            
            query = """
            SELECT c.relname as name,
                   CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized view' WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence' WHEN 's' THEN 'special' WHEN 'f' THEN 'foreign table' WHEN 'p' THEN 'partitioned table' WHEN 'I' THEN 'partitioned index' END as type,
                   pg_catalog.pg_get_userbyid(c.relowner) as owner,
                   pg_catalog.pg_size_pretty(pg_catalog.pg_table_size(c.oid)) as size,
                   pg_catalog.obj_description(c.oid, 'pg_class') as description
            FROM pg_catalog.pg_class c
                 LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('r','p','v','m','f')
                  AND n.nspname = %s
                  AND pg_catalog.pg_table_is_visible(c.oid)
            ORDER BY 1
            LIMIT %s
            """
            
            tables = service._execute_query(query, (schema, limit))
            
            return tables
        except Exception as e:
            self.postgresql._handle_error("list_tables", e)
    
    def get_table_info(self, table: str, database: Optional[str] = None, schema: str = "public") -> Dict[str, Any]:
        """
        Get information about a table.
        
        Args:
            table: Table name
            database: Database name (optional, uses the current connection if not specified)
            schema: Schema name (default: public)
            
        Returns:
            Table information
        """
        try:
            # Create a new service instance if a different database is specified
            service = self._get_service_for_database(database)
            
            # Get basic table information
            query = """
            SELECT c.relname as name,
                   CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized view' WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence' WHEN 's' THEN 'special' WHEN 'f' THEN 'foreign table' WHEN 'p' THEN 'partitioned table' WHEN 'I' THEN 'partitioned index' END as type,
                   pg_catalog.pg_get_userbyid(c.relowner) as owner,
                   pg_catalog.pg_size_pretty(pg_catalog.pg_table_size(c.oid)) as size,
                   pg_catalog.pg_size_pretty(pg_catalog.pg_total_relation_size(c.oid)) as total_size,
                   pg_catalog.obj_description(c.oid, 'pg_class') as description
            FROM pg_catalog.pg_class c
                 LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relname = %s
                  AND n.nspname = %s
            """
            
            table_info = service._execute_query(query, (table, schema), fetch_all=False)
            
            if not table_info:
                raise ValueError(f"Table '{schema}.{table}' not found")
            
            # Get column information
            query = """
            SELECT a.attname as name,
                   pg_catalog.format_type(a.atttypid, a.atttypmod) as type,
                   CASE WHEN a.attnotnull THEN 'not null' ELSE 'null' END as nullable,
                   (SELECT pg_catalog.pg_get_expr(d.adbin, d.adrelid)
                    FROM pg_catalog.pg_attrdef d
                    WHERE d.adrelid = a.attrelid AND d.adnum = a.attnum AND a.atthasdef) as default_value,
                   pg_catalog.col_description(a.attrelid, a.attnum) as description
            FROM pg_catalog.pg_attribute a
            WHERE a.attrelid = (
                SELECT c.oid
                FROM pg_catalog.pg_class c
                     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                WHERE c.relname = %s
                      AND n.nspname = %s
                      AND c.relkind IN ('r','p','v','m','f')
            ) AND a.attnum > 0 AND NOT a.attisdropped
            ORDER BY a.attnum
            """
            
            columns = service._execute_query(query, (table, schema))
            
            # Get index information
            query = """
            SELECT i.relname as name,
                   pg_catalog.pg_get_indexdef(i.oid, 0, true) as definition,
                   CASE WHEN i.indisunique THEN 'unique' ELSE 'non-unique' END as uniqueness,
                   CASE WHEN i.indisprimary THEN 'primary key' ELSE 'index' END as type
            FROM pg_catalog.pg_index x
                 JOIN pg_catalog.pg_class c ON c.oid = x.indrelid
                 JOIN pg_catalog.pg_class i ON i.oid = x.indexrelid
                 LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relname = %s
                  AND n.nspname = %s
            ORDER BY i.relname
            """
            
            indexes = service._execute_query(query, (table, schema))
            
            # Add columns and indexes to table information
            table_info["columns"] = columns
            table_info["indexes"] = indexes
            
            return table_info
        except Exception as e:
            self.postgresql._handle_error(f"get_table_info({table})", e)
    
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
    
    def _format_size(self, size_bytes: int) -> str:
        """
        Format a size in bytes to a human-readable string.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Human-readable size
        """
        if size_bytes is None:
            return "unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.2f} PB"