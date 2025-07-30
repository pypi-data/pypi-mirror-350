"""
AWS SSM (Systems Manager) tools for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from services.aws.service import AWSServiceManager
from tools.aws.base_tools import AWSBaseTools
from utils.logging import setup_logger


class AWSSSMTools(AWSBaseTools):
    """Tools for AWS SSM operations."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS SSM tools.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        super().__init__(mcp, aws_service)
        self.logger = setup_logger("devops_mcp_server.tools.aws.ssm")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register AWS SSM tools with the MCP server."""
        
        @self.mcp.tool()
        def list_ssm_parameters(parameter_filters: str = None, max_results: int = 50) -> str:
            """
            List SSM parameters.
            
            This tool lists SSM parameters in your AWS account.
            
            Args:
                parameter_filters: JSON string of parameter filters (optional)
                max_results: Maximum number of results to return (default: 50, max: 50)
                
            Returns:
                List of parameters in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 50)
            
            # Parse parameter_filters
            filters = None
            if parameter_filters:
                try:
                    import json
                    filters = json.loads(parameter_filters)
                except Exception as e:
                    return self._format_error(f"Invalid parameter_filters JSON: {str(e)}")
            
            try:
                parameters = self.aws_service.ssm.list_parameters(filters, max_results)
                return self._format_response(parameters)
            except Exception as e:
                self.logger.error(f"Error listing SSM parameters: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_ssm_parameter(name: str, with_decryption: bool = False) -> str:
            """
            Get an SSM parameter.
            
            This tool retrieves an SSM parameter.
            
            Args:
                name: Parameter name
                with_decryption: Whether to decrypt the parameter value (default: False)
                
            Returns:
                Parameter details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                parameter = self.aws_service.ssm.get_parameter(name, with_decryption)
                return self._format_response(parameter)
            except Exception as e:
                self.logger.error(f"Error getting SSM parameter: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_ssm_parameters(names: str, with_decryption: bool = False) -> str:
            """
            Get multiple SSM parameters.
            
            This tool retrieves multiple SSM parameters.
            
            Args:
                names: Comma-separated list of parameter names
                with_decryption: Whether to decrypt the parameter values (default: False)
                
            Returns:
                Parameters details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Parse names
            name_list = [name.strip() for name in names.split(",")]
            if not name_list:
                return self._format_error("No parameter names provided")
            
            try:
                parameters = self.aws_service.ssm.get_parameters(name_list, with_decryption)
                return self._format_response(parameters)
            except Exception as e:
                self.logger.error(f"Error getting SSM parameters: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_ssm_parameters_by_path(path: str, recursive: bool = True, 
                                    with_decryption: bool = False, max_results: int = 50) -> str:
            """
            Get SSM parameters by path.
            
            This tool retrieves SSM parameters by path.
            
            Args:
                path: Parameter path
                recursive: Whether to retrieve parameters recursively (default: True)
                with_decryption: Whether to decrypt the parameter values (default: False)
                max_results: Maximum number of results to return (default: 50, max: 50)
                
            Returns:
                Parameters details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 50)
            
            try:
                parameters = self.aws_service.ssm.get_parameters_by_path(
                    path, recursive, with_decryption, max_results
                )
                return self._format_response(parameters)
            except Exception as e:
                self.logger.error(f"Error getting SSM parameters by path: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_ssm_document_versions(name: str, max_results: int = 50) -> str:
            """
            List SSM document versions.
            
            This tool lists SSM document versions.
            
            Args:
                name: Document name
                max_results: Maximum number of results to return (default: 50, max: 50)
                
            Returns:
                List of document versions in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 50)
            
            try:
                versions = self.aws_service.ssm.list_document_versions(name, max_results)
                return self._format_response(versions)
            except Exception as e:
                self.logger.error(f"Error listing SSM document versions: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_ssm_documents(document_filter_key: str = None, document_filter_value: str = None, 
                            max_results: int = 50) -> str:
            """
            List SSM documents.
            
            This tool lists SSM documents in your AWS account.
            
            Args:
                document_filter_key: Document filter key (optional)
                document_filter_value: Document filter value (optional)
                max_results: Maximum number of results to return (default: 50, max: 50)
                
            Returns:
                List of documents in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 50)
            
            # Create document filter
            document_filter = None
            if document_filter_key and document_filter_value:
                document_filter = {
                    'key': document_filter_key,
                    'value': document_filter_value
                }
            
            try:
                documents = self.aws_service.ssm.list_documents(document_filter, max_results)
                return self._format_response(documents)
            except Exception as e:
                self.logger.error(f"Error listing SSM documents: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def get_ssm_document(name: str, document_version: str = None) -> str:
            """
            Get an SSM document.
            
            This tool retrieves an SSM document.
            
            Args:
                name: Document name
                document_version: Document version (optional)
                
            Returns:
                Document details in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            try:
                document = self.aws_service.ssm.get_document(name, document_version)
                return self._format_response(document)
            except Exception as e:
                self.logger.error(f"Error getting SSM document: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_ssm_associations(association_filter_key: str = None, 
                               association_filter_value: str = None, 
                               max_results: int = 50) -> str:
            """
            List SSM associations.
            
            This tool lists SSM associations in your AWS account.
            
            Args:
                association_filter_key: Association filter key (optional)
                association_filter_value: Association filter value (optional)
                max_results: Maximum number of results to return (default: 50, max: 50)
                
            Returns:
                List of associations in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 50)
            
            # Create association filter
            association_filter = None
            if association_filter_key and association_filter_value:
                association_filter = {
                    'key': association_filter_key,
                    'value': association_filter_value
                }
            
            try:
                associations = self.aws_service.ssm.list_associations(association_filter, max_results)
                return self._format_response(associations)
            except Exception as e:
                self.logger.error(f"Error listing SSM associations: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_ssm_command_invocations(command_id: str = None, instance_id: str = None, 
                                      max_results: int = 50) -> str:
            """
            List SSM command invocations.
            
            This tool lists SSM command invocations.
            
            Args:
                command_id: Command ID (optional)
                instance_id: Instance ID (optional)
                max_results: Maximum number of results to return (default: 50, max: 50)
                
            Returns:
                List of command invocations in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 50)
            
            try:
                invocations = self.aws_service.ssm.list_command_invocations(
                    command_id, instance_id, max_results
                )
                return self._format_response(invocations)
            except Exception as e:
                self.logger.error(f"Error listing SSM command invocations: {e}")
                return self._format_error(str(e))
        
        @self.mcp.tool()
        def list_ssm_commands(command_id: str = None, instance_id: str = None, 
                           max_results: int = 50) -> str:
            """
            List SSM commands.
            
            This tool lists SSM commands.
            
            Args:
                command_id: Command ID (optional)
                instance_id: Instance ID (optional)
                max_results: Maximum number of results to return (default: 50, max: 50)
                
            Returns:
                List of commands in JSON format
            """
            if not self._check_service_available():
                return self._format_error("AWS service is not available")
            
            # Validate max_results
            max_results = min(max(1, max_results), 50)
            
            try:
                commands = self.aws_service.ssm.list_commands(
                    command_id, instance_id, max_results
                )
                return self._format_response(commands)
            except Exception as e:
                self.logger.error(f"Error listing SSM commands: {e}")
                return self._format_error(str(e))