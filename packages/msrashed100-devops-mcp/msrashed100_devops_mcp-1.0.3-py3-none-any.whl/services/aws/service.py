"""
AWS service manager for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional

from services.aws.client import AWSService
from services.aws.ecs_client import AWSECSClient
from services.aws.s3_client import AWSS3Client
from services.aws.elb_client import AWSELBClient
from services.aws.vpc_client import AWSVPCClient
from services.aws.cost_client import AWSCostClient
from services.aws.cloudfront_client import AWSCloudFrontClient
from services.aws.iam_client import AWSIAMClient
from services.aws.lambda_client import AWSLambdaClient
from services.aws.rds_client import AWSRDSClient
from services.aws.elasticache_client import AWSElastiCacheClient
from services.aws.ssm_client import AWSSSMClient
from services.aws.cloudwatch_client import CloudWatchClient
from services.aws.ec2_client import AWSEC2Client
from services.aws.route53_client import AWSRoute53Client
from services.aws.codepipeline_client import AWSCodePipelineClient
from services.aws.codebuild_client import AWSCodeBuildClient
from services.aws.codecommit_client import AWSCodeCommitClient


class AWSServiceManager:
    """Manager for all AWS services."""
    
    def __init__(self, region: Optional[str] = None, profile: Optional[str] = None):
        """
        Initialize the AWS service manager.
        
        Args:
            region: AWS region
            profile: AWS profile name
        """
        # Initialize the base service
        self.base_service = AWSService(region, profile)
        
        # Initialize specialized clients
        self.ecs = AWSECSClient(self.base_service)
        self.s3 = AWSS3Client(self.base_service)
        self.elb = AWSELBClient(self.base_service)
        self.vpc = AWSVPCClient(self.base_service)
        self.cost = AWSCostClient(self.base_service)
        self.cloudfront = AWSCloudFrontClient(self.base_service)
        self.iam = AWSIAMClient(self.base_service)
        self.lambda_client = AWSLambdaClient(self.base_service)
        self.rds = AWSRDSClient(self.base_service)
        self.elasticache = AWSElastiCacheClient(self.base_service)
        self.ssm = AWSSSMClient(self.base_service)
        self.cloudwatch = CloudWatchClient(self.base_service.region)
        self.ec2 = AWSEC2Client(self.base_service)
        self.route53 = AWSRoute53Client(self.base_service)
        self.codepipeline = AWSCodePipelineClient(self.base_service)
        self.codebuild = AWSCodeBuildClient(self.base_service)
        self.codecommit = AWSCodeCommitClient(self.base_service)
        
        self.logger = self.base_service.logger
        self.logger.info("AWS service manager initialized")
    
    def is_available(self) -> bool:
        """
        Check if the AWS API is available.
        
        Returns:
            True if the API is available, False otherwise
        """
        return self.base_service.is_available()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the service status.
        
        Returns:
            A dictionary with the service status
        """
        return self.base_service.get_status()