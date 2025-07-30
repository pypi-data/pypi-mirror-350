"""
AWS Route 53 Client.
"""
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError

from utils.logging import setup_logger
from services.aws.client import AWSService

class AWSRoute53Client:
    """Client for interacting with AWS Route 53."""

    def __init__(self, base_service: AWSService):
        """
        Initialize Route 53 client.

        Args:
            base_service: The base AWSService instance.
        """
        self.service_name = "route53"
        self.client = base_service.get_client(self.service_name)
        self.logger = setup_logger(f"devops_mcp_server.services.aws.{self.service_name}")

    def list_hosted_zones(self, max_items: int = 100) -> List[Dict[str, Any]]:
        """
        List all public and private hosted zones.

        Args:
            max_items: Maximum number of hosted zones to return.

        Returns:
            List of hosted zones.
        """
        self.logger.info(f"Listing Route 53 hosted zones with max_items: {max_items}")
        try:
            hosted_zones = []
            paginator = self.client.get_paginator('list_hosted_zones')
            page_iterator = paginator.paginate(MaxItems=str(max_items)) # MaxItems is a string for this API
            for page in page_iterator:
                hosted_zones.extend(page.get("HostedZones", []))
            self.logger.info(f"Successfully listed {len(hosted_zones)} Route 53 hosted zones.")
            return hosted_zones
        except ClientError as e:
            self.logger.error(f"Error listing Route 53 hosted zones: {e}")
            raise

    def list_resource_record_sets(self, hosted_zone_id: str, start_record_name: Optional[str] = None, start_record_type: Optional[str] = None, max_items: int = 100) -> List[Dict[str, Any]]:
        """
        List DNS records within a specific hosted zone.

        Args:
            hosted_zone_id: The ID of the hosted zone.
            start_record_name: The first record name in the lexicographical order to return.
            start_record_type: The first record type in the lexicographical order to return.
            max_items: Maximum number of record sets to return.

        Returns:
            List of resource record sets.
        """
        self.logger.info(f"Listing resource record sets for hosted zone: {hosted_zone_id}")
        try:
            params = {'HostedZoneId': hosted_zone_id, 'MaxItems': str(max_items)}
            if start_record_name:
                params['StartRecordName'] = start_record_name
            if start_record_type:
                params['StartRecordType'] = start_record_type
            
            record_sets = []
            paginator = self.client.get_paginator('list_resource_record_sets')
            page_iterator = paginator.paginate(**params)
            for page in page_iterator:
                record_sets.extend(page.get("ResourceRecordSets", []))
            
            self.logger.info(f"Successfully listed {len(record_sets)} resource record sets for hosted zone: {hosted_zone_id}")
            return record_sets
        except ClientError as e:
            self.logger.error(f"Error listing resource record sets for hosted zone {hosted_zone_id}: {e}")
            raise

    def get_health_check_status(self, health_check_id: str) -> Dict[str, Any]:
        """
        Get the status of a Route 53 health check.

        Args:
            health_check_id: The ID of the health check.

        Returns:
            Dictionary containing the health check status.
        """
        self.logger.info(f"Getting status for Route 53 health check: {health_check_id}")
        try:
            response = self.client.get_health_check_status(HealthCheckId=health_check_id)
            self.logger.info(f"Successfully retrieved status for health check: {health_check_id}")
            # The response directly contains HealthCheckObservations
            return {"HealthCheckObservations": response.get("HealthCheckObservations", [])}
        except ClientError as e:
            self.logger.error(f"Error getting status for Route 53 health check {health_check_id}: {e}")
            raise