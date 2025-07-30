"""
AWS EC2 tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from services.aws.service import AWSServiceManager
from utils.logging import setup_logger


class AWSEC2Tools:
    """Tools for interacting with AWS EC2."""

    def __init__(self, mcp: FastMCP, aws_service: AWSServiceManager):
        """
        Initialize AWS EC2 tools.

        Args:
            mcp: The MCP server instance.
            aws_service: The AWS service manager instance.
        """
        self.mcp = mcp
        self.aws_service = aws_service
        self.logger = setup_logger("devops_mcp_server.tools.aws.ec2")
        self._register_tools()

    def _register_tools(self) -> None:
        """Register EC2 tools with the MCP server."""

        @self.mcp.tool()
        def list_ec2_instances(max_results: int = 50) -> Dict[str, Any]:
            """
            List EC2 instances.

            Args:
                max_results: Maximum number of instances to return (default: 50)
            
            Returns:
                List of EC2 instances in JSON format
            """
            self.logger.info(f"Listing EC2 instances with max_results: {max_results}")
            try:
                instances = self.aws_service.ec2.list_instances(max_results=max_results)
                return {"instances": instances, "count": len(instances)}
            except Exception as e:
                self.logger.error(f"Error listing EC2 instances: {e}")
                return {"error": str(e)}

        @self.mcp.tool()
        def get_ec2_instance_details(instance_id: str) -> Dict[str, Any]:
            """
            Get detailed information for a specific EC2 instance.

            Args:
                instance_id: The ID of the EC2 instance.
            
            Returns:
                Dictionary containing instance details in JSON format.
            """
            self.logger.info(f"Getting details for EC2 instance: {instance_id}")
            try:
                details = self.aws_service.ec2.get_instance_details(instance_id=instance_id)
                return details
            except Exception as e:
                self.logger.error(f"Error getting EC2 instance details for {instance_id}: {e}")
                return {"error": str(e)}

        self.logger.info("AWS EC2 tools registered successfully")