"""
Custom exceptions for the DevOps MCP Server.
"""
from mcp.types import JSONRPCError, INVALID_REQUEST, INTERNAL_ERROR


class DevOpsServerError(Exception):
    """Base exception for DevOps MCP Server errors."""
    pass


class ServiceConnectionError(DevOpsServerError):
    """Exception raised when a service connection fails."""
    def __init__(self, service_name, message=None):
        self.service_name = service_name
        self.message = message or f"Failed to connect to {service_name} service"
        super().__init__(self.message)


class ServiceOperationError(DevOpsServerError):
    """Exception raised when a service operation fails."""
    def __init__(self, service_name, operation, message=None):
        self.service_name = service_name
        self.operation = operation
        self.message = message or f"Failed to perform {operation} on {service_name} service"
        super().__init__(self.message)


class ResourceNotFoundError(DevOpsServerError):
    """Exception raised when a resource is not found."""
    def __init__(self, resource_type, resource_name, namespace=None):
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.namespace = namespace
        message = f"Resource {resource_type}/{resource_name}"
        if namespace:
            message += f" in namespace {namespace}"
        message += " not found"
        super().__init__(message)


class InvalidArgumentError(DevOpsServerError):
    """Exception raised when an invalid argument is provided."""
    def __init__(self, argument_name, message=None):
        self.argument_name = argument_name
        self.message = message or f"Invalid argument: {argument_name}"
        super().__init__(self.message)


def to_mcp_error(error):
    """Convert a DevOpsServerError to an MCP JSONRPCError."""
    if isinstance(error, InvalidArgumentError):
        return JSONRPCError(
            code=INVALID_REQUEST,
            message=str(error)
        )
    elif isinstance(error, ResourceNotFoundError):
        return JSONRPCError(
            code=INVALID_REQUEST,
            message=str(error)
        )
    elif isinstance(error, (ServiceConnectionError, ServiceOperationError)):
        return JSONRPCError(
            code=INTERNAL_ERROR,
            message=str(error)
        )
    else:
        return JSONRPCError(
            code=INTERNAL_ERROR,
            message=f"Internal server error: {str(error)}"
        )