"""
Loki query client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
import datetime
import re # For parsing relative time

from services.loki.client import LokiService
from utils.logging import setup_logger


class LokiQueryClient:
    """Client for Loki query operations."""

    def __init__(self, loki_service: LokiService):
        """
        Initialize the Loki query client.

        Args:
            loki_service: An instance of LokiService.
        """
        self.service = loki_service
        self.logger = setup_logger(f"devops_mcp_server.services.loki.query_client")
        self.logger.info("LokiQueryClient initialized")

    def _parse_time_param(self, time_str: str) -> str:
        """
        Parse a time string (which can be relative like "1h", "5m", or "now",
        Unix timestamp, or RFC3339) into an RFC3339 formatted "YYYY-MM-DDTHH:MM:SSZ" string.
        """
        if not time_str:
            self.logger.warning("Received empty time string for parsing.")
            return None 

        time_str_input = str(time_str) 
        time_str_lower = time_str_input.lower()
        now_utc = datetime.datetime.now(datetime.timezone.utc)

        if time_str_lower == "now":
            return now_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

        match = re.match(r"(\d+)([smhdw])", time_str_lower)
        if match:
            value = int(match.group(1))
            unit = match.group(2)
            delta = None
            if unit == 's':
                delta = datetime.timedelta(seconds=value)
            elif unit == 'm':
                delta = datetime.timedelta(minutes=value)
            elif unit == 'h':
                delta = datetime.timedelta(hours=value)
            elif unit == 'd':
                delta = datetime.timedelta(days=value)
            elif unit == 'w':
                delta = datetime.timedelta(weeks=value)
            
            if delta:
                return (now_utc - delta).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        try:
            ts_seconds = float(time_str_input)
            dt_from_ts = datetime.datetime.fromtimestamp(ts_seconds, datetime.timezone.utc)
            return dt_from_ts.strftime('%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            pass

        try:
            time_str_upper = time_str_input.upper()
            if 'Z' in time_str_upper:
                parts_after_z = time_str_upper.split('Z', 1)[1]
                if parts_after_z and (parts_after_z.startswith('+') or parts_after_z.startswith('-')):
                    raise ValueError("Timestamp contains 'Z' and a subsequent offset, which is invalid.")
            
            # Handle Z correctly for fromisoformat by replacing it with +00:00 if it's at the end.
            # Otherwise, fromisoformat handles offsets like +0X:XX correctly.
            if time_str_input.endswith('Z'):
                 dt_obj = datetime.datetime.fromisoformat(time_str_input[:-1] + '+00:00')
            else:
                 dt_obj = datetime.datetime.fromisoformat(time_str_input)

            if dt_obj.tzinfo is None or dt_obj.tzinfo.utcoffset(dt_obj) is None:
                dt_obj_utc = dt_obj.replace(tzinfo=datetime.timezone.utc)
            else:
                dt_obj_utc = dt_obj.astimezone(datetime.timezone.utc)
            
            return dt_obj_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
        except ValueError as e_iso:
            self.logger.warning(f"Could not parse time string '{time_str_input}' as relative, Unix timestamp, or RFC3339: {e_iso}. Using as is.")
            return time_str_input

    def query_range(self, query: str, start: str, end: str, limit: Optional[int] = 100,
                    direction: Optional[str] = "backward", step: Optional[str] = None,
                    interval: Optional[str] = None) -> Dict[str, Any]: # interval is not standard Loki
        """
        Query logs within a time range.

        Args:
            query: LogQL query string.
            start: Start timestamp (Unix epoch ns, RFC3339, or relative time like "1h").
            end: End timestamp (Unix epoch ns, RFC3339, or relative time like "now").
            limit: Maximum number of log lines to return.
            direction: 'forward' or 'backward'. Determines the search direction.
            step: Query resolution step width for metric queries.
            interval: Interval for grouping metric queries (Note: not a standard Loki param for query_range).

        Returns:
            The query result from Loki.
        """
        parsed_start = self._parse_time_param(start)
        parsed_end = self._parse_time_param(end)

        if not parsed_start or not parsed_end:
            # Or raise a more specific error if _parse_time_param returns None for invalid inputs
            raise ValueError(f"Invalid start ('{start}') or end ('{end}') time provided.")

        params = {
            "query": query,
            "start": parsed_start,
            "end": parsed_end,
            "limit": limit,
            "direction": direction,
        }
        if step:
            params["step"] = step
        # if interval: # Not standard for Loki query_range, consider removing or conditional logic
        #     params["interval"] = interval 
        
        self.logger.debug(f"Executing Loki query_range with processed params: {params}")
        response = self.service._request("GET", "/loki/api/v1/query_range", params=params)
        return response.json()

    def get_labels(self, start: Optional[str] = None, end: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a list of all label names.

        Args:
            start: Optional start timestamp (Unix epoch ns, RFC3339, or relative time) to filter labels.
            end: Optional end timestamp (Unix epoch ns, RFC3339, or relative time) to filter labels.

        Returns:
            A list of label names.
        """
        params = {}
        if start:
            params["start"] = self._parse_time_param(start)
        if end:
            params["end"] = self._parse_time_param(end)
            
        self.logger.debug(f"Executing Loki get_labels with params: {params}")
        response = self.service._request("GET", "/loki/api/v1/labels", params=params)
        return response.json()

    def get_label_values(self, label_name: str, start: Optional[str] = None, end: Optional[str] = None) -> Dict[str, Any]:
        """
        Get values for a specific label name.

        Args:
            label_name: The name of the label.
            start: Optional start timestamp (Unix epoch ns, RFC3339, or relative time) to filter label values.
            end: Optional end timestamp (Unix epoch ns, RFC3339, or relative time) to filter label values.

        Returns:
            A list of values for the given label.
        """
        params = {}
        if start:
            params["start"] = self._parse_time_param(start)
        if end:
            params["end"] = self._parse_time_param(end)
            
        endpoint = f"/loki/api/v1/label/{label_name}/values"
        self.logger.debug(f"Executing Loki get_label_values for '{label_name}' with params: {params}")
        response = self.service._request("GET", endpoint, params=params)
        return response.json()