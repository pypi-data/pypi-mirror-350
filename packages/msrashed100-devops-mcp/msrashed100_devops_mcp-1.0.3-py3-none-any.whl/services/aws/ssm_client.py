"""
AWS SSM (Systems Manager) client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.aws.client import AWSService


class AWSSSMClient:
    """Client for AWS SSM operations."""
    
    def __init__(self, aws_service: AWSService):
        """
        Initialize the AWS SSM client.
        
        Args:
            aws_service: The base AWS service
        """
        self.aws = aws_service
        self.logger = aws_service.logger
        self.client = None
    
    def _get_client(self):
        """Get the SSM client."""
        if self.client is None:
            self.client = self.aws.get_client('ssm')
        return self.client
    
    def list_parameters(self, parameter_filters: Optional[List[Dict[str, Any]]] = None, 
                      max_results: int = 50) -> Dict[str, Any]:
        """
        List SSM parameters.
        
        Args:
            parameter_filters: Parameter filters (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of parameters
        """
        try:
            client = self._get_client()
            
            params = {'MaxResults': min(max_results, 50)}
            if parameter_filters:
                params['ParameterFilters'] = parameter_filters
            
            response = client.describe_parameters(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error("list_parameters", e)
    
    def get_parameter(self, name: str, with_decryption: bool = False) -> Dict[str, Any]:
        """
        Get an SSM parameter.
        
        Args:
            name: Parameter name
            with_decryption: Whether to decrypt the parameter value
            
        Returns:
            Parameter details
        """
        try:
            client = self._get_client()
            
            response = client.get_parameter(
                Name=name,
                WithDecryption=with_decryption
            )
            parameter = response.get('Parameter', {})
            
            return parameter
        except Exception as e:
            self.aws._handle_error(f"get_parameter({name})", e)
    
    def get_parameters(self, names: List[str], with_decryption: bool = False) -> Dict[str, Any]:
        """
        Get multiple SSM parameters.
        
        Args:
            names: Parameter names
            with_decryption: Whether to decrypt the parameter values
            
        Returns:
            Parameters details
        """
        try:
            client = self._get_client()
            
            response = client.get_parameters(
                Names=names,
                WithDecryption=with_decryption
            )
            
            return response
        except Exception as e:
            self.aws._handle_error("get_parameters", e)
    
    def get_parameters_by_path(self, path: str, recursive: bool = True, 
                             with_decryption: bool = False, max_results: int = 50) -> Dict[str, Any]:
        """
        Get SSM parameters by path.
        
        Args:
            path: Parameter path
            recursive: Whether to retrieve parameters recursively
            with_decryption: Whether to decrypt the parameter values
            max_results: Maximum number of results to return
            
        Returns:
            Parameters details
        """
        try:
            client = self._get_client()
            
            response = client.get_parameters_by_path(
                Path=path,
                Recursive=recursive,
                WithDecryption=with_decryption,
                MaxResults=min(max_results, 50)
            )
            
            return response
        except Exception as e:
            self.aws._handle_error(f"get_parameters_by_path({path})", e)
    
    def list_document_versions(self, name: str, max_results: int = 50) -> Dict[str, Any]:
        """
        List SSM document versions.
        
        Args:
            name: Document name
            max_results: Maximum number of results to return
            
        Returns:
            List of document versions
        """
        try:
            client = self._get_client()
            
            response = client.list_document_versions(
                Name=name,
                MaxResults=min(max_results, 50)
            )
            
            return response
        except Exception as e:
            self.aws._handle_error(f"list_document_versions({name})", e)
    
    def list_documents(self, document_filter: Optional[Dict[str, str]] = None, 
                     max_results: int = 50) -> Dict[str, Any]:
        """
        List SSM documents.
        
        Args:
            document_filter: Document filter (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of documents
        """
        try:
            client = self._get_client()
            
            params = {'MaxResults': min(max_results, 50)}
            if document_filter:
                params['DocumentFilterList'] = [document_filter]
            
            response = client.list_documents(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error("list_documents", e)
    
    def get_document(self, name: str, document_version: Optional[str] = None) -> Dict[str, Any]:
        """
        Get an SSM document.
        
        Args:
            name: Document name
            document_version: Document version (optional)
            
        Returns:
            Document details
        """
        try:
            client = self._get_client()
            
            params = {'Name': name}
            if document_version:
                params['DocumentVersion'] = document_version
            
            response = client.get_document(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error(f"get_document({name})", e)
    
    def list_associations(self, association_filter: Optional[Dict[str, str]] = None, 
                        max_results: int = 50) -> Dict[str, Any]:
        """
        List SSM associations.
        
        Args:
            association_filter: Association filter (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of associations
        """
        try:
            client = self._get_client()
            
            params = {'MaxResults': min(max_results, 50)}
            if association_filter:
                params['AssociationFilterList'] = [association_filter]
            
            response = client.list_associations(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error("list_associations", e)
    
    def describe_association(self, name: str, instance_id: Optional[str] = None, 
                           association_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Describe an SSM association.
        
        Args:
            name: Document name
            instance_id: Instance ID (optional)
            association_id: Association ID (optional)
            
        Returns:
            Association details
        """
        try:
            client = self._get_client()
            
            params = {'Name': name}
            if instance_id:
                params['InstanceId'] = instance_id
            if association_id:
                params['AssociationId'] = association_id
            
            response = client.describe_association(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error(f"describe_association({name})", e)
    
    def list_command_invocations(self, command_id: Optional[str] = None, 
                               instance_id: Optional[str] = None, 
                               max_results: int = 50) -> Dict[str, Any]:
        """
        List SSM command invocations.
        
        Args:
            command_id: Command ID (optional)
            instance_id: Instance ID (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of command invocations
        """
        try:
            client = self._get_client()
            
            params = {'MaxResults': min(max_results, 50)}
            if command_id:
                params['CommandId'] = command_id
            if instance_id:
                params['InstanceId'] = instance_id
            
            response = client.list_command_invocations(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error("list_command_invocations", e)
    
    def list_commands(self, command_id: Optional[str] = None, 
                    instance_id: Optional[str] = None, 
                    max_results: int = 50) -> Dict[str, Any]:
        """
        List SSM commands.
        
        Args:
            command_id: Command ID (optional)
            instance_id: Instance ID (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of commands
        """
        try:
            client = self._get_client()
            
            params = {'MaxResults': min(max_results, 50)}
            if command_id:
                params['CommandId'] = command_id
            if instance_id:
                params['InstanceId'] = instance_id
            
            response = client.list_commands(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error("list_commands", e)
    
    def list_inventory_entries(self, instance_id: str, type_name: str, 
                             max_results: int = 50) -> Dict[str, Any]:
        """
        List SSM inventory entries.
        
        Args:
            instance_id: Instance ID
            type_name: Inventory type name
            max_results: Maximum number of results to return
            
        Returns:
            List of inventory entries
        """
        try:
            client = self._get_client()
            
            response = client.list_inventory_entries(
                InstanceId=instance_id,
                TypeName=type_name,
                MaxResults=min(max_results, 50)
            )
            
            return response
        except Exception as e:
            self.aws._handle_error(f"list_inventory_entries({instance_id}, {type_name})", e)
    
    def get_inventory(self, inventory_filter: Optional[List[Dict[str, Any]]] = None, 
                    max_results: int = 50) -> Dict[str, Any]:
        """
        Get SSM inventory.
        
        Args:
            inventory_filter: Inventory filter (optional)
            max_results: Maximum number of results to return
            
        Returns:
            Inventory details
        """
        try:
            client = self._get_client()
            
            params = {'MaxResults': min(max_results, 50)}
            if inventory_filter:
                params['Filters'] = inventory_filter
            
            response = client.get_inventory(**params)
            
            return response
        except Exception as e:
            self.aws._handle_error("get_inventory", e)