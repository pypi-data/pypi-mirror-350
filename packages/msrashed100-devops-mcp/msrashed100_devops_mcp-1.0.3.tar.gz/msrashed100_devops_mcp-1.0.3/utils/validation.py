"""
Input validation utilities for the DevOps MCP Server.
"""
from typing import Any, Dict, List, Optional, Union
from core.exceptions import InvalidArgumentError


def validate_required_args(args: Dict[str, Any], required_args: List[str]) -> None:
    """
    Validate that required arguments are present.
    
    Args:
        args: The arguments dictionary
        required_args: List of required argument names
        
    Raises:
        InvalidArgumentError: If a required argument is missing
    """
    for arg in required_args:
        if arg not in args:
            raise InvalidArgumentError(arg, f"Missing required argument: {arg}")


def validate_string_arg(args: Dict[str, Any], arg_name: str, required: bool = True) -> Optional[str]:
    """
    Validate a string argument.
    
    Args:
        args: The arguments dictionary
        arg_name: The argument name
        required: Whether the argument is required
        
    Returns:
        The validated string value or None if not required and not present
        
    Raises:
        InvalidArgumentError: If the argument is invalid
    """
    if arg_name not in args:
        if required:
            raise InvalidArgumentError(arg_name, f"Missing required argument: {arg_name}")
        return None
    
    value = args[arg_name]
    if not isinstance(value, str):
        raise InvalidArgumentError(arg_name, f"Argument {arg_name} must be a string")
    
    return value


def validate_int_arg(args: Dict[str, Any], arg_name: str, required: bool = True, 
                    min_value: Optional[int] = None, max_value: Optional[int] = None) -> Optional[int]:
    """
    Validate an integer argument.
    
    Args:
        args: The arguments dictionary
        arg_name: The argument name
        required: Whether the argument is required
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)
        
    Returns:
        The validated integer value or None if not required and not present
        
    Raises:
        InvalidArgumentError: If the argument is invalid
    """
    if arg_name not in args:
        if required:
            raise InvalidArgumentError(arg_name, f"Missing required argument: {arg_name}")
        return None
    
    value = args[arg_name]
    
    try:
        value = int(value)
    except (ValueError, TypeError):
        raise InvalidArgumentError(arg_name, f"Argument {arg_name} must be an integer")
    
    if min_value is not None and value < min_value:
        raise InvalidArgumentError(arg_name, f"Argument {arg_name} must be at least {min_value}")
    
    if max_value is not None and value > max_value:
        raise InvalidArgumentError(arg_name, f"Argument {arg_name} must be at most {max_value}")
    
    return value


def validate_bool_arg(args: Dict[str, Any], arg_name: str, required: bool = True) -> Optional[bool]:
    """
    Validate a boolean argument.
    
    Args:
        args: The arguments dictionary
        arg_name: The argument name
        required: Whether the argument is required
        
    Returns:
        The validated boolean value or None if not required and not present
        
    Raises:
        InvalidArgumentError: If the argument is invalid
    """
    if arg_name not in args:
        if required:
            raise InvalidArgumentError(arg_name, f"Missing required argument: {arg_name}")
        return None
    
    value = args[arg_name]
    
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        if value.lower() in ("true", "yes", "1", "y"):
            return True
        if value.lower() in ("false", "no", "0", "n"):
            return False
    
    raise InvalidArgumentError(arg_name, f"Argument {arg_name} must be a boolean")


def validate_enum_arg(args: Dict[str, Any], arg_name: str, allowed_values: List[str], 
                     required: bool = True, case_sensitive: bool = False) -> Optional[str]:
    """
    Validate an enumeration argument.
    
    Args:
        args: The arguments dictionary
        arg_name: The argument name
        allowed_values: List of allowed values
        required: Whether the argument is required
        case_sensitive: Whether to perform case-sensitive validation
        
    Returns:
        The validated enumeration value or None if not required and not present
        
    Raises:
        InvalidArgumentError: If the argument is invalid
    """
    if arg_name not in args:
        if required:
            raise InvalidArgumentError(arg_name, f"Missing required argument: {arg_name}")
        return None
    
    value = args[arg_name]
    
    if not isinstance(value, str):
        raise InvalidArgumentError(arg_name, f"Argument {arg_name} must be a string")
    
    if case_sensitive:
        if value not in allowed_values:
            raise InvalidArgumentError(arg_name, 
                                      f"Argument {arg_name} must be one of: {', '.join(allowed_values)}")
        return value
    else:
        value_lower = value.lower()
        allowed_lower = [v.lower() for v in allowed_values]
        
        if value_lower not in allowed_lower:
            raise InvalidArgumentError(arg_name, 
                                      f"Argument {arg_name} must be one of: {', '.join(allowed_values)}")
        
        # Return the original case from allowed_values
        index = allowed_lower.index(value_lower)
        return allowed_values[index]


def validate_list_arg(args: Dict[str, Any], arg_name: str, required: bool = True, 
                     item_type: Optional[type] = None) -> Optional[List[Any]]:
    """
    Validate a list argument.
    
    Args:
        args: The arguments dictionary
        arg_name: The argument name
        required: Whether the argument is required
        item_type: Expected type of list items (optional)
        
    Returns:
        The validated list or None if not required and not present
        
    Raises:
        InvalidArgumentError: If the argument is invalid
    """
    if arg_name not in args:
        if required:
            raise InvalidArgumentError(arg_name, f"Missing required argument: {arg_name}")
        return None
    
    value = args[arg_name]
    
    if not isinstance(value, list):
        raise InvalidArgumentError(arg_name, f"Argument {arg_name} must be a list")
    
    if item_type is not None:
        for i, item in enumerate(value):
            if not isinstance(item, item_type):
                raise InvalidArgumentError(arg_name, 
                                         f"Item {i} in {arg_name} must be of type {item_type.__name__}")
    
    return value


def validate_dict_arg(args: Dict[str, Any], arg_name: str, required: bool = True, 
                     required_keys: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
    """
    Validate a dictionary argument.
    
    Args:
        args: The arguments dictionary
        arg_name: The argument name
        required: Whether the argument is required
        required_keys: List of required keys in the dictionary (optional)
        
    Returns:
        The validated dictionary or None if not required and not present
        
    Raises:
        InvalidArgumentError: If the argument is invalid
    """
    if arg_name not in args:
        if required:
            raise InvalidArgumentError(arg_name, f"Missing required argument: {arg_name}")
        return None
    
    value = args[arg_name]
    
    if not isinstance(value, dict):
        raise InvalidArgumentError(arg_name, f"Argument {arg_name} must be a dictionary")
    
    if required_keys is not None:
        for key in required_keys:
            if key not in value:
                raise InvalidArgumentError(arg_name, f"Missing required key '{key}' in {arg_name}")
    
    return value