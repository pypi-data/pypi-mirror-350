"""
PostgreSQL information tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.postgresql.service import PostgreSQLServiceManager
from tools.postgresql.base_tools import PostgreSQLBaseTools
from utils.logging import setup_logger


class PostgreSQLInfoTools(PostgreSQLBaseTools):
    """Tools for PostgreSQL server information operations."""
    
    def __init__(self, mcp: FastMCP, postgresql_service: Optional[PostgreSQLServiceManager] = None):
        """
        Initialize PostgreSQL information tools.
        
        Args:
            mcp: The MCP server instance
            postgresql_service: The PostgreSQL service manager instance (optional)
        """
        super().__init__(mcp, postgresql_service)
        self.logger = setup_logger("devops_mcp_server.tools.postgresql.info")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register PostgreSQL information tools with the MCP server."""
        
        @self.mcp.tool()
        def get_postgresql_server_info() -> str:
            """
            Get PostgreSQL server information.
            
            This tool retrieves information about the PostgreSQL server.
            
            Returns:
                Server information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            try:
                info = self.postgresql_service.info.get_server_info()
                return self._format_response(info)
            except Exception as e:
                self.logger.error(f"Error getting PostgreSQL server info: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_postgresql_server_stats() -> str:
            """
            Get PostgreSQL server statistics.
            
            This tool retrieves statistics about the PostgreSQL server.
            
            Returns:
                Server statistics in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            try:
                stats = self.postgresql_service.info.get_server_stats()
                return self._format_response(stats)
            except Exception as e:
                self.logger.error(f"Error getting PostgreSQL server stats: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_postgresql_active_queries(limit: int = 100) -> str:
            """
            Get active queries on the PostgreSQL server.
            
            This tool retrieves active queries on the PostgreSQL server.
            
            Args:
                limit: Maximum number of queries to return (default: 100, max: 500)
                
            Returns:
                List of active queries in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                queries = self.postgresql_service.info.get_active_queries(limit)
                return self._format_response({"queries": queries, "count": len(queries)})
            except Exception as e:
                self.logger.error(f"Error getting PostgreSQL active queries: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_postgresql_slow_queries(min_duration: int = 1000, limit: int = 100) -> str:
            """
            Get slow queries on the PostgreSQL server.
            
            This tool retrieves slow queries from pg_stat_statements on the PostgreSQL server.
            
            Args:
                min_duration: Minimum query duration in milliseconds (default: 1000)
                limit: Maximum number of queries to return (default: 100, max: 500)
                
            Returns:
                List of slow queries in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                queries = self.postgresql_service.info.get_slow_queries(min_duration, limit)
                return self._format_response({"queries": queries, "count": len(queries)})
            except Exception as e:
                self.logger.error(f"Error getting PostgreSQL slow queries: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_postgresql_table_bloat(limit: int = 100) -> str:
            """
            Get table bloat information on the PostgreSQL server.
            
            This tool retrieves table bloat information on the PostgreSQL server.
            
            Args:
                limit: Maximum number of tables to return (default: 100, max: 500)
                
            Returns:
                List of tables with bloat information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                tables = self.postgresql_service.info.get_table_bloat(limit)
                return self._format_response({"tables": tables, "count": len(tables)})
            except Exception as e:
                self.logger.error(f"Error getting PostgreSQL table bloat: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_postgresql_index_usage(limit: int = 100) -> str:
            """
            Get index usage information on the PostgreSQL server.
            
            This tool retrieves index usage information on the PostgreSQL server.
            
            Args:
                limit: Maximum number of indexes to return (default: 100, max: 500)
                
            Returns:
                List of indexes with usage information in JSON format
            """
            if not self._check_service_available():
                return self._format_error("PostgreSQL service is not available")
            
            # Validate limit
            limit = min(max(1, limit), 500)
            
            try:
                indexes = self.postgresql_service.info.get_index_usage(limit)
                return self._format_response({"indexes": indexes, "count": len(indexes)})
            except Exception as e:
                self.logger.error(f"Error getting PostgreSQL index usage: {e}")
                return self._format_error(str(e))