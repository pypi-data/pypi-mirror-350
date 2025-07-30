"""
Base AWS tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from utils.logging import setup_logger
from utils.formatting import format_json_response, format_error_response


class AWSBaseTools:
    """Base class for AWS tools."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS base tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        self.mcp = mcp
        self.aws_service = aws_service or AWSServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.aws.base")
    
    def _check_service_available(self) -> bool:
        """
        Check if the AWS service is available.
        
        Returns:
            True if available, False otherwise
        """
        if not self.aws_service:
            self.logger.error("AWS service is not available")
            return False
        
        if not self.aws_service.is_available():
            self.logger.error("AWS API is not available")
            return False
        
        return True
    
    def _format_response(self, result: Any) -> str:
        """
        Format a response from the AWS API.
        
        Args:
            result: The result from the AWS API
            
        Returns:
            Formatted response
        """
        return format_json_response(result)
    
    def _format_error(self, message: str) -> str:
        """
        Format an error message.
        
        Args:
            message: The error message
            
        Returns:
            Formatted error response
        """
        return format_error_response(message)