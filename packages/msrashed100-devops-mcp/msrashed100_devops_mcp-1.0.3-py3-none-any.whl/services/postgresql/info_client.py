"""
PostgreSQL information client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.postgresql.client import PostgreSQLService


class PostgreSQLInfoClient:
    """Client for PostgreSQL server information operations."""
    
    def __init__(self, postgresql_service: PostgreSQLService):
        """
        Initialize the PostgreSQL information client.
        
        Args:
            postgresql_service: The base PostgreSQL service
        """
        self.postgresql = postgresql_service
        self.logger = postgresql_service.logger
    
    def get_server_info(self) -> Dict[str, Any]:
        """
        Get PostgreSQL server information.
        
        Returns:
            Server information
        """
        try:
            query = """
            SELECT version() as version,
                   current_setting('server_version') as server_version,
                   current_setting('server_version_num') as server_version_num,
                   current_setting('data_directory') as data_directory,
                   current_setting('max_connections') as max_connections,
                   current_setting('shared_buffers') as shared_buffers,
                   current_setting('work_mem') as work_mem,
                   current_setting('maintenance_work_mem') as maintenance_work_mem,
                   current_setting('effective_cache_size') as effective_cache_size,
                   current_setting('timezone') as timezone
            """
            
            info = self.postgresql._execute_query(query, fetch_all=False)
            
            return info
        except Exception as e:
            self.postgresql._handle_error("get_server_info", e)
    
    def get_server_stats(self) -> Dict[str, Any]:
        """
        Get PostgreSQL server statistics.
        
        Returns:
            Server statistics
        """
        try:
            # Get database statistics
            query = """
            SELECT sum(numbackends) as active_connections,
                   sum(xact_commit) as transactions_committed,
                   sum(xact_rollback) as transactions_rolled_back,
                   sum(blks_read) as blocks_read,
                   sum(blks_hit) as blocks_hit,
                   sum(tup_returned) as rows_returned,
                   sum(tup_fetched) as rows_fetched,
                   sum(tup_inserted) as rows_inserted,
                   sum(tup_updated) as rows_updated,
                   sum(tup_deleted) as rows_deleted,
                   sum(conflicts) as conflicts,
                   sum(temp_files) as temp_files,
                   sum(temp_bytes) as temp_bytes,
                   sum(deadlocks) as deadlocks,
                   sum(checksum_failures) as checksum_failures,
                   sum(blk_read_time) as block_read_time_ms,
                   sum(blk_write_time) as block_write_time_ms
            FROM pg_stat_database
            """
            
            db_stats = self.postgresql._execute_query(query, fetch_all=False)
            
            # Get connection statistics
            query = """
            SELECT count(*) as total_connections,
                   count(*) FILTER (WHERE state = 'active') as active_queries,
                   count(*) FILTER (WHERE state = 'idle') as idle_connections,
                   count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_transaction,
                   count(*) FILTER (WHERE wait_event_type IS NOT NULL) as waiting_connections,
                   max(extract(epoch from now() - query_start)) FILTER (WHERE state = 'active') as longest_running_query_seconds
            FROM pg_stat_activity
            WHERE backend_type = 'client backend'
            """
            
            conn_stats = self.postgresql._execute_query(query, fetch_all=False)
            
            # Get table statistics
            query = """
            SELECT sum(n_live_tup) as live_rows,
                   sum(n_dead_tup) as dead_rows,
                   sum(pg_relation_size(schemaname || '.' || relname)) as total_table_size_bytes
            FROM pg_stat_user_tables
            """
            
            table_stats = self.postgresql._execute_query(query, fetch_all=False)
            
            # Format table size
            if table_stats.get("total_table_size_bytes") is not None:
                table_stats["total_table_size_human"] = self._format_size(table_stats["total_table_size_bytes"])
            
            # Get index statistics
            query = """
            SELECT sum(pg_relation_size(schemaname || '.' || relname)) as total_index_size_bytes
            FROM pg_stat_user_indexes
            """
            
            index_stats = self.postgresql._execute_query(query, fetch_all=False)
            
            # Format index size
            if index_stats.get("total_index_size_bytes") is not None:
                index_stats["total_index_size_human"] = self._format_size(index_stats["total_index_size_bytes"])
            
            # Combine all statistics
            stats = {
                "connections": conn_stats,
                "database": db_stats,
                "tables": table_stats,
                "indexes": index_stats
            }
            
            return stats
        except Exception as e:
            self.postgresql._handle_error("get_server_stats", e)
    
    def get_active_queries(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get active queries.
        
        Args:
            limit: Maximum number of queries to return
            
        Returns:
            List of active queries
        """
        try:
            query = """
            SELECT pid,
                   usename as username,
                   datname as database,
                   application_name,
                   client_addr as client_address,
                   client_port,
                   backend_start,
                   query_start,
                   state,
                   wait_event_type,
                   wait_event,
                   query
            FROM pg_stat_activity
            WHERE state = 'active'
              AND backend_type = 'client backend'
              AND pid <> pg_backend_pid()
            ORDER BY query_start
            LIMIT %s
            """
            
            queries = self.postgresql._execute_query(query, (limit,))
            
            return queries
        except Exception as e:
            self.postgresql._handle_error("get_active_queries", e)
    
    def get_slow_queries(self, min_duration: int = 1000, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get slow queries from pg_stat_statements.
        
        Args:
            min_duration: Minimum query duration in milliseconds
            limit: Maximum number of queries to return
            
        Returns:
            List of slow queries
        """
        try:
            # Check if pg_stat_statements is available
            check_query = """
            SELECT 1
            FROM pg_available_extensions
            WHERE name = 'pg_stat_statements' AND installed_version IS NOT NULL
            """
            
            result = self.postgresql._execute_query(check_query, fetch_all=False)
            
            if not result:
                self.logger.warning("pg_stat_statements extension is not installed")
                return []
            
            # Get slow queries
            query = """
            SELECT queryid,
                   calls,
                   total_time / calls as avg_time_ms,
                   min_time as min_time_ms,
                   max_time as max_time_ms,
                   mean_time as mean_time_ms,
                   stddev_time as stddev_time_ms,
                   rows,
                   shared_blks_hit,
                   shared_blks_read,
                   shared_blks_dirtied,
                   shared_blks_written,
                   local_blks_hit,
                   local_blks_read,
                   local_blks_dirtied,
                   local_blks_written,
                   temp_blks_read,
                   temp_blks_written,
                   query
            FROM pg_stat_statements
            WHERE mean_time >= %s
            ORDER BY mean_time DESC
            LIMIT %s
            """
            
            queries = self.postgresql._execute_query(query, (min_duration, limit))
            
            return queries
        except Exception as e:
            self.postgresql._handle_error("get_slow_queries", e)
    
    def get_table_bloat(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get table bloat information.
        
        Args:
            limit: Maximum number of tables to return
            
        Returns:
            List of tables with bloat information
        """
        try:
            query = """
            SELECT schemaname as schema,
                   tablename as table,
                   reltuples::bigint as row_count,
                   pg_size_pretty(relpages::bigint * 8192) as table_size,
                   pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) as actual_size,
                   CASE WHEN relpages > 0
                        THEN round(100 * (relpages::bigint * 8192 - pg_relation_size(schemaname || '.' || tablename)) / (relpages::bigint * 8192))
                        ELSE 0
                   END as bloat_percentage
            FROM pg_catalog.pg_stat_user_tables
            ORDER BY bloat_percentage DESC
            LIMIT %s
            """
            
            tables = self.postgresql._execute_query(query, (limit,))
            
            return tables
        except Exception as e:
            self.postgresql._handle_error("get_table_bloat", e)
    
    def get_index_usage(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get index usage information.
        
        Args:
            limit: Maximum number of indexes to return
            
        Returns:
            List of indexes with usage information
        """
        try:
            query = """
            SELECT schemaname as schema,
                   relname as table,
                   indexrelname as index,
                   idx_scan as scans,
                   idx_tup_read as tuples_read,
                   idx_tup_fetch as tuples_fetched,
                   pg_size_pretty(pg_relation_size(schemaname || '.' || indexrelname)) as index_size
            FROM pg_stat_user_indexes
            ORDER BY idx_scan DESC
            LIMIT %s
            """
            
            indexes = self.postgresql._execute_query(query, (limit,))
            
            return indexes
        except Exception as e:
            self.postgresql._handle_error("get_index_usage", e)
    
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