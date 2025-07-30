"""
MongoDB tools for the DevOps MCP Server.
"""
from typing import Optional
from mcp.server.fastmcp import FastMCP

from services.mongodb.service import MongoDBServiceManager
from tools.mongodb.database_tools import MongoDBDatabaseTools
from tools.mongodb.collection_tools import MongoDBCollectionTools
from tools.mongodb.info_tools import MongoDBInfoTools
from utils.logging import setup_logger


class MongoDBTools:
    """Tools for interacting with MongoDB."""
    
    def __init__(self, mcp: FastMCP, mongodb_service: Optional[MongoDBServiceManager] = None):
        """
        Initialize MongoDB tools.
        
        Args:
            mcp: The MCP server instance
            mongodb_service: The MongoDB service manager instance (optional)
        """
        self.mcp = mcp
        self.mongodb_service = mongodb_service or MongoDBServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.mongodb")
        
        # Initialize specialized tools
        self.database_tools = MongoDBDatabaseTools(mcp, self.mongodb_service)
        self.collection_tools = MongoDBCollectionTools(mcp, self.mongodb_service)
        self.info_tools = MongoDBInfoTools(mcp, self.mongodb_service)
        
        self.logger.info("MongoDB tools initialized successfully")