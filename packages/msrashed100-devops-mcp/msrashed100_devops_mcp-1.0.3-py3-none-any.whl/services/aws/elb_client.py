"""
AWS Elastic Load Balancing client for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional, List

from services.aws.client import AWSService


class AWSELBClient:
    """Client for AWS Elastic Load Balancing operations."""
    
    def __init__(self, aws_service: AWSService):
        """
        Initialize the AWS ELB client.
        
        Args:
            aws_service: The base AWS service
        """
        self.aws = aws_service
        self.logger = aws_service.logger
        self.elbv2_client = None
    
    def _get_elbv2_client(self):
        """Get the ELBv2 client."""
        if self.elbv2_client is None:
            self.elbv2_client = self.aws.get_client('elbv2')
        return self.elbv2_client
    
    def list_load_balancers(self, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List Application Load Balancers.
        
        Args:
            max_results: Maximum number of results to return
            
        Returns:
            List of load balancers
        """
        try:
            client = self._get_elbv2_client()
            
            # Get load balancers
            response = client.describe_load_balancers(PageSize=min(max_results, 100))
            load_balancers = response.get('LoadBalancers', [])
            
            return load_balancers
        except Exception as e:
            self.aws._handle_error("list_load_balancers", e)
    
    def get_load_balancer(self, load_balancer_arn: str) -> Dict[str, Any]:
        """
        Get details of a load balancer.
        
        Args:
            load_balancer_arn: Load balancer ARN
            
        Returns:
            Load balancer details
        """
        try:
            client = self._get_elbv2_client()
            
            response = client.describe_load_balancers(LoadBalancerArns=[load_balancer_arn])
            load_balancers = response.get('LoadBalancers', [])
            
            if not load_balancers:
                raise ValueError(f"Load balancer '{load_balancer_arn}' not found")
            
            return load_balancers[0]
        except Exception as e:
            self.aws._handle_error(f"get_load_balancer({load_balancer_arn})", e)
    
    def list_listeners(self, load_balancer_arn: str) -> List[Dict[str, Any]]:
        """
        List listeners for a load balancer.
        
        Args:
            load_balancer_arn: Load balancer ARN
            
        Returns:
            List of listeners
        """
        try:
            client = self._get_elbv2_client()
            
            response = client.describe_listeners(LoadBalancerArn=load_balancer_arn)
            listeners = response.get('Listeners', [])
            
            return listeners
        except Exception as e:
            self.aws._handle_error(f"list_listeners({load_balancer_arn})", e)
    
    def get_listener(self, listener_arn: str) -> Dict[str, Any]:
        """
        Get details of a listener.
        
        Args:
            listener_arn: Listener ARN
            
        Returns:
            Listener details
        """
        try:
            client = self._get_elbv2_client()
            
            response = client.describe_listeners(ListenerArns=[listener_arn])
            listeners = response.get('Listeners', [])
            
            if not listeners:
                raise ValueError(f"Listener '{listener_arn}' not found")
            
            return listeners[0]
        except Exception as e:
            self.aws._handle_error(f"get_listener({listener_arn})", e)
    
    def list_target_groups(self, load_balancer_arn: Optional[str] = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List target groups.
        
        Args:
            load_balancer_arn: Load balancer ARN (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of target groups
        """
        try:
            client = self._get_elbv2_client()
            
            params = {}
            if load_balancer_arn:
                params['LoadBalancerArn'] = load_balancer_arn
            
            response = client.describe_target_groups(**params)
            target_groups = response.get('TargetGroups', [])
            
            # Apply limit
            if len(target_groups) > max_results:
                target_groups = target_groups[:max_results]
            
            return target_groups
        except Exception as e:
            self.aws._handle_error("list_target_groups", e)
    
    def get_target_group(self, target_group_arn: str) -> Dict[str, Any]:
        """
        Get details of a target group.
        
        Args:
            target_group_arn: Target group ARN
            
        Returns:
            Target group details
        """
        try:
            client = self._get_elbv2_client()
            
            response = client.describe_target_groups(TargetGroupArns=[target_group_arn])
            target_groups = response.get('TargetGroups', [])
            
            if not target_groups:
                raise ValueError(f"Target group '{target_group_arn}' not found")
            
            return target_groups[0]
        except Exception as e:
            self.aws._handle_error(f"get_target_group({target_group_arn})", e)
    
    def list_target_health(self, target_group_arn: str) -> List[Dict[str, Any]]:
        """
        List health of targets in a target group.
        
        Args:
            target_group_arn: Target group ARN
            
        Returns:
            List of target health descriptions
        """
        try:
            client = self._get_elbv2_client()
            
            response = client.describe_target_health(TargetGroupArn=target_group_arn)
            target_health_descriptions = response.get('TargetHealthDescriptions', [])
            
            return target_health_descriptions
        except Exception as e:
            self.aws._handle_error(f"list_target_health({target_group_arn})", e)
    
    def list_rules(self, listener_arn: str) -> List[Dict[str, Any]]:
        """
        List rules for a listener.
        
        Args:
            listener_arn: Listener ARN
            
        Returns:
            List of rules
        """
        try:
            client = self._get_elbv2_client()
            
            response = client.describe_rules(ListenerArn=listener_arn)
            rules = response.get('Rules', [])
            
            return rules
        except Exception as e:
            self.aws._handle_error(f"list_rules({listener_arn})", e)
    
    def get_rule(self, rule_arn: str) -> Dict[str, Any]:
        """
        Get details of a rule.
        
        Args:
            rule_arn: Rule ARN
            
        Returns:
            Rule details
        """
        try:
            client = self._get_elbv2_client()
            
            response = client.describe_rules(RuleArns=[rule_arn])
            rules = response.get('Rules', [])
            
            if not rules:
                raise ValueError(f"Rule '{rule_arn}' not found")
            
            return rules[0]
        except Exception as e:
            self.aws._handle_error(f"get_rule({rule_arn})", e)