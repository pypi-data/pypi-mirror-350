"""
AWS IAM client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.aws.client import AWSService


class AWSIAMClient:
    """Client for AWS IAM operations."""
    
    def __init__(self, aws_service: AWSService):
        """
        Initialize the AWS IAM client.
        
        Args:
            aws_service: The base AWS service
        """
        self.aws = aws_service
        self.logger = aws_service.logger
        self.client = None
    
    def _get_client(self):
        """Get the IAM client."""
        if self.client is None:
            self.client = self.aws.get_client('iam')
        return self.client
    
    def list_users(self, path_prefix: Optional[str] = None, max_items: int = 100) -> List[Dict[str, Any]]:
        """
        List IAM users.
        
        Args:
            path_prefix: Path prefix for filtering users
            max_items: Maximum number of items to return
            
        Returns:
            List of IAM users
        """
        try:
            client = self._get_client()
            
            params = {'MaxItems': min(max_items, 100)}
            if path_prefix:
                params['PathPrefix'] = path_prefix
            
            response = client.list_users(**params)
            users = response.get('Users', [])
            
            return users
        except Exception as e:
            self.aws._handle_error("list_users", e)
    
    def get_user(self, user_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get details of an IAM user.
        
        Args:
            user_name: User name (if not provided, gets the current user)
            
        Returns:
            User details
        """
        try:
            client = self._get_client()
            
            params = {}
            if user_name:
                params['UserName'] = user_name
            
            response = client.get_user(**params)
            user = response.get('User', {})
            
            return user
        except Exception as e:
            self.aws._handle_error(f"get_user({user_name})", e)
    
    def list_groups(self, path_prefix: Optional[str] = None, max_items: int = 100) -> List[Dict[str, Any]]:
        """
        List IAM groups.
        
        Args:
            path_prefix: Path prefix for filtering groups
            max_items: Maximum number of items to return
            
        Returns:
            List of IAM groups
        """
        try:
            client = self._get_client()
            
            params = {'MaxItems': min(max_items, 100)}
            if path_prefix:
                params['PathPrefix'] = path_prefix
            
            response = client.list_groups(**params)
            groups = response.get('Groups', [])
            
            return groups
        except Exception as e:
            self.aws._handle_error("list_groups", e)
    
    def get_group(self, group_name: str) -> Dict[str, Any]:
        """
        Get details of an IAM group.
        
        Args:
            group_name: Group name
            
        Returns:
            Group details
        """
        try:
            client = self._get_client()
            
            response = client.get_group(GroupName=group_name)
            
            return response
        except Exception as e:
            self.aws._handle_error(f"get_group({group_name})", e)
    
    def list_roles(self, path_prefix: Optional[str] = None, max_items: int = 100) -> List[Dict[str, Any]]:
        """
        List IAM roles.
        
        Args:
            path_prefix: Path prefix for filtering roles
            max_items: Maximum number of items to return
            
        Returns:
            List of IAM roles
        """
        try:
            client = self._get_client()
            
            params = {'MaxItems': min(max_items, 100)}
            if path_prefix:
                params['PathPrefix'] = path_prefix
            
            response = client.list_roles(**params)
            roles = response.get('Roles', [])
            
            return roles
        except Exception as e:
            self.aws._handle_error("list_roles", e)
    
    def get_role(self, role_name: str) -> Dict[str, Any]:
        """
        Get details of an IAM role.
        
        Args:
            role_name: Role name
            
        Returns:
            Role details
        """
        try:
            client = self._get_client()
            
            response = client.get_role(RoleName=role_name)
            role = response.get('Role', {})
            
            return role
        except Exception as e:
            self.aws._handle_error(f"get_role({role_name})", e)
    
    def list_policies(self, scope: str = 'All', only_attached: bool = False, 
                     path_prefix: Optional[str] = None, max_items: int = 100) -> List[Dict[str, Any]]:
        """
        List IAM policies.
        
        Args:
            scope: Policy scope (All, AWS, Local)
            only_attached: Only include attached policies
            path_prefix: Path prefix for filtering policies
            max_items: Maximum number of items to return
            
        Returns:
            List of IAM policies
        """
        try:
            client = self._get_client()
            
            params = {
                'Scope': scope,
                'OnlyAttached': only_attached,
                'MaxItems': min(max_items, 100)
            }
            if path_prefix:
                params['PathPrefix'] = path_prefix
            
            response = client.list_policies(**params)
            policies = response.get('Policies', [])
            
            return policies
        except Exception as e:
            self.aws._handle_error("list_policies", e)
    
    def get_policy(self, policy_arn: str) -> Dict[str, Any]:
        """
        Get details of an IAM policy.
        
        Args:
            policy_arn: Policy ARN
            
        Returns:
            Policy details
        """
        try:
            client = self._get_client()
            
            response = client.get_policy(PolicyArn=policy_arn)
            policy = response.get('Policy', {})
            
            return policy
        except Exception as e:
            self.aws._handle_error(f"get_policy({policy_arn})", e)
    
    def get_policy_version(self, policy_arn: str, version_id: str) -> Dict[str, Any]:
        """
        Get details of an IAM policy version.
        
        Args:
            policy_arn: Policy ARN
            version_id: Policy version ID
            
        Returns:
            Policy version details
        """
        try:
            client = self._get_client()
            
            response = client.get_policy_version(
                PolicyArn=policy_arn,
                VersionId=version_id
            )
            policy_version = response.get('PolicyVersion', {})
            
            return policy_version
        except Exception as e:
            self.aws._handle_error(f"get_policy_version({policy_arn}, {version_id})", e)
    
    def list_user_policies(self, user_name: str, max_items: int = 100) -> List[str]:
        """
        List inline policies for an IAM user.
        
        Args:
            user_name: User name
            max_items: Maximum number of items to return
            
        Returns:
            List of policy names
        """
        try:
            client = self._get_client()
            
            response = client.list_user_policies(
                UserName=user_name,
                MaxItems=min(max_items, 100)
            )
            policy_names = response.get('PolicyNames', [])
            
            return policy_names
        except Exception as e:
            self.aws._handle_error(f"list_user_policies({user_name})", e)
    
    def list_attached_user_policies(self, user_name: str, path_prefix: Optional[str] = None, 
                                  max_items: int = 100) -> List[Dict[str, Any]]:
        """
        List attached policies for an IAM user.
        
        Args:
            user_name: User name
            path_prefix: Path prefix for filtering policies
            max_items: Maximum number of items to return
            
        Returns:
            List of attached policies
        """
        try:
            client = self._get_client()
            
            params = {
                'UserName': user_name,
                'MaxItems': min(max_items, 100)
            }
            if path_prefix:
                params['PathPrefix'] = path_prefix
            
            response = client.list_attached_user_policies(**params)
            attached_policies = response.get('AttachedPolicies', [])
            
            return attached_policies
        except Exception as e:
            self.aws._handle_error(f"list_attached_user_policies({user_name})", e)

    def get_account_summary(self) -> Dict[str, Any]:
        """
        Provide a summary of IAM entities in the account.

        Returns:
            Dictionary containing the account summary.
        """
        try:
            client = self._get_client()
            response = client.get_account_summary()
            summary_map = response.get('SummaryMap', {})
            return summary_map
        except Exception as e:
            self.aws._handle_error("get_account_summary", e)

    def list_instance_profiles(self, path_prefix: Optional[str] = None, max_items: int = 100) -> List[Dict[str, Any]]:
        """
        List IAM instance profiles.

        Args:
            path_prefix: Path prefix for filtering instance profiles.
            max_items: Maximum number of items to return.

        Returns:
            List of IAM instance profiles.
        """
        try:
            client = self._get_client()
            params = {'MaxItems': min(max_items, 100)}
            if path_prefix:
                params['PathPrefix'] = path_prefix
            
            response = client.list_instance_profiles(**params)
            instance_profiles = response.get('InstanceProfiles', [])
            return instance_profiles
        except Exception as e:
            self.aws._handle_error("list_instance_profiles", e)

    def get_instance_profile(self, instance_profile_name: str) -> Dict[str, Any]:
        """
        Get details of a specific IAM instance profile.

        Args:
            instance_profile_name: The name of the instance profile.

        Returns:
            Dictionary containing instance profile details.
        """
        try:
            client = self._get_client()
            response = client.get_instance_profile(InstanceProfileName=instance_profile_name)
            instance_profile = response.get('InstanceProfile', {})
            return instance_profile
        except Exception as e:
            self.aws._handle_error(f"get_instance_profile({instance_profile_name})", e)

    def list_server_certificates(self, path_prefix: Optional[str] = None, max_items: int = 100) -> List[Dict[str, Any]]:
        """
        List imported SSL/TLS server certificates.

        Args:
            path_prefix: Path prefix for filtering server certificates.
            max_items: Maximum number of items to return.

        Returns:
            List of server certificate metadata.
        """
        try:
            client = self._get_client()
            params = {'MaxItems': min(max_items, 100)}
            if path_prefix:
                params['PathPrefix'] = path_prefix
            
            response = client.list_server_certificates(**params)
            server_certificates = response.get('ServerCertificateMetadataList', [])
            return server_certificates
        except Exception as e:
            self.aws._handle_error("list_server_certificates", e)