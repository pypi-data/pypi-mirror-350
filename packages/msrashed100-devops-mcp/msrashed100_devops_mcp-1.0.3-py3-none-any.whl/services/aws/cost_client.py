"""
AWS Cost Explorer client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from services.aws.client import AWSService


class AWSCostClient:
    """Client for AWS Cost Explorer operations."""
    
    def __init__(self, aws_service: AWSService):
        """
        Initialize the AWS Cost Explorer client.
        
        Args:
            aws_service: The base AWS service
        """
        self.aws = aws_service
        self.logger = aws_service.logger
        self.client = None
    
    def _get_client(self):
        """Get the Cost Explorer client."""
        if self.client is None:
            self.client = self.aws.get_client('ce')
        return self.client
    
    def get_cost_and_usage(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                          granularity: str = 'MONTHLY', metrics: Optional[List[str]] = None,
                          group_by: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Get cost and usage data.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
            end_date: End date in YYYY-MM-DD format (default: today)
            granularity: Time granularity (DAILY, MONTHLY, or HOURLY)
            metrics: Cost metrics to return (default: ["BlendedCost", "UnblendedCost", "UsageQuantity"])
            group_by: Dimensions to group by (default: None)
            
        Returns:
            Cost and usage data
        """
        try:
            client = self._get_client()
            
            # Set default dates if not provided
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            # Set default metrics if not provided
            if not metrics:
                metrics = ["BlendedCost", "UnblendedCost", "UsageQuantity"]
            
            # Build request parameters
            params = {
                'TimePeriod': {
                    'Start': start_date,
                    'End': end_date
                },
                'Granularity': granularity,
                'Metrics': metrics
            }
            
            # Add group by if provided
            if group_by:
                params['GroupBy'] = group_by
            
            response = client.get_cost_and_usage(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error("get_cost_and_usage", e)
    
    def get_cost_by_service(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                           granularity: str = 'MONTHLY') -> Dict[str, Any]:
        """
        Get cost data grouped by service.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
            end_date: End date in YYYY-MM-DD format (default: today)
            granularity: Time granularity (DAILY, MONTHLY, or HOURLY)
            
        Returns:
            Cost data grouped by service
        """
        try:
            # Group by service
            group_by = [
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ]
            
            return self.get_cost_and_usage(
                start_date=start_date,
                end_date=end_date,
                granularity=granularity,
                metrics=["BlendedCost"],
                group_by=group_by
            )
        except Exception as e:
            self.aws._handle_error("get_cost_by_service", e)
    
    def get_cost_by_account(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                           granularity: str = 'MONTHLY') -> Dict[str, Any]:
        """
        Get cost data grouped by account.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
            end_date: End date in YYYY-MM-DD format (default: today)
            granularity: Time granularity (DAILY, MONTHLY, or HOURLY)
            
        Returns:
            Cost data grouped by account
        """
        try:
            # Group by account
            group_by = [
                {
                    'Type': 'DIMENSION',
                    'Key': 'LINKED_ACCOUNT'
                }
            ]
            
            return self.get_cost_and_usage(
                start_date=start_date,
                end_date=end_date,
                granularity=granularity,
                metrics=["BlendedCost"],
                group_by=group_by
            )
        except Exception as e:
            self.aws._handle_error("get_cost_by_account", e)
    
    def get_cost_by_region(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                          granularity: str = 'MONTHLY') -> Dict[str, Any]:
        """
        Get cost data grouped by region.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
            end_date: End date in YYYY-MM-DD format (default: today)
            granularity: Time granularity (DAILY, MONTHLY, or HOURLY)
            
        Returns:
            Cost data grouped by region
        """
        try:
            # Group by region
            group_by = [
                {
                    'Type': 'DIMENSION',
                    'Key': 'REGION'
                }
            ]
            
            return self.get_cost_and_usage(
                start_date=start_date,
                end_date=end_date,
                granularity=granularity,
                metrics=["BlendedCost"],
                group_by=group_by
            )
        except Exception as e:
            self.aws._handle_error("get_cost_by_region", e)
    
    def get_cost_forecast(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                         granularity: str = 'MONTHLY', metric: str = 'BLENDED_COST') -> Dict[str, Any]:
        """
        Get cost forecast.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (default: today)
            end_date: End date in YYYY-MM-DD format (default: 30 days from now)
            granularity: Time granularity (DAILY, MONTHLY, or HOURLY)
            metric: Cost metric to forecast (BLENDED_COST, UNBLENDED_COST, or AMORTIZED_COST)
            
        Returns:
            Cost forecast data
        """
        try:
            client = self._get_client()
            
            # Set default dates if not provided
            if not start_date:
                start_date = datetime.now().strftime('%Y-%m-%d')
            if not end_date:
                end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            
            response = client.get_cost_forecast(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity=granularity,
                Metric=metric
            )
            
            return response
        except Exception as e:
            self.aws._handle_error("get_cost_forecast", e)
    
    def get_cost_categories(self, max_results: int = 100) -> Dict[str, Any]:
        """
        Get cost categories.
        
        Args:
            max_results: Maximum number of results to return
            
        Returns:
            Cost categories
        """
        try:
            client = self._get_client()
            
            response = client.list_cost_category_definitions(
                MaxResults=min(max_results, 100)
            )
            
            return response
        except Exception as e:
            self.aws._handle_error("get_cost_categories", e)
    
    def get_cost_anomalies(self, start_date: Optional[str] = None, end_date: Optional[str] = None,
                          max_results: int = 100) -> Dict[str, Any]:
        """
        Get cost anomalies.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
            end_date: End date in YYYY-MM-DD format (default: today)
            max_results: Maximum number of results to return
            
        Returns:
            Cost anomalies
        """
        try:
            client = self._get_client()
            
            # Set default dates if not provided
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            response = client.get_anomalies(
                DateInterval={
                    'StartDate': start_date,
                    'EndDate': end_date
                },
                MaxResults=min(max_results, 100)
            )
            
            return response
        except Exception as e:
            self.aws._handle_error("get_cost_anomalies", e)