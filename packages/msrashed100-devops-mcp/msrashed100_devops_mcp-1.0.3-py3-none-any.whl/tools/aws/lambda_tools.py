"""
AWS Lambda tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.base_tools import AWSBaseTools
from utils.logging import setup_logger


class AWSLambdaTools(AWSBaseTools):
    """Tools for AWS Lambda operations."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS Lambda tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.lambda")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register AWS Lambda tools with the MCP server."""
        
        @self.mcp.tool()
        def list_lambda_functions(function_version: str = "ALL", max_items: int = 50) -> str:
            """
            List Lambda functions.
            
            This tool lists Lambda functions in your AWS account.
            
            Args:
                function_version: Function version (ALL or LATEST) (default: ALL)
                max_items: Maximum number of items to return (default: 50, max: 50)
                
            Returns:
                List of Lambda functions in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate function_version
            if function_version not in ["ALL", "LATEST"]:
                return self._format_error("Invalid function_version. Must be one of: ALL, LATEST")
            
            # Validate max_items
            max_items = min(max(1, max_items), 50)
            
            try:
                functions = self.aws_service.lambda_client.list_functions(function_version, max_items)
                return self._format_response({"functions": functions, "count": len(functions)})
            except Exception as e:
                self.logger.error(f"Error listing Lambda functions: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_lambda_function(function_name: str) -> str:
            """
            Get details of a Lambda function.
            
            This tool retrieves details of a Lambda function.
            
            Args:
                function_name: Function name or ARN
                
            Returns:
                Function details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                function = self.aws_service.lambda_client.get_function(function_name)
                return self._format_response(function)
            except Exception as e:
                self.logger.error(f"Error getting Lambda function: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_lambda_aliases(function_name: str, max_items: int = 50) -> str:
            """
            List aliases for a Lambda function.
            
            This tool lists aliases for a Lambda function.
            
            Args:
                function_name: Function name or ARN
                max_items: Maximum number of items to return (default: 50, max: 50)
                
            Returns:
                List of function aliases in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 50)
            
            try:
                aliases = self.aws_service.lambda_client.list_aliases(function_name, max_items)
                return self._format_response({"aliases": aliases, "count": len(aliases)})
            except Exception as e:
                self.logger.error(f"Error listing Lambda aliases: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_lambda_alias(function_name: str, alias_name: str) -> str:
            """
            Get details of a Lambda function alias.
            
            This tool retrieves details of a Lambda function alias.
            
            Args:
                function_name: Function name or ARN
                alias_name: Alias name
                
            Returns:
                Alias details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                alias = self.aws_service.lambda_client.get_alias(function_name, alias_name)
                return self._format_response(alias)
            except Exception as e:
                self.logger.error(f"Error getting Lambda alias: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_lambda_versions(function_name: str, max_items: int = 50) -> str:
            """
            List versions of a Lambda function.
            
            This tool lists versions of a Lambda function.
            
            Args:
                function_name: Function name or ARN
                max_items: Maximum number of items to return (default: 50, max: 50)
                
            Returns:
                List of function versions in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 50)
            
            try:
                versions = self.aws_service.lambda_client.list_versions(function_name, max_items)
                return self._format_response({"versions": versions, "count": len(versions)})
            except Exception as e:
                self.logger.error(f"Error listing Lambda versions: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_lambda_event_source_mappings(function_name: str = None, 
                                           event_source_arn: str = None,
                                           max_items: int = 50) -> str:
            """
            List event source mappings for a Lambda function.
            
            This tool lists event source mappings for a Lambda function.
            
            Args:
                function_name: Function name or ARN (optional)
                event_source_arn: Event source ARN (optional)
                max_items: Maximum number of items to return (default: 50, max: 50)
                
            Returns:
                List of event source mappings in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 50)
            
            try:
                mappings = self.aws_service.lambda_client.list_event_source_mappings(
                    function_name, event_source_arn, max_items
                )
                return self._format_response({"eventSourceMappings": mappings, "count": len(mappings)})
            except Exception as e:
                self.logger.error(f"Error listing Lambda event source mappings: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_lambda_event_source_mapping(uuid: str) -> str:
            """
            Get details of a Lambda event source mapping.
            
            This tool retrieves details of a Lambda event source mapping.
            
            Args:
                uuid: Event source mapping UUID
                
            Returns:
                Event source mapping details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                mapping = self.aws_service.lambda_client.get_event_source_mapping(uuid)
                return self._format_response(mapping)
            except Exception as e:
                self.logger.error(f"Error getting Lambda event source mapping: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_lambda_function_event_invoke_configs(function_name: str, max_items: int = 50) -> str:
            """
            List event invoke configurations for a Lambda function.
            
            This tool lists event invoke configurations for a Lambda function.
            
            Args:
                function_name: Function name or ARN
                max_items: Maximum number of items to return (default: 50, max: 50)
                
            Returns:
                List of function event invoke configurations in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 50)
            
            try:
                configs = self.aws_service.lambda_client.list_function_event_invoke_configs(function_name, max_items)
                return self._format_response({"functionEventInvokeConfigs": configs, "count": len(configs)})
            except Exception as e:
                self.logger.error(f"Error listing Lambda function event invoke configs: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_lambda_function_concurrency(function_name: str) -> str:
            """
            Get reserved concurrency configuration for a Lambda function.
            
            This tool retrieves reserved concurrency configuration for a Lambda function.
            
            Args:
                function_name: Function name or ARN
                
            Returns:
                Reserved concurrency configuration in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                concurrency = self.aws_service.lambda_client.get_function_concurrency(function_name)
                return self._format_response(concurrency)
            except Exception as e:
                self.logger.error(f"Error getting Lambda function concurrency: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_lambda_layers(compatible_runtime: str = None, max_items: int = 50) -> str:
            """
            List Lambda layers.
            
            This tool lists Lambda layers.
            
            Args:
                compatible_runtime: Compatible runtime (optional)
                max_items: Maximum number of items to return (default: 50, max: 50)
                
            Returns:
                List of Lambda layers in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_items
            max_items = min(max(1, max_items), 50)
            
            try:
                layers = self.aws_service.lambda_client.list_layers(compatible_runtime, max_items)
                return self._format_response(layers)
            except Exception as e:
                self.logger.error(f"Error listing Lambda layers: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_lambda_layer_version(layer_name: str, version_number: int) -> str:
            """
            Get details of a Lambda layer version.
            
            This tool retrieves details of a Lambda layer version.
            
            Args:
                layer_name: Layer name or ARN
                version_number: Version number
                
            Returns:
                Layer version details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                layer_version = self.aws_service.lambda_client.get_layer_version(layer_name, version_number)
                return self._format_response(layer_version)
            except Exception as e:
                self.logger.error(f"Error getting Lambda layer version: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def get_lambda_policy(function_name: str, qualifier: Optional[str] = None) -> str:
            """
            Retrieve the resource-based policy for a Lambda function.

            Args:
                function_name: The name of the Lambda function.
                qualifier: Specify a version or alias to get the policy for that resource (optional).
            
            Returns:
                A dictionary containing the policy and revision ID in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                policy_info = self.aws_service.lambda_client.get_policy(function_name=function_name, qualifier=qualifier)
                return self._format_response(policy_info)
            except Exception as e:
                self.logger.error(f"Error getting Lambda policy for {function_name}: {e}")
                return self._format_error(str(e))

        @self.mcp.tool()
        def list_lambda_tags(resource_arn: str) -> str:
            """
            List tags associated with a Lambda function.

            Args:
                resource_arn: The ARN of the Lambda function.
            
            Returns:
                A dictionary of tags in JSON format.
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                tags = self.aws_service.lambda_client.list_tags(resource_arn=resource_arn)
                return self._format_response({"Tags": tags}) # Ensure top-level key for consistency
            except Exception as e:
                self.logger.error(f"Error listing Lambda tags for {resource_arn}: {e}")
                return self._format_error(str(e))