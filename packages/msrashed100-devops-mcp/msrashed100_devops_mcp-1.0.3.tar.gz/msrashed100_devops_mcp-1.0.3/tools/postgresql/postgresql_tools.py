"""
PostgreSQL tools for the DevOps MCP Server.
"""
from typing import Optional
from mcp.server.fastmcp import FastMCP

from services.postgresql.service import PostgreSQLServiceManager
from tools.postgresql.database_tools import PostgreSQLDatabaseTools
from tools.postgresql.query_tools import PostgreSQLQueryTools
from tools.postgresql.info_tools import PostgreSQLInfoTools
from utils.logging import setup_logger


class PostgreSQLTools:
    """Tools for interacting with PostgreSQL."""
    
    def __init__(self, mcp: FastMCP, postgresql_service: Optional[PostgreSQLServiceManager] = None):
        """
        Initialize PostgreSQL tools.
        
        Args:
            mcp: The MCP server instance
            postgresql_service: The PostgreSQL service manager instance (optional)
        """
        self.mcp = mcp
        self.postgresql_service = postgresql_service or PostgreSQLServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.postgresql")
        
        # Initialize specialized tools
        self.database_tools = PostgreSQLDatabaseTools(mcp, self.postgresql_service)
        self.query_tools = PostgreSQLQueryTools(mcp, self.postgresql_service)
        self.info_tools = PostgreSQLInfoTools(mcp, self.postgresql_service)
        
        self.logger.info("PostgreSQL tools initialized successfully")