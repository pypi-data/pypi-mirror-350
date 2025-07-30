"""
AWS ElastiCache tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.base_tools import AWSBaseTools
from utils.logging import setup_logger


class AWSElastiCacheTools(AWSBaseTools):
    """Tools for AWS ElastiCache operations."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS ElastiCache tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.elasticache")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register AWS ElastiCache tools with the MCP server."""
        
        @self.mcp.tool()
        def list_elasticache_clusters(max_records: int = 100) -> str:
            """
            List ElastiCache clusters.
            
            This tool lists ElastiCache clusters in your AWS account.
            
            Args:
                max_records: Maximum number of records to return (default: 100, max: 100)
                
            Returns:
                List of cache clusters in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_records
            max_records = min(max(1, max_records), 100)
            
            try:
                clusters = self.aws_service.elasticache.list_cache_clusters(max_records)
                return self._format_response({"cacheClusters": clusters, "count": len(clusters)})
            except Exception as e:
                self.logger.error(f"Error listing ElastiCache clusters: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_elasticache_cluster(cache_cluster_id: str, show_cache_node_info: bool = True) -> str:
            """
            Get details of an ElastiCache cluster.
            
            This tool retrieves details of an ElastiCache cluster.
            
            Args:
                cache_cluster_id: Cache cluster ID
                show_cache_node_info: Whether to include cache node info (default: True)
                
            Returns:
                Cache cluster details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                cluster = self.aws_service.elasticache.get_cache_cluster(cache_cluster_id, show_cache_node_info)
                return self._format_response(cluster)
            except Exception as e:
                self.logger.error(f"Error getting ElastiCache cluster: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_elasticache_replication_groups(max_records: int = 100) -> str:
            """
            List ElastiCache replication groups.
            
            This tool lists ElastiCache replication groups in your AWS account.
            
            Args:
                max_records: Maximum number of records to return (default: 100, max: 100)
                
            Returns:
                List of replication groups in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_records
            max_records = min(max(1, max_records), 100)
            
            try:
                groups = self.aws_service.elasticache.list_replication_groups(max_records)
                return self._format_response({"replicationGroups": groups, "count": len(groups)})
            except Exception as e:
                self.logger.error(f"Error listing ElastiCache replication groups: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_elasticache_replication_group(replication_group_id: str) -> str:
            """
            Get details of an ElastiCache replication group.
            
            This tool retrieves details of an ElastiCache replication group.
            
            Args:
                replication_group_id: Replication group ID
                
            Returns:
                Replication group details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                group = self.aws_service.elasticache.get_replication_group(replication_group_id)
                return self._format_response(group)
            except Exception as e:
                self.logger.error(f"Error getting ElastiCache replication group: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_elasticache_parameter_groups(max_records: int = 100) -> str:
            """
            List ElastiCache parameter groups.
            
            This tool lists ElastiCache parameter groups in your AWS account.
            
            Args:
                max_records: Maximum number of records to return (default: 100, max: 100)
                
            Returns:
                List of cache parameter groups in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_records
            max_records = min(max(1, max_records), 100)
            
            try:
                groups = self.aws_service.elasticache.list_cache_parameter_groups(max_records)
                return self._format_response({"cacheParameterGroups": groups, "count": len(groups)})
            except Exception as e:
                self.logger.error(f"Error listing ElastiCache parameter groups: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_elasticache_parameter_group(cache_parameter_group_name: str) -> str:
            """
            Get details of an ElastiCache parameter group.
            
            This tool retrieves details of an ElastiCache parameter group.
            
            Args:
                cache_parameter_group_name: Cache parameter group name
                
            Returns:
                Cache parameter group details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                group = self.aws_service.elasticache.get_cache_parameter_group(cache_parameter_group_name)
                return self._format_response(group)
            except Exception as e:
                self.logger.error(f"Error getting ElastiCache parameter group: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_elasticache_parameters(cache_parameter_group_name: str, source: str = None, 
                                     max_records: int = 100) -> str:
            """
            List parameters in an ElastiCache parameter group.
            
            This tool lists parameters in an ElastiCache parameter group.
            
            Args:
                cache_parameter_group_name: Cache parameter group name
                source: Parameter source (user, system, engine-default) (optional)
                max_records: Maximum number of records to return (default: 100, max: 100)
                
            Returns:
                List of parameters in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_records
            max_records = min(max(1, max_records), 100)
            
            try:
                parameters = self.aws_service.elasticache.list_cache_parameters(
                    cache_parameter_group_name, source, max_records
                )
                return self._format_response(parameters)
            except Exception as e:
                self.logger.error(f"Error listing ElastiCache parameters: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_elasticache_subnet_groups(max_records: int = 100) -> str:
            """
            List ElastiCache subnet groups.
            
            This tool lists ElastiCache subnet groups in your AWS account.
            
            Args:
                max_records: Maximum number of records to return (default: 100, max: 100)
                
            Returns:
                List of cache subnet groups in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_records
            max_records = min(max(1, max_records), 100)
            
            try:
                groups = self.aws_service.elasticache.list_cache_subnet_groups(max_records)
                return self._format_response({"cacheSubnetGroups": groups, "count": len(groups)})
            except Exception as e:
                self.logger.error(f"Error listing ElastiCache subnet groups: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_elasticache_subnet_group(cache_subnet_group_name: str) -> str:
            """
            Get details of an ElastiCache subnet group.
            
            This tool retrieves details of an ElastiCache subnet group.
            
            Args:
                cache_subnet_group_name: Cache subnet group name
                
            Returns:
                Cache subnet group details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                group = self.aws_service.elasticache.get_cache_subnet_group(cache_subnet_group_name)
                return self._format_response(group)
            except Exception as e:
                self.logger.error(f"Error getting ElastiCache subnet group: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_elasticache_engine_versions(engine: str = None, max_records: int = 100) -> str:
            """
            List ElastiCache engine versions.
            
            This tool lists ElastiCache engine versions.
            
            Args:
                engine: Cache engine (optional)
                max_records: Maximum number of records to return (default: 100, max: 100)
                
            Returns:
                List of cache engine versions in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_records
            max_records = min(max(1, max_records), 100)
            
            try:
                versions = self.aws_service.elasticache.list_cache_engine_versions(engine, max_records)
                return self._format_response(versions)
            except Exception as e:
                self.logger.error(f"Error listing ElastiCache engine versions: {e}")
                return self._format_error(str(e))