"""
AWS Route 53 tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from services.aws.service import AWSServiceManager
from utils.logging import setup_logger
from tools.aws.base_tools import AWSBaseTools


class AWSRoute53Tools(AWSBaseTools):
    """Tools for interacting with AWS Route 53."""

    def __init__(self, mcp: FastMCP, aws_service: AWSServiceManager):
        """
        Initialize AWS Route 53 tools.

        Args:
            mcp: The MCP server instance.
            aws_service: The AWS service manager instance.
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.route53")
        self._register_tools()

    def _register_tools(self) -> None:
        """Register Route 53 tools with the MCP server."""

        @self.mcp.tool()
        def list_route53_hosted_zones(max_items: int = 100) -> str:
            """
            List all public and private hosted zones in Route 53.

            Args:
                max_items: Maximum number of hosted zones to return (default: 100).
            
            Returns:
                List of hosted zones in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                hosted_zones = self.aws_service.route53.list_hosted_zones(max_items=max_items)
                return self._format_response({"hosted_zones": hosted_zones, "count": len(hosted_zones)})
            except Exception as e:
                self.logger.error(f"Error listing Route 53 hosted zones: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def list_route53_resource_record_sets(hosted_zone_id: str, start_record_name: Optional[str] = None, start_record_type: Optional[str] = None, max_items: int = 100) -> str:
            """
            List DNS records within a specific Route 53 hosted zone.

            Args:
                hosted_zone_id: The ID of the hosted zone.
                start_record_name: The first record name to return (optional).
                start_record_type: The first record type to return (optional).
                max_items: Maximum number of record sets to return (default: 100).
            
            Returns:
                List of resource record sets in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")

            try:
                record_sets = self.aws_service.route53.list_resource_record_sets(
                    hosted_zone_id=hosted_zone_id,
                    start_record_name=start_record_name,
                    start_record_type=start_record_type,
                    max_items=max_items
                )
                return self._format_response({"resource_record_sets": record_sets, "count": len(record_sets)})
            except Exception as e:
                self.logger.error(f"Error listing Route 53 resource record sets for {hosted_zone_id}: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_route53_health_check_status(health_check_id: str) -> str:
            """
            Get the status of a Route 53 health check.

            Args:
                health_check_id: The ID of the health check.
            
            Returns:
                Dictionary containing the health check status in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                status = self.aws_service.route53.get_health_check_status(health_check_id=health_check_id)
                return self._format_response(status)
            except Exception as e:
                self.logger.error(f"Error getting Route 53 health check status for {health_check_id}: {e}")
                return self._format_error(str(e))

        self.logger.info("AWS Route 53 tools registered successfully")