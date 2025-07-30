"""
AWS Lambda client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.aws.client import AWSService


class AWSLambdaClient:
    """Client for AWS Lambda operations."""
    
    def __init__(self, aws_service: AWSService):
        """
        Initialize the AWS Lambda client.
        
        Args:
            aws_service: The base AWS service
        """
        self.aws = aws_service
        self.logger = aws_service.logger
        self.client = None
    
    def _get_client(self):
        """Get the Lambda client."""
        if self.client is None:
            self.client = self.aws.get_client('lambda')
        return self.client
    
    def list_functions(self, function_version: str = 'ALL', max_items: int = 50) -> List[Dict[str, Any]]:
        """
        List Lambda functions.
        
        Args:
            function_version: Function version (ALL or LATEST)
            max_items: Maximum number of items to return
            
        Returns:
            List of Lambda functions
        """
        try:
            client = self._get_client()
            
            response = client.list_functions(
                FunctionVersion=function_version,
                MaxItems=min(max_items, 50)
            )
            functions = response.get('Functions', [])
            
            return functions
        except Exception as e:
            self.aws._handle_error("list_functions", e)
    
    def get_function(self, function_name: str) -> Dict[str, Any]:
        """
        Get details of a Lambda function.
        
        Args:
            function_name: Function name or ARN
            
        Returns:
            Function details
        """
        try:
            client = self._get_client()
            
            response = client.get_function(FunctionName=function_name)
            
            return response
        except Exception as e:
            self.aws._handle_error(f"get_function({function_name})", e)
    
    def list_aliases(self, function_name: str, max_items: int = 50) -> List[Dict[str, Any]]:
        """
        List aliases for a Lambda function.
        
        Args:
            function_name: Function name or ARN
            max_items: Maximum number of items to return
            
        Returns:
            List of function aliases
        """
        try:
            client = self._get_client()
            
            response = client.list_aliases(
                FunctionName=function_name,
                MaxItems=min(max_items, 50)
            )
            aliases = response.get('Aliases', [])
            
            return aliases
        except Exception as e:
            self.aws._handle_error(f"list_aliases({function_name})", e)
    
    def get_alias(self, function_name: str, alias_name: str) -> Dict[str, Any]:
        """
        Get details of a Lambda function alias.
        
        Args:
            function_name: Function name or ARN
            alias_name: Alias name
            
        Returns:
            Alias details
        """
        try:
            client = self._get_client()
            
            response = client.get_alias(
                FunctionName=function_name,
                Name=alias_name
            )
            
            return response
        except Exception as e:
            self.aws._handle_error(f"get_alias({function_name}, {alias_name})", e)
    
    def list_versions(self, function_name: str, max_items: int = 50) -> List[Dict[str, Any]]:
        """
        List versions of a Lambda function.
        
        Args:
            function_name: Function name or ARN
            max_items: Maximum number of items to return
            
        Returns:
            List of function versions
        """
        try:
            client = self._get_client()
            
            response = client.list_versions_by_function(
                FunctionName=function_name,
                MaxItems=min(max_items, 50)
            )
            versions = response.get('Versions', [])
            
            return versions
        except Exception as e:
            self.aws._handle_error(f"list_versions({function_name})", e)
    
    def list_event_source_mappings(self, function_name: Optional[str] = None, 
                                 event_source_arn: Optional[str] = None,
                                 max_items: int = 50) -> List[Dict[str, Any]]:
        """
        List event source mappings for a Lambda function.
        
        Args:
            function_name: Function name or ARN (optional)
            event_source_arn: Event source ARN (optional)
            max_items: Maximum number of items to return
            
        Returns:
            List of event source mappings
        """
        try:
            client = self._get_client()
            
            params = {'MaxItems': min(max_items, 50)}
            if function_name:
                params['FunctionName'] = function_name
            if event_source_arn:
                params['EventSourceArn'] = event_source_arn
            
            response = client.list_event_source_mappings(**params)
            mappings = response.get('EventSourceMappings', [])
            
            return mappings
        except Exception as e:
            self.aws._handle_error("list_event_source_mappings", e)
    
    def get_event_source_mapping(self, uuid: str) -> Dict[str, Any]:
        """
        Get details of a Lambda event source mapping.
        
        Args:
            uuid: Event source mapping UUID
            
        Returns:
            Event source mapping details
        """
        try:
            client = self._get_client()
            
            response = client.get_event_source_mapping(UUID=uuid)
            
            return response
        except Exception as e:
            self.aws._handle_error(f"get_event_source_mapping({uuid})", e)
    
    def list_function_event_invoke_configs(self, function_name: str, max_items: int = 50) -> List[Dict[str, Any]]:
        """
        List event invoke configurations for a Lambda function.
        
        Args:
            function_name: Function name or ARN
            max_items: Maximum number of items to return
            
        Returns:
            List of function event invoke configurations
        """
        try:
            client = self._get_client()
            
            response = client.list_function_event_invoke_configs(
                FunctionName=function_name,
                MaxItems=min(max_items, 50)
            )
            configs = response.get('FunctionEventInvokeConfigs', [])
            
            return configs
        except Exception as e:
            self.aws._handle_error(f"list_function_event_invoke_configs({function_name})", e)
    
    def get_function_concurrency(self, function_name: str) -> Dict[str, Any]:
        """
        Get reserved concurrency configuration for a Lambda function.
        
        Args:
            function_name: Function name or ARN
            
        Returns:
            Reserved concurrency configuration
        """
        try:
            client = self._get_client()
            
            response = client.get_function_concurrency(FunctionName=function_name)
            
            return response
        except Exception as e:
            self.aws._handle_error(f"get_function_concurrency({function_name})", e)
    
    def list_layers(self, compatible_runtime: Optional[str] = None, max_items: int = 50) -> Dict[str, Any]:
        """
        List Lambda layers.
        
        Args:
            compatible_runtime: Compatible runtime (optional)
            max_items: Maximum number of items to return
            
        Returns:
            List of Lambda layers
        """
        try:
            client = self._get_client()
            
            params = {'MaxItems': min(max_items, 50)}
            if compatible_runtime:
                params['CompatibleRuntime'] = compatible_runtime
            
            response = client.list_layers(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error("list_layers", e)
    
    def get_layer_version(self, layer_name: str, version_number: int) -> Dict[str, Any]:
        """
        Get details of a Lambda layer version.
        
        Args:
            layer_name: Layer name or ARN
            version_number: Version number
            
        Returns:
            Layer version details
        """
        try:
            client = self._get_client()
            
            response = client.get_layer_version(
                LayerName=layer_name,
                VersionNumber=version_number
            )
            
            return response
        except Exception as e:
            self.aws._handle_error(f"get_layer_version({layer_name}, {version_number})", e)

    def get_policy(self, function_name: str, qualifier: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve the resource-based policy for a Lambda function.

        Args:
            function_name: The name of the Lambda function.
            qualifier: Specify a version or alias to get the policy for that resource.

        Returns:
            A dictionary containing the policy and revision ID.
        """
        self.logger.info(f"Getting policy for Lambda function: {function_name}")
        try:
            client = self._get_client()
            params = {'FunctionName': function_name}
            if qualifier:
                params['Qualifier'] = qualifier
            
            response = client.get_policy(**params)
            # The policy is a JSON string, parse it for easier use if needed by tools
            import json
            policy_document = {}
            if response.get('Policy'):
                try:
                    policy_document = json.loads(response['Policy'])
                except json.JSONDecodeError:
                    self.logger.warning(f"Could not parse policy JSON for function {function_name}")
                    # Keep it as a string if parsing fails
                    policy_document = response['Policy']
            
            return {
                "Policy": policy_document,
                "RevisionId": response.get("RevisionId")
            }
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                 self.logger.warning(f"No policy found for Lambda function: {function_name}")
                 return {"Policy": {}, "RevisionId": None} # Return empty if no policy
            self.logger.error(f"Error getting policy for Lambda function {function_name}: {e}")
            raise

    def list_tags(self, resource_arn: str) -> Dict[str, str]:
        """
        List tags associated with a Lambda function.

        Args:
            resource_arn: The ARN of the Lambda function.

        Returns:
            A dictionary of tags.
        """
        self.logger.info(f"Listing tags for Lambda resource: {resource_arn}")
        try:
            client = self._get_client()
            response = client.list_tags(Resource=resource_arn)
            return response.get("Tags", {})
        except Exception as e:
            self.logger.error(f"Error listing tags for Lambda resource {resource_arn}: {e}")
            raise