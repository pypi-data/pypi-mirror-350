"""
AWS CloudFront tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.base_tools import AWSBaseTools
from utils.logging import setup_logger


class AWSCloudFrontTools(AWSBaseTools):
    """Tools for AWS CloudFront operations."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS CloudFront tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.cloudfront")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register AWS CloudFront tools with the MCP server."""
        
        @self.mcp.tool()
        def list_cloudfront_distributions(max_items: int = 100) -> str:
            """
            List CloudFront distributions.
            
            This tool lists all CloudFront distributions in your AWS account.
            
            Args:
                max_items: Maximum number of items to return (default: 100, max: 100)
                
            Returns:
                List of CloudFront distributions in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 100)
            
            try:
                distributions = self.aws_service.cloudfront.list_distributions(max_items)
                return self._format_response(distributions)
            except Exception as e:
                self.logger.error(f"Error listing CloudFront distributions: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_cloudfront_distribution(distribution_id: str) -> str:
            """
            Get details of a CloudFront distribution.
            
            This tool retrieves details of a CloudFront distribution.
            
            Args:
                distribution_id: Distribution ID
                
            Returns:
                Distribution details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                distribution = self.aws_service.cloudfront.get_distribution(distribution_id)
                return self._format_response(distribution)
            except Exception as e:
                self.logger.error(f"Error getting CloudFront distribution: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_cloudfront_cache_policies(max_items: int = 100) -> str:
            """
            List CloudFront cache policies.
            
            This tool lists all CloudFront cache policies in your AWS account.
            
            Args:
                max_items: Maximum number of items to return (default: 100, max: 100)
                
            Returns:
                List of CloudFront cache policies in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 100)
            
            try:
                policies = self.aws_service.cloudfront.list_cache_policies(max_items)
                return self._format_response(policies)
            except Exception as e:
                self.logger.error(f"Error listing CloudFront cache policies: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_cloudfront_cache_policy(cache_policy_id: str) -> str:
            """
            Get details of a CloudFront cache policy.
            
            This tool retrieves details of a CloudFront cache policy.
            
            Args:
                cache_policy_id: Cache policy ID
                
            Returns:
                Cache policy details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                policy = self.aws_service.cloudfront.get_cache_policy(cache_policy_id)
                return self._format_response(policy)
            except Exception as e:
                self.logger.error(f"Error getting CloudFront cache policy: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_cloudfront_origin_request_policies(max_items: int = 100) -> str:
            """
            List CloudFront origin request policies.
            
            This tool lists all CloudFront origin request policies in your AWS account.
            
            Args:
                max_items: Maximum number of items to return (default: 100, max: 100)
                
            Returns:
                List of CloudFront origin request policies in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 100)
            
            try:
                policies = self.aws_service.cloudfront.list_origin_request_policies(max_items)
                return self._format_response(policies)
            except Exception as e:
                self.logger.error(f"Error listing CloudFront origin request policies: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_cloudfront_origin_request_policy(origin_request_policy_id: str) -> str:
            """
            Get details of a CloudFront origin request policy.
            
            This tool retrieves details of a CloudFront origin request policy.
            
            Args:
                origin_request_policy_id: Origin request policy ID
                
            Returns:
                Origin request policy details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                policy = self.aws_service.cloudfront.get_origin_request_policy(origin_request_policy_id)
                return self._format_response(policy)
            except Exception as e:
                self.logger.error(f"Error getting CloudFront origin request policy: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_cloudfront_invalidations(distribution_id: str, max_items: int = 100) -> str:
            """
            List CloudFront invalidations.
            
            This tool lists all CloudFront invalidations for a distribution.
            
            Args:
                distribution_id: Distribution ID
                max_items: Maximum number of items to return (default: 100, max: 100)
                
            Returns:
                List of CloudFront invalidations in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 100)
            
            try:
                invalidations = self.aws_service.cloudfront.list_invalidations(distribution_id, max_items)
                return self._format_response(invalidations)
            except Exception as e:
                self.logger.error(f"Error listing CloudFront invalidations: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_cloudfront_invalidation(distribution_id: str, invalidation_id: str) -> str:
            """
            Get details of a CloudFront invalidation.
            
            This tool retrieves details of a CloudFront invalidation.
            
            Args:
                distribution_id: Distribution ID
                invalidation_id: Invalidation ID
                
            Returns:
                Invalidation details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                invalidation = self.aws_service.cloudfront.get_invalidation(distribution_id, invalidation_id)
                return self._format_response(invalidation)
            except Exception as e:
                self.logger.error(f"Error getting CloudFront invalidation: {e}")
                return self._format_error(str(e))