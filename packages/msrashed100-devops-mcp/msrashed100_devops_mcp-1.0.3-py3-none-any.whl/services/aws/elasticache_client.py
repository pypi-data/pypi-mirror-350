"""
AWS ElastiCache client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.aws.client import AWSService


class AWSElastiCacheClient:
    """Client for AWS ElastiCache operations."""
    
    def __init__(self, aws_service: AWSService):
        """
        Initialize the AWS ElastiCache client.
        
        Args:
            aws_service: The base AWS service
        """
        self.aws = aws_service
        self.logger = aws_service.logger
        self.client = None
    
    def _get_client(self):
        """Get the ElastiCache client."""
        if self.client is None:
            self.client = self.aws.get_client('elasticache')
        return self.client
    
    def list_cache_clusters(self, max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List ElastiCache clusters.
        
        Args:
            max_records: Maximum number of records to return
            
        Returns:
            List of cache clusters
        """
        try:
            client = self._get_client()
            
            response = client.describe_cache_clusters(MaxRecords=min(max_records, 100))
            clusters = response.get('CacheClusters', [])
            
            return clusters
        except Exception as e:
            self.aws._handle_error("list_cache_clusters", e)
    
    def get_cache_cluster(self, cache_cluster_id: str, show_cache_node_info: bool = True) -> Dict[str, Any]:
        """
        Get details of an ElastiCache cluster.
        
        Args:
            cache_cluster_id: Cache cluster ID
            show_cache_node_info: Whether to include cache node info
            
        Returns:
            Cache cluster details
        """
        try:
            client = self._get_client()
            
            response = client.describe_cache_clusters(
                CacheClusterId=cache_cluster_id,
                ShowCacheNodeInfo=show_cache_node_info
            )
            clusters = response.get('CacheClusters', [])
            
            if not clusters:
                raise ValueError(f"Cache cluster '{cache_cluster_id}' not found")
            
            return clusters[0]
        except Exception as e:
            self.aws._handle_error(f"get_cache_cluster({cache_cluster_id})", e)
    
    def list_replication_groups(self, max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List ElastiCache replication groups.
        
        Args:
            max_records: Maximum number of records to return
            
        Returns:
            List of replication groups
        """
        try:
            client = self._get_client()
            
            response = client.describe_replication_groups(MaxRecords=min(max_records, 100))
            groups = response.get('ReplicationGroups', [])
            
            return groups
        except Exception as e:
            self.aws._handle_error("list_replication_groups", e)
    
    def get_replication_group(self, replication_group_id: str) -> Dict[str, Any]:
        """
        Get details of an ElastiCache replication group.
        
        Args:
            replication_group_id: Replication group ID
            
        Returns:
            Replication group details
        """
        try:
            client = self._get_client()
            
            response = client.describe_replication_groups(ReplicationGroupId=replication_group_id)
            groups = response.get('ReplicationGroups', [])
            
            if not groups:
                raise ValueError(f"Replication group '{replication_group_id}' not found")
            
            return groups[0]
        except Exception as e:
            self.aws._handle_error(f"get_replication_group({replication_group_id})", e)
    
    def list_cache_parameter_groups(self, max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List ElastiCache parameter groups.
        
        Args:
            max_records: Maximum number of records to return
            
        Returns:
            List of cache parameter groups
        """
        try:
            client = self._get_client()
            
            response = client.describe_cache_parameter_groups(MaxRecords=min(max_records, 100))
            groups = response.get('CacheParameterGroups', [])
            
            return groups
        except Exception as e:
            self.aws._handle_error("list_cache_parameter_groups", e)
    
    def get_cache_parameter_group(self, cache_parameter_group_name: str) -> Dict[str, Any]:
        """
        Get details of an ElastiCache parameter group.
        
        Args:
            cache_parameter_group_name: Cache parameter group name
            
        Returns:
            Cache parameter group details
        """
        try:
            client = self._get_client()
            
            response = client.describe_cache_parameter_groups(
                CacheParameterGroupName=cache_parameter_group_name
            )
            groups = response.get('CacheParameterGroups', [])
            
            if not groups:
                raise ValueError(f"Cache parameter group '{cache_parameter_group_name}' not found")
            
            return groups[0]
        except Exception as e:
            self.aws._handle_error(f"get_cache_parameter_group({cache_parameter_group_name})", e)
    
    def list_cache_parameters(self, cache_parameter_group_name: str, source: Optional[str] = None, 
                            max_records: int = 100) -> Dict[str, Any]:
        """
        List parameters in an ElastiCache parameter group.
        
        Args:
            cache_parameter_group_name: Cache parameter group name
            source: Parameter source (user, system, engine-default)
            max_records: Maximum number of records to return
            
        Returns:
            List of parameters
        """
        try:
            client = self._get_client()
            
            params = {
                'CacheParameterGroupName': cache_parameter_group_name,
                'MaxRecords': min(max_records, 100)
            }
            if source:
                params['Source'] = source
            
            response = client.describe_cache_parameters(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error(f"list_cache_parameters({cache_parameter_group_name})", e)
    
    def list_cache_subnet_groups(self, max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List ElastiCache subnet groups.
        
        Args:
            max_records: Maximum number of records to return
            
        Returns:
            List of cache subnet groups
        """
        try:
            client = self._get_client()
            
            response = client.describe_cache_subnet_groups(MaxRecords=min(max_records, 100))
            groups = response.get('CacheSubnetGroups', [])
            
            return groups
        except Exception as e:
            self.aws._handle_error("list_cache_subnet_groups", e)
    
    def get_cache_subnet_group(self, cache_subnet_group_name: str) -> Dict[str, Any]:
        """
        Get details of an ElastiCache subnet group.
        
        Args:
            cache_subnet_group_name: Cache subnet group name
            
        Returns:
            Cache subnet group details
        """
        try:
            client = self._get_client()
            
            response = client.describe_cache_subnet_groups(
                CacheSubnetGroupName=cache_subnet_group_name
            )
            groups = response.get('CacheSubnetGroups', [])
            
            if not groups:
                raise ValueError(f"Cache subnet group '{cache_subnet_group_name}' not found")
            
            return groups[0]
        except Exception as e:
            self.aws._handle_error(f"get_cache_subnet_group({cache_subnet_group_name})", e)
    
    def list_cache_security_groups(self, max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List ElastiCache security groups.
        
        Args:
            max_records: Maximum number of records to return
            
        Returns:
            List of cache security groups
        """
        try:
            client = self._get_client()
            
            response = client.describe_cache_security_groups(MaxRecords=min(max_records, 100))
            groups = response.get('CacheSecurityGroups', [])
            
            return groups
        except Exception as e:
            self.aws._handle_error("list_cache_security_groups", e)
    
    def get_cache_security_group(self, cache_security_group_name: str) -> Dict[str, Any]:
        """
        Get details of an ElastiCache security group.
        
        Args:
            cache_security_group_name: Cache security group name
            
        Returns:
            Cache security group details
        """
        try:
            client = self._get_client()
            
            response = client.describe_cache_security_groups(
                CacheSecurityGroupName=cache_security_group_name
            )
            groups = response.get('CacheSecurityGroups', [])
            
            if not groups:
                raise ValueError(f"Cache security group '{cache_security_group_name}' not found")
            
            return groups[0]
        except Exception as e:
            self.aws._handle_error(f"get_cache_security_group({cache_security_group_name})", e)
    
    def list_cache_engine_versions(self, engine: Optional[str] = None, 
                                 max_records: int = 100) -> List[Dict[str, Any]]:
        """
        List ElastiCache engine versions.
        
        Args:
            engine: Cache engine (optional)
            max_records: Maximum number of records to return
            
        Returns:
            List of cache engine versions
        """
        try:
            client = self._get_client()
            
            params = {'MaxRecords': min(max_records, 100)}
            if engine:
                params['Engine'] = engine
            
            response = client.describe_cache_engine_versions(**params)
            versions = response.get('CacheEngineVersions', [])
            
            return versions
        except Exception as e:
            self.aws._handle_error("list_cache_engine_versions", e)
    
    def list_allowed_node_type_modifications(self, cache_cluster_id: Optional[str] = None,
                                          replication_group_id: Optional[str] = None) -> List[str]:
        """
        List allowed node type modifications.
        
        Args:
            cache_cluster_id: Cache cluster ID (optional)
            replication_group_id: Replication group ID (optional)
            
        Returns:
            List of allowed node types
        """
        try:
            client = self._get_client()
            
            params = {}
            if cache_cluster_id:
                params['CacheClusterId'] = cache_cluster_id
            if replication_group_id:
                params['ReplicationGroupId'] = replication_group_id
            
            response = client.list_allowed_node_type_modifications(**params)
            node_types = response.get('ScaleUpModifications', [])
            
            return node_types
        except Exception as e:
            self.aws._handle_error("list_allowed_node_type_modifications", e)