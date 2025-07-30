"""
AWS CloudWatch tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from services.aws.service import AWSServiceManager
from utils.logging import setup_logger


class AWSCloudWatchTools:
    """Tools for interacting with AWS CloudWatch."""

    def __init__(self, mcp: FastMCP, aws_service: AWSServiceManager):
        """
        Initialize AWS CloudWatch tools.

        Args:
            mcp: The MCP server instance.
            aws_service: The AWS service manager instance.
        """
        self.mcp = mcp
        self.aws_service = aws_service
        self.logger = setup_logger("devops_mcp_server.tools.aws.cloudwatch")
        self._register_tools()

    def _register_tools(self) -> None:
        """Register CloudWatch tools with the MCP server."""

        @self.mcp.tool()
        def list_cloudwatch_log_groups(limit: int = 50) -> Dict[str, Any]:
            """
            List CloudWatch log groups.

            Args:
                limit: Maximum number of log groups to return (default: 50, max: 50 for now)
            
            Returns:
                List of log groups in JSON format
            """
            self.logger.info(f"Listing CloudWatch log groups with limit: {limit}")
            try:
                log_groups = self.aws_service.cloudwatch.list_log_groups(limit=limit)
                return {"log_groups": log_groups, "count": len(log_groups)}
            except Exception as e:
                self.logger.error(f"Error listing CloudWatch log groups: {e}")
                # Consider re-raising or returning an error structure
                return {"error": str(e)}

        @self.mcp.tool()
        def list_cloudwatch_alarms(state_value: Optional[str] = None, max_results: int = 50) -> Dict[str, Any]:
            """
            List CloudWatch alarms.

            Args:
                state_value: Filter by alarm state (e.g., ALARM, INSUFFICIENT_DATA, OK).
                max_results: Maximum number of alarms to return (default: 50).
            
            Returns:
                List of CloudWatch alarms in JSON format.
            """
            self.logger.info(f"Listing CloudWatch alarms with state: {state_value}, max_results: {max_results}")
            try:
                alarms = self.aws_service.cloudwatch.list_alarms(state_value=state_value, max_results=max_results)
                return {"alarms": alarms, "count": len(alarms)}
            except Exception as e:
                self.logger.error(f"Error listing CloudWatch alarms: {e}")
                return {"error": str(e)}

        @self.mcp.tool()
        def get_cloudwatch_alarm_history(alarm_name: str, start_date: Optional[str] = None, end_date: Optional[str] = None, max_records: int = 50) -> Dict[str, Any]:
            """
            Get the history for a specific CloudWatch alarm.

            Args:
                alarm_name: The name of the alarm.
                start_date: The start date for the history (ISO 8601 format, optional).
                end_date: The end date for the history (ISO 8601 format, optional).
                max_records: Maximum number of history items to return (default: 50).
            
            Returns:
                List of alarm history items in JSON format.
            """
            self.logger.info(f"Getting history for CloudWatch alarm: {alarm_name}")
            try:
                history = self.aws_service.cloudwatch.get_alarm_history(alarm_name=alarm_name, start_date=start_date, end_date=end_date, max_records=max_records)
                return {"alarm_history": history, "count": len(history)}
            except Exception as e:
                self.logger.error(f"Error getting CloudWatch alarm history for {alarm_name}: {e}")
                return {"error": str(e)}

        @self.mcp.tool()
        def get_cloudwatch_metric_data(metric_data_queries: str, start_time: str, end_time: str, scan_by: str = 'TimestampDescending', max_datapoints: Optional[int] = None) -> Dict[str, Any]: # Type hint for metric_data_queries is str
            """
            Fetch specific metric data points over a time range.
            IMPORTANT: metric_data_queries should be a JSON string representing a list of MetricDataQuery objects.

            Args:
                metric_data_queries: JSON string of a list of metric data query structures.
                                     Example: '[{"Id": "m1", "MetricStat": {"Metric": {"Namespace": "AWS/EC2", "MetricName": "CPUUtilization", "Dimensions": [{"Name": "InstanceId", "Value": "i-12345"}]}, "Period": 300, "Stat": "Average"}, "ReturnData": true}]'
                start_time: The start time for the data (ISO 8601 format or datetime object).
                end_time: The end time for the data (ISO 8601 format or datetime object).
                scan_by: The order to scan by ('TimestampDescending' or 'TimestampAscending', default: TimestampDescending).
                max_datapoints: The maximum number of data points to return (optional).
            
            Returns:
                Dictionary containing metric data results in JSON format.
            """
            import json
            self.logger.info(f"Fetching CloudWatch metric data.")
            try:
                queries = json.loads(metric_data_queries)
                data = self.aws_service.cloudwatch.get_metric_data(
                    metric_data_queries=queries,
                    start_time=start_time,
                    end_time=end_time,
                    scan_by=scan_by,
                    max_datapoints=max_datapoints
                )
                return data
            except json.JSONDecodeError as e:
                self.logger.error(f"Error decoding metric_data_queries JSON: {e}")
                return {"error": f"Invalid JSON in metric_data_queries: {str(e)}"}
            except Exception as e:
                self.logger.error(f"Error fetching CloudWatch metric data: {e}")
                return {"error": str(e)}

        @self.mcp.tool()
        def describe_cloudwatch_dashboards(dashboard_name_prefix: Optional[str] = None, max_results: int = 50) -> Dict[str, Any]:
            """
            List available CloudWatch dashboards.

            Args:
                dashboard_name_prefix: Optional prefix to filter dashboards by name.
                max_results: Maximum number of dashboards to return (default: 50).
            
            Returns:
                List of dashboard entries in JSON format.
            """
            self.logger.info(f"Describing CloudWatch dashboards with prefix: {dashboard_name_prefix}")
            try:
                dashboards = self.aws_service.cloudwatch.describe_dashboards(dashboard_name_prefix=dashboard_name_prefix, max_results=max_results)
                return {"dashboards": dashboards, "count": len(dashboards)}
            except Exception as e:
                self.logger.error(f"Error describing CloudWatch dashboards: {e}")
                return {"error": str(e)}

        @self.mcp.tool()
        def get_cloudwatch_dashboard(dashboard_name: str) -> Dict[str, Any]:
            """
            Get the JSON definition of a specific CloudWatch dashboard.

            Args:
                dashboard_name: The name of the dashboard.
            
            Returns:
                Dictionary containing the dashboard body (JSON string) and ARN.
            """
            self.logger.info(f"Getting CloudWatch dashboard: {dashboard_name}")
            try:
                dashboard_info = self.aws_service.cloudwatch.get_dashboard(dashboard_name=dashboard_name)
                return dashboard_info
            except Exception as e:
                self.logger.error(f"Error getting CloudWatch dashboard {dashboard_name}: {e}")
                return {"error": str(e)}

        self.logger.info("AWS CloudWatch tools registered successfully")