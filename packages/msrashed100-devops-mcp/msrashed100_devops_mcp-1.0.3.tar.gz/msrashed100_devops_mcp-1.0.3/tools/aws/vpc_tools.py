"""
AWS VPC tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.base_tools import AWSBaseTools
from utils.logging import setup_logger


class AWSVPCTools(AWSBaseTools):
    """Tools for AWS VPC operations."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS VPC tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.vpc")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register AWS VPC tools with the MCP server."""
        
        @self.mcp.tool()
        def list_vpcs(max_results: int = 100) -> str:
            """
            List VPCs.
            
            This tool lists all VPCs in your AWS account.
            
            Args:
                max_results: Maximum number of results to return (default: 100, max: 1000)
                
            Returns:
                List of VPCs in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 1000)
            
            try:
                vpcs = self.aws_service.vpc.list_vpcs(max_results)
                return self._format_response({"vpcs": vpcs, "count": len(vpcs)})
            except Exception as e:
                self.logger.error(f"Error listing VPCs: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_vpc(vpc_id: str) -> str:
            """
            Get details of a VPC.
            
            This tool retrieves details of a VPC.
            
            Args:
                vpc_id: VPC ID
                
            Returns:
                VPC details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                vpc_details = self.aws_service.vpc.get_vpc(vpc_id)
                return self._format_response(vpc_details)
            except Exception as e:
                self.logger.error(f"Error getting VPC: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_subnets(vpc_id: str = None, max_results: int = 100) -> str:
            """
            List subnets.
            
            This tool lists all subnets, optionally filtered by VPC.
            
            Args:
                vpc_id: VPC ID (optional)
                max_results: Maximum number of results to return (default: 100, max: 1000)
                
            Returns:
                List of subnets in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 1000)
            
            try:
                subnets = self.aws_service.vpc.list_subnets(vpc_id, max_results)
                return self._format_response({"subnets": subnets, "count": len(subnets)})
            except Exception as e:
                self.logger.error(f"Error listing subnets: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_subnet(subnet_id: str) -> str:
            """
            Get details of a subnet.
            
            This tool retrieves details of a subnet.
            
            Args:
                subnet_id: Subnet ID
                
            Returns:
                Subnet details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                subnet_details = self.aws_service.vpc.get_subnet(subnet_id)
                return self._format_response(subnet_details)
            except Exception as e:
                self.logger.error(f"Error getting subnet: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_security_groups(vpc_id: str = None, max_results: int = 100) -> str:
            """
            List security groups.
            
            This tool lists all security groups, optionally filtered by VPC.
            
            Args:
                vpc_id: VPC ID (optional)
                max_results: Maximum number of results to return (default: 100, max: 1000)
                
            Returns:
                List of security groups in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 1000)
            
            try:
                security_groups = self.aws_service.vpc.list_security_groups(vpc_id, max_results)
                return self._format_response({"securityGroups": security_groups, "count": len(security_groups)})
            except Exception as e:
                self.logger.error(f"Error listing security groups: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_security_group(security_group_id: str) -> str:
            """
            Get details of a security group.
            
            This tool retrieves details of a security group.
            
            Args:
                security_group_id: Security group ID
                
            Returns:
                Security group details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                security_group_details = self.aws_service.vpc.get_security_group(security_group_id)
                return self._format_response(security_group_details)
            except Exception as e:
                self.logger.error(f"Error getting security group: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_route_tables(vpc_id: str = None, max_results: int = 100) -> str:
            """
            List route tables.
            
            This tool lists all route tables, optionally filtered by VPC.
            
            Args:
                vpc_id: VPC ID (optional)
                max_results: Maximum number of results to return (default: 100, max: 1000)
                
            Returns:
                List of route tables in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 1000)
            
            try:
                route_tables = self.aws_service.vpc.list_route_tables(vpc_id, max_results)
                return self._format_response({"routeTables": route_tables, "count": len(route_tables)})
            except Exception as e:
                self.logger.error(f"Error listing route tables: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_route_table(route_table_id: str) -> str:
            """
            Get details of a route table.
            
            This tool retrieves details of a route table.
            
            Args:
                route_table_id: Route table ID
                
            Returns:
                Route table details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                route_table_details = self.aws_service.vpc.get_route_table(route_table_id)
                return self._format_response(route_table_details)
            except Exception as e:
                self.logger.error(f"Error getting route table: {e}")
                return self._format_error(str(e))