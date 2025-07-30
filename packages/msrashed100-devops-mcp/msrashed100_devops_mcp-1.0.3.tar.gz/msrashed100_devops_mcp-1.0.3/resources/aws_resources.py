"""
AWS resources for the DevOps MCP Server.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import JSONRPCError, INVALID_REQUEST

from services.aws.service import AWSServiceManager
from utils.logging import setup_logger


class AWSResources:
    """AWS resources for the MCP server."""
    
    def __init__(self, mcp: FastMCP, aws_service: Optional[AWSServiceManager] = None):
        """
        Initialize AWS resources.
        
        Args:
            mcp: The MCP server instance
            aws_service: The AWS service manager instance (optional)
        """
        self.mcp = mcp
        self.aws_service = aws_service or AWSServiceManager()
        self.logger = setup_logger("devops_mcp_server.resources.aws")
        self._register_resources()
    
    def _register_resources(self) -> None:
        """Register AWS resources with the MCP server."""
        
        @self.mcp.resource("aws://{aws_path:path}")
        def handle_aws_resource(aws_path: str):
            """Handle AWS resource requests."""
            if not self.aws_service:
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message="AWS service is not available"
                )
            
            # Path is already extracted by the router
            path = aws_path
            
            try:
                # ECS resources
                if path == "ecs/clusters":
                    return self._handle_ecs_clusters_resource()
                elif path.startswith("ecs/cluster/"):
                    cluster = path[len("ecs/cluster/"):]
                    if "/" not in cluster:
                        return self._handle_ecs_cluster_resource(cluster)
                    else:
                        parts = cluster.split("/", 1)
                        if parts[1].startswith("services"):
                            return self._handle_ecs_services_resource(parts[0])
                        elif parts[1].startswith("service/"):
                            service = parts[1][len("service/"):]
                            return self._handle_ecs_service_resource(parts[0], service)
                        elif parts[1].startswith("tasks"):
                            return self._handle_ecs_tasks_resource(parts[0])
                
                # S3 resources
                elif path == "s3/buckets":
                    return self._handle_s3_buckets_resource()
                elif path.startswith("s3/bucket/"):
                    bucket = path[len("s3/bucket/"):]
                    if "/" not in bucket:
                        return self._handle_s3_bucket_resource(bucket)
                    else:
                        parts = bucket.split("/", 1)
                        if parts[1].startswith("objects"):
                            prefix = parts[1][len("objects/"):] if len(parts[1]) > len("objects/") else None
                            return self._handle_s3_objects_resource(parts[0], prefix)
                
                # ELB resources
                elif path == "elb/load-balancers":
                    return self._handle_elb_load_balancers_resource()
                elif path.startswith("elb/load-balancer/"):
                    lb_arn = path[len("elb/load-balancer/"):]
                    if "/" not in lb_arn:
                        return self._handle_elb_load_balancer_resource(lb_arn)
                    else:
                        parts = lb_arn.split("/", 1)
                        if parts[1].startswith("listeners"):
                            return self._handle_elb_listeners_resource(parts[0])
                        elif parts[1].startswith("target-groups"):
                            return self._handle_elb_target_groups_resource(parts[0])
                
                # VPC resources
                elif path == "vpc/vpcs":
                    return self._handle_vpc_vpcs_resource()
                elif path.startswith("vpc/vpc/"):
                    vpc_id = path[len("vpc/vpc/"):]
                    if "/" not in vpc_id:
                        return self._handle_vpc_vpc_resource(vpc_id)
                    else:
                        parts = vpc_id.split("/", 1)
                        if parts[1].startswith("subnets"):
                            return self._handle_vpc_subnets_resource(parts[0])
                        elif parts[1].startswith("security-groups"):
                            return self._handle_vpc_security_groups_resource(parts[0])
                        elif parts[1].startswith("route-tables"):
                            return self._handle_vpc_route_tables_resource(parts[0])
                
                # Cost resources
                elif path == "cost/usage":
                    return self._handle_cost_usage_resource()
                elif path == "cost/by-service":
                    return self._handle_cost_by_service_resource()
                elif path == "cost/by-account":
                    return self._handle_cost_by_account_resource()
                elif path == "cost/by-region":
                    return self._handle_cost_by_region_resource()
                elif path == "cost/forecast":
                    return self._handle_cost_forecast_resource()
                elif path == "cost/anomalies":
                    return self._handle_cost_anomalies_resource()
                
                # CloudWatch Log Groups
                elif path == "cloudwatch/log-groups":
                    return self._handle_cloudwatch_log_groups_resource()
                
                else:
                    raise JSONRPCError(
                        code=INVALID_REQUEST,
                        message=f"Invalid AWS resource: aws://{aws_path}"
                    )
            except Exception as e:
                self.logger.error(f"Error handling AWS resource: {e}")
                raise JSONRPCError(
                    code=INVALID_REQUEST,
                    message=f"Error handling AWS resource: {str(e)}"
                )
        
        @self.mcp.list_resource_templates()
        def list_aws_resource_templates():
            """List AWS resource templates."""
            templates = []
            
            # ECS templates
            templates.append({
                "uriTemplate": "aws://ecs/clusters",
                "name": "AWS ECS Clusters",
                "mimeType": "application/json",
                "description": "List all ECS clusters"
            })
            
            templates.append({
                "uriTemplate": "aws://ecs/cluster/{cluster}",
                "name": "AWS ECS Cluster",
                "mimeType": "application/json",
                "description": "Get details of an ECS cluster"
            })
            
            templates.append({
                "uriTemplate": "aws://ecs/cluster/{cluster}/services",
                "name": "AWS ECS Services",
                "mimeType": "application/json",
                "description": "List all services in an ECS cluster"
            })
            
            templates.append({
                "uriTemplate": "aws://ecs/cluster/{cluster}/service/{service}",
                "name": "AWS ECS Service",
                "mimeType": "application/json",
                "description": "Get details of an ECS service"
            })
            
            templates.append({
                "uriTemplate": "aws://ecs/cluster/{cluster}/tasks",
                "name": "AWS ECS Tasks",
                "mimeType": "application/json",
                "description": "List all tasks in an ECS cluster"
            })
            
            # S3 templates
            templates.append({
                "uriTemplate": "aws://s3/buckets",
                "name": "AWS S3 Buckets",
                "mimeType": "application/json",
                "description": "List all S3 buckets"
            })
            
            templates.append({
                "uriTemplate": "aws://s3/bucket/{bucket}",
                "name": "AWS S3 Bucket",
                "mimeType": "application/json",
                "description": "Get details of an S3 bucket"
            })
            
            templates.append({
                "uriTemplate": "aws://s3/bucket/{bucket}/objects/{prefix}",
                "name": "AWS S3 Objects",
                "mimeType": "application/json",
                "description": "List objects in an S3 bucket with optional prefix"
            })
            
            # ELB templates
            templates.append({
                "uriTemplate": "aws://elb/load-balancers",
                "name": "AWS Load Balancers",
                "mimeType": "application/json",
                "description": "List all load balancers"
            })
            
            templates.append({
                "uriTemplate": "aws://elb/load-balancer/{loadBalancerArn}",
                "name": "AWS Load Balancer",
                "mimeType": "application/json",
                "description": "Get details of a load balancer"
            })
            
            templates.append({
                "uriTemplate": "aws://elb/load-balancer/{loadBalancerArn}/listeners",
                "name": "AWS Load Balancer Listeners",
                "mimeType": "application/json",
                "description": "List all listeners for a load balancer"
            })
            
            templates.append({
                "uriTemplate": "aws://elb/load-balancer/{loadBalancerArn}/target-groups",
                "name": "AWS Load Balancer Target Groups",
                "mimeType": "application/json",
                "description": "List all target groups for a load balancer"
            })
            
            # VPC templates
            templates.append({
                "uriTemplate": "aws://vpc/vpcs",
                "name": "AWS VPCs",
                "mimeType": "application/json",
                "description": "List all VPCs"
            })
            
            templates.append({
                "uriTemplate": "aws://vpc/vpc/{vpcId}",
                "name": "AWS VPC",
                "mimeType": "application/json",
                "description": "Get details of a VPC"
            })
            
            templates.append({
                "uriTemplate": "aws://vpc/vpc/{vpcId}/subnets",
                "name": "AWS VPC Subnets",
                "mimeType": "application/json",
                "description": "List all subnets in a VPC"
            })
            
            templates.append({
                "uriTemplate": "aws://vpc/vpc/{vpcId}/security-groups",
                "name": "AWS VPC Security Groups",
                "mimeType": "application/json",
                "description": "List all security groups in a VPC"
            })
            
            templates.append({
                "uriTemplate": "aws://vpc/vpc/{vpcId}/route-tables",
                "name": "AWS VPC Route Tables",
                "mimeType": "application/json",
                "description": "List all route tables in a VPC"
            })
            
            # Cost templates
            templates.append({
                "uriTemplate": "aws://cost/by-service",
                "name": "AWS Cost by Service",
                "mimeType": "application/json",
                "description": "Get AWS cost data grouped by service"
            })
            
            templates.append({
                "uriTemplate": "aws://cost/by-account",
                "name": "AWS Cost by Account",
                "mimeType": "application/json",
                "description": "Get AWS cost data grouped by account"
            })
            
            templates.append({
                "uriTemplate": "aws://cost/by-region",
                "name": "AWS Cost by Region",
                "mimeType": "application/json",
                "description": "Get AWS cost data grouped by region"
            })
            
            templates.append({
                "uriTemplate": "aws://cost/usage",
                "name": "AWS Cost and Usage",
                "mimeType": "application/json",
                "description": "Get AWS cost and usage data"
            })
            
            templates.append({
                "uriTemplate": "aws://cost/forecast",
                "name": "AWS Cost Forecast",
                "mimeType": "application/json",
                "description": "Get AWS cost forecast"
            })
            
            templates.append({
                "uriTemplate": "aws://cost/anomalies",
                "name": "AWS Cost Anomalies",
                "mimeType": "application/json",
                "description": "Get AWS cost anomalies"
            })
            
            # CloudWatch Log Groups templates
            templates.append({
                "uriTemplate": "aws://cloudwatch/log-groups",
                "name": "AWS CloudWatch Log Groups",
                "mimeType": "application/json",
                "description": "List all CloudWatch Log Groups"
            })
            
            return templates
    
    # ECS resource handlers
    
    def _handle_ecs_clusters_resource(self) -> Dict[str, Any]:
        """
        Handle ECS clusters resource.
        
        Returns:
            Resource response
        """
        clusters = self.aws_service.ecs.list_clusters()
        
        return {
            "contents": [
                {
                    "uri": "aws://ecs/clusters",
                    "mimeType": "application/json",
                    "text": self._format_json({"clusters": clusters, "count": len(clusters)})
                }
            ]
        }
    
    def _handle_ecs_cluster_resource(self, cluster: str) -> Dict[str, Any]:
        """
        Handle ECS cluster resource.
        
        Args:
            cluster: Cluster name or ARN
            
        Returns:
            Resource response
        """
        cluster_details = self.aws_service.ecs.get_cluster(cluster)
        
        return {
            "contents": [
                {
                    "uri": f"aws://ecs/cluster/{cluster}",
                    "mimeType": "application/json",
                    "text": self._format_json(cluster_details)
                }
            ]
        }
    
    def _handle_ecs_services_resource(self, cluster: str) -> Dict[str, Any]:
        """
        Handle ECS services resource.
        
        Args:
            cluster: Cluster name or ARN
            
        Returns:
            Resource response
        """
        services = self.aws_service.ecs.list_services(cluster)
        
        return {
            "contents": [
                {
                    "uri": f"aws://ecs/cluster/{cluster}/services",
                    "mimeType": "application/json",
                    "text": self._format_json({"services": services, "count": len(services)})
                }
            ]
        }
    
    def _handle_ecs_service_resource(self, cluster: str, service: str) -> Dict[str, Any]:
        """
        Handle ECS service resource.
        
        Args:
            cluster: Cluster name or ARN
            service: Service name or ARN
            
        Returns:
            Resource response
        """
        service_details = self.aws_service.ecs.get_service(cluster, service)
        
        return {
            "contents": [
                {
                    "uri": f"aws://ecs/cluster/{cluster}/service/{service}",
                    "mimeType": "application/json",
                    "text": self._format_json(service_details)
                }
            ]
        }
    
    def _handle_ecs_tasks_resource(self, cluster: str) -> Dict[str, Any]:
        """
        Handle ECS tasks resource.
        
        Args:
            cluster: Cluster name or ARN
            
        Returns:
            Resource response
        """
        tasks = self.aws_service.ecs.list_tasks(cluster)
        
        return {
            "contents": [
                {
                    "uri": f"aws://ecs/cluster/{cluster}/tasks",
                    "mimeType": "application/json",
                    "text": self._format_json({"tasks": tasks, "count": len(tasks)})
                }
            ]
        }
    
    # S3 resource handlers
    
    def _handle_s3_buckets_resource(self) -> Dict[str, Any]:
        """
        Handle S3 buckets resource.
        
        Returns:
            Resource response
        """
        buckets = self.aws_service.s3.list_buckets()
        
        return {
            "contents": [
                {
                    "uri": "aws://s3/buckets",
                    "mimeType": "application/json",
                    "text": self._format_json({"buckets": buckets, "count": len(buckets)})
                }
            ]
        }
    
    def _handle_s3_bucket_resource(self, bucket: str) -> Dict[str, Any]:
        """
        Handle S3 bucket resource.
        
        Args:
            bucket: Bucket name
            
        Returns:
            Resource response
        """
        bucket_details = self.aws_service.s3.get_bucket(bucket)
        
        return {
            "contents": [
                {
                    "uri": f"aws://s3/bucket/{bucket}",
                    "mimeType": "application/json",
                    "text": self._format_json(bucket_details)
                }
            ]
        }
    
    def _handle_s3_objects_resource(self, bucket: str, prefix: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle S3 objects resource.
        
        Args:
            bucket: Bucket name
            prefix: Object key prefix (optional)
            
        Returns:
            Resource response
        """
        objects = self.aws_service.s3.list_objects(bucket, prefix)
        
        return {
            "contents": [
                {
                    "uri": f"aws://s3/bucket/{bucket}/objects/{prefix or ''}",
                    "mimeType": "application/json",
                    "text": self._format_json(objects)
                }
            ]
        }
    
    # ELB resource handlers
    
    def _handle_elb_load_balancers_resource(self) -> Dict[str, Any]:
        """
        Handle ELB load balancers resource.
        
        Returns:
            Resource response
        """
        load_balancers = self.aws_service.elb.list_load_balancers()
        
        return {
            "contents": [
                {
                    "uri": "aws://elb/load-balancers",
                    "mimeType": "application/json",
                    "text": self._format_json({"loadBalancers": load_balancers, "count": len(load_balancers)})
                }
            ]
        }
    
    def _handle_elb_load_balancer_resource(self, load_balancer_arn: str) -> Dict[str, Any]:
        """
        Handle ELB load balancer resource.
        
        Args:
            load_balancer_arn: Load balancer ARN
            
        Returns:
            Resource response
        """
        load_balancer_details = self.aws_service.elb.get_load_balancer(load_balancer_arn)
        
        return {
            "contents": [
                {
                    "uri": f"aws://elb/load-balancer/{load_balancer_arn}",
                    "mimeType": "application/json",
                    "text": self._format_json(load_balancer_details)
                }
            ]
        }
    
    def _handle_elb_listeners_resource(self, load_balancer_arn: str) -> Dict[str, Any]:
        """
        Handle ELB listeners resource.
        
        Args:
            load_balancer_arn: Load balancer ARN
            
        Returns:
            Resource response
        """
        listeners = self.aws_service.elb.list_listeners(load_balancer_arn)
        
        return {
            "contents": [
                {
                    "uri": f"aws://elb/load-balancer/{load_balancer_arn}/listeners",
                    "mimeType": "application/json",
                    "text": self._format_json({"listeners": listeners, "count": len(listeners)})
                }
            ]
        }
    
    def _handle_elb_target_groups_resource(self, load_balancer_arn: str) -> Dict[str, Any]:
        """
        Handle ELB target groups resource.
        
        Args:
            load_balancer_arn: Load balancer ARN
            
        Returns:
            Resource response
        """
        target_groups = self.aws_service.elb.list_target_groups(load_balancer_arn)
        
        return {
            "contents": [
                {
                    "uri": f"aws://elb/load-balancer/{load_balancer_arn}/target-groups",
                    "mimeType": "application/json",
                    "text": self._format_json({"targetGroups": target_groups, "count": len(target_groups)})
                }
            ]
        }
    
    # VPC resource handlers
    
    def _handle_vpc_vpcs_resource(self) -> Dict[str, Any]:
        """
        Handle VPC VPCs resource.
        
        Returns:
            Resource response
        """
        vpcs = self.aws_service.vpc.list_vpcs()
        
        return {
            "contents": [
                {
                    "uri": "aws://vpc/vpcs",
                    "mimeType": "application/json",
                    "text": self._format_json({"vpcs": vpcs, "count": len(vpcs)})
                }
            ]
        }
    
    def _handle_vpc_vpc_resource(self, vpc_id: str) -> Dict[str, Any]:
        """
        Handle VPC VPC resource.
        
        Args:
            vpc_id: VPC ID
            
        Returns:
            Resource response
        """
        vpc_details = self.aws_service.vpc.get_vpc(vpc_id)
        
        return {
            "contents": [
                {
                    "uri": f"aws://vpc/vpc/{vpc_id}",
                    "mimeType": "application/json",
                    "text": self._format_json(vpc_details)
                }
            ]
        }
    
    def _handle_vpc_subnets_resource(self, vpc_id: str) -> Dict[str, Any]:
        """
        Handle VPC subnets resource.
        
        Args:
            vpc_id: VPC ID
            
        Returns:
            Resource response
        """
        subnets = self.aws_service.vpc.list_subnets(vpc_id)
        
        return {
            "contents": [
                {
                    "uri": f"aws://vpc/vpc/{vpc_id}/subnets",
                    "mimeType": "application/json",
                    "text": self._format_json({"subnets": subnets, "count": len(subnets)})
                }
            ]
        }
    
    def _handle_vpc_security_groups_resource(self, vpc_id: str) -> Dict[str, Any]:
        """
        Handle VPC security groups resource.
        
        Args:
            vpc_id: VPC ID
            
        Returns:
            Resource response
        """
        security_groups = self.aws_service.vpc.list_security_groups(vpc_id)
        
        return {
            "contents": [
                {
                    "uri": f"aws://vpc/vpc/{vpc_id}/security-groups",
                    "mimeType": "application/json",
                    "text": self._format_json({"securityGroups": security_groups, "count": len(security_groups)})
                }
            ]
        }
    
    def _handle_vpc_route_tables_resource(self, vpc_id: str) -> Dict[str, Any]:
        """
        Handle VPC route tables resource.
        
        Args:
            vpc_id: VPC ID
            
        Returns:
            Resource response
        """
        route_tables = self.aws_service.vpc.list_route_tables(vpc_id)
        
        return {
            "contents": [
                {
                    "uri": f"aws://vpc/vpc/{vpc_id}/route-tables",
                    "mimeType": "application/json",
                    "text": self._format_json({"routeTables": route_tables, "count": len(route_tables)})
                }
            ]
        }
    
    # Cost resource handlers
    
    def _handle_cost_by_service_resource(self) -> Dict[str, Any]:
        """
        Handle cost by service resource.
        
        Returns:
            Resource response
        """
        cost_data = self.aws_service.cost.get_cost_by_service()
        
        return {
            "contents": [
                {
                    "uri": "aws://cost/by-service",
                    "mimeType": "application/json",
                    "text": self._format_json(cost_data)
                }
            ]
        }
    
    def _handle_cost_by_account_resource(self) -> Dict[str, Any]:
        """
        Handle cost by account resource.
        
        Returns:
            Resource response
        """
        cost_data = self.aws_service.cost.get_cost_by_account()
        
        return {
            "contents": [
                {
                    "uri": "aws://cost/by-account",
                    "mimeType": "application/json",
                    "text": self._format_json(cost_data)
                }
            ]
        }
    
    def _handle_cost_by_region_resource(self) -> Dict[str, Any]:
        """
        Handle cost by region resource.
        
        Returns:
            Resource response
        """
        cost_data = self.aws_service.cost.get_cost_by_region()
        
        return {
            "contents": [
                {
                    "uri": "aws://cost/by-region",
                    "mimeType": "application/json",
                    "text": self._format_json(cost_data)
                }
            ]
        }
    
    def _handle_cost_forecast_resource(self) -> Dict[str, Any]:
        """
        Handle cost forecast resource.
        
        Returns:
            Resource response
        """
        forecast_data = self.aws_service.cost.get_cost_forecast()
        
        return {
            "contents": [
                {
                    "uri": "aws://cost/forecast",
                    "mimeType": "application/json",
                    "text": self._format_json(forecast_data)
                }
            ]
        }
    
    def _handle_cost_usage_resource(self) -> Dict[str, Any]:
        """
        Handle cost and usage resource.
        
        Returns:
            Resource response
        """
        cost_data = self.aws_service.cost.get_cost_and_usage()
        
        return {
            "contents": [
                {
                    "uri": "aws://cost/usage",
                    "mimeType": "application/json",
                    "text": self._format_json(cost_data)
                }
            ]
        }
    
    def _handle_cost_anomalies_resource(self) -> Dict[str, Any]:
        """
        Handle cost anomalies resource.
        
        Returns:
            Resource response
        """
        anomalies_data = self.aws_service.cost.get_cost_anomalies()
        
        return {
            "contents": [
                {
                    "uri": "aws://cost/anomalies",
                    "mimeType": "application/json",
                    "text": self._format_json(anomalies_data)
                }
            ]
        }

    # CloudWatch resource handlers

    def _handle_cloudwatch_log_groups_resource(self) -> Dict[str, Any]:
        """
        Handle CloudWatch Log Groups resource.

        Returns:
            Resource response
        """
        log_groups = self.aws_service.cloudwatch.list_log_groups() # This method will be implemented later

        return {
            "contents": [
                {
                    "uri": "aws://cloudwatch/log-groups",
                    "mimeType": "application/json",
                    "text": self._format_json({"logGroups": log_groups, "count": len(log_groups)})
                }
            ]
        }
    
    def _format_json(self, data: Any) -> str:
        """Format data as JSON string."""
        import json
        return json.dumps(data, indent=2)