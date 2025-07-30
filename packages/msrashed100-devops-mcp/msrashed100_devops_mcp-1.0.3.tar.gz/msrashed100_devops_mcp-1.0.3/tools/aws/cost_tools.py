"""
AWS Cost Explorer tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.base_tools import AWSBaseTools
from utils.logging import setup_logger


class AWSCostTools(AWSBaseTools):
    """Tools for AWS Cost Explorer operations."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS Cost Explorer tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.cost")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register AWS Cost Explorer tools with the MCP server."""
        
        @self.mcp.tool()
        def get_aws_cost_and_usage(start_date: str = None, end_date: str = None,
                                 granularity: str = "MONTHLY", metrics: str = None) -> str:
            """
            Get AWS cost and usage data.
            
            This tool retrieves cost and usage data from AWS Cost Explorer.
            
            Args:
                start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
                end_date: End date in YYYY-MM-DD format (default: today)
                granularity: Time granularity (DAILY, MONTHLY, or HOURLY) (default: MONTHLY)
                metrics: Comma-separated list of cost metrics to return (default: "BlendedCost,UnblendedCost,UsageQuantity")
                
            Returns:
                Cost and usage data in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate granularity
            if granularity not in ["DAILY", "MONTHLY", "HOURLY"]:
                return self._format_error("Invalid granularity. Must be one of: DAILY, MONTHLY, HOURLY")
            
            # Parse metrics
            metrics_list = None
            if metrics:
                metrics_list = [m.strip() for m in metrics.split(",")]
            
            try:
                cost_data = self.aws_service.cost.get_cost_and_usage(
                    start_date=start_date,
                    end_date=end_date,
                    granularity=granularity,
                    metrics=metrics_list
                )
                return self._format_response(cost_data)
            except Exception as e:
                self.logger.error(f"Error getting AWS cost and usage: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_aws_cost_by_service(start_date: str = None, end_date: str = None,
                                  granularity: str = "MONTHLY") -> str:
            """
            Get AWS cost data grouped by service.
            
            This tool retrieves cost data grouped by service from AWS Cost Explorer.
            
            Args:
                start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
                end_date: End date in YYYY-MM-DD format (default: today)
                granularity: Time granularity (DAILY, MONTHLY, or HOURLY) (default: MONTHLY)
                
            Returns:
                Cost data grouped by service in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate granularity
            if granularity not in ["DAILY", "MONTHLY", "HOURLY"]:
                return self._format_error("Invalid granularity. Must be one of: DAILY, MONTHLY, HOURLY")
            
            try:
                cost_data = self.aws_service.cost.get_cost_by_service(
                    start_date=start_date,
                    end_date=end_date,
                    granularity=granularity
                )
                return self._format_response(cost_data)
            except Exception as e:
                self.logger.error(f"Error getting AWS cost by service: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_aws_cost_by_account(start_date: str = None, end_date: str = None,
                                  granularity: str = "MONTHLY") -> str:
            """
            Get AWS cost data grouped by account.
            
            This tool retrieves cost data grouped by account from AWS Cost Explorer.
            
            Args:
                start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
                end_date: End date in YYYY-MM-DD format (default: today)
                granularity: Time granularity (DAILY, MONTHLY, or HOURLY) (default: MONTHLY)
                
            Returns:
                Cost data grouped by account in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate granularity
            if granularity not in ["DAILY", "MONTHLY", "HOURLY"]:
                return self._format_error("Invalid granularity. Must be one of: DAILY, MONTHLY, HOURLY")
            
            try:
                cost_data = self.aws_service.cost.get_cost_by_account(
                    start_date=start_date,
                    end_date=end_date,
                    granularity=granularity
                )
                return self._format_response(cost_data)
            except Exception as e:
                self.logger.error(f"Error getting AWS cost by account: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_aws_cost_by_region(start_date: str = None, end_date: str = None,
                                 granularity: str = "MONTHLY") -> str:
            """
            Get AWS cost data grouped by region.
            
            This tool retrieves cost data grouped by region from AWS Cost Explorer.
            
            Args:
                start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
                end_date: End date in YYYY-MM-DD format (default: today)
                granularity: Time granularity (DAILY, MONTHLY, or HOURLY) (default: MONTHLY)
                
            Returns:
                Cost data grouped by region in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate granularity
            if granularity not in ["DAILY", "MONTHLY", "HOURLY"]:
                return self._format_error("Invalid granularity. Must be one of: DAILY, MONTHLY, HOURLY")
            
            try:
                cost_data = self.aws_service.cost.get_cost_by_region(
                    start_date=start_date,
                    end_date=end_date,
                    granularity=granularity
                )
                return self._format_response(cost_data)
            except Exception as e:
                self.logger.error(f"Error getting AWS cost by region: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_aws_cost_forecast(start_date: str = None, end_date: str = None,
                                granularity: str = "MONTHLY", metric: str = "BLENDED_COST") -> str:
            """
            Get AWS cost forecast.
            
            This tool retrieves cost forecast data from AWS Cost Explorer.
            
            Args:
                start_date: Start date in YYYY-MM-DD format (default: today)
                end_date: End date in YYYY-MM-DD format (default: 30 days from now)
                granularity: Time granularity (DAILY, MONTHLY, or HOURLY) (default: MONTHLY)
                metric: Cost metric to forecast (BLENDED_COST, UNBLENDED_COST, or AMORTIZED_COST) (default: BLENDED_COST)
                
            Returns:
                Cost forecast data in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate granularity
            if granularity not in ["DAILY", "MONTHLY", "HOURLY"]:
                return self._format_error("Invalid granularity. Must be one of: DAILY, MONTHLY, HOURLY")
            
            # Validate metric
            if metric not in ["BLENDED_COST", "UNBLENDED_COST", "AMORTIZED_COST"]:
                return self._format_error("Invalid metric. Must be one of: BLENDED_COST, UNBLENDED_COST, AMORTIZED_COST")
            
            try:
                forecast_data = self.aws_service.cost.get_cost_forecast(
                    start_date=start_date,
                    end_date=end_date,
                    granularity=granularity,
                    metric=metric
                )
                return self._format_response(forecast_data)
            except Exception as e:
                self.logger.error(f"Error getting AWS cost forecast: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_aws_cost_anomalies(start_date: str = None, end_date: str = None,
                                 max_results: int = 100) -> str:
            """
            Get AWS cost anomalies.
            
            This tool retrieves cost anomalies from AWS Cost Explorer.
            
            Args:
                start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
                end_date: End date in YYYY-MM-DD format (default: today)
                max_results: Maximum number of results to return (default: 100, max: 100)
                
            Returns:
                Cost anomalies in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 100)
            
            try:
                anomalies = self.aws_service.cost.get_cost_anomalies(
                    start_date=start_date,
                    end_date=end_date,
                    max_results=max_results
                )
                return self._format_response(anomalies)
            except Exception as e:
                self.logger.error(f"Error getting AWS cost anomalies: {e}")
                return self._format_error(str(e))