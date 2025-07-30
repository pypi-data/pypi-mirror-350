"""
PostgreSQL resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.postgresql.service import PostgreSQLServiceManager
from utils.logging import setup_logger


class PostgreSQLResources:
    """PostgreSQL resources for the MCP server."""
    
    def __init__(self, mcp: FastMCP, postgresql_service: Optional[PostgreSQLServiceManager] = None):
        """
        Initialize PostgreSQL resources.
        
        Args:
            mcp: The MCP server instance
            postgresql_service: The PostgreSQL service manager instance (optional)
        """
        self.mcp = mcp
        self.postgresql_service = postgresql_service or PostgreSQLServiceManager()
        self.logger = setup_logger("devops_mcp_server.resources.postgresql")
        self._register_resources()
    
    def _register_resources(self) -> None:
        """Register PostgreSQL resources with the MCP server."""
        
        @self.mcp.resource("postgresql://.*")
        def handle_postgresql_resource(uri: str):
            """Handle PostgreSQL resource requests."""
            if not self.postgresql_service:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message="PostgreSQL service is not available"
                )
            
            # Parse URI
            if not uri.startswith("postgresql://"):
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid URI format: {uri}"
                )
            
            path = uri[len("postgresql://"):]
            
            try:
                if path == "info":
                    # Handle info resource
                    return self._handle_info_resource()
                elif path == "stats":
                    # Handle stats resource
                    return self._handle_stats_resource()
                elif path == "databases":
                    # Handle databases resource
                    return self._handle_databases_resource()
                elif path.startswith("db/"):
                    # Handle database resource
                    parts = path[len("db/"):].split("/")
                    if len(parts) == 1:
                        # Database info
                        database = parts[0]
                        return self._handle_database_resource(database)
                    elif len(parts) == 2 and parts[1] == "schemas":
                        # Schemas in database
                        database = parts[0]
                        return self._handle_schemas_resource(database)
                    elif len(parts) == 3 and parts[1] == "schema":
                        # Schema info
                        database = parts[0]
                        schema = parts[2]
                        return self._handle_schema_resource(database, schema)
                    elif len(parts) == 4 and parts[1] == "schema" and parts[3] == "tables":
                        # Tables in schema
                        database = parts[0]
                        schema = parts[2]
                        return self._handle_tables_resource(database, schema)
                    elif len(parts) == 5 and parts[1] == "schema" and parts[3] == "table":
                        # Table info
                        database = parts[0]
                        schema = parts[2]
                        table = parts[4]
                        return self._handle_table_resource(database, schema, table)
                else:
                    raise JSONRPCError(
                        code=INVALID_REQUEST,
                        message=f"Invalid PostgreSQL resource: {uri}"
                    )
            except Exception as e:
                self.logger.error(f"Error handling PostgreSQL resource: {e}")
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Error handling PostgreSQL resource: {str(e)}"
                )
        
        @self.mcp.list_resource_templates()
        def list_postgresql_resource_templates():
            """List PostgreSQL resource templates."""
            templates = []
            
            # Add template for info
            templates.append({
                "uriTemplate": "postgresql://info",
                "name": "PostgreSQL server information",
                "mimeType": "application/json",
                "description": "Get PostgreSQL server information"
            })
            
            # Add template for stats
            templates.append({
                "uriTemplate": "postgresql://stats",
                "name": "PostgreSQL server statistics",
                "mimeType": "application/json",
                "description": "Get PostgreSQL server statistics"
            })
            
            # Add template for databases
            templates.append({
                "uriTemplate": "postgresql://databases",
                "name": "PostgreSQL databases",
                "mimeType": "application/json",
                "description": "List all PostgreSQL databases"
            })
            
            # Add template for database
            templates.append({
                "uriTemplate": "postgresql://db/{database}",
                "name": "PostgreSQL database",
                "mimeType": "application/json",
                "description": "Get information about a PostgreSQL database"
            })
            
            # Add template for schemas
            templates.append({
                "uriTemplate": "postgresql://db/{database}/schemas",
                "name": "PostgreSQL schemas",
                "mimeType": "application/json",
                "description": "List all schemas in a PostgreSQL database"
            })
            
            # Add template for schema
            templates.append({
                "uriTemplate": "postgresql://db/{database}/schema/{schema}",
                "name": "PostgreSQL schema",
                "mimeType": "application/json",
                "description": "Get information about a PostgreSQL schema"
            })
            
            # Add template for tables
            templates.append({
                "uriTemplate": "postgresql://db/{database}/schema/{schema}/tables",
                "name": "PostgreSQL tables",
                "mimeType": "application/json",
                "description": "List all tables in a PostgreSQL schema"
            })
            
            # Add template for table
            templates.append({
                "uriTemplate": "postgresql://db/{database}/schema/{schema}/table/{table}",
                "name": "PostgreSQL table",
                "mimeType": "application/json",
                "description": "Get information about a PostgreSQL table"
            })
            
            return templates
    
    def _handle_info_resource(self) -> Dict[str, Any]:
        """
        Handle info resource.
        
        Returns:
            Resource response
        """
        info = self.postgresql_service.info.get_server_info()
        
        return {
            "contents": [
                {
                    "uri": "postgresql://info",
                    "mimeType": "application/json",
                    "text": self._format_json(info)
                }
            ]
        }
    
    def _handle_stats_resource(self) -> Dict[str, Any]:
        """
        Handle stats resource.
        
        Returns:
            Resource response
        """
        stats = self.postgresql_service.info.get_server_stats()
        
        return {
            "contents": [
                {
                    "uri": "postgresql://stats",
                    "mimeType": "application/json",
                    "text": self._format_json(stats)
                }
            ]
        }
    
    def _handle_databases_resource(self) -> Dict[str, Any]:
        """
        Handle databases resource.
        
        Returns:
            Resource response
        """
        databases = self.postgresql_service.database.list_databases()
        
        return {
            "contents": [
                {
                    "uri": "postgresql://databases",
                    "mimeType": "application/json",
                    "text": self._format_json({"databases": databases, "count": len(databases)})
                }
            ]
        }
    
    def _handle_database_resource(self, database: str) -> Dict[str, Any]:
        """
        Handle database resource.
        
        Args:
            database: Database name
            
        Returns:
            Resource response
        """
        info = self.postgresql_service.database.get_database_info(database)
        
        return {
            "contents": [
                {
                    "uri": f"postgresql://db/{database}",
                    "mimeType": "application/json",
                    "text": self._format_json(info)
                }
            ]
        }
    
    def _handle_schemas_resource(self, database: str) -> Dict[str, Any]:
        """
        Handle schemas resource.
        
        Args:
            database: Database name
            
        Returns:
            Resource response
        """
        schemas = self.postgresql_service.database.list_schemas(database)
        
        return {
            "contents": [
                {
                    "uri": f"postgresql://db/{database}/schemas",
                    "mimeType": "application/json",
                    "text": self._format_json({"schemas": schemas, "count": len(schemas)})
                }
            ]
        }
    
    def _handle_schema_resource(self, database: str, schema: str) -> Dict[str, Any]:
        """
        Handle schema resource.
        
        Args:
            database: Database name
            schema: Schema name
            
        Returns:
            Resource response
        """
        # Get schema information (not directly available in the service)
        # Return tables in the schema instead
        tables = self.postgresql_service.database.list_tables(database, schema)
        
        return {
            "contents": [
                {
                    "uri": f"postgresql://db/{database}/schema/{schema}",
                    "mimeType": "application/json",
                    "text": self._format_json({"schema": schema, "tables": tables, "count": len(tables)})
                }
            ]
        }
    
    def _handle_tables_resource(self, database: str, schema: str) -> Dict[str, Any]:
        """
        Handle tables resource.
        
        Args:
            database: Database name
            schema: Schema name
            
        Returns:
            Resource response
        """
        tables = self.postgresql_service.database.list_tables(database, schema)
        
        return {
            "contents": [
                {
                    "uri": f"postgresql://db/{database}/schema/{schema}/tables",
                    "mimeType": "application/json",
                    "text": self._format_json({"tables": tables, "count": len(tables)})
                }
            ]
        }
    
    def _handle_table_resource(self, database: str, schema: str, table: str) -> Dict[str, Any]:
        """
        Handle table resource.
        
        Args:
            database: Database name
            schema: Schema name
            table: Table name
            
        Returns:
            Resource response
        """
        info = self.postgresql_service.database.get_table_info(table, database, schema)
        
        return {
            "contents": [
                {
                    "uri": f"postgresql://db/{database}/schema/{schema}/table/{table}",
                    "mimeType": "application/json",
                    "text": self._format_json(info)
                }
            ]
        }
    
    def _format_json(self, data: Any) -> str:
        """Format data as JSON string."""
        import json
        return json.dumps(data, indent=2)