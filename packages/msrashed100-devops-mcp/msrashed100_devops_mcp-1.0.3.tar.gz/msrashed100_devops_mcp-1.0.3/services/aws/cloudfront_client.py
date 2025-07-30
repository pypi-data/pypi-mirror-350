"""
AWS CloudFront client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.aws.client import AWSService


class AWSCloudFrontClient:
    """Client for AWS CloudFront operations."""
    
    def __init__(self, aws_service: AWSService):
        """
        Initialize the AWS CloudFront client.
        
        Args:
            aws_service: The base AWS service
        """
        self.aws = aws_service
        self.logger = aws_service.logger
        self.client = None
    
    def _get_client(self):
        """Get the CloudFront client."""
        if self.client is None:
            self.client = self.aws.get_client('cloudfront')
        return self.client
    
    def list_distributions(self, max_items: int = 100) -> Dict[str, Any]:
        """
        List CloudFront distributions.
        
        Args:
            max_items: Maximum number of items to return
            
        Returns:
            List of CloudFront distributions
        """
        try:
            client = self._get_client()
            
            response = client.list_distributions(MaxItems=str(min(max_items, 100)))
            
            return response.get('DistributionList', {})
        except Exception as e:
            self.aws._handle_error("list_distributions", e)
    
    def get_distribution(self, distribution_id: str) -> Dict[str, Any]:
        """
        Get details of a CloudFront distribution.
        
        Args:
            distribution_id: Distribution ID
            
        Returns:
            Distribution details
        """
        try:
            client = self._get_client()
            
            response = client.get_distribution(Id=distribution_id)
            
            return response.get('Distribution', {})
        except Exception as e:
            self.aws._handle_error(f"get_distribution({distribution_id})", e)
    
    def list_cache_policies(self, max_items: int = 100) -> Dict[str, Any]:
        """
        List CloudFront cache policies.
        
        Args:
            max_items: Maximum number of items to return
            
        Returns:
            List of CloudFront cache policies
        """
        try:
            client = self._get_client()
            
            response = client.list_cache_policies(MaxItems=str(min(max_items, 100)))
            
            return response.get('CachePolicyList', {})
        except Exception as e:
            self.aws._handle_error("list_cache_policies", e)
    
    def get_cache_policy(self, cache_policy_id: str) -> Dict[str, Any]:
        """
        Get details of a CloudFront cache policy.
        
        Args:
            cache_policy_id: Cache policy ID
            
        Returns:
            Cache policy details
        """
        try:
            client = self._get_client()
            
            response = client.get_cache_policy(Id=cache_policy_id)
            
            return response.get('CachePolicy', {})
        except Exception as e:
            self.aws._handle_error(f"get_cache_policy({cache_policy_id})", e)
    
    def list_origin_request_policies(self, max_items: int = 100) -> Dict[str, Any]:
        """
        List CloudFront origin request policies.
        
        Args:
            max_items: Maximum number of items to return
            
        Returns:
            List of CloudFront origin request policies
        """
        try:
            client = self._get_client()
            
            response = client.list_origin_request_policies(MaxItems=str(min(max_items, 100)))
            
            return response.get('OriginRequestPolicyList', {})
        except Exception as e:
            self.aws._handle_error("list_origin_request_policies", e)
    
    def get_origin_request_policy(self, origin_request_policy_id: str) -> Dict[str, Any]:
        """
        Get details of a CloudFront origin request policy.
        
        Args:
            origin_request_policy_id: Origin request policy ID
            
        Returns:
            Origin request policy details
        """
        try:
            client = self._get_client()
            
            response = client.get_origin_request_policy(Id=origin_request_policy_id)
            
            return response.get('OriginRequestPolicy', {})
        except Exception as e:
            self.aws._handle_error(f"get_origin_request_policy({origin_request_policy_id})", e)
    
    def list_invalidations(self, distribution_id: str, max_items: int = 100) -> Dict[str, Any]:
        """
        List CloudFront invalidations.
        
        Args:
            distribution_id: Distribution ID
            max_items: Maximum number of items to return
            
        Returns:
            List of CloudFront invalidations
        """
        try:
            client = self._get_client()
            
            response = client.list_invalidations(
                DistributionId=distribution_id,
                MaxItems=str(min(max_items, 100))
            )
            
            return response.get('InvalidationList', {})
        except Exception as e:
            self.aws._handle_error(f"list_invalidations({distribution_id})", e)
    
    def get_invalidation(self, distribution_id: str, invalidation_id: str) -> Dict[str, Any]:
        """
        Get details of a CloudFront invalidation.
        
        Args:
            distribution_id: Distribution ID
            invalidation_id: Invalidation ID
            
        Returns:
            Invalidation details
        """
        try:
            client = self._get_client()
            
            response = client.get_invalidation(
                DistributionId=distribution_id,
                Id=invalidation_id
            )
            
            return response.get('Invalidation', {})
        except Exception as e:
            self.aws._handle_error(f"get_invalidation({distribution_id}, {invalidation_id})", e)