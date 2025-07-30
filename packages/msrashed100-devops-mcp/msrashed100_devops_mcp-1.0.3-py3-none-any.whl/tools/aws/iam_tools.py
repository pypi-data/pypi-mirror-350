"""
AWS IAM tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.base_tools import AWSBaseTools
from utils.logging import setup_logger


class AWSIAMTools(AWSBaseTools):
    """Tools for AWS IAM operations."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS IAM tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.iam")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register AWS IAM tools with the MCP server."""
        
        @self.mcp.tool()
        def list_iam_users(path_prefix: str = None, max_items: int = 100) -> str:
            """
            List IAM users.
            
            This tool lists IAM users in your AWS account.
            
            Args:
                path_prefix: Path prefix for filtering users (optional)
                max_items: Maximum number of items to return (default: 100, max: 100)
                
            Returns:
                List of IAM users in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 100)
            
            try:
                users = self.aws_service.iam.list_users(path_prefix, max_items)
                return self._format_response({"users": users, "count": len(users)})
            except Exception as e:
                self.logger.error(f"Error listing IAM users: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_iam_user(user_name: str = None) -> str:
            """
            Get details of an IAM user.
            
            This tool retrieves details of an IAM user. If no user name is provided,
            it returns details of the current user.
            
            Args:
                user_name: User name (optional)
                
            Returns:
                User details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                user = self.aws_service.iam.get_user(user_name)
                return self._format_response(user)
            except Exception as e:
                self.logger.error(f"Error getting IAM user: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_iam_groups(path_prefix: str = None, max_items: int = 100) -> str:
            """
            List IAM groups.
            
            This tool lists IAM groups in your AWS account.
            
            Args:
                path_prefix: Path prefix for filtering groups (optional)
                max_items: Maximum number of items to return (default: 100, max: 100)
                
            Returns:
                List of IAM groups in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 100)
            
            try:
                groups = self.aws_service.iam.list_groups(path_prefix, max_items)
                return self._format_response({"groups": groups, "count": len(groups)})
            except Exception as e:
                self.logger.error(f"Error listing IAM groups: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_iam_group(group_name: str) -> str:
            """
            Get details of an IAM group.
            
            This tool retrieves details of an IAM group.
            
            Args:
                group_name: Group name
                
            Returns:
                Group details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                group = self.aws_service.iam.get_group(group_name)
                return self._format_response(group)
            except Exception as e:
                self.logger.error(f"Error getting IAM group: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_iam_roles(path_prefix: str = None, max_items: int = 100) -> str:
            """
            List IAM roles.
            
            This tool lists IAM roles in your AWS account.
            
            Args:
                path_prefix: Path prefix for filtering roles (optional)
                max_items: Maximum number of items to return (default: 100, max: 100)
                
            Returns:
                List of IAM roles in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 100)
            
            try:
                roles = self.aws_service.iam.list_roles(path_prefix, max_items)
                return self._format_response({"roles": roles, "count": len(roles)})
            except Exception as e:
                self.logger.error(f"Error listing IAM roles: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_iam_role(role_name: str) -> str:
            """
            Get details of an IAM role.
            
            This tool retrieves details of an IAM role.
            
            Args:
                role_name: Role name
                
            Returns:
                Role details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                role = self.aws_service.iam.get_role(role_name)
                return self._format_response(role)
            except Exception as e:
                self.logger.error(f"Error getting IAM role: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_iam_policies(scope: str = "All", only_attached: bool = False, 
                            path_prefix: str = None, max_items: int = 100) -> str:
            """
            List IAM policies.
            
            This tool lists IAM policies in your AWS account.
            
            Args:
                scope: Policy scope (All, AWS, Local) (default: All)
                only_attached: Only include attached policies (default: False)
                path_prefix: Path prefix for filtering policies (optional)
                max_items: Maximum number of items to return (default: 100, max: 100)
                
            Returns:
                List of IAM policies in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate scope
            if scope not in ["All", "AWS", "Local"]:
                return self._format_error("Invalid scope. Must be one of: All, AWS, Local")
            
            # Validate max_items
            max_items = min(max(1, max_items), 100)
            
            try:
                policies = self.aws_service.iam.list_policies(scope, only_attached, path_prefix, max_items)
                return self._format_response({"policies": policies, "count": len(policies)})
            except Exception as e:
                self.logger.error(f"Error listing IAM policies: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_iam_policy(policy_arn: str) -> str:
            """
            Get details of an IAM policy.
            
            This tool retrieves details of an IAM policy.
            
            Args:
                policy_arn: Policy ARN
                
            Returns:
                Policy details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                policy = self.aws_service.iam.get_policy(policy_arn)
                return self._format_response(policy)
            except Exception as e:
                self.logger.error(f"Error getting IAM policy: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_iam_policy_version(policy_arn: str, version_id: str) -> str:
            """
            Get details of an IAM policy version.
            
            This tool retrieves details of an IAM policy version.
            
            Args:
                policy_arn: Policy ARN
                version_id: Policy version ID
                
            Returns:
                Policy version details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                policy_version = self.aws_service.iam.get_policy_version(policy_arn, version_id)
                return self._format_response(policy_version)
            except Exception as e:
                self.logger.error(f"Error getting IAM policy version: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_user_policies(user_name: str, max_items: int = 100) -> str:
            """
            List inline policies for an IAM user.
            
            This tool lists inline policies for an IAM user.
            
            Args:
                user_name: User name
                max_items: Maximum number of items to return (default: 100, max: 100)
                
            Returns:
                List of policy names in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 100)
            
            try:
                policy_names = self.aws_service.iam.list_user_policies(user_name, max_items)
                return self._format_response({"policyNames": policy_names, "count": len(policy_names)})
            except Exception as e:
                self.logger.error(f"Error listing user policies: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_attached_user_policies(user_name: str, path_prefix: str = None, 
                                      max_items: int = 100) -> str:
            """
            List attached policies for an IAM user.
            
            This tool lists attached policies for an IAM user.
            
            Args:
                user_name: User name
                path_prefix: Path prefix for filtering policies (optional)
                max_items: Maximum number of items to return (default: 100, max: 100)
                
            Returns:
                List of attached policies in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 100)
            
            try:
                attached_policies = self.aws_service.iam.list_attached_user_policies(
                    user_name, path_prefix, max_items
                )
                return self._format_response({"attachedPolicies": attached_policies, "count": len(attached_policies)})
            except Exception as e:
                self.logger.error(f"Error listing attached user policies: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_iam_account_summary() -> str:
            """
            Get a summary of IAM entities in the account.

            This tool provides a summary of IAM entities such as users, groups,
            roles, and policies in your AWS account.

            Returns:
                Account summary in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                summary = self.aws_service.iam.get_account_summary()
                return self._format_response(summary)
            except Exception as e:
                self.logger.error(f"Error getting IAM account summary: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def list_iam_instance_profiles(path_prefix: Optional[str] = None, max_items: int = 100) -> str:
            """
            List IAM instance profiles.

            This tool lists IAM instance profiles in your AWS account.

            Args:
                path_prefix: Path prefix for filtering instance profiles (optional).
                max_items: Maximum number of items to return (default: 100, max: 100).

            Returns:
                List of IAM instance profiles in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            max_items = min(max(1, max_items), 100)
            
            try:
                instance_profiles = self.aws_service.iam.list_instance_profiles(path_prefix, max_items)
                return self._format_response({"instanceProfiles": instance_profiles, "count": len(instance_profiles)})
            except Exception as e:
                self.logger.error(f"Error listing IAM instance profiles: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_iam_instance_profile(instance_profile_name: str) -> str:
            """
            Get details of a specific IAM instance profile.

            Args:
                instance_profile_name: The name of the instance profile.

            Returns:
                Dictionary containing instance profile details in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                instance_profile = self.aws_service.iam.get_instance_profile(instance_profile_name)
                return self._format_response(instance_profile)
            except Exception as e:
                self.logger.error(f"Error getting IAM instance profile {instance_profile_name}: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def list_server_certificates(path_prefix: Optional[str] = None, max_items: int = 100) -> str:
            """
            List imported SSL/TLS server certificates.

            Args:
                path_prefix: Path prefix for filtering server certificates (optional).
                max_items: Maximum number of items to return (default: 100, max: 100).

            Returns:
                List of server certificate metadata in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")

            max_items = min(max(1, max_items), 100)

            try:
                server_certificates = self.aws_service.iam.list_server_certificates(path_prefix, max_items)
                return self._format_response({"serverCertificateMetadataList": server_certificates, "count": len(server_certificates)})
            except Exception as e:
                self.logger.error(f"Error listing server certificates: {e}")
                return self._format_error(str(e))