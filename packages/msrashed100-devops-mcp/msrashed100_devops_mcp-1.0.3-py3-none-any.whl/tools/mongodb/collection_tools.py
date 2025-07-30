"""
MongoDB collection tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.mongodb.service import MongoDBServiceManager
from tools.mongodb.base_tools import MongoDBBaseTools
from utils.logging import setup_logger


class MongoDBCollectionTools(MongoDBBaseTools):
    """Tools for MongoDB collection operations."""
    
    def __init__(self, mcp: FastMCP, mongodb_service: Optional[MongoDBServiceManager] = None):
        """
        Initialize MongoDB collection tools.
        
        Args:
            mcp: The MCP server instance
            mongodb_service: The MongoDB service manager instance (optional)
        """
        super().__init__(mcp, mongodb_service)
        self.logger = setup_logger("devops_mcp_server.tools.mongodb.collection")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register MongoDB collection tools with the MCP server."""
        
        @self.mcp.tool()
        def find_mongodb_documents(database: str, collection: str, filter: str = None,
                                 projection: str = None, sort: str = None,
                                 limit: int = 100, skip: int = 0) -> str:
            """
            Find documents in a MongoDB collection.
            
            This tool finds documents in a collection in a database in the MongoDB server.
            
            Args:
                database: Database name
                collection: Collection name
                filter: Filter criteria in JSON format (optional)
                projection: Fields to include or exclude in JSON format (optional)
                sort: Sort criteria in JSON format (optional)
                limit: Maximum number of documents to return (default: 100, max: 500)
                skip: Number of documents to skip (default: 0)
                
            Returns:
                List of documents in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                # Parse parameters if provided
                import json
                
                filter_dict = json.loads(filter) if filter else None
                projection_dict = json.loads(projection) if projection else None
                
                # Parse sort parameter
                sort_list = None
                if sort:
                    sort_dict = json.loads(sort)
                    sort_list = [(k, v) for k, v in sort_dict.items()]
                
                documents = self.mongodb_service.collection.find_documents(
                    database, collection, filter_dict, projection_dict, sort_list, limit, skip
                )
                
                return self._format_response({"documents": documents, "count": len(documents)})
            except Exception as e:
                self.logger.error(f"Error finding MongoDB documents: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_document(database: str, collection: str, document_id: str) -> str:
            """
            Get a document by ID from a MongoDB collection.
            
            This tool retrieves a document by ID from a collection in a database in the MongoDB server.
            
            Args:
                database: Database name
                collection: Collection name
                document_id: Document ID
                
            Returns:
                Document in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                document = self.mongodb_service.collection.get_document(database, collection, document_id)
                
                if not document:
                    return self._format_error(f"Document with ID '{document_id}' not found")
                
                return self._format_response(document)
            except Exception as e:
                self.logger.error(f"Error getting MongoDB document: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def aggregate_mongodb_documents(database: str, collection: str, pipeline: str, limit: int = 100) -> str:
            """
            Run an aggregation pipeline on a MongoDB collection.
            
            This tool runs an aggregation pipeline on a collection in a database in the MongoDB server.
            
            Args:
                database: Database name
                collection: Collection name
                pipeline: Aggregation pipeline in JSON format
                limit: Maximum number of documents to return (default: 100, max: 500)
                
            Returns:
                Aggregation results in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                # Parse pipeline
                import json
                pipeline_list = json.loads(pipeline)
                
                results = self.mongodb_service.collection.aggregate(database, collection, pipeline_list, limit)
                
                return self._format_response({"results": results, "count": len(results)})
            except Exception as e:
                self.logger.error(f"Error aggregating MongoDB documents: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_distinct_values(database: str, collection: str, field: str,
                                      filter: str = None, limit: int = 100) -> str:
            """
            Get distinct values for a field in a MongoDB collection.
            
            This tool retrieves distinct values for a field in a collection in a database in the MongoDB server.
            
            Args:
                database: Database name
                collection: Collection name
                field: Field name
                filter: Filter criteria in JSON format (optional)
                limit: Maximum number of values to return (default: 100, max: 500)
                
            Returns:
                List of distinct values in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                # Parse filter if provided
                filter_dict = None
                if filter:
                    import json
                    filter_dict = json.loads(filter)
                
                values = self.mongodb_service.collection.distinct(database, collection, field, filter_dict, limit)
                
                return self._format_response({"values": values, "count": len(values)})
            except Exception as e:
                self.logger.error(f"Error getting MongoDB distinct values: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_mongodb_indexes(database: str, collection: str) -> str:
            """
            Get indexes for a MongoDB collection.
            
            This tool retrieves indexes for a collection in a database in the MongoDB server.
            
            Args:
                database: Database name
                collection: Collection name
                
            Returns:
                List of indexes in JSON format
            """
            if not self._check_service_available():
                return self._format_error("MongoDB service is not available")
            
            try:
                indexes = self.mongodb_service.collection.get_indexes(database, collection)
                
                return self._format_response({"indexes": indexes, "count": len(indexes)})
            except Exception as e:
                self.logger.error(f"Error getting MongoDB indexes: {e}")
                return self._format_error(str(e))