"""
AWS RDS tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.base_tools import AWSBaseTools
from utils.logging import setup_logger


class AWSRDSTools(AWSBaseTools):
    """Tools for AWS RDS operations."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS RDS tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.rds")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register AWS RDS tools with the MCP server."""
        
        @self.mcp.tool()
        def list_rds_instances(max_records: int = 100) -> str:
            """
            List RDS DB instances.
            
            This tool lists RDS DB instances in your AWS account.
            
            Args:
                max_records: Maximum number of records to return (default: 100, max: 100)
                
            Returns:
                List of DB instances in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_records
            max_records = min(max(1, max_records), 100)
            
            try:
                instances = self.aws_service.rds.list_db_instances(max_records)
                return self._format_response({"dbInstances": instances, "count": len(instances)})
            except Exception as e:
                self.logger.error(f"Error listing RDS instances: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_rds_instance(db_instance_identifier: str) -> str:
            """
            Get details of an RDS DB instance.
            
            This tool retrieves details of an RDS DB instance.
            
            Args:
                db_instance_identifier: DB instance identifier
                
            Returns:
                DB instance details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                instance = self.aws_service.rds.get_db_instance(db_instance_identifier)
                return self._format_response(instance)
            except Exception as e:
                self.logger.error(f"Error getting RDS instance: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_rds_clusters(max_records: int = 100) -> str:
            """
            List RDS DB clusters.
            
            This tool lists RDS DB clusters in your AWS account.
            
            Args:
                max_records: Maximum number of records to return (default: 100, max: 100)
                
            Returns:
                List of DB clusters in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_records
            max_records = min(max(1, max_records), 100)
            
            try:
                clusters = self.aws_service.rds.list_db_clusters(max_records)
                return self._format_response({"dbClusters": clusters, "count": len(clusters)})
            except Exception as e:
                self.logger.error(f"Error listing RDS clusters: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_rds_cluster(db_cluster_identifier: str) -> str:
            """
            Get details of an RDS DB cluster.
            
            This tool retrieves details of an RDS DB cluster.
            
            Args:
                db_cluster_identifier: DB cluster identifier
                
            Returns:
                DB cluster details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                cluster = self.aws_service.rds.get_db_cluster(db_cluster_identifier)
                return self._format_response(cluster)
            except Exception as e:
                self.logger.error(f"Error getting RDS cluster: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_rds_parameter_groups(max_records: int = 100) -> str:
            """
            List RDS DB parameter groups.
            
            This tool lists RDS DB parameter groups in your AWS account.
            
            Args:
                max_records: Maximum number of records to return (default: 100, max: 100)
                
            Returns:
                List of DB parameter groups in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_records
            max_records = min(max(1, max_records), 100)
            
            try:
                parameter_groups = self.aws_service.rds.list_db_parameter_groups(max_records)
                return self._format_response({"dbParameterGroups": parameter_groups, "count": len(parameter_groups)})
            except Exception as e:
                self.logger.error(f"Error listing RDS parameter groups: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_rds_parameter_group(db_parameter_group_name: str) -> str:
            """
            Get details of an RDS DB parameter group.
            
            This tool retrieves details of an RDS DB parameter group.
            
            Args:
                db_parameter_group_name: DB parameter group name
                
            Returns:
                DB parameter group details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                parameter_group = self.aws_service.rds.get_db_parameter_group(db_parameter_group_name)
                return self._format_response(parameter_group)
            except Exception as e:
                self.logger.error(f"Error getting RDS parameter group: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_rds_parameters(db_parameter_group_name: str, source: str = None, 
                             max_records: int = 100) -> str:
            """
            List parameters in an RDS DB parameter group.
            
            This tool lists parameters in an RDS DB parameter group.
            
            Args:
                db_parameter_group_name: DB parameter group name
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
                parameters = self.aws_service.rds.list_db_parameters(db_parameter_group_name, source, max_records)
                return self._format_response({"parameters": parameters, "count": len(parameters)})
            except Exception as e:
                self.logger.error(f"Error listing RDS parameters: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_rds_subnet_groups(max_records: int = 100) -> str:
            """
            List RDS DB subnet groups.
            
            This tool lists RDS DB subnet groups in your AWS account.
            
            Args:
                max_records: Maximum number of records to return (default: 100, max: 100)
                
            Returns:
                List of DB subnet groups in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_records
            max_records = min(max(1, max_records), 100)
            
            try:
                subnet_groups = self.aws_service.rds.list_db_subnet_groups(max_records)
                return self._format_response({"dbSubnetGroups": subnet_groups, "count": len(subnet_groups)})
            except Exception as e:
                self.logger.error(f"Error listing RDS subnet groups: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_rds_subnet_group(db_subnet_group_name: str) -> str:
            """
            Get details of an RDS DB subnet group.
            
            This tool retrieves details of an RDS DB subnet group.
            
            Args:
                db_subnet_group_name: DB subnet group name
                
            Returns:
                DB subnet group details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                subnet_group = self.aws_service.rds.get_db_subnet_group(db_subnet_group_name)
                return self._format_response(subnet_group)
            except Exception as e:
                self.logger.error(f"Error getting RDS subnet group: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_rds_snapshots(db_instance_identifier: str = None, 
                            snapshot_type: str = None, max_records: int = 100) -> str:
            """
            List RDS DB snapshots.
            
            This tool lists RDS DB snapshots in your AWS account.
            
            Args:
                db_instance_identifier: DB instance identifier (optional)
                snapshot_type: Snapshot type (optional)
                max_records: Maximum number of records to return (default: 100, max: 100)
                
            Returns:
                List of DB snapshots in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_records
            max_records = min(max(1, max_records), 100)
            
            try:
                snapshots = self.aws_service.rds.list_db_snapshots(
                    db_instance_identifier, snapshot_type, max_records
                )
                return self._format_response({"dbSnapshots": snapshots, "count": len(snapshots)})
            except Exception as e:
                self.logger.error(f"Error listing RDS snapshots: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_rds_snapshot(db_snapshot_identifier: str) -> str:
            """
            Get details of an RDS DB snapshot.
            
            This tool retrieves details of an RDS DB snapshot.
            
            Args:
                db_snapshot_identifier: DB snapshot identifier
                
            Returns:
                DB snapshot details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                snapshot = self.aws_service.rds.get_db_snapshot(db_snapshot_identifier)
                return self._format_response(snapshot)
            except Exception as e:
                self.logger.error(f"Error getting RDS snapshot: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def describe_rds_db_log_files(db_instance_identifier: str, filename_contains: Optional[str] = None, max_records: int = 100) -> str:
            """
            List log files for an RDS DB instance.

            Args:
                db_instance_identifier: The identifier of the DB instance.
                filename_contains: Filter log files by a string in the filename (optional).
                max_records: Maximum number of log files to return (default: 100, max: 100).
            
            Returns:
                A list of log file metadata in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            max_records = min(max(1, max_records), 100)

            try:
                log_files = self.aws_service.rds.describe_db_log_files(
                    db_instance_identifier=db_instance_identifier,
                    filename_contains=filename_contains,
                    max_records=max_records
                )
                return self._format_response({"log_files": log_files, "count": len(log_files)})
            except Exception as e:
                self.logger.error(f"Error describing RDS DB log files for {db_instance_identifier}: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def download_rds_db_log_file_portion(db_instance_identifier: str, log_file_name: str, marker: Optional[str] = None, number_of_lines: int = 1000) -> str:
            """
            Download a portion of an RDS DB log file.

            Args:
                db_instance_identifier: The identifier of the DB instance.
                log_file_name: The name of the log file.
                marker: A pagination token for retrieving the next set of results (optional).
                number_of_lines: The number of lines to retrieve (default: 1000).
            
            Returns:
                A dictionary containing the log file data, marker, and additional data pending flag in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")

            try:
                log_data = self.aws_service.rds.download_db_log_file_portion(
                    db_instance_identifier=db_instance_identifier,
                    log_file_name=log_file_name,
                    marker=marker,
                    number_of_lines=number_of_lines
                )
                return self._format_response(log_data)
            except Exception as e:
                self.logger.error(f"Error downloading RDS DB log file portion for {log_file_name} from {db_instance_identifier}: {e}")
                return self._format_error(str(e))