"""
AWS tools for the DevOps MCP Server.
"""
from typing import Optional
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.ecs_tools import AWSECSTools
from tools.aws.s3_tools import AWSS3Tools
from tools.aws.elb_tools import AWSELBTools
from tools.aws.vpc_tools import AWSVPCTools
from tools.aws.cost_tools import AWSCostTools
from tools.aws.cloudfront_tools import AWSCloudFrontTools
from tools.aws.iam_tools import AWSIAMTools
from tools.aws.lambda_tools import AWSLambdaTools
from tools.aws.rds_tools import AWSRDSTools
from tools.aws.elasticache_tools import AWSElastiCacheTools
from tools.aws.ssm_tools import AWSSSMTools
from tools.aws.cloudwatch_tools import AWSCloudWatchTools
from tools.aws.ec2_tools import AWSEC2Tools
from tools.aws.route53_tools import AWSRoute53Tools
from tools.aws.codepipeline_tools import AWSCodePipelineTools
from tools.aws.codebuild_tools import AWSCodeBuildTools
from tools.aws.codecommit_tools import AWSCodeCommitTools
from utils.logging import setup_logger


class AWSTools:
    """Tools for interacting with AWS."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        self.mcp = mcp
        self.aws_service = aws_service or AWSServiceManager()
        self.logger = setup_logger("devops_mcp_server.tools.aws")
        
        # Initialize specialized tools
        self.ecs_tools = AWSECSTools(mcp, self.aws_service)
        self.s3_tools = AWSS3Tools(mcp, self.aws_service)
        self.elb_tools = AWSELBTools(mcp, self.aws_service)
        self.vpc_tools = AWSVPCTools(mcp, self.aws_service)
        self.cost_tools = AWSCostTools(mcp, self.aws_service)
        self.cloudfront_tools = AWSCloudFrontTools(mcp, self.aws_service)
        self.iam_tools = AWSIAMTools(mcp, self.aws_service)
        self.lambda_tools = AWSLambdaTools(mcp, self.aws_service)
        self.rds_tools = AWSRDSTools(mcp, self.aws_service)
        self.elasticache_tools = AWSElastiCacheTools(mcp, self.aws_service)
        self.ssm_tools = AWSSSMTools(mcp, self.aws_service)
        self.cloudwatch_tools = AWSCloudWatchTools(mcp, self.aws_service)
        self.ec2_tools = AWSEC2Tools(mcp, self.aws_service)
        self.route53_tools = AWSRoute53Tools(mcp, self.aws_service)
        self.codepipeline_tools = AWSCodePipelineTools(mcp, self.aws_service)
        self.codebuild_tools = AWSCodeBuildTools(mcp, self.aws_service)
        self.codecommit_tools = AWSCodeCommitTools(mcp, self.aws_service)
        
        self.logger.info("AWS tools initialized successfully")