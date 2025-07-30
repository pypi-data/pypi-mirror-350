"""
MongoDB resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.mongodb.service import MongoDBServiceManager
from utils.logging import setup_logger


class MongoDBResources:
    """MongoDB resources for the MCP server."""
    
    def __init__(self, mcp: FastMCP, mongodb_service: Optional[MongoDBServiceManager] = None):
        """
        Initialize MongoDB resources.
        
        Args:
            mcp: The MCP server instance
            mongodb_service: The MongoDB service manager instance (optional)
        """
        self.mcp = mcp
        self.mongodb_service = mongodb_service or MongoDBServiceManager()
        self.logger = setup_logger("devops_mcp_server.resources.mongodb")
        self._register_resources()
    
    def _register_resources(self) -> None:
        """Register MongoDB resources with the MCP server."""
        
        @self.mcp.resource("mongodb://.*")
        def handle_mongodb_resource(uri: str):
            """Handle MongoDB resource requests."""
            if not self.mongodb_service:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message="MongoDB service is not available"
                )
            
            # Parse URI
            if not uri.startswith("mongodb://"):
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Invalid URI format: {uri}"
                )
            
            path = uri[len("mongodb://"):]
            
            try:
                if path == "info":
                    # Handle info resource
                    return self._handle_info_resource()
                elif path == "status":
                    # Handle status resource
                    return self._handle_status_resource()
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
                    elif len(parts) == 2 and parts[1] == "collections":
                        # Collections in database
                        database = parts[0]
                        return self._handle_collections_resource(database)
                    elif len(parts) == 3 and parts[1] == "collection":
                        # Collection info
                        database = parts[0]
                        collection = parts[2]
                        return self._handle_collection_resource(database, collection)
                else:
                    raise JSONRPCError(
                        code=INVALID_REQUEST,
                        message=f"Invalid MongoDB resource: {uri}"
                    )
            except Exception as e:
                self.logger.error(f"Error handling MongoDB resource: {e}")
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Error handling MongoDB resource: {str(e)}"
                )
        
        @self.mcp.list_resource_templates()
        def list_mongodb_resource_templates():
            """List MongoDB resource templates."""
            templates = []
            
            # Add template for info
            templates.append({
                "uriTemplate": "mongodb://info",
                "name": "MongoDB server information",
                "mimeType": "application/json",
                "description": "Get MongoDB server information"
            })
            
            # Add template for status
            templates.append({
                "uriTemplate": "mongodb://status",
                "name": "MongoDB server status",
                "mimeType": "application/json",
                "description": "Get MongoDB server status"
            })
            
            # Add template for databases
            templates.append({
                "uriTemplate": "mongodb://databases",
                "name": "MongoDB databases",
                "mimeType": "application/json",
                "description": "List all MongoDB databases"
            })
            
            # Add template for database
            templates.append({
                "uriTemplate": "mongodb://db/{database}",
                "name": "MongoDB database",
                "mimeType": "application/json",
                "description": "Get information about a MongoDB database"
            })
            
            # Add template for collections
            templates.append({
                "uriTemplate": "mongodb://db/{database}/collections",
                "name": "MongoDB collections",
                "mimeType": "application/json",
                "description": "List all collections in a MongoDB database"
            })
            
            # Add template for collection
            templates.append({
                "uriTemplate": "mongodb://db/{database}/collection/{collection}",
                "name": "MongoDB collection",
                "mimeType": "application/json",
                "description": "Get information about a MongoDB collection"
            })
            
            return templates
    
    def _handle_info_resource(self) -> Dict[str, Any]:
        """
        Handle info resource.
        
        Returns:
            Resource response
        """
        info = self.mongodb_service.info.get_server_info()
        
        return {
            "contents": [
                {
                    "uri": "mongodb://info",
                    "mimeType": "application/json",
                    "text": self._format_json(info)
                }
            ]
        }
    
    def _handle_status_resource(self) -> Dict[str, Any]:
        """
        Handle status resource.
        
        Returns:
            Resource response
        """
        status = self.mongodb_service.info.get_server_status()
        
        return {
            "contents": [
                {
                    "uri": "mongodb://status",
                    "mimeType": "application/json",
                    "text": self._format_json(status)
                }
            ]
        }
    
    def _handle_databases_resource(self) -> Dict[str, Any]:
        """
        Handle databases resource.
        
        Returns:
            Resource response
        """
        databases = self.mongodb_service.database.list_databases()
        
        return {
            "contents": [
                {
                    "uri": "mongodb://databases",
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
        stats = self.mongodb_service.database.get_database_stats(database)
        
        return {
            "contents": [
                {
                    "uri": f"mongodb://db/{database}",
                    "mimeType": "application/json",
                    "text": self._format_json(stats)
                }
            ]
        }
    
    def _handle_collections_resource(self, database: str) -> Dict[str, Any]:
        """
        Handle collections resource.
        
        Args:
            database: Database name
            
        Returns:
            Resource response
        """
        collections = self.mongodb_service.database.list_collections(database)
        
        return {
            "contents": [
                {
                    "uri": f"mongodb://db/{database}/collections",
                    "mimeType": "application/json",
                    "text": self._format_json({"collections": collections, "count": len(collections)})
                }
            ]
        }
    
    def _handle_collection_resource(self, database: str, collection: str) -> Dict[str, Any]:
        """
        Handle collection resource.
        
        Args:
            database: Database name
            collection: Collection name
            
        Returns:
            Resource response
        """
        stats = self.mongodb_service.database.get_collection_stats(database, collection)
        
        return {
            "contents": [
                {
                    "uri": f"mongodb://db/{database}/collection/{collection}",
                    "mimeType": "application/json",
                    "text": self._format_json(stats)
                }
            ]
        }
    
    def _format_json(self, data: Any) -> str:
        """Format data as JSON string."""
        import json
        return json.dumps(data, indent=2)