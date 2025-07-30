"""
MongoDB database tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.mongodb.service import MongoDBServiceManager
from tools.mongodb.base_tools import MongoDBBaseTools
from utils.logging import setup_logger


class MongoDBDatabaseTools(MongoDBBaseTools):
    """Tools for MongoDB database operations."""
    
    def __init__(self, mcp: FastMCP, mongodb_service: Optional[MongoDBServiceManager] = None):
        """
        Initialize MongoDB database tools.
        
        Args:
            mcp: The MCP server instance
            mongodb_service: The MongoDB service manager instance (optional)
        """
        super().__init__(mcp, mongodb_service)
        self.logger = setup_logger("devops_mcp_server.tools.mongodb.database")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register MongoDB database tools with the MCP server."""
        
        @self.mcp.tool()
        def list_mongodb_databases(limit: int = 100) -> str:
            """
            List all MongoDB databases.
            
            This tool lists all databases in the MongoDB server.
            
            Args:
                limit: Maximum number of databases to return (default: 100, max: 500)
                
            Returns:
                List of databases in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                databases = self.mongodb_service.database.list_databases(limit)
                return self._format_response({"databases": databases, "count": len(databases)})
            except Exception as e:
                self.logger.error(f"Error listing MongoDB databases: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_database_stats(database: str) -> str:
            """
            Get statistics for a MongoDB database.
            
            This tool retrieves statistics for a database in the MongoDB server.
            
            Args:
                database: Database name
                
            Returns:
                Database statistics in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                stats = self.mongodb_service.database.get_database_stats(database)
                return self._format_response(stats)
            except Exception as e:
                self.logger.error(f"Error getting MongoDB database stats: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_mongodb_collections(database: str, limit: int = 100) -> str:
            """
            List all collections in a MongoDB database.
            
            This tool lists all collections in a database in the MongoDB server.
            
            Args:
                database: Database name
                limit: Maximum number of collections to return (default: 100, max: 500)
                
            Returns:
                List of collections in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                collections = self.mongodb_service.database.list_collections(database, limit)
                return self._format_response({"collections": collections, "count": len(collections)})
            except Exception as e:
                self.logger.error(f"Error listing MongoDB collections: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_collection_stats(database: str, collection: str) -> str:
            """
            Get statistics for a MongoDB collection.
            
            This tool retrieves statistics for a collection in a database in the MongoDB server.
            
            Args:
                database: Database name
                collection: Collection name
                
            Returns:
                Collection statistics in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                stats = self.mongodb_service.database.get_collection_stats(database, collection)
                return self._format_response(stats)
            except Exception as e:
                self.logger.error(f"Error getting MongoDB collection stats: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def count_mongodb_documents(database: str, collection: str, filter: str = None) -> str:
            """
            Count documents in a MongoDB collection.
            
            This tool counts documents in a collection in a database in the MongoDB server.
            
            Args:
                database: Database name
                collection: Collection name
                filter: Filter criteria in JSON format (optional)
                
            Returns:
                Document count in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                # Parse filter if provided
                filter_dict = None
                if filter:
                    import json
                    filter_dict = json.loads(filter)
                
                count = self.mongodb_service.database.count_documents(database, collection, filter_dict)
                return self._format_response({"count": count})
            except Exception as e:
                self.logger.error(f"Error counting MongoDB documents: {e}")
                return self._format_error(str(e))