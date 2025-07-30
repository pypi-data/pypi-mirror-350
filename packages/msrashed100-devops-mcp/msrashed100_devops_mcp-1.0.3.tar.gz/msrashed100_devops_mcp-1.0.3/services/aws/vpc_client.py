"""
AWS VPC client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.aws.client import AWSService


class AWSVPCClient:
    """Client for AWS VPC operations."""
    
    def __init__(self, aws_service: AWSService):
        """
        Initialize the AWS VPC client.
        
        Args:
            aws_service: The base AWS service
        """
        self.aws = aws_service
        self.logger = aws_service.logger
        self.client = None
    
    def _get_client(self):
        """Get the EC2 client."""
        if self.client is None:
            self.client = self.aws.get_client('ec2')
        return self.client
    
    def list_vpcs(self, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List VPCs.
        
        Args:
            max_results: Maximum number of results to return
            
        Returns:
            List of VPCs
        """
        try:
            client = self._get_client()
            
            response = client.describe_vpcs()
            vpcs = response.get('Vpcs', [])
            
            # Apply limit
            if len(vpcs) > max_results:
                vpcs = vpcs[:max_results]
            
            return vpcs
        except Exception as e:
            self.aws._handle_error("list_vpcs", e)
    
    def get_vpc(self, vpc_id: str) -> Dict[str, Any]:
        """
        Get details of a VPC.
        
        Args:
            vpc_id: VPC ID
            
        Returns:
            VPC details
        """
        try:
            client = self._get_client()
            
            response = client.describe_vpcs(VpcIds=[vpc_id])
            vpcs = response.get('Vpcs', [])
            
            if not vpcs:
                raise ValueError(f"VPC '{vpc_id}' not found")
            
            return vpcs[0]
        except Exception as e:
            self.aws._handle_error(f"get_vpc({vpc_id})", e)
    
    def list_subnets(self, vpc_id: Optional[str] = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List subnets.
        
        Args:
            vpc_id: VPC ID (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of subnets
        """
        try:
            client = self._get_client()
            
            filters = []
            if vpc_id:
                filters.append({
                    'Name': 'vpc-id',
                    'Values': [vpc_id]
                })
            
            params = {}
            if filters:
                params['Filters'] = filters
            
            response = client.describe_subnets(**params)
            subnets = response.get('Subnets', [])
            
            # Apply limit
            if len(subnets) > max_results:
                subnets = subnets[:max_results]
            
            return subnets
        except Exception as e:
            self.aws._handle_error("list_subnets", e)
    
    def get_subnet(self, subnet_id: str) -> Dict[str, Any]:
        """
        Get details of a subnet.
        
        Args:
            subnet_id: Subnet ID
            
        Returns:
            Subnet details
        """
        try:
            client = self._get_client()
            
            response = client.describe_subnets(SubnetIds=[subnet_id])
            subnets = response.get('Subnets', [])
            
            if not subnets:
                raise ValueError(f"Subnet '{subnet_id}' not found")
            
            return subnets[0]
        except Exception as e:
            self.aws._handle_error(f"get_subnet({subnet_id})", e)
    
    def list_security_groups(self, vpc_id: Optional[str] = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List security groups.
        
        Args:
            vpc_id: VPC ID (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of security groups
        """
        try:
            client = self._get_client()
            
            filters = []
            if vpc_id:
                filters.append({
                    'Name': 'vpc-id',
                    'Values': [vpc_id]
                })
            
            params = {}
            if filters:
                params['Filters'] = filters
            
            response = client.describe_security_groups(**params)
            security_groups = response.get('SecurityGroups', [])
            
            # Apply limit
            if len(security_groups) > max_results:
                security_groups = security_groups[:max_results]
            
            return security_groups
        except Exception as e:
            self.aws._handle_error("list_security_groups", e)
    
    def get_security_group(self, security_group_id: str) -> Dict[str, Any]:
        """
        Get details of a security group.
        
        Args:
            security_group_id: Security group ID
            
        Returns:
            Security group details
        """
        try:
            client = self._get_client()
            
            response = client.describe_security_groups(GroupIds=[security_group_id])
            security_groups = response.get('SecurityGroups', [])
            
            if not security_groups:
                raise ValueError(f"Security group '{security_group_id}' not found")
            
            return security_groups[0]
        except Exception as e:
            self.aws._handle_error(f"get_security_group({security_group_id})", e)
    
    def list_route_tables(self, vpc_id: Optional[str] = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List route tables.
        
        Args:
            vpc_id: VPC ID (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of route tables
        """
        try:
            client = self._get_client()
            
            filters = []
            if vpc_id:
                filters.append({
                    'Name': 'vpc-id',
                    'Values': [vpc_id]
                })
            
            params = {}
            if filters:
                params['Filters'] = filters
            
            response = client.describe_route_tables(**params)
            route_tables = response.get('RouteTables', [])
            
            # Apply limit
            if len(route_tables) > max_results:
                route_tables = route_tables[:max_results]
            
            return route_tables
        except Exception as e:
            self.aws._handle_error("list_route_tables", e)
    
    def get_route_table(self, route_table_id: str) -> Dict[str, Any]:
        """
        Get details of a route table.
        
        Args:
            route_table_id: Route table ID
            
        Returns:
            Route table details
        """
        try:
            client = self._get_client()
            
            response = client.describe_route_tables(RouteTableIds=[route_table_id])
            route_tables = response.get('RouteTables', [])
            
            if not route_tables:
                raise ValueError(f"Route table '{route_table_id}' not found")
            
            return route_tables[0]
        except Exception as e:
            self.aws._handle_error(f"get_route_table({route_table_id})", e)
    
    def list_network_acls(self, vpc_id: Optional[str] = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List network ACLs.
        
        Args:
            vpc_id: VPC ID (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of network ACLs
        """
        try:
            client = self._get_client()
            
            filters = []
            if vpc_id:
                filters.append({
                    'Name': 'vpc-id',
                    'Values': [vpc_id]
                })
            
            params = {}
            if filters:
                params['Filters'] = filters
            
            response = client.describe_network_acls(**params)
            network_acls = response.get('NetworkAcls', [])
            
            # Apply limit
            if len(network_acls) > max_results:
                network_acls = network_acls[:max_results]
            
            return network_acls
        except Exception as e:
            self.aws._handle_error("list_network_acls", e)
    
    def get_network_acl(self, network_acl_id: str) -> Dict[str, Any]:
        """
        Get details of a network ACL.
        
        Args:
            network_acl_id: Network ACL ID
            
        Returns:
            Network ACL details
        """
        try:
            client = self._get_client()
            
            response = client.describe_network_acls(NetworkAclIds=[network_acl_id])
            network_acls = response.get('NetworkAcls', [])
            
            if not network_acls:
                raise ValueError(f"Network ACL '{network_acl_id}' not found")
            
            return network_acls[0]
        except Exception as e:
            self.aws._handle_error(f"get_network_acl({network_acl_id})", e)