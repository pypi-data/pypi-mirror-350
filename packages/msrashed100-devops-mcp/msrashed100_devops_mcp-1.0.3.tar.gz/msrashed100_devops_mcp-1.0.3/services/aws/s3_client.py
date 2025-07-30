"""
AWS S3 client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List, BinaryIO
from botocore.exceptions import ClientError

from services.aws.client import AWSService


class AWSS3Client:
    """Client for AWS S3 operations."""
    
    def __init__(self, aws_service: AWSService):
        """
        Initialize the AWS S3 client.
        
        Args:
            aws_service: The base AWS service
        """
        self.aws = aws_service
        self.logger = aws_service.logger
        self.client = None
        self.resource = None
    
    def _get_client(self):
        """Get the S3 client."""
        if self.client is None:
            self.client = self.aws.get_client('s3')
        return self.client
    
    def _get_resource(self):
        """Get the S3 resource."""
        if self.resource is None:
            self.resource = self.aws.get_resource('s3')
        return self.resource
    
    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        List S3 buckets.
        
        Returns:
            List of S3 buckets
        """
        try:
            client = self._get_client()
            
            response = client.list_buckets()
            buckets = response.get('Buckets', [])
            
            return buckets
        except Exception as e:
            self.aws._handle_error("list_buckets", e)
    
    def get_bucket(self, bucket: str) -> Dict[str, Any]:
        """
        Get details of an S3 bucket.
        
        Args:
            bucket: Bucket name
            
        Returns:
            Bucket details
        """
        try:
            client = self._get_client()
            
            # Check if bucket exists
            client.head_bucket(Bucket=bucket)
            
            # Get bucket location
            location_response = client.get_bucket_location(Bucket=bucket)
            location = location_response.get('LocationConstraint', 'us-east-1')
            
            # Get bucket policy
            try:
                policy_response = client.get_bucket_policy(Bucket=bucket)
                policy = policy_response.get('Policy')
            except Exception:
                policy = None
            
            # Get bucket versioning
            try:
                versioning_response = client.get_bucket_versioning(Bucket=bucket)
                versioning = versioning_response.get('Status', 'Disabled')
            except Exception:
                versioning = 'Disabled'
            
            # Get bucket encryption
            try:
                encryption_response = client.get_bucket_encryption(Bucket=bucket)
                encryption = encryption_response.get('ServerSideEncryptionConfiguration', {})
            except Exception:
                encryption = {}
            
            # Combine all details
            bucket_details = {
                'Name': bucket,
                'Location': location,
                'Policy': policy,
                'Versioning': versioning,
                'Encryption': encryption
            }
            
            return bucket_details
        except Exception as e:
            self.aws._handle_error(f"get_bucket({bucket})", e)
    
    def list_objects(self, bucket: str, prefix: Optional[str] = None, max_keys: int = 1000) -> Dict[str, Any]:
        """
        List objects in an S3 bucket.
        
        Args:
            bucket: Bucket name
            prefix: Object key prefix (optional)
            max_keys: Maximum number of keys to return
            
        Returns:
            List of S3 objects
        """
        try:
            client = self._get_client()
            
            params = {
                'Bucket': bucket,
                'MaxKeys': min(max_keys, 1000)
            }
            
            if prefix:
                params['Prefix'] = prefix
            
            response = client.list_objects_v2(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error(f"list_objects({bucket})", e)
    
    def get_object(self, bucket: str, key: str) -> Dict[str, Any]:
        """
        Get metadata of an S3 object.
        
        Args:
            bucket: Bucket name
            key: Object key
            
        Returns:
            Object metadata
        """
        try:
            client = self._get_client()
            
            response = client.head_object(Bucket=bucket, Key=key)
            
            # Add bucket and key to response
            response['Bucket'] = bucket
            response['Key'] = key
            
            return response
        except Exception as e:
            self.aws._handle_error(f"get_object({bucket}, {key})", e)
    
    def get_object_url(self, bucket: str, key: str, expires_in: int = 3600) -> str:
        """
        Generate a presigned URL for an S3 object.
        
        Args:
            bucket: Bucket name
            key: Object key
            expires_in: URL expiration time in seconds
            
        Returns:
            Presigned URL
        """
        try:
            client = self._get_client()
            
            url = client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=expires_in
            )
            
            return url
        except Exception as e:
            self.aws._handle_error(f"get_object_url({bucket}, {key})", e)
    
    def get_bucket_size(self, bucket: str, prefix: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the size of an S3 bucket.
        
        Args:
            bucket: Bucket name
            prefix: Object key prefix (optional)
            
        Returns:
            Bucket size information
        """
        try:
            resource = self._get_resource()
            
            # Get bucket
            s3_bucket = resource.Bucket(bucket)
            
            # Initialize counters
            total_size = 0
            total_objects = 0
            
            # Iterate through objects
            for obj in s3_bucket.objects.filter(Prefix=prefix or ''):
                total_size += obj.size
                total_objects += 1
            
            # Format size
            size_mb = total_size / (1024 * 1024)
            size_gb = size_mb / 1024
            
            return {
                'Bucket': bucket,
                'Prefix': prefix or '',
                'TotalObjects': total_objects,
                'TotalSizeBytes': total_size,
                'TotalSizeMB': round(size_mb, 2),
                'TotalSizeGB': round(size_gb, 2)
            }
        except Exception as e:
            self.aws._handle_error(f"get_bucket_size({bucket})", e)

    def get_bucket_policy(self, bucket_name: str) -> Dict[str, Any]:
        """
        Retrieve the policy for a specified S3 bucket.

        Args:
            bucket_name: The name of the S3 bucket.

        Returns:
            A dictionary containing the bucket policy.
        """
        self.logger.info(f"Getting policy for S3 bucket: {bucket_name}")
        try:
            client = self._get_client()
            response = client.get_bucket_policy(Bucket=bucket_name)
            policy = response.get('Policy', '{}') # Return empty JSON if no policy
            import json
            return json.loads(policy)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                self.logger.info(f"No policy found for bucket: {bucket_name}")
                return {} # Return empty dict if no policy exists
            self.logger.error(f"Error getting S3 bucket policy for {bucket_name}: {e}")
            raise

    def get_bucket_cors(self, bucket_name: str) -> List[Dict[str, Any]]:
        """
        Retrieve the CORS (Cross-Origin Resource Sharing) configuration for a bucket.

        Args:
            bucket_name: The name of the S3 bucket.

        Returns:
            A list of CORS rules.
        """
        self.logger.info(f"Getting CORS configuration for S3 bucket: {bucket_name}")
        try:
            client = self._get_client()
            response = client.get_bucket_cors(Bucket=bucket_name)
            cors_rules = response.get('CORSRules', [])
            return cors_rules
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchCORSConfiguration':
                self.logger.info(f"No CORS configuration found for bucket: {bucket_name}")
                return [] # Return empty list if no CORS config
            self.logger.error(f"Error getting S3 bucket CORS for {bucket_name}: {e}")
            raise

    def get_bucket_versioning(self, bucket_name: str) -> Dict[str, str]:
        """
        Check the versioning status of a bucket.

        Args:
            bucket_name: The name of the S3 bucket.

        Returns:
            A dictionary containing the versioning status ('Enabled', 'Suspended', or 'Disabled').
        """
        self.logger.info(f"Getting versioning status for S3 bucket: {bucket_name}")
        try:
            client = self._get_client()
            response = client.get_bucket_versioning(Bucket=bucket_name)
            status = response.get('Status', 'Disabled') # Default to Disabled if not present
            mfa_delete = response.get('MFADelete', 'Disabled') # Default to Disabled
            return {"Status": status, "MFADelete": mfa_delete}
        except ClientError as e:
            self.logger.error(f"Error getting S3 bucket versioning for {bucket_name}: {e}")
            raise

    def get_object_acl(self, bucket_name: str, object_key: str) -> Dict[str, Any]:
        """
        Get the Access Control List (ACL) for a specific S3 object.

        Args:
            bucket_name: The name of the S3 bucket.
            object_key: The key of the S3 object.

        Returns:
            A dictionary containing the object's ACL information.
        """
        self.logger.info(f"Getting ACL for S3 object: s3://{bucket_name}/{object_key}")
        try:
            client = self._get_client()
            response = client.get_object_acl(Bucket=bucket_name, Key=object_key)
            return {
                "Owner": response.get("Owner"),
                "Grants": response.get("Grants")
            }
        except ClientError as e:
            self.logger.error(f"Error getting S3 object ACL for s3://{bucket_name}/{object_key}: {e}")
            raise