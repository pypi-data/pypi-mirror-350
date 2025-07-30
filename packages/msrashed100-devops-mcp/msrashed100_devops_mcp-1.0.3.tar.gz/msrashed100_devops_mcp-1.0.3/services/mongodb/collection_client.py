"""
MongoDB collection client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.mongodb.client import MongoDBService


class MongoDBCollectionClient:
    """Client for MongoDB collection operations."""
    
    def __init__(self, mongodb_service: MongoDBService):
        """
        Initialize the MongoDB collection client.
        
        Args:
            mongodb_service: The base MongoDB service
        """
        self.mongodb = mongodb_service
        self.logger = mongodb_service.logger
    
    def find_documents(self, database: str, collection: str, filter: Optional[Dict[str, Any]] = None,
                      projection: Optional[Dict[str, Any]] = None, sort: Optional[List[tuple]] = None,
                      limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
        """
        Find documents in a collection.
        
        Args:
            database: Database name
            collection: Collection name
            filter: Filter criteria (optional)
            projection: Fields to include or exclude (optional)
            sort: Sort criteria (optional)
            limit: Maximum number of documents to return
            skip: Number of documents to skip
            
        Returns:
            List of documents
        """
        try:
            # Get database and collection
            db = self.mongodb.client[database]
            coll = db[collection]
            
            # Find documents
            cursor = coll.find(
                filter or {},
                projection or None
            )
            
            # Apply sort, skip, and limit
            if sort:
                cursor = cursor.sort(sort)
            
            cursor = cursor.skip(skip).limit(limit)
            
            # Convert cursor to list
            documents = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for doc in documents:
                if "_id" in doc and hasattr(doc["_id"], "__str__"):
                    doc["_id"] = str(doc["_id"])
            
            return documents
        except Exception as e:
            self.mongodb._handle_error(f"find_documents({database}, {collection})", e)
    
    def get_document(self, database: str, collection: str, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document by ID.
        
        Args:
            database: Database name
            collection: Collection name
            document_id: Document ID
            
        Returns:
            Document or None if not found
        """
        try:
            # Get database and collection
            db = self.mongodb.client[database]
            coll = db[collection]
            
            # Find document by ID
            from bson.objectid import ObjectId
            
            try:
                # Try to convert to ObjectId
                obj_id = ObjectId(document_id)
                document = coll.find_one({"_id": obj_id})
            except Exception:
                # If not a valid ObjectId, try as string
                document = coll.find_one({"_id": document_id})
            
            # Convert ObjectId to string for JSON serialization
            if document and "_id" in document and hasattr(document["_id"], "__str__"):
                document["_id"] = str(document["_id"])
            
            return document
        except Exception as e:
            self.mongodb._handle_error(f"get_document({database}, {collection}, {document_id})", e)
    
    def aggregate(self, database: str, collection: str, pipeline: List[Dict[str, Any]],
                 limit: int = 100) -> List[Dict[str, Any]]:
        """
        Run an aggregation pipeline.
        
        Args:
            database: Database name
            collection: Collection name
            pipeline: Aggregation pipeline
            limit: Maximum number of documents to return
            
        Returns:
            Aggregation results
        """
        try:
            # Get database and collection
            db = self.mongodb.client[database]
            coll = db[collection]
            
            # Add limit stage if not already present
            has_limit = any(stage for stage in pipeline if "$limit" in stage)
            if not has_limit:
                pipeline.append({"$limit": limit})
            
            # Run aggregation
            cursor = coll.aggregate(pipeline)
            
            # Convert cursor to list
            results = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for doc in results:
                if "_id" in doc and hasattr(doc["_id"], "__str__"):
                    doc["_id"] = str(doc["_id"])
            
            return results
        except Exception as e:
            self.mongodb._handle_error(f"aggregate({database}, {collection})", e)
    
    def distinct(self, database: str, collection: str, field: str,
                filter: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Any]:
        """
        Get distinct values for a field.
        
        Args:
            database: Database name
            collection: Collection name
            field: Field name
            filter: Filter criteria (optional)
            limit: Maximum number of values to return
            
        Returns:
            List of distinct values
        """
        try:
            # Get database and collection
            db = self.mongodb.client[database]
            coll = db[collection]
            
            # Get distinct values
            values = coll.distinct(field, filter or {})
            
            # Apply limit
            if len(values) > limit:
                values = values[:limit]
            
            return values
        except Exception as e:
            self.mongodb._handle_error(f"distinct({database}, {collection}, {field})", e)
    
    def get_indexes(self, database: str, collection: str) -> List[Dict[str, Any]]:
        """
        Get indexes for a collection.
        
        Args:
            database: Database name
            collection: Collection name
            
        Returns:
            List of indexes
        """
        try:
            # Get database and collection
            db = self.mongodb.client[database]
            coll = db[collection]
            
            # Get indexes
            indexes = list(coll.list_indexes())
            
            # Format indexes
            formatted_indexes = []
            for index in indexes:
                formatted_indexes.append({
                    "name": index["name"],
                    "key": index["key"],
                    "unique": index.get("unique", False),
                    "background": index.get("background", False),
                    "sparse": index.get("sparse", False)
                })
            
            return formatted_indexes
        except Exception as e:
            self.mongodb._handle_error(f"get_indexes({database}, {collection})", e)