"""
AWS Elastic Load Balancing tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.base_tools import AWSBaseTools
from utils.logging import setup_logger


class AWSELBTools(AWSBaseTools):
    """Tools for AWS Elastic Load Balancing operations."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS ELB tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.elb")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register AWS ELB tools with the MCP server."""
        
        @self.mcp.tool()
        def list_load_balancers(max_results: int = 100) -> str:
            """
            List Application Load Balancers.
            
            This tool lists all Application Load Balancers in your AWS account.
            
            Args:
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of load balancers in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                load_balancers = self.aws_service.elb.list_load_balancers(max_results)
                return self._format_response({"loadBalancers": load_balancers, "count": len(load_balancers)})
            except Exception as e:
                self.logger.error(f"Error listing load balancers: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_load_balancer(load_balancer_arn: str) -> str:
            """
            Get details of a load balancer.
            
            This tool retrieves details of a load balancer.
            
            Args:
                load_balancer_arn: Load balancer ARN
                
            Returns:
                Load balancer details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                load_balancer_details = self.aws_service.elb.get_load_balancer(load_balancer_arn)
                return self._format_response(load_balancer_details)
            except Exception as e:
                self.logger.error(f"Error getting load balancer: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_listeners(load_balancer_arn: str) -> str:
            """
            List listeners for a load balancer.
            
            This tool lists all listeners for a load balancer.
            
            Args:
                load_balancer_arn: Load balancer ARN
                
            Returns:
                List of listeners in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                listeners = self.aws_service.elb.list_listeners(load_balancer_arn)
                return self._format_response({"listeners": listeners, "count": len(listeners)})
            except Exception as e:
                self.logger.error(f"Error listing listeners: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_listener(listener_arn: str) -> str:
            """
            Get details of a listener.
            
            This tool retrieves details of a listener.
            
            Args:
                listener_arn: Listener ARN
                
            Returns:
                Listener details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                listener_details = self.aws_service.elb.get_listener(listener_arn)
                return self._format_response(listener_details)
            except Exception as e:
                self.logger.error(f"Error getting listener: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_target_groups(load_balancer_arn: str = None, max_results: int = 100) -> str:
            """
            List target groups.
            
            This tool lists all target groups, optionally filtered by load balancer.
            
            Args:
                load_balancer_arn: Load balancer ARN (optional)
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                List of target groups in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                target_groups = self.aws_service.elb.list_target_groups(load_balancer_arn, max_results)
                return self._format_response({"targetGroups": target_groups, "count": len(target_groups)})
            except Exception as e:
                self.logger.error(f"Error listing target groups: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_target_group(target_group_arn: str) -> str:
            """
            Get details of a target group.
            
            This tool retrieves details of a target group.
            
            Args:
                target_group_arn: Target group ARN
                
            Returns:
                Target group details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                target_group_details = self.aws_service.elb.get_target_group(target_group_arn)
                return self._format_response(target_group_details)
            except Exception as e:
                self.logger.error(f"Error getting target group: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_target_health(target_group_arn: str) -> str:
            """
            List health of targets in a target group.
            
            This tool lists the health of all targets in a target group.
            
            Args:
                target_group_arn: Target group ARN
                
            Returns:
                List of target health descriptions in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                target_health = self.aws_service.elb.list_target_health(target_group_arn)
                return self._format_response({"targetHealthDescriptions": target_health, "count": len(target_health)})
            except Exception as e:
                self.logger.error(f"Error listing target health: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_rules(listener_arn: str) -> str:
            """
            List rules for a listener.
            
            This tool lists all rules for a listener.
            
            Args:
                listener_arn: Listener ARN
                
            Returns:
                List of rules in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                rules = self.aws_service.elb.list_rules(listener_arn)
                return self._format_response({"rules": rules, "count": len(rules)})
            except Exception as e:
                self.logger.error(f"Error listing rules: {e}")
                return self._format_error(str(e))