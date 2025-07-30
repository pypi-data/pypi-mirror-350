"""
MongoDB database client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.mongodb.client import MongoDBService


class MongoDBDatabaseClient:
    """Client for MongoDB database operations."""
    
    def __init__(self, mongodb_service: MongoDBService):
        """
        Initialize the MongoDB database client.
        
        Args:
            mongodb_service: The base MongoDB service
        """
        self.mongodb = mongodb_service
        self.logger = mongodb_service.logger
    
    def list_databases(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all databases.
        
        Args:
            limit: Maximum number of databases to return
            
        Returns:
            List of databases
        """
        try:
            # Get list of databases
            databases = self.mongodb.client.list_databases()
            
            # Convert to list and apply limit
            database_list = list(databases)
            if len(database_list) > limit:
                database_list = database_list[:limit]
            
            # Format database information
            formatted_databases = []
            for db in database_list:
                formatted_databases.append({
                    "name": db["name"],
                    "sizeOnDisk": db.get("sizeOnDisk", 0),
                    "empty": db.get("empty", False)
                })
            
            return formatted_databases
        except Exception as e:
            self.mongodb._handle_error("list_databases", e)
    
    def get_database_stats(self, database: str) -> Dict[str, Any]:
        """
        Get statistics for a database.
        
        Args:
            database: Database name
            
        Returns:
            Database statistics
        """
        try:
            # Get database statistics
            db = self.mongodb.client[database]
            stats = db.command("dbStats")
            
            return stats
        except Exception as e:
            self.mongodb._handle_error(f"get_database_stats({database})", e)
    
    def list_collections(self, database: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all collections in a database.
        
        Args:
            database: Database name
            limit: Maximum number of collections to return
            
        Returns:
            List of collections
        """
        try:
            # Get database
            db = self.mongodb.client[database]
            
            # Get list of collections
            collections = db.list_collections()
            
            # Convert to list and apply limit
            collection_list = list(collections)
            if len(collection_list) > limit:
                collection_list = collection_list[:limit]
            
            # Format collection information
            formatted_collections = []
            for collection in collection_list:
                formatted_collections.append({
                    "name": collection["name"],
                    "type": collection.get("type", "collection"),
                    "options": collection.get("options", {})
                })
            
            return formatted_collections
        except Exception as e:
            self.mongodb._handle_error(f"list_collections({database})", e)
    
    def get_collection_stats(self, database: str, collection: str) -> Dict[str, Any]:
        """
        Get statistics for a collection.
        
        Args:
            database: Database name
            collection: Collection name
            
        Returns:
            Collection statistics
        """
        try:
            # Get database and collection
            db = self.mongodb.client[database]
            
            # Get collection statistics
            stats = db.command("collStats", collection)
            
            return stats
        except Exception as e:
            self.mongodb._handle_error(f"get_collection_stats({database}, {collection})", e)
    
    def count_documents(self, database: str, collection: str, filter: Optional[Dict[str, Any]] = None) -> int:
        """
        Count documents in a collection.
        
        Args:
            database: Database name
            collection: Collection name
            filter: Filter criteria (optional)
            
        Returns:
            Number of documents
        """
        try:
            # Get database and collection
            db = self.mongodb.client[database]
            coll = db[collection]
            
            # Count documents
            if filter:
                count = coll.count_documents(filter)
            else:
                count = coll.count_documents({})
            
            return count
        except Exception as e:
            self.mongodb._handle_error(f"count_documents({database}, {collection})", e)