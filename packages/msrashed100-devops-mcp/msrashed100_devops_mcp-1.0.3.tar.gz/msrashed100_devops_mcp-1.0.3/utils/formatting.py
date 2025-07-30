"""
Response formatting utilities for the DevOps MCP Server.
"""
import json
import datetime # Added import
from typing import Dict, List, Any, Union
from mcp.types import TextContent

# Helper function to serialize datetime objects
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def format_text_response(text: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Format a text response for the MCP server.
    
    Args:
        text: The text to format
        
    Returns:
        A dictionary with the formatted response
    """
    return {
        "content": [
            TextContent(type="text", text=text)
        ]
    }


def format_json_response(data: Any) -> Dict[str, List[Dict[str, str]]]:
    """
    Format a JSON response for the MCP server.
    
    Args:
        data: The data to format as JSON
        
    Returns:
        A dictionary with the formatted response
    """
    json_text = json.dumps(data, indent=2, default=json_serial) # Added default serializer
    return format_text_response(json_text)


def format_table_response(headers: List[str], rows: List[List[Any]]) -> Dict[str, List[Dict[str, str]]]:
    """
    Format a table response for the MCP server.
    
    Args:
        headers: The table headers
        rows: The table rows
        
    Returns:
        A dictionary with the formatted response
    """
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Format the table
    lines = []
    
    # Add header
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    lines.append(header_line)
    
    # Add separator
    separator = "-+-".join("-" * w for w in col_widths)
    lines.append(separator)
    
    # Add rows
    for row in rows:
        row_line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        lines.append(row_line)
    
    return format_text_response("\n".join(lines))


def format_list_response(items: List[Any], title: str = None) -> Dict[str, List[Dict[str, str]]]:
    """
    Format a list response for the MCP server.
    
    Args:
        items: The list items
        title: An optional title for the list
        
    Returns:
        A dictionary with the formatted response
    """
    lines = []
    
    if title:
        lines.append(f"{title}:")
        lines.append("")
    
    for i, item in enumerate(items, 1):
        lines.append(f"{i}. {item}")
    
    return format_text_response("\n".join(lines))


def format_key_value_response(data: Dict[str, Any], title: str = None) -> Dict[str, List[Dict[str, str]]]:
    """
    Format a key-value response for the MCP server.
    
    Args:
        data: The key-value data
        title: An optional title
        
    Returns:
        A dictionary with the formatted response
    """
    lines = []
    
    if title:
        lines.append(f"{title}:")
        lines.append("")
    
    # Find the maximum key length for alignment
    max_key_len = max(len(key) for key in data.keys()) if data else 0
    
    for key, value in data.items():
        lines.append(f"{key.ljust(max_key_len)}: {value}")
    
    return format_text_response("\n".join(lines))


def format_error_response(error: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Format an error response for the MCP server.
    
    Args:
        error: The error message
        
    Returns:
        A dictionary with the formatted response
    """
    return {
        "content": [
            TextContent(type="text", text=f"Error: {error}")
        ],
        "isError": True
    }