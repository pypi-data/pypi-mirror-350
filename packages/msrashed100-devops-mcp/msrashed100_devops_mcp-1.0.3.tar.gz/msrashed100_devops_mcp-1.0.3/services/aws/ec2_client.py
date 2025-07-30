"""
AWS EC2 Client.
"""
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError

from utils.logging import setup_logger
from services.aws.client import AWSService # Assuming AWSService provides base session/client setup

class AWSEC2Client:
    """Client for interacting with AWS EC2."""

    def __init__(self, base_service: AWSService):
        """
        Initialize EC2 client.

        Args:
            base_service: The base AWSService instance.
        """
        self.service_name = "ec2"
        self.region_name = base_service.region
        self.client = base_service.get_client(self.service_name)
        self.logger = setup_logger(f"devops_mcp_server.services.aws.{self.service_name}")

    def list_instances(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        List EC2 instances.

        Args:
            max_results: Maximum number of instances to return.

        Returns:
            List of EC2 instances.
        """
        self.logger.info(f"Listing EC2 instances with max_results: {max_results}")
        try:
            instances = []
            paginator = self.client.get_paginator('describe_instances')
            page_iterator = paginator.paginate(MaxResults=max_results)
            for page in page_iterator:
                for reservation in page.get("Reservations", []):
                    instances.extend(reservation.get("Instances", []))
            self.logger.info(f"Successfully listed {len(instances)} EC2 instances.")
            return instances
        except ClientError as e:
            self.logger.error(f"Error listing EC2 instances: {e}")
            raise

    def get_instance_details(self, instance_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific EC2 instance.

        Args:
            instance_id: The ID of the EC2 instance.

        Returns:
            Dictionary containing instance details.
        """
        self.logger.info(f"Getting details for EC2 instance: {instance_id}")
        try:
            response = self.client.describe_instances(InstanceIds=[instance_id])
            reservations = response.get("Reservations", [])
            if reservations and reservations[0].get("Instances"):
                instance_details = reservations[0]["Instances"][0]
                self.logger.info(f"Successfully retrieved details for EC2 instance: {instance_id}")
                return instance_details
            else:
                self.logger.warning(f"EC2 instance not found: {instance_id}")
                return {"error": "Instance not found"}
        except ClientError as e:
            self.logger.error(f"Error getting EC2 instance details for {instance_id}: {e}")
            raise