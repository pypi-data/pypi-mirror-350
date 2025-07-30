"""
AWS CloudWatch Client.
"""
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError

from utils.logging import setup_logger


class CloudWatchClient:
    """Client for interacting with AWS CloudWatch."""

    def __init__(self, region_name: str = "us-east-1"):
        """
        Initialize CloudWatch client.

        Args:
            region_name: AWS region name
        """
        self.client = boto3.client("cloudwatch", region_name=region_name) # Changed from "logs" to "cloudwatch"
        self.logger = setup_logger("devops_mcp_server.services.aws.cloudwatch")

    def list_log_groups(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        List CloudWatch log groups.

        Args:
            limit: Maximum number of log groups to return

        Returns:
            List of log groups
        """
        try:
            log_groups = []
            paginator = self.client.get_paginator('describe_log_groups')
            page_iterator = paginator.paginate(PaginationConfig={'MaxItems': limit})
            for page in page_iterator:
                log_groups.extend(page.get("logGroups", []))
            self.logger.info(f"Successfully listed {len(log_groups)} CloudWatch log groups.")
            return log_groups
        except ClientError as e:
            self.logger.error(f"Error listing CloudWatch log groups: {e}")
            raise

    def list_alarms(self, state_value: Optional[str] = None, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        List CloudWatch alarms.

        Args:
            state_value: Filter by alarm state (e.g., ALARM, INSUFFICIENT_DATA, OK).
            max_results: Maximum number of alarms to return.

        Returns:
            List of CloudWatch alarms.
        """
        self.logger.info(f"Listing CloudWatch alarms with state: {state_value}, max_results: {max_results}")
        try:
            alarms = []
            paginator = self.client.get_paginator('describe_alarms')
            paginate_params = {'MaxRecords': max_results}
            if state_value:
                paginate_params['StateValue'] = state_value
            
            page_iterator = paginator.paginate(**paginate_params)
            for page in page_iterator:
                alarms.extend(page.get("MetricAlarms", []))
                alarms.extend(page.get("CompositeAlarms", [])) # Include composite alarms
            self.logger.info(f"Successfully listed {len(alarms)} CloudWatch alarms.")
            return alarms
        except ClientError as e:
            self.logger.error(f"Error listing CloudWatch alarms: {e}")
            raise

    def get_alarm_history(self, alarm_name: str, start_date: Optional[str] = None, end_date: Optional[str] = None, max_records: int = 50) -> List[Dict[str, Any]]:
        """
        Get the history for a specific CloudWatch alarm.

        Args:
            alarm_name: The name of the alarm.
            start_date: The start date for the history (ISO 8601 format).
            end_date: The end date for the history (ISO 8601 format).
            max_records: Maximum number of history items to return.

        Returns:
            List of alarm history items.
        """
        self.logger.info(f"Getting history for CloudWatch alarm: {alarm_name}")
        try:
            params = {'AlarmName': alarm_name, 'MaxRecords': max_records, 'ScanBy': 'TimestampDescending'}
            if start_date:
                params['StartDate'] = start_date
            if end_date:
                params['EndDate'] = end_date
            
            history_items = []
            paginator = self.client.get_paginator('describe_alarm_history')
            page_iterator = paginator.paginate(**params)
            for page in page_iterator:
                history_items.extend(page.get("AlarmHistoryItems", []))
            
            self.logger.info(f"Successfully retrieved {len(history_items)} history items for alarm: {alarm_name}")
            return history_items
        except ClientError as e:
            self.logger.error(f"Error getting history for CloudWatch alarm {alarm_name}: {e}")
            raise

    def get_metric_data(self, metric_data_queries: List[Dict[str, Any]], start_time: str, end_time: str, scan_by: str = 'TimestampDescending', max_datapoints: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetch specific metric data points over a time range.

        Args:
            metric_data_queries: A list of metric data query structures.
                                 See: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_metric_data.html#get-metric-data
            start_time: The start time for the data (ISO 8601 format or datetime object).
            end_time: The end time for the data (ISO 8601 format or datetime object).
            scan_by: The order to scan by ('TimestampDescending' or 'TimestampAscending').
            max_datapoints: The maximum number of data points to return.

        Returns:
            Dictionary containing metric data results.
        """
        self.logger.info(f"Fetching CloudWatch metric data.")
        try:
            params = {
                'MetricDataQueries': metric_data_queries,
                'StartTime': start_time,
                'EndTime': end_time,
                'ScanBy': scan_by
            }
            if max_datapoints:
                params['MaxDatapoints'] = max_datapoints
            
            response = self.client.get_metric_data(**params)
            self.logger.info("Successfully fetched CloudWatch metric data.")
            return response
        except ClientError as e:
            self.logger.error(f"Error fetching CloudWatch metric data: {e}")
            raise

    def describe_dashboards(self, dashboard_name_prefix: Optional[str] = None, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        List available CloudWatch dashboards.

        Args:
            dashboard_name_prefix: Optional prefix to filter dashboards by name.
            max_results: Maximum number of dashboards to return.

        Returns:
            List of dashboard entries.
        """
        self.logger.info(f"Describing CloudWatch dashboards with prefix: {dashboard_name_prefix}")
        try:
            dashboards = []
            paginator = self.client.get_paginator('list_dashboards')
            pagination_config = {'MaxItems': max_results}
            
            paginate_params = {}
            if dashboard_name_prefix:
                paginate_params['DashboardNamePrefix'] = dashboard_name_prefix
            
            page_iterator = paginator.paginate(**paginate_params, PaginationConfig=pagination_config)
            for page in page_iterator:
                dashboards.extend(page.get("DashboardEntries", []))
            self.logger.info(f"Successfully described {len(dashboards)} CloudWatch dashboards.")
            return dashboards
        except ClientError as e:
            self.logger.error(f"Error describing CloudWatch dashboards: {e}")
            raise

    def get_dashboard(self, dashboard_name: str) -> Dict[str, Any]:
        """
        Get the JSON definition of a specific CloudWatch dashboard.

        Args:
            dashboard_name: The name of the dashboard.

        Returns:
            Dictionary containing the dashboard body (JSON string) and ARN.
        """
        self.logger.info(f"Getting CloudWatch dashboard: {dashboard_name}")
        try:
            response = self.client.get_dashboard(DashboardName=dashboard_name)
            self.logger.info(f"Successfully retrieved dashboard: {dashboard_name}")
            return {
                "DashboardBody": response.get("DashboardBody"),
                "DashboardArn": response.get("DashboardArn"),
                "DashboardName": response.get("DashboardName")
            }
        except ClientError as e:
            self.logger.error(f"Error getting CloudWatch dashboard {dashboard_name}: {e}")
            raise